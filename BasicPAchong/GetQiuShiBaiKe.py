#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：爬取糗事百科
import re
import urllib2

baseUrl = "http://www.qiushibaike.com"
header = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0")
fileBase = "C:/Users/ggq/Desktop/python code/qishi/"
for pageNum in range(1, 3):
    url = "http://www.qiushibaike.com/8hr/page/" + str(pageNum) + "/"
    opener = urllib2.build_opener()
    opener.addheaders = [header]
    urllib2.install_opener(opener)
    htmlData = urllib2.urlopen(url).read().decode("utf-8", "ignore")
    aUrls = re.findall(r'<a href="(/article/.*?)"', htmlData)
    for i in range(0, len(aUrls)):
        Surl = baseUrl + aUrls[i]
        file = fileBase + str(pageNum) + str(i) + ".html"
        story = urllib2.urlopen(Surl).read().decode("utf-8", "ignore")
        f = open(file, "w")
        f.write(story.encode("utf-8"))
        f.close()
        # content = re.findall(r'<div class="content">(.*?)</div>', story, re.S)
        # for c in content:
        #     print c
