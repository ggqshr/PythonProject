# -*- coding: utf-8 -*-
import scrapy
from ts.items import TsItem
from scrapy.http import Request


class LessonSpider(scrapy.Spider):
    name = 'lesson'
    allowed_domains = ['hellobi.com']
    start_urls = ['https://edu.hellobi.com/course/143/']

    def parse(self, response):
        item = TsItem()
        item["title"] = response.xpath("//ol[@class='breadcrumb']/li[@class='active']/text()").extract()
        item['link'] = response.xpath("//input[@name='redirect_url']/@value").extract()
        item['stu'] = response.xpath("//span[@class='course-view']/text()").extract()
        for i in item["title"]:
            print i
        print item["link"]
        print item["stu"]
        yield item
        for i in xrange(0, 121):
            url = "https://edu.hellobi.com/course/" + str(i)
            yield Request(url, callback=self.parse)
