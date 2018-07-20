#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：生成青岛旅游景点的词图云
# 获取每个景点的关键词，前30个
import pymysql
from wordcloud import WordCloud, ImageColorGenerator
from scipy.misc import imread
import matplotlib.pyplot as plt
import os

for _, _, x in os.walk("./pic"):
    pass
allfile = [z.decode("gbk") for z in x]


def getData(cur, emotion, place):
    sql = ''
    if emotion == '正面':
        sql = "select keyword,countNum " \
              "from xcmostkey " \
              "where emotion='正面' and comment_place=%s " \
              "order by countNum desc"
    else:
        sql = "select keyword,countNum " \
              "from xcmostkey " \
              "where emotion='负面' and comment_place=%s " \
              "order by countNum desc"
    cur.execute(sql, (place))
    data = cur.fetchmany(100)
    dd = {}
    for i in data:
        dd[i[0]] = i[1]
    return dd


# 获取所有景点的名称
def getName(cur):
    cur.execute("select distinct comment_place from xcmostkey")
    lines = cur.fetchall()
    cur.close()
    return [x[0] for x in lines]


bimg = imread("./circle.png")
ww = WordCloud(background_color='white',
                  font_path="simfang.ttf",
                  random_state=60,
                  mask=bimg
                  )


# 绘制词图云
def drawPic(data, place):
    ww.generate_from_frequencies(data)
    image_colors = ImageColorGenerator(bimg)
    ww.to_file("./pic/" + place + ".png")


if __name__ == '__main__':
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123',
        db='xchadoopdataexport',
        charset='utf8',
    )
    place_line = getName(conn.cursor())
    for place in place_line:
        if place + ".png" in allfile:
            print "跳过了", place, "的图片"
            continue
        place_key_word = getData(conn.cursor(), "正面", place)
        if place_key_word.__len__()<50:
            continue
        try:
            drawPic(place_key_word, place)
        except ValueError as e:
            continue
        print "生成了", place, "的图片"
    conn.close()
