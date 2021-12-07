# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
#  - название источника;
#  - наименование новости;
#  - ссылку на новость;
#  - дата публикации.
#
# 2. Сложить собранные новости в БД
#
# Минимум один сайт, максимум - все три
from lxml import html
import requests
from pprint import pprint
from datetime import datetime
from pymongo import MongoClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

datetime_format = '%d.%m.%Y %H:%M'

ru_months = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}


def replace_ru_months_to_number(str_datetime):
    """Возвращает строку с замененным на порядковый номер названием месяца"""
    for k, v in ru_months.items():
        str_datetime = str_datetime.replace(k, str(v))
    return str_datetime


def get_first_element(list):
    """Возвращает первый элемент в списке"""
    if list is None or len(list) == 0:
        return None
    else:
        return list[0]


def get_news_by_hrefs(hrefs):
    """Сбор информации по новости по ссылке для mail.ru"""
    news = []
    for href in hrefs:
        one_news = {}
        response = requests.get(href)
        if not response.ok:
            continue
        dom = html.fromstring(response.text)

        one_news['source'] = get_first_element(
            dom.xpath("//span[contains(@class, 'note__text')]/following-sibling::a/@href"))
        one_news['news'] = get_first_element(dom.xpath("//h1[@class='hdr__inner']/text()"))
        one_news['url'] = href
        news_time = get_first_element(dom.xpath("//span[contains(@class, 'note__text')]/@datetime"))
        try:
            one_news['datetime'] = datetime.strptime(news_time, '%Y-%m-%dT%H:%M:%S%z').strftime(datetime_format)
        except ValueError:
            one_news[""] = None

        news.append(one_news)

    return news


def get_news_from_mail_ru(news_url):
    """Сбор новостей с сайта mail.ru"""
    response = requests.get(news_url, headers)
    if not response.ok:
        return {}

    news = []
    dom = html.fromstring(response.text)
    items = get_news_by_hrefs(dom.xpath("//td[@class='daynews__main' or @class='daynews__items']//a/@href"))
    news += items

    items = get_news_by_hrefs(dom.xpath("//ul[contains(@class, 'list_half')]/li[@class='list__item']//@href"))
    news += items

    return news


def get_news_from_lenta_ru(news_url):
    """Сбор главный новостей с сайта lenta.ru"""
    response = requests.get(news_url, headers)
    if not response.ok:
        return {}

    dom = html.fromstring(response.text)

    news = []
    items = dom.xpath("//time[@class='g-time']/..")
    for item in items:
        one_news = {}
        one_news['source'] = news_url
        one_news['news'] = get_first_element(item.xpath("./text()"))
        href = get_first_element(item.xpath("./@href"))
        if len(href) > 5 and href[1:5] == 'http':
            one_news['url'] = href
        else:
            one_news['url'] = news_url + href
        news_time = replace_ru_months_to_number(get_first_element(item.xpath(".//@datetime"))).strip()
        try:
            one_news['datetime'] = datetime.strptime(news_time, '%H:%M, %d %m %Y').strftime(datetime_format)
        except ValueError:
            one_news[""] = None

        news.append(one_news)

    return news


def get_news_from_yandex_ru(news_url):
    """Сбор новостей с сайте yandex.ru"""
    response = requests.get(news_url, headers)
    if not response.ok:
        return {}

    dom = html.fromstring(response.text)

    news = []
    items = dom.xpath("//a[contains(@href, 'rubric=index') and @class='mg-card__link']/ancestor::article")
    for item in items:
        one_news = {}

        one_news['source'] = get_first_element(item.xpath(".//a[@class='mg-card__source-link']/text()"))
        one_news['news'] = get_first_element(item.xpath(".//h2[@class='mg-card__title']/text()")).replace('\xa0', ' ')
        one_news['url'] = get_first_element(item.xpath(".//a[@class='mg-card__link']/@href"))
        news_time = datetime.now().strftime("%d.%m.%Y ") + \
                    get_first_element(item.xpath(".//span[@class='mg-card-source__time']/text()"))
        try:
            one_news['datetime'] = datetime.strptime(news_time, datetime_format).strftime(datetime_format)
        except ValueError:
            one_news[""] = None

        news.append(one_news)

    return news


def save_news_to_db(news):
    """Сохранение новостей в базу монго"""
    client = MongoClient("mongodb://localhost:27017/?readPreference=primary&directConnection=true&ssl=false")
    db = client.news
    db_news = db.news
    for item in news:
        db_news.update_one(item, {'$set': item}, upsert=True)


news = get_news_from_mail_ru('https://news.mail.ru/') \
       + get_news_from_lenta_ru('https://lenta.ru/') \
       + get_news_from_yandex_ru('https://yandex.ru/news/')

save_news_to_db(news)

pprint(news)
