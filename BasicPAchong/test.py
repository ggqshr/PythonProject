#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib2, urllib

url = "http://news.sina.com.cn/"
data = urllib2.urlopen(url).read()
data2 = data.decode("utf-8", "ignore")
newurl = re.findall(r'href="(http://news.sina.com.cn/.+?shtml)', data2)
j = 0
for i in newurl:
    try:
        file = "C:/Users/ggq/Desktop/新建文件夹/xmltest/".decode("utf-8") + str(j) + ".html"
        urllib.urlretrieve(i, file)
        j += 1
    except urllib2.URLError as e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason

