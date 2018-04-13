# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from baikecrawl.items import BaikecrawlItem
from scrapy import Request
import re


class BkSpider(CrawlSpider):
    name = 'bk'
    allowed_domains = ['baike.baidu.com']

    # start_urls = ['http://baike.baidu.com/']
    def start_requests(self):
        ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
        yield Request("https://baike.baidu.com/", headers=ua)

    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = BaikecrawlItem()
        thisurl = response.url
        x = re.search(r'baike.baidu.com/item/(.*?)', thisurl)
        if x:
            item['title'] = response.xpath("//head/title/text()").extract()
            item['url'] = thisurl
            item['content'] = response.xpath("//div[@class='para']/text()").extract()
            print item['title']
            print item['url']
            print item['content']
            yield item
        else:
            pass
