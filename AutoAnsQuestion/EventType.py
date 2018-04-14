#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：实现监听接口
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
import time

class EventType(AbstractEventListener):

    def after_execute_script(self, script, driver):
        span = driver.find_element_by_xpath("//span[@class='W_ml10 w_fz18']")
        text = span.text
        try:
            driver.execute_script("confirm('" + text + "');")
        except Exception as e:
            driver.switch_to_alert().accept()

