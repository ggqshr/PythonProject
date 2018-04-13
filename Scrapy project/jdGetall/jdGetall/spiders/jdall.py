# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from jdGetall.items import JdgetallItem
import re
import urllib2


class JdallSpider(CrawlSpider):
    name = 'jdall'
    allowed_domains = ['jd.com']

    def start_requests(self):
        ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
        yield Request("https://www.jd.com/", headers=ua)

    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        thisurl = response.url
        item = JdgetallItem()
        x = re.search(r'item.jd.com/(.+?).html', thisurl)
        if x:
            item['name'] = response.xpath("//div[@class='sku-name']/text()").extract()
            item['url'] = thisurl
            id = re.findall(r'item.jd.com/(.*?).html', item['url'])
            pricedata = urllib2.urlopen(
                'https://p.3.cn/prices/mgets?callback=jQuery8154371&type=1&area=1_72_2799_0&pdtk=&pduid=796372035'
                '&pdpin=&pin=null&pdbp=0&skuIds=J_' +
                id[0]).read()
            item['price'] = re.findall(r'"p":"(.*?)"', pricedata)
            commitdata = urllib2.urlopen(
                'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='+id[0]).read()
            item['commit'] = re.findall(r'"CommentCount":(.*?),',commitdata)
            yield item
        else:
            pass
