# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field()
    authors = scrapy.Field()
    translators = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    discount_price = scrapy.Field()
    currency = scrapy.Field()
    rate = scrapy.Field()
    isbn = scrapy.Field()
