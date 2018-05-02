# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiechengItem(scrapy.Item):
    authorName = scrapy.Field()  # 作者名称
    content = scrapy.Field()  # 评论内容
    useful = scrapy.Field()  # 多少人表示有用
    view_score = scrapy.Field()  # 对景色的评分
    interest_score = scrapy.Field()  # 对趣味的评分
    price_score = scrapy.Field()  # 性价比评分
    view_type = scrapy.Field()  # 出游类型
    total_score = scrapy.Field()  # 总评分
    comment_time = scrapy.Field()  # 评论时间
    comment_place = scrapy.Field()  # 评论的景点

