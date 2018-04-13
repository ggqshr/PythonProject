#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 功能：爬取豆瓣电影图片 需要用到抓包
import re
import urllib2
import urllib

fileBase = "C:/Users/ggq/Desktop/python code/doubanPIc/"
for pageNum in range(0, 4):
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20" \
          "&page_start=" + str(pageNum * 20)
    Json = urllib2.urlopen(url).read().decode("utf-8", "ignore")
    imgUrl = re.findall(r'"cover":"(.*?)"', Json)
    fileNum = 0
    for img in imgUrl:
        img = img.replace("\\", "")
        img = img[0:4]+img[5:] #爬取图片不能使用https协议 此处是处理https的S
        try:
            print img
            filePath = fileBase + str(pageNum) + str(fileNum) + ".jpg"
            fileNum += 1
            urllib.urlretrieve(img, filePath)
            print "第", str(pageNum + 1), "轮", "第", str(fileNum ), "次", "爬取成功"
        except urllib2.HTTPError as e:
            if hasattr(e, "reason"):
                print e.reason
            if hasattr(e, "code"):
                print e.code
            print e.message
