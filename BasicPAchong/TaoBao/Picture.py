#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 功能：抓取商品图片
import re
import urllib
import urllib2
import sys


def getPic(k, o):
    baseDir = 'C:/Users/ggq/Desktop/python code/xmltest/'.decode("utf-8")
    keyname = k
    key = urllib.quote(keyname)  # 编码
    ii = 0
    offset = o
    for i in range(0, 4):
        url = 'https://s.taobao.com/search?q=' + key + '&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb' \
                                                       '.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8' \
                                                       '&initiative_id=tbindexz_20170306&bcoffset=4&ntoffset=4' \
                                                       '&p4ppushleft=1%2C48&s=' + str(
            i * offset)
        data = urllib2.urlopen(url).read().decode("gbk", "ignore")
        ll = re.findall(r'pic_url":"//(.*?)"', data)
        ii += 1
        ss = 0
        for j in ll:
            realUrl = "http://" + j
            file = baseDir + str(ii) + str(ss) + ".jpg"
            ss += 1
            try:
                urllib.urlretrieve(realUrl, file)
                content = "第" + str(ii) + "轮第" + str(ss) + "次爬取成功"
                print(content.decode("utf-8"))
            except Exception as e:
                print e.message


if __name__ == "__main__":
    getPic("耳塞", 44)
