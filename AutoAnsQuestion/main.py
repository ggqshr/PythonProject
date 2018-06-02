#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：获得答案
import re
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import sys
import easygui as g
from changFIle import getnewdata

# 加载数据
def getdata(filePath):
    ansFile = open(r'' + filePath, "r")
    data = ansFile.read().decode("utf8")
    return data


# 将所有题目的编号和答案对应起来
def getAnsContent(filePath):
    data = getdata(filePath)
    questions = data.split("####")
    allAns = {}
    qNum = 1
    allAnsContent = {}
    # 获得所有题目的答案
    for ques in questions:
        pattern = u"参考答案 : (.*?)\n"
        quesAns = re.findall(pattern, ques)
        allAns[qNum] = quesAns
        ansContent = ''
        for op in quesAns[0].split(","):
            pattern = op.strip() + u'、(.*?)\s'
            cont = re.findall(pattern, ques)
            ansContent += cont[0] + "\n"
        allAnsContent[qNum] = ansContent
        qNum += 1
    return allAnsContent


# 根据题目内容获取题目编号
def getQuesNum(ss, data):
    pattern = u'(.*?)' + ss
    num = re.findall(pattern, data)
    return num


# 进入到答题页面
def getIntoAns():
    brower = webdriver.Chrome()
    brower.get("https://www.dtdjzx.gov.cn/")
    brower.implicitly_wait(10)
    brower.find_element_by_class_name("top-href").click()
    brower.switch_to_window(brower.window_handles[1])
    time.sleep(3)
    try:
        brower.find_element_by_xpath("//div[@id='myxiaoxi']//button['mkjh']").click()
    except Exception as e:
        brower.find_element_by_xpath("//div[@id='myxiaoxi']//button['mkjh']").click()
    dt = brower.find_element_by_xpath("//div[@class='l-moniks']//button['lbuts']")
    brower.execute_script("arguments[0].scrollIntoView();", dt)
    time.sleep(0.5)
    dt.click()
    time.sleep(0.5)
    select_item = Select(brower.find_element_by_xpath("//div[@id='myshenfe']//select[@id='shenfen']"))
    select_item.select_by_index(1)
    brower.find_element_by_id("bts").click()
    # 登陆
    username = brower.find_element_by_id("username")
    pwd = brower.find_element_by_id("password")
    username.send_keys("18663278150")
    pwd.send_keys("5515225gg5")
    raw_input("after you input the key please input Enter")
    brower.find_element_by_class_name("js-submit").click()
    time.sleep(0.5)
    brower.find_element_by_xpath("//div[@id='myxiaoxi']//button['mkjh']").click()
    dt = brower.find_element_by_xpath("//div[@class='l-moniks']//button['lbuts']")
    brower.execute_script("arguments[0].scrollIntoView();", dt)
    time.sleep(0.5)
    dt.click()
    time.sleep(0.5)
    allQues = brower.page_source
    allcont = re.findall(r'<span class="W_ml10 w_fz18">(.*?)</span>', allQues, re.S)
    return allcont, brower


# 获得当前是哪个题目可见
def getdisplayques(ques):
    time.sleep(0.3)
    for i in ques:
        if i.is_displayed():
            try:
                return int(i.text) + 1
            except ValueError as ve:
                time.sleep(1)
                return getdisplayques(ques)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    ans = getAnsContent(r".\ans.txt")
    allQuestion, brower = getIntoAns()
    data = getdata(r".\ans.txt")
    newdata = getnewdata()
    nowAns = {}
    index = 1
    if len(allQuestion) < 20:
        g.msgbox("数量小于20，题目没全 ")
    for i in allQuestion:
        i.replace('\n', '')
        quesNum = getQuesNum(i, newdata)
        if len(quesNum) == 0:
            nowAns[index] = "A"
            index += 1
        else:
            nowAns[index] = ans.get(int(quesNum[0]))
            index += 1
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
