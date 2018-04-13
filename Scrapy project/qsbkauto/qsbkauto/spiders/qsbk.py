# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qsbkauto.items import QsbkautoItem
from scrapy.http import Request


class QsbkSpider(CrawlSpider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']

    # start_urls = ['http://qiushibaike.com/']
    def start_requests(self):
        ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
        yield Request('http://qiushibaike.com/',headers=ua)
    rules = (
        Rule(LinkExtractor(allow=r'article'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = QsbkautoItem()
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        i['content'] = response.xpath("//div[@class='content']/text()").extract()
        i["link"] = response.xpath("//link[@rel='canonical']/@href").extract()
        yield i
