# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты).
# Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска продуктов с рейтингом не ниже введенного или
# качеством не ниже введенного (то есть цифра вводится одна, а запрос проверяет оба поля)
from pprint import pprint

from pymongo import MongoClient


def find_jobs_with_salary_gt(vacancies, salary):
    """Поиск вакансий с зарплатой больше указанной"""

    condition = {'$or': [
        # минимальная больше указанной
        {'salary_min': {'$gt': salary}},
        # попадает между минимальной и максимальной
        {'$and': [{'salary_min': {'$lt': salary}}, {'salary_max': {'$gt': salary}}]},
        # спорное условие... если минимальная не определена, а максимальная больше заданной
        {'$and': [{'salary_min': {'$eq': None}}, {'salary_max': {'$gt': salary}}]}
    ]}

    found_jobs = vacancies.find(condition)
    count = 0
    for job in found_jobs:
        count += 1
        pprint(job)

    print(f'\nКоличество найденных вакансий - {count}')


client = MongoClient("mongodb://localhost:27017/?readPreference=primary&directConnection=true&ssl=false")
db = client.jobs
vacancies = db.vacancies

find_jobs_with_salary_gt(vacancies, 350000)
