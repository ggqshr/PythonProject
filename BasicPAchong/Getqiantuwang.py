#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib2
import urllib

file = "C:/Users/ggq/Desktop/python code/xmltest/"

page = 1

for i in range(1, 4):
    url = "http://www.58pic.com/tupian/43027704-0-0-" + str(i) + ".html"
    data = urllib2.urlopen(url).read().decode("utf-8", "ignore")
    imgurl = re.compile('(?:data-original="((?:.+?)\.(?i)(?:jpg|png))!)').findall(data)#findall(r'data-original="(.+?).jpg!', data)
    jj = 0
    for ii in imgurl:
        ss = u'http://pic.qiantucdn.com/58pic/28/26/16/25x58PICgbj.jpg'
        try:
            filePath = file + str(i) + str(jj) + ".jpg"
            urllib.urlretrieve(ii, filePath)
            jj += 1
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                print e.reason
            if hasattr(e, "code"):
                print e.code
