# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    city_name = scrapy.Field()  # 所在城市
    volume = scrapy.Field()  # 成交量

    house_addr = scrapy.Field()  # 链家网的位置
    house_type = scrapy.Field()  # 房子户型
    area = scrapy.Field()  # 面积

    view_num = scrapy.Field()  # 看房人数
    price = scrapy.Field()  # 成交价格
    deal_cycle = scrapy.Field()  # 成交时间
    browse_num = scrapy.Field()  # 浏览人数
    concern_num = scrapy.Field()  # 关注人数
    list_time = scrapy.Field()  # 挂牌日期（挂在链家网上的时间）
    sell_time = scrapy.Field()  # 卖出日期
    price_per_square = scrapy.Field()  # 每平方的价格
    lj_num = scrapy.Field()  # 链家网的编号
    decoration_status = scrapy.Field()  # 装修情况
    completion_year = scrapy.Field()  # 建成时间
