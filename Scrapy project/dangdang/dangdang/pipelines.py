# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymysql


class DangdangPipeline(object):

    def __init__(self):
        self.con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123',
            db='sql_text',
            charset='utf8')
        self.cur = self.con.cursor()

    def process_item(self, item, spider):
        title = item["title"]
        link = item["link"]
        comment = item["comment"]
        price = item["price"]
        sql = "insert into dangdang values(%s,%s,%s,%s)"
        for i in range(0, len(item["title"])):
            self.cur.execute(sql, (title[i], link[i], re.findall(r'(\d+).*?', comment[i]), price[i][1:]))
        self.con.commit()
        return item

    def close_spider(self):
        self.con.close()
        self.cur.close()
