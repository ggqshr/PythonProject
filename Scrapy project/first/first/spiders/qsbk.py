# -*- coding: utf-8 -*-
import scrapy
from first.items import FirstItem
from scrapy.http import Request


class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']

    # start_urls = ['http://qiushibaike.com/']
    def start_requests(self):
        us = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Fire"}
        yield Request('http://qiushibaike.com/', headers=us)

    def parse(self, response):
        item = FirstItem()
        item["content"] = response.xpath("//div[@class='content']/span/text()").extract()
        item["link"] = response.xpath("//a[@class='contentHerf']/@href").extract()
        yield item
