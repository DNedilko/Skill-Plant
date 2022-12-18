import requests
import re
import json
import time
import itertools
import sys
sys.path.append('.')

from Kafka.KafkaProducer import KafkaProducer
from bs4 import BeautifulSoup
from multiprocessing import Pool, Lock
from datetime import date
from parser_raw import parse_date, parse_remote_type, parse_seniority, parse_employment_type, parse_region

today = date.today()

main_page = 'https://www.work.ua/jobs-it/?advs=1'
page_next = 'https://www.work.ua/jobs-it/?advs=1&page={}'
file_name = f"work.ua_{today.strftime('%d-%m')}.json"

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
WORKERS = 20
lock = Lock()
kafka_producer = KafkaProducer()


def write_to_json(vacancies):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump({"jobs": vacancies}, f, indent=2, ensure_ascii=False)


def get_response_with_sleep_time(link, sleep_time=1.0):
    if sleep_time > 300:
        print('Can`t get a data from page')
        return ''
    else:
        response = requests.get(link, headers=HEADERS)
        if response.status_code != requests.codes.ok:
            time.sleep(sleep_time)
            return get_response_with_sleep_time(link, sleep_time * 2)
        else:
            return BeautifulSoup(response.text, 'html.parser')


def get_pages_links():
    response = requests.get(main_page, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        total_pages = soup.find('ul', class_='pagination pagination-small visible-xs-block').get_text().strip()
        total_pages = int(re.search('\d+$', total_pages).group(0))
    except Exception as e:
        print(f'Can`t get count of total pages.\n{e}\nPages set 600')
        total_pages = 310

    pages_links = [page_next.format(page) for page in range(1, total_pages + 1)]
    return pages_links


def get_job_links(page_link):

    print(f'Page: {page_link}')
    soup = get_response_with_sleep_time(page_link)

    jobLink_tags = soup.find('div', id='pjax-job-list').find_all('h2')
    jobLinks = []
    for jobLink_tag in jobLink_tags:
        a_tag = jobLink_tag.find('a', {'href': re.compile('/jobs/\d+')})
        try:
            jobDate = a_tag.get('title')
            jobDate = re.sub('.*вакансія від\s*', '', jobDate)
        except:
            jobDate = ''
        try:
            jobLink = 'https://www.work.ua' + a_tag.get('href')
        except:
            continue

        jobLinks.append([jobLink, jobDate])

    return jobLinks


def get_jobs_data(job_link_and_date):

    job_link, date_raw = job_link_and_date
    soup_job = get_response_with_sleep_time(job_link)

    try:
        description = soup_job.find('div', id='job-description').text.strip()
    except:
        description = ''

    try:
        title = soup_job.find('h1', id='h1-name').text.strip()
    except:
        title = ''

    seniority = parse_seniority(title)

    try:
        company = soup_job.find('span', class_='glyphicon glyphicon-company text-black glyphicon-large').nextSibling.getText().strip()
    except:
        company = ''

    date = parse_date(date_raw).strftime('%d/%m/%Y')

    try:
        region_raw = soup_job.find('span', class_='glyphicon glyphicon-map-marker text-black glyphicon-large').nextSibling.getText().strip()
        region = parse_region(region_raw)
    except:
        region = ''

    try:
        remote_type_raw = soup_job.find('span', class_='glyphicon glyphicon-remote text-black glyphicon-large').parent.getText().strip()
        remote_type = parse_remote_type(remote_type_raw)
    except:
        remote_type = ''

    try:
        employment_type_raw = soup_job.find('span', class_='glyphicon glyphicon-tick text-black glyphicon-large').parent.getText().strip()
        employment_type = parse_employment_type(employment_type_raw)
    except:
        employment_type = ''

    try:
        salary = soup_job.find('span', class_='glyphicon glyphicon-hryvnia text-black glyphicon-large').nextSibling.getText().strip()
    except:
        salary = ''

    try:
        additional_info = soup_job.find('span', class_='glyphicon glyphicon-tick text-black glyphicon-large').parent.getText().strip()
    except:
        additional_info = ''

    vacancy = {
        'url': job_link,
        'title': title,
        'description': description,
        'company': company,
        'updated': date,
        'region': region,
        'country': 'Україна',
        'remote_type': remote_type,
        'employment_type': employment_type,
        'salary': salary,
        'additional_info': additional_info,
        'seniority': seniority,
        'date_gathered': today.strftime('%d/%m/%Y %H:%M:%S')
    }

    kafka_producer.produce_broker_message(vacancy)

    return [vacancy]


if __name__ == '__main__':

    pages = get_pages_links()

    with Pool(WORKERS) as pool:
        jobs = list(itertools.chain(*pool.map(get_job_links, pages)))

    with Pool(WORKERS) as pool:
        jobs_data = list(itertools.chain(*pool.map(get_jobs_data, jobs)))

    # write_to_json(jobs_data)



