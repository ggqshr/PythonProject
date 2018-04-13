#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：爬取腾讯视频评论
import re
import urllib
import urllib2

header = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0")
opener = urllib2.build_opener()
opener.addheaders = [header]
urllib2.install_opener(opener)  # 添加头部信息，模仿成浏览器
commentId = '6164678298352311010'
url = "https://video.coral.qq.com/filmreviewr/c/upcomment/0dfpyvfa7tp0ewe?callback" \
      "=_filmreviewrcupcomment0dfpyvfa7tp0ewe&reqnum=3&commentid=" + commentId + "&_=1517110413185 "
for i in range(0, 3):
    data = urllib2.urlopen(url).read().decode("utf-8", "ignore")
    lastId = re.findall(r'"last":"(.*?)"', data)
    lastId = lastId[0]
    tatle = re.findall(r'"title":"(.*?)",',data)
    content = re.findall(r'"content":"(.*?)",', data)
    for j in range(0, len(content)):
        print "第", str(i), str(j), "条标题是", tatle[j].decode('unicode-escape')  #如何将\u771f\u5fc3\u559c\u6b22\u8bdb\u4ed9转换成中文输出
        print "第", str(i), str(j), "条评论是", content[j].decode('unicode-escape')
        url = "https://video.coral.qq.com/filmreviewr/c/upcomment/0dfpyvfa7tp0ewe?callback" \
              "=_filmreviewrcupcomment0dfpyvfa7tp0ewe&reqnum=3&commentid=" + lastId + "&_=1517110413185 "
