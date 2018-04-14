#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：答案显示的界面
import easygui as g
ch = ("上一个","下一个","退出")
msg = g.indexbox("zheshidaan",choices=ch)
while(True):
    if msg==0:
        msg = g.indexbox("上一个", choices=ch)
    elif msg==1:
        msg = g.indexbox("下一个", choices=ch)
    elif msg==2:
        break

