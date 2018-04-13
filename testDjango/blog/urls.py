#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
import blog.views as v

urlpatterns = [
    url(r'^index/$', v.hello),  # 使用正则表达式开始符号和结束符号连起来写表示空，
    # 若使用此种方式，若是匹配地址就必须向index/，因为地址访问时会自动加一个/
    url(r'^article/(?P<id>[0-9]+)$', v.article_page, name='article_page'),
    url(r'^edit/(?P<id>[0-9]+)$', v.edit_page, name='edit_page'),
    url(r'^edit/action$', v.edit_action, name='edit_action'),
    url(r'^posttest/$',v.posttest,name = 'posttest'),
]
