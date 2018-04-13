# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QsbkautoPipeline(object):
    def process_item(self, item, spider):
        for i in xrange(0, len(item["content"])):
            print item["content"][i]
        print item["link"]
        return item
