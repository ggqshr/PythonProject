# -*- coding: utf-8 -*-
from _mysql import IntegrityError

import scrapy
from scrapy.http import Request
import re
import pymysql
from lianjia.items import LianjiaItem


class LjSpider(scrapy.Spider):
    name = 'lj'
    allowed_domains = ['lianjia.com']
    all_dict = {}
    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}

    # start_urls = ['http://lianjia.com/']
    def start_requests(self):
        yield Request("https://qd.lianjia.com/", headers=self.ua, callback=self.parse,dont_filter=True)

    # 获取所有城市的url并且过滤掉旅游房源
    def parse(self, response):
        # 提取url和城市名称的url
        left_city_name_xpath = "//div[@class='city-change animated']//div[@class='fl citys-l']//div[@class='city-enum " \
                               "fl']//a/text() "
        left_city_url_xpath = "//div[@class='city-change animated']//div[@class='fl citys-l']//div[@class='city-enum " \
                              "fl']//a/@href "
        right_city_name_xpath = "//div[@class='city-change animated']//div[@class='fl citys-r']//div[" \
                                "@class='city-enum fl']//a/text() "
        right_city_url_xpath = "//div[@class='city-change animated']//div[@class='fl citys-r']//div[@class='city-enum " \
                               "fl']//a/@href "
        left_city_name = response.xpath(left_city_name_xpath).extract()
        left_city_url = response.xpath(left_city_url_xpath).extract()
        # 将url和城市名对应起来
        left_dict = dict(zip(left_city_url, left_city_name))
        right_city_name = response.xpath(right_city_name_xpath).extract()
        right_city_url = response.xpath(right_city_url_xpath).extract()
        right_dict = dict(zip(right_city_url, right_city_name))
        # 将两个dict合并
        self.all_dict = left_dict.copy()
        self.all_dict.update(right_dict)
        pattern = r''
        whis_dict = {}
        for key in self.all_dict.keys():
            if str(key).find("you.lianjia.com") != -1:
                self.all_dict.pop(key)
        for key in self.all_dict.keys():
            yield Request(key + "chengjiao", callback=self.wish, headers=self.ua)

    # 过滤掉没有二手房的城市url
    def wish(self, response):
        con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123',
            db='sql_text',
            charset='utf8',
        )
        cur = con.cursor()
        this_url = response.url
        if this_url.find("chengjiao") == -1:
            pass
        else:
            total_page = response.xpath("//div[@class='page-box house-lst-page-box']/@page-data").extract()
            total_page_num = re.findall(r'{"totalPage":(.*?),"', total_page[0])[0]
            volume = response.xpath("//div[@class='total fl']/span/text()").extract()
            city_url = re.findall(r'(.*?)chengjiao', this_url)[0]
            city_name = self.all_dict.get(city_url)
            try:
                cur.execute("insert into city_data values(%s,%s)",(city_name,int(volume[0])))
                con.commit()
            except Exception as e:
                a = 1
            for num in xrange(1, int(total_page_num)):
                yield Request(this_url + 'pg' + str(num) + "/", callback=self.redirect,
                              headers=self.ua, meta={"volume": volume[0], "city_name": city_name})
        con.close()
        cur.close()

    def redirect(self, response):
        all_house_info = response.xpath("//div[@class='info']//div[@class='title']/a/@href").extract()
        for this_url in all_house_info:
            yield Request(this_url, callback=self.get_data,
                          headers=self.ua,
                          meta={"volume": response.meta["volume"], "city_name": response.meta["city_name"]})

    def get_data(self, response):
        item = LianjiaItem()
        item["city_name"] = response.meta["city_name"]
        item["volume"] = response.meta["volume"]
        area = None
        try:
            area = re.findall(u'(.*?)平米', response.xpath("/html/body/div[4]/div/h1/text()").extract()[0].split()[2])[0]
        except IndexError as e :
            area = re.findall(u'(.*?)平米', response.xpath("/html/body/div[4]/div/h1/text()").extract()[0].split()[3])[0]
        item["area"] = area
        item["sell_time"] = response.xpath("/html/body/div[4]/div/span/text()").extract()[0].split()[0]
        item["house_addr"] = response.xpath("/html/body/div[4]/div/h1/text()").extract()[0].split()[0]
        price = None
        try:
            price = response.xpath("/html/body/section[1]/div[2]/div[2]/div[1]/span/i/text()").extract()[0]
        except IndexError as e:
            price = response.xpath("/html/body/section[1]/div[2]/div[2]/div[3]/span[1]/label/text()").extract()[0]
        item["price"] = price
        item["price_per_square"] = response.xpath("/html/body/section[1]/div[2]/div[2]/div[1]/b/text()").extract()[0]
        deal_cycle= response.xpath("/html/body/section[1]/div[2]/div[2]/div[3]/span[2]/label/text()").extract()[0]
        if deal_cycle==u"暂无数据":
            item["deal_cycle"]=-1
        else :
            item["deal_cycle"] = deal_cycle
        item["view_num"] = response.xpath("/html/body/section[1]/div[2]/div[2]/div[3]/span[4]/label/text()").extract()[0]
        browse_num = response.xpath("/html/body/section[1]/div[2]/div[2]/div[3]/span[6]/label/text()").extract()[0]
        if browse_num==u"暂无数据":
            item["browse_num"] = 0
        else :
            item["browse_num"] = browse_num
        item["concern_num"] = response.xpath("/html/body/section[1]/div[2]/div[2]/div[3]/span[5]/label/text()").extract()[0]
        item["list_time"]= response.xpath("/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[3]/text()").extract()[0]
        item["house_type"] = response.xpath("/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[1]/text()").extract()[0]
        item["lj_num"]= response.xpath("/html/body/section[2]/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[1]/text()").extract()[0].split()[0]
        item["decoration_status"]= response.xpath("/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[9]/text()").extract()[0].split()[0]
        completion_year = response.xpath("/html/body/section[2]/div[1]/div[1]/div[1]/div[1]/div[2]/ul/li[8]/text()").extract()[0].split()[0]
        if completion_year==u"未知":
            item["completion_year"] = -1
        else:
            item["completion_year"] = completion_year
        yield item
