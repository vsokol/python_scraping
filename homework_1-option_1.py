# Вариант 1
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем
# должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# 1. Наименование вакансии.
# 2. Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# 3. Ссылку на саму вакансию.
# 4. Сайт, откуда собрана вакансия.
# 5.По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame
# через pandas. Сохраните в json либо csv.
import requests
from pprint import pprint

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/96.0.4664.45 Safari/537.36'}

def get_vacancy_from_hh(vacancy_name, base_search_link, items_on_page, page):
    # search_url_hh = f'{base_search_url_hh}?area=1&fromSearchLine=true&text={vacancy_name}
    # &items_on_page={items_on_page}&page={page}'
    params = {'area': '1',
              'fromSearchLine': 'true',
              'text': vacancy_name,
              'items_on_page': items_on_page,
              'page': page}

    response = requests.get(base_search_link, params=params, headers=headers)
    if not response.ok:
        return

    jobs = []
    # for

    pprint(response)

base_search_url_hh = 'https://hh.ru/search/vacancy'
vacancy_name = 'python'
items_on_page = 20

get_vacancy_from_hh(vacancy_name, base_search_url_hh, items_on_page, 0)

print()