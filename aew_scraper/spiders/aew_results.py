# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class AewResultsSpider(scrapy.Spider):
    name = 'aew_results'
    allowed_domains = ['www.profightdb.com']
    start_urls = ['http://www.profightdb.com/cards/aew-cards-pg1-no-285.html']

    def parse(self, response):
        events = response.xpath(
            '//tr[@class="gray"]/td/a[starts-with(@href, "/cards/aew/")]/@href').extract()

        for event in events:
            absolute_url = f"http://{self.allowed_domains[0]}{event}"

            yield Request(absolute_url, callback=self.parse_results)
