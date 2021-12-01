# Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять
# только новые вакансии/продукты в вашу базу.

from pprint import pprint

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/96.0.4664.45 Safari/537.36'}


def determine_number_of_pages(response):
    """Определение количества страниц"""
    try:
        dom = BeautifulSoup(response.text, 'html.parser')
        pages_block = dom.find('div', {'class': 'pager'}).findChild()
        pages = pages_block.find_all('a', {'class': 'bloko-button'})
        page_count = int(pages[len(pages) - 2: -1][0].getText())
    except:
        page_count = 1
    return page_count


def get_salary(job_block):
    """Разбор блока с зарплатами и определение минимальной, максимальной и валюты"""
    salary_block = job_block.find('div', {'class': 'vacancy-serp-item__sidebar'})
    try:
        if not salary_block:
            salary_min = None
            salary_max = None
            currency = None
        else:
            salary_info = list(salary_block.getText().replace(u'\u202f', u'').split())
            if len(salary_info) == 4:
                salary_min = int(salary_info[0])
                salary_max = int(salary_info[2])
                currency = salary_info[3]
            elif len(salary_info) == 3:
                if salary_info[0].lower() == 'от':
                    salary_min = int(salary_info[1])
                    salary_max = None
                    currency = salary_info[2]
                elif salary_info[0].lower() == 'до':
                    salary_min = None
                    salary_max = int(salary_info[1])
                    currency = salary_info[2]
            else:
                salary_min = None
                salary_max = None
                currency = None
    except ValueError:
        return None, None, None

    return salary_min, salary_max, currency


def save_jobs_to_db(jobs):
    """Сохранение вакансий в базу монго"""
    client = MongoClient("mongodb://localhost:27017/?readPreference=primary&directConnection=true&ssl=false")
    db = client.jobs
    vacancies = db.vacancies
    for job in jobs:
        found_job = vacancies.find_one(
            {'$and': [
                {'name': job.get('name')},
                {'url': job.get('url')},
                {'salary_min': job.get('salary_min')},
                {'salary_max': job.get('salary_max')},
                {'currency': job.get('currency')},
                {'employer': job.get('employer')},
            ]
            }
        )
        if not found_job:
            vacancies.insert_one(job)
        else:
            print('Вакансия:')
            pprint(found_job)
            print('уже есть в базе!')




def get_employer(job_block):
    """Получение информации по работодателю"""
    employer_block = job_block.find('div', {'class': 'vacancy-serp-item__meta-info-company'})
    employer_info = employer_block.findChild()
    return employer_info.getText().replace(u'\xa0', ' ')


def get_vacancy_from_hh(vacancy_name, base_url, items_on_page):
    """Разбор вакансий с HH"""
    search_link = f"{base_url}/search/vacancy"
    params = {'area': '1',
              'fromSearchLine': 'true',
              'text': vacancy_name,
              'items_on_page': items_on_page,
              'page': '0'}

    response = requests.get(search_link, params=params, headers=headers)
    if not response.ok:
        return

    jobs = []
    page_count = determine_number_of_pages(response)
    for i in range(0, page_count):
        params.update(page=i)
        response = requests.get(search_link, params=params, headers=headers)
        if not response.ok:
            return

        dom = BeautifulSoup(response.text, 'html.parser')
        job_blocks = dom.find_all('div', {'class': 'vacancy-serp-item'})
        for job_block in job_blocks:
            job = {}
            user_content = job_block.find('span', {'class': 'g-user-content'})
            if user_content is None:
                continue
            info = user_content.findChild()
            if info is None:
                continue

            job['name'] = info.getText()
            job['url'] = info.get('href')

            salary_min, salary_max, currency = get_salary(job_block)
            job['salary_min'] = salary_min
            job['salary_max'] = salary_max
            job['currency'] = currency
            job['site'] = base_url

            job['employer'] = get_employer(job_block)
            pprint(jobs)
            jobs.append(job)
    return jobs


url_hh = 'https://hh.ru'
vacancy_name = 'python'
items_on_page = 20

jobs = get_vacancy_from_hh(vacancy_name, url_hh, items_on_page)
save_jobs_to_db(jobs=jobs)

print('Finish!')
