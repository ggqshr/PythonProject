#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from django.contrib import admin
from blog2.views import hello
urlpatterns = [
    url(r'^index/$',hello) #使用正则表达式开始符号和结束符号连起来写表示空，
                        # 若使用此种方式，若是匹配地址就必须向index/，因为地址访问时会自动加一个/
]