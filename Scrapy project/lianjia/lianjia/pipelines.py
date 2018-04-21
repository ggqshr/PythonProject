# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymysql


class LianjiaPipeline(object):
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
        sql = "insert into lianjia_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cur.execute(sql, (
            item["lj_num"], item["house_addr"], item["house_type"], float(item["area"]), int(item["view_num"]),
            item["price"],
            int(item["deal_cycle"]),
            int(item["browse_num"]),
            int(item["concern_num"]),
            item["list_time"],
            item["sell_time"],
            int(item["price_per_square"]),
            item["decoration_status"],
            int(item["completion_year"]),
            item["city_name"]))

    def close_spider(self,item):
        self.con.commit()
        self.con.close()
        self.cur.close()
