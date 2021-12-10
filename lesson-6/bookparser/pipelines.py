# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

def price_to_number(price):
    try:
        pr = int(price)
    except ValueError:
        pr = None
    return pr


def rate_to_number(rate):
    try:
        pr = float(rate)
    except ValueError:
        pr = None
    return pr


def get_book_name(full_name:str):
    idx = full_name.find(":")
    if idx != -1:
        book_name = full_name[idx + 1:]
    else:
        book_name = full_name
    return book_name.strip()


def get_isbn(full_isbn):
    idx = full_isbn.upper().find("ISBN:")
    if idx != -1:
        isbn = full_isbn[idx + 5:]
    else:
        isbn = full_isbn
    return isbn.strip().replace('\xa0', '')


class BookparserPipeline:


    def __init__(self) -> None:
        client = MongoClient("mongodb://localhost:27017/?readPreference=primary&directConnection=true&ssl=false")
        self.mongobase = client.books

    def process_item(self, item, spider):

        item['name'] = get_book_name(item['name'])
        item['price'] = price_to_number(item['price'])
        item['discount_price'] = price_to_number(item['discount_price'])
        item['rate'] = rate_to_number(item['rate'])
        item['isbn'] = get_isbn(item['isbn'])

        collection = self.mongobase[spider.name]
        collection.update_one({'isbn': item['isbn']}, {'$set': item}, upsert=True)

        return item
