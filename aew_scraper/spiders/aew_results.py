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

        next_page_url = response.xpath(
            '//div[@class="pager"]/a[starts-with(@class , "selected")]/following-sibling::a[1]/@href').extract_first()

        absolute_next_page_url = f"http://{self.allowed_domains[0]}{next_page_url}"

        yield Request(absolute_next_page_url)

    def parse_results(self, response):
        event_name = response.xpath(
            '//div[@class="right-content"]/h1/text()').extract_first().strip()

        event_details = response.xpath('//table')[0]
        date = event_details.xpath(
            './/tr')[0].xpath('.//a/@href').extract_first().split('/')[-1].replace('.html', "")
        country = event_details.xpath(
            './/tr')[1].xpath('.//td/img/@alt').extract_first()
        arena = event_details.xpath(
            './/tr')[1].xpath('.//td/a/text()')[0].extract()
        city = event_details.xpath(
            './/tr')[1].xpath('.//td/a/text()')[1].extract()
        state = event_details.xpath(
            './/tr')[1].xpath('.//td/a/text()')[2].extract()
