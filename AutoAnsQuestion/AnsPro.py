#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：V2.0
import re
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import sys
import easygui as g
from changFIle import getnewdata
from main import getIntoAns, getdata, getdisplayques


def getAnsCount(content, jx):  # 获取题目中ABCD对应的数量
    dd = {}
    dd["A"] = re.findall(u'A', content).__len__()
    dd["B"] = re.findall(u'B', content).__len__()
    dd["C"] = re.findall(u'C', content).__len__()
    dd["D"] = re.findall(u'D', content).__len__()
    ss = []
    for k, v in dd.items():
        if v == jx:
            ss.append(u'' + k)
    return ss


def getAnsByContent(ques):  # 根据题目内容获得答案
    data = getdata("./pro.txt")  # 获得所有题目数据
    data = re.sub(pattern=u"(?P<nn>\n([0-9]{1,3})、)", repl=r"\n####\g<nn>", string=data)  # 所有题目编号前加上####
    allQuestionCell = data.split(u"####")  # 将每一个题目分割出来
    for everyQues in allQuestionCell:
        mm = re.search(ques, everyQues)  # 找到题目所在的那一块
        if mm:
            ll = re.findall(u"参考答案", everyQues)  # 接茬题目中是否有参考答案字样
            if ll.__len__() != 0:  # 若有
                ee = everyQues
                numCount = getAnsCount(everyQues, 2)
                realAns = ""
                for aa in numCount:
                    pp = aa.strip() + u"、(.+?)[\sA-D\n\b\r.]"
                    realAns += re.findall(pp, ee)[0] + "\n"
                return realAns
            else:  # 若没有参考答案
                numCount = getAnsCount(everyQues, 1)
                realAns = ""
                for aa in numCount.split(","):
                    realAns += re.findall(aa.strip() + u"(.*?)]", everyQues)[0] + "\n"
                return realAns
    return None


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    nowAns = {}
    index = 1
    allQuestion, brower = getIntoAns()  # 获得页面上的所有题目
    for i in allQuestion:
        i.replace('\n', '')
        quesNum = getAnsByContent(i)
        if quesNum == None:
            nowAns[index] = "无答案"
            index += 1
        else:
            nowAns[index] = quesNum
            index += 1
    print nowAns[1]
    oldNum = 0
    index = 1
    num = brower.find_elements_by_class_name("W_num_i")
    while True:
        nownum = getdisplayques(num)
        # 如果当前正在显示的题目和上一次一样，则说明这一题还没答完
        try:
            if int(nownum) == int(oldNum):
                continue
            # 如果和上一次的num不一样，则说明上一次已经答完，需要切换答案
            if int(nownum) > int(oldNum):
                oldNum = nownum
                print allQuestion[index - 1] + "答案是：\n" + nowAns.get(index)
                index += 1
            else:
                continue
        except TypeError as te:
            continue
        time.sleep(1)
