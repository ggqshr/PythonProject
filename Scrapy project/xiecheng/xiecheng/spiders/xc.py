# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy import log
from scrapy.http import Request
from scrapy.http import FormRequest
from xiecheng.items import XiechengItem
import pymysql


class XcSpider(scrapy.Spider):
    name = 'xc'
    allowed_domains = ['ctrip.com']
    thisSiteName = None
    # start_urls = ['http://ctrip.com/']
    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
    # 通过post方式获取评论数据
    get_commit_data_url = "http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView"

    def start_requests(self):
        yield Request("http://you.ctrip.com", headers=self.ua, callback=self.parse)

    def parse(self, response):
        for pageNum in xrange(1, 98):
            thisurl = "http://you.ctrip.com/sight/Qingdao5/s0-p" + str(pageNum) + ".html#sightname"
            yield Request(thisurl, callback=self.requestData, headers=self.ua)

    def requestData(self, response):
        # 若需要验证码就会打开shell界面，然后view（response）来输入验证码
        if response.url == "http://seccenter.ctrip.com/seccenter/main.aspx?returnurl=http%3a%2f%2fyou.ctrip.com%2fdestinationsite%2fsight%2fQingdao5%2fs0-p1.html&bgref=1988767613":
            from scrapy.shell import inspect_response
            inspect_response(response, self)
        selector = response.css(
            "html body div.ttd2_background div.content.cf div.des_wide.f_right div.normalbox div.list_wide_mod2 div.list_mod2 div.rdetailbox dl dt a")
        siteurl = selector.xpath("./@href").extract()
        for url in siteurl:
            yield Request("http://you.ctrip.com" + url, callback=self.getdata, headers=self.ua)

    def getdata(self, response):
        selector = response.css("html body div.content.cf div.dest_toptitle.detail_tt div.cf div.f_left h1 a")
        try:
            sitename = selector.xpath("./text()").extract()[0]
        except IndexError as e:
            time.sleep(0.5)
            selector = response.css("html body div.content.cf div.dest_toptitle.detail_tt div.cf div.f_left h1 a")
            sitename = selector.xpath("./text()").extract()[0]
        comment_id = response.xpath(
            "//div[@class='comment_entrance']//a[@class='b_orange_m f_right write_recomment']/@data-id").extract()[0]
        selector = response.css(
            "html body div.ttd2_background div.content.cf.dest_details div.des_wide.f_left div#sightcommentbox1.normalbox.boxcomment_v1 div.comment_wrap div.weibocombox div#weiboCom1.weiboitem.active div#sightcommentbox.comment_ctrip div.ttd_pager.cf div.pager_v1 span b.numpage")
        total_page = selector.xpath("./text()").extract()
        if len(total_page) == 0:  # 有些景点的评论过少
            total_page = 1
        else:
            total_page = total_page[0]
        for now_page in xrange(1, int(total_page) + 1):
            for start_num in xrange(1,6):
                data = {
                    "poiID": str(comment_id),
                    "districtId": "5",
                    "districtEName": " Qingdao",
                    "pagenow": str(now_page),
                    "order": "3.0",
                    "star": str(start_num),
                    "tourist": "0.0",
                    "resourceId": "1265",
                    "resourcetype": "2"
                }
                yield FormRequest(url=self.get_commit_data_url,
                                  headers=self.ua,
                                  formdata=data,
                                  callback=self.extract_data,
                                  meta={"sitename":sitename}
                                  )

    def extract_data(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        total_commit_num = response.xpath("//span[@class='f_orange']/text()").extract()[0]
        if total_commit_num != u"0":
            all_author = response.xpath("//a[@itemprop='author']/text()").extract()
            all_content = response.xpath("//span[@class='heightbox']/text()").extract()
            all_useful = response.xpath(
                "//li[@class='from_link']//span[@class='f_right']//span[@class='useful']//em/text()").extract()
            all_comment_time = response.xpath(
                "//li[@class='from_link']//span[@class='f_left']//span[@class='time_line']//em/text()").extract()
            all_view_score = []
            all_interest_score = []
            all_price_score = []
            all_view_type = []
            all_div = response.xpath("//div[@class='comment_single']")
            all_total_score = []
            for this_data in response.xpath("//span[@itemprop='reviewRating']//span/@style").extract():
                this_comment = int(this_data.split(":")[1].replace("%;", "")) / 20
                all_total_score.append(this_comment)
            index = 0
            for this_div in all_div:
                this_data = this_div.xpath(".//span[@class='sblockline']/text()").extract()
                this_type = this_div.xpath(".//span[@class='youcate']/i/@title").extract()
                if len(this_data) == 0:
                    all_view_score.append(all_total_score[index])
                    all_interest_score.append(all_total_score[index])
                    all_price_score.append(all_total_score[index])
                else:
                    try:
                        all_view_score.append(
                            this_div.xpath(".//span[@class='sblockline']/text()").extract()[0].replace(" ", "").split(u'：')[
                                1][:1])
                        all_interest_score.append(
                            this_div.xpath(".//span[@class='sblockline']/text()").extract()[0].replace(" ", "").split(u'：')[
                                2][:1])
                        all_price_score.append(
                            this_div.xpath(".//span[@class='sblockline']/text()").extract()[0].replace(" ", "").split(u'：')[
                                3][:1])
                    except IndexError as e:
                        all_view_score.append(all_total_score[index])
                        all_interest_score.append(all_total_score[index])
                        all_price_score.append(all_total_score[index])
                if len(this_type) == 0:
                    all_view_type.append(u"单独旅行")
                else:
                    all_view_type.append(this_type[0])
                index += 1
            item = XiechengItem()
            item["comment_place"] = response.meta["sitename"]
            item["authorName"] = all_author
            item["content"] = all_content
            item["useful"] = all_useful
            item["view_score"] = all_view_score
            item["interest_score"] = all_interest_score
            item["price_score"] = all_price_score
            item["view_type"] = all_view_type
            item["total_score"] = all_total_score
            item["comment_time"] = all_comment_time
            yield item
