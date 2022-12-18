import requests
import re
import json
import itertools
import sys
sys.path.append('.')

from Kafka.KafkaProducer import KafkaProducer
from lxml import etree
from bs4 import BeautifulSoup
from multiprocessing import Pool, Lock
from datetime import date
from parser_raw import parse_date, parse_remote_type, parse_region, parse_seniority
from scripts.description_parser import skills_extractor
import spacy

today = date.today()

page_next = 'https://djinni.co/jobs/?region=UKR&page={}'
main_page = 'https://djinni.co/jobs/?region=UKR'
file_name = f"djinni.co_{today.strftime('%d-%m')}.json"

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

WORKERS = 20
lock = Lock()
kafka_producer = KafkaProducer()


def write_to_json(vacancies):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump({"jobs": vacancies}, f, indent=2, ensure_ascii=False)


def get_pages_links():
    response = requests.get(main_page, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    total_pages = etree.HTML(str(soup)).xpath("//li[@class='page-item'][last()]/preceding-sibling::li[@class='page-item'][1]/a")[0].text
    try:
        total_pages = int(total_pages)
    except Exception as e:
        print(f'Can`t get count of total pages.\n{e}\nPages set 600')
        total_pages = 600

    pages_links = [page_next.format(page) for page in range(1, total_pages + 1)]
    return pages_links


def get_job_links(page_link):

    print(f'Page: {page_link}')

    response = requests.get(page_next.format(page_link), headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobLink_tags = soup.find_all('a', {'class': 'profile'})
    jobLinks = []
    for jobLink_tag in jobLink_tags:
        jobLink = 'https://djinni.co' + jobLink_tag.get('href')
        jobLinks.append(jobLink)

    return jobLinks

def get_jobs_data(job_link):

    response_job = requests.get(job_link, headers=HEADERS)
    soup_job = BeautifulSoup(response_job.text, 'html.parser')

    description = soup_job.find('div', class_='col-sm-8 row-mobile-order-2').text.strip()
    title = soup_job.find('div', class_='detail--title-wrapper').text.strip()
    title = re.sub('\s*\\n.*', '', title)
    seniority = parse_seniority(title)

    try:
        company = soup_job.find('a', class_='job-details--title').text.strip()
    except:
        company = ''

    date_raw = soup_job.find('span', class_='bi bi-pencil-square').nextSibling.strip()
    date_raw = re.search('\d.*', date_raw).group(0)
    date = parse_date(date_raw).strftime('%d/%m/%Y')

    regions = soup_job.find('span', class_='location-text')
    try:
        additional_regions = regions.find('span', {'data-toggle': 'tooltip'}).get('title')
    except:
        additional_regions = ''

    regions_text = regions.text.strip()
    region_raw = re.sub('\s*\+ ще \d+ міст(a)?', ', ' + additional_regions, regions_text)
    region, country = parse_region(region_raw)

    try:
        remote_type_raw = soup_job.find('span', {'class': re.compile('^bi bi-building mr-2.*')}).parent()[1].text
        remote_type = parse_remote_type(remote_type_raw)
    except:
        remote_type = ''

    try:
        employment_type = soup_job.find('span', {'class': re.compile('^bi bi-clock-history mr-2.*')}).parent()[1].text
    except:
        employment_type = ''

    try:
        business_type = soup_job.find('span', {'class': re.compile('^bi bi-exclude mr-2.*')}).parent()[1].text
    except:
        business_type = ''

    try:
        salary = soup_job.find('span', class_='public-salary-item').text.strip()
    except:
        salary = ''

    additional_info = soup_job.find('div', class_='card job-additional-info').text.strip()

    vacancy = {
        'url': job_link,
        'title': title,
        'description': description,
        'company': company,
        'updated': date,
        'region': region,
        'country': country,
        'remote_type': remote_type,
        'employment_type': employment_type,
        'business_type': business_type,
        'salary': salary,
        'additional_info': additional_info,
        'seniority': seniority,
        'date_gathered': today.strftime('%d/%m/%Y %H:%M:%S')
    }

    nlp = spacy.load("en_core_web_lg")
    vacancy_parsed = skills_extractor(vacancy, nlp)
    print(vacancy_parsed)

    kafka_producer.produce_broker_message(vacancy_parsed)

    return [vacancy_parsed]


if __name__ == '__main__':
    pages = get_pages_links()

    with Pool(WORKERS) as pool:
        jobs = list(itertools.chain(*pool.map(get_job_links, pages)))

    with Pool(WORKERS) as pool:
        jobs_data = list(itertools.chain(*pool.map(get_jobs_data, jobs)))

    # write_to_json(jobs_data)