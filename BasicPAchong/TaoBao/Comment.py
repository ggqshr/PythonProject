#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 功能：商品评论
import re
import urllib
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
for pageNum in range(1, 4):
    url = "https://rate.taobao.com/feedRateList.htm?auctionNumId=562922858803&userNumId=672443807&currentPageNum=" + str(
        pageNum) + "" \
                   "&pageSize=20&rateType=&orderType=sort_weight&attribute=&sku=&hasSku=false&folded=0&&_ksTS" \
                   "=1517051818366_2015" \
                   "&callback=jsonp_tbcrate_reviews_list "
    viewData = urllib2.urlopen(url).read().decode("gbk", "ignore")
    commantUrl = re.findall(r'"content":"(.*?)"', viewData)
    for i in commantUrl:
        print u"" + str(i).encode("utf-8")
