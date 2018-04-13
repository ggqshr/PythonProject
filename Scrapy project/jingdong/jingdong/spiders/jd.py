# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jingdong.items import JingdongItem
import urllib2
import pymysql


class JdSpider(CrawlSpider):
    commitbaseurl = 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds='
    pricebaseurl = 'https://p.3.cn/prices/mgets?callback=jQuery1621888&ext=11000000&pin=&type=1&area=1_72_2799_0&skuIds='
    name = 'jd'
    allowed_domains = ['jd.com']

    # start_urls = ['http://jd.com/']

    def start_requests(self):
        ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
        yield Request("https://list.jd.com/list.html?cat=670,671,672&page=1", headers=ua)

    rules = (
        Rule(LinkExtractor(allow=r'cat=670,671,672&page='), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        item = JingdongItem()
        item["title"] = response.xpath("//div[@class='p-name']/a/em/text()").extract()
        item["url"] = response.xpath("//div[@class='p-name']/a/@href").extract()
        item["p_id"] = response.xpath("//div[@class='p-operate']/a[@class='p-o-btn contrast J_contrast "
                              "contrast-hide']/@data-sku").extract()
        priceurl = self.pricebaseurl
        commiturl = self.commitbaseurl
        for i in item["p_id"]:
            priceurl = priceurl + "J_" + i + "%2C"
            commiturl = commiturl + i + ","
        # print priceurl
        # print commiturl
        item["price"] = urllib2.urlopen(priceurl).read().decode('utf-8', 'ignore')
        item['commit'] = urllib2.urlopen(commiturl).read().decode('utf-8', 'ignore')
        yield item
