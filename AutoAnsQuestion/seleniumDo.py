#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')
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
allQues = brower.page_source
allcont = re.findall(r'<span class="W_ml10 w_fz18">(.*?)</span>', allQues)
print len(allcont)
