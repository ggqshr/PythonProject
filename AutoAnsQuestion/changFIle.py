#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：将题目编号格式化
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def getdata(filePath):
    ansFile = open(r'' + filePath, "r")
    data = ansFile.read().decode("utf8")
    return data


def getcount(match):
    try:
        getcount.sum += 1
    except AttributeError:
        getcount.sum = 2
    return str(getcount.sum)


def getnewdata():
    data = getdata(r".\ans.txt")
    dd = re.findall(r'####\n[0-9]+', data)
    ll = dd.__len__()
    data = re.sub(pattern=r'####\n([0-9]+)', repl=getcount, string=data)
    return data
