# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import re


class JdgetallPipeline(object):
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
        sql = 'insert into jdallitem values(%s,%s,%s,%s)'
        name = item['name'][0]
        url = item['url']
        price = item['price'][0]
        commit = item['commit'][0]
        name = re.sub(r'\s+', '', name)
        print '---', name, '---', url, '---', price, '---', commit
        if len(name) and len(url) and len(price) and len(name):
            self.cur.execute(sql, (name, url, price, commit))
            self.con.commit()
        return item

    def close_spider(self):
        self.con.close()
        self.cur.close()
