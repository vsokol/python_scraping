import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//div[@class="pagination-next"]//@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//div[contains(@class, "card-column")]//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name = response.xpath('//h1/text()').get()
        authors = response.xpath('//div[contains(text(), "Автор: ")]/a/text()').getall()
        translators = response.xpath('//div[contains(text(), "Переводчик: ")]/a/text()').getall()
        link = response.url
        price = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        discount_price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        currency = response.xpath('//span[@class="buying-pricenew-val-currency"]/text()').get()
        rate = response.xpath('//div[@id="rate"]/text()').get()
        isbn = response.xpath('//div[@class="isbn"]/text()').get()
        item = BookparserItem(name=name, authors=authors, translators=translators, link=link, price=price,
                              discount_price=discount_price, currency=currency, rate=rate, isbn=isbn)
        yield item
