# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem
from scrapy.http import Request
from scrapy.http import FormRequest
import urllib


class DbSpider(scrapy.Spider):
    name = 'db'
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
    allowed_domains = ['douban.com']

    # start_urls = ['http://douban.com/']
    def start_requests(self):
        return [Request("http://accounts.douban.com/login", headers=self.header, callback=self.parse,
                        meta={"cookiejar": 1})]

    def parse(self, response):
        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()
        if len(captcha) > 0:
            print u"此时有验证码"
            lc = "C:/Users/ggq/Desktop/python code/xmltest/ss.png"
            urllib.urlretrieve(captcha[0], filename=lc)
            print u'请查看本地验证码图片并输入'
            yy = raw_input()
            data = {
                "form_email": "942490944@qq.com",
                "form_password": "5515225gg5",
                "redir": "https://www.douban.com/people/173313239/",
                "captcha-solution": yy
            }
        else:
            print u"此时没有验证码"
            data = {
                "form_email": "942490944@qq.com",
                "form_password": "5515225gg5",
                "redir": "https://www.douban.com/people/173313239/",
            }
        print u"登陆中...."
        return [FormRequest.from_response(response,
                                          meta={"cookiejar": response.meta["cookiejar"]},
                                          headers=self.header,
                                          formdata=data,
                                          callback=self.next
                                          )]

    def next(self, response):
        print u"此时已经登陆完成,并爬取数据"
        info = response.xpath("/html/head/title/text()").extract()
        title = response.xpath("//div[@class='note-header pl2']/a/@title").extract()
        content = response.xpath("//div[@class='note']/text()").extract()
        print info[0]
        print title[0]
        print content[0]
