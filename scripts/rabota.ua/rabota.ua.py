import re
import json
import itertools
import sys
sys.path.append('.')

from Kafka.KafkaProducer import KafkaProducer
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from multiprocessing import Pool, Lock
from datetime import date
from parser_raw import parse_date, parse_remote_type, parse_seniority, parse_employment_type

today = date.today()

main_page = 'https://rabota.ua/ua/zapros/it/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0'
page_next = 'https://rabota.ua/ua/zapros/it/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0?page={}'
file_name = f"rabota.ua_{today.strftime('%d-%m')}.json"

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
WORKERS = 20
lock = Lock()

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('start-maximized')
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--hide-scrollbars')
options.add_argument('--single-process')
web_driver = webdriver.Chrome(options=options)

kafka_producer = KafkaProducer()


def write_to_json(vacancies):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump({"jobs": vacancies}, f, indent=2, ensure_ascii=False)


def get_pages_links():
    web_driver.get(main_page)
    try:
        total_pages = web_driver.find_element(by=By.XPATH,
                                              value="//div[@class='disable ng-star-inserted']/following-sibling::div").text
    except:
        web_driver.implicitly_wait(2)
        total_pages = web_driver.find_element(by=By.XPATH,
                                              value="//div[@class='disable ng-star-inserted']/following-sibling::div").text

    try:
        total_pages = int(total_pages)
    except Exception as e:
        print(f'Can`t get count of total pages.\n{e}\nPages set 110')
        total_pages = 110

    pages_links = [page_next.format(page) for page in range(1, total_pages + 1)]

    # web_driver.close()
    return pages_links


def get_job_links(page_link):

    print(f'Page: {page_link}')

    web_driver.get(page_link)
    for scroll in range(0, 15000, 100):
        web_driver.execute_script(f"window.scrollTo(0, window.scrollY + {scroll})")

    soup = BeautifulSoup(web_driver.page_source, 'html.parser')
    jobLink_tags = soup.find_all('a', {'class': re.compile('^card ng-tns')})
    jobLinks = []
    for jobLink_tag in jobLink_tags:
        jobLink = 'https://rabota.ua/ua' + jobLink_tag.get('href')
        jobLinks.append(jobLink)

    # web_driver.close()
    return jobLinks


def get_jobs_data(job_link):

    web_driver.get(job_link)

    try:
        soup_job = BeautifulSoup(web_driver.page_source, 'html.parser')
    except:
        web_driver.implicitly_wait(1.5)
        soup_job = BeautifulSoup(web_driver.page_source, 'html.parser')

    try:
        description = soup_job.find('div', class_='full-desc ng-star-inserted').getText().strip()
    except Exception as e:
        # print(e, 'trying again ...')
        web_driver.implicitly_wait(1.5)
        return get_jobs_data(job_link)

    try:
        title = soup_job.find('h1', {'data-id': 'vacancy-title'}).text.strip()
    except:
        title = ''
    title = re.sub('\s*\\n.*', '', title)
    seniority = parse_seniority(title)

    try:
        company = soup_job.find('div', class_='santa-mr-10 ng-star-inserted').find('a').text.strip()
    except:
        company = ''

    try:
        date_raw = soup_job.find('span', class_='santa-text-white santa-flex santa-justify-center santa-typo-additional ng-star-inserted').text.strip()
        date = parse_date(date_raw).strftime('%d/%m/%Y')
    except:
        date = ''

    try:
        region = soup_job.find('span', {'data-id': 'vacancy-city'}).text.strip()
    except:
        region = ''

    try:
        labels = soup_job.find('div', class_='santa-flex santa-flex-wrap').text
    except:
        labels = ''

    remote_type = parse_remote_type(labels + title)
    employment_type = parse_employment_type(labels)

    try:
        salary = soup_job.find('span', {'data-id': 'vacancy-salary-from-to'}).text.strip()
    except:
        salary = ''

    additional_info = labels

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

    print(f'job: {job_link}')
    # return vacancy
    return [vacancy]


if __name__ == '__main__':

    pages = get_pages_links()

    with Pool(WORKERS) as pool:
        jobs = list(itertools.chain(*pool.map(get_job_links, pages)))

    with Pool(WORKERS) as pool:
        jobs_data = list(itertools.chain(*pool.map(get_jobs_data, jobs)))

    web_driver.quit()
    # write_to_json(jobs_data)

