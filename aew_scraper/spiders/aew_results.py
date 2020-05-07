# -*- coding: utf-8 -*-
import scrapy


class AewResultsSpider(scrapy.Spider):
    name = 'aew_results'
    allowed_domains = ['www.profightdb.com/cards/aew-cards-pg1-no-285.html']
    start_urls = ['http://www.profightdb.com/cards/aew-cards-pg1-no-285.html/']

    def parse(self, response):
        pass
