# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re


class JingdongPipeline(object):
    commitbaseurl = 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds='
    pricebaseurl = 'https://p.3.cn/prices/mgets?callback=jQuery1621888&ext=11000000&pin=&type=1&area=1_72_2799_0&skuIds='

    def __init__(self):
        self.con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123',
            db='sql_text',
            charset='utf8',
        )
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        title = item["title"]
        lt = len(title)
        lp = len(item['p_id'])
        if lt != lp:
            return item
        url = item["url"]
        price = re.findall(r'"p":"(.*?)"', item["price"])
        sumcommit = re.findall(r'"CommentCount":(.*?),', item['commit'])
        goodcommid = re.findall(r'"GoodCount":(.*?),', item['commit'])
        badcommid = re.findall(r'"PoorCount":(.*?),', item['commit'])
        sql = "insert into jdcomputer values(%s,%s,%s,%s,%s,%s)"
        for i in xrange(0, len(item['title'])):
            self.cur.execute(sql, (
                re.sub(r'\s+', '', title[i]), url[i], price[i], sumcommit[i], goodcommid[i], badcommid[i]))
        self.con.commit()
        print '爬取成功'
        return item

    def close_spider(self):
        self.con.close()
        self.cur.close()
