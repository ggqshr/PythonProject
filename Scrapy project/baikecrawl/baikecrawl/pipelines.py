# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re


class BaikecrawlPipeline(object):
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
        # self.fh = open(r'C:\Users\ggq\Desktop\test.txt', 'a')

    def process_item(self, item, spider):
        sql = 'insert into baike values(%s,%s,%s)'
        title = item['title'][0]
        url = item['url']
        content = ''
        for i in item['content']:
            content += i
        if content.__len__() == 0:
            return item
        self.cur.execute(sql, (title, url, content))
        self.con.commit()
        # self.fh.writelines(str(title[0]))
        # self.fh.writelines(url)
        # self.fh.writelines(str(content[0]))
        return item

    def close_spider(self):
        # self.fh.close()
        self.con.close()
        self.cur.close()
