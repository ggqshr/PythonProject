# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class XiechengPipeline(object):
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
        for authorName, content, useful, \
            view_score, interest_score, price_score, view_type, total_score, comment_time in \
                zip(item["authorName"], item["content"], item["useful"], \
                    item["view_score"], item["interest_score"], item["price_score"], \
                    item["view_type"], item["total_score"], item["comment_time"]):
            sql = "insert into xiecheng values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cur.execute(sql, (authorName, u""+content, int(useful),
                                   int(view_score),
                                   int(interest_score),
                                   int(price_score),
                                   view_type, int(total_score), comment_time,
                                   item["comment_place"]))
        return item

    def close_spider(self, item):
        self.con.commit()
        self.con.close()
        self.cur.close()
