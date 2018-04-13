# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import pymysql
import re


class TsPipeline(object):
    def __init__(self):
        self.f = open("C:/Users/ggq/Desktop/python code/xmltest/1.txt", 'a')
        self.con = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123',
            db='sql_text',
            charset='utf8')
        self.cur = self.con.cursor()
        reload(sys)
        sys.setdefaultencoding("utf-8")

    def process_item(self, item, spider):
        sql = 'insert into StoreData values(%s,%s,%s)'  # 占位符
        num = re.findall(r'(\d+).+?', item["stu"][0])
        self.cur.execute(sql, (item["link"][0], item["title"][0], num))
        self.con.commit()
        for i in item["title"]:
            print i
        print item["link"][0]
        print item["stu"][0]
        self.f.write(item["title"][0] + "\t" + item["link"][0] + "\t" + item["stu"][0] + "\t" + "---------\n")

    def close_spider(self):
        self.con.close()
        self.cur.close()
        self.f.close()
