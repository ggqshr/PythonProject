#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：爬取百度图片可以设置关键字
import re
import urllib
import urllib2
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded"}
fileBase = "C:/Users/ggq/Desktop/python code/dog1/"

for pageNum in xrange(1, 30):
    url = r'http://search.originoo.net/searchpic/ws.setsearch.php'
    value = {"pic_keywords": "狗", "page_index": pageNum, "medium_type": "pic"}
    data = urllib.urlencode(value)
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
    htmlData = response.read().decode("utf-8", "ignore")
    allPicUrl = re.findall(r'"PI_URL":"(.*?)",', htmlData)
    for i in xrange(0, len(allPicUrl)):
        try:
            thisUrl = allPicUrl[i]
            # print thisUrl
            fileName = random.randint(10000, 99999)
            file = fileBase + str(fileName) + ".jpg"
            print file
            urllib.urlretrieve(thisUrl, filename=file)
            # print "第", str(pageNum), "轮", "第", str(i), "次", "爬取成功"
        except urllib2.HTTPError as e:
            if hasattr(e, "reason"):
                print e.reason
            if hasattr(e, "code"):
                print e.code
            print e.message
