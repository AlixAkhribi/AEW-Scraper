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

        matches = response.xpath('.//tr[@class="head"]/following-sibling::tr')

        for match in matches:
            spot = match.xpath('.//td/i/text()|.//td/text()')[0].extract()
            winner = match.xpath('.//td')[1]
            vitory_type = match.xpath(
                './/td/following-sibling::td')[1].xpath('.//text()').extract_first()
            loser = match.xpath('.//td')[3]
            duration = match.xpath(
                './/td/following-sibling::td')[3].xpath('.//text()').extract_first()
            match_type = match.xpath(
                './/td/following-sibling::td')[4].xpath('.//text()').extract_first().replace('\xa0', "")
            title = match.xpath(
                './/td/following-sibling::td')[5].xpath('.//text()').extract()

            yield{
                "date": date,
                "event name": event_name,
                "match number": spot,
                "winner(s)": winner.xpath('.//a/text()').extract(),
                "victory type": vitory_type,
                "loser(s)": loser.xpath('.//a/text()').extract(),
                "duration": duration,
                "match_type": match_type,
                "title": title,
                'arena': arena,
                "city": city,
                "state": state,
                "country": country
            }
