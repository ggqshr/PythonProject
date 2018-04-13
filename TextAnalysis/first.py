#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：测试jieba使用
import jieba
import jieba.posseg as jp

sentence = '我喜欢上海东方明珠'
w1 = jieba.cut(sentence, cut_all=True)#全模式
# for i in w1:
#     print i
w2 = jieba.cut(sentence, cut_all=False)#精简模式
# for i in w2:
#     print i

w3 = jieba.cut_for_search(sentence)#搜索引擎模式
# for i in w3:
#     print i

#词性分析

w4 = jp.cut(sentence)
for i in w4:
    print i.word,i.flag #词性显示

#加载词典
jieba.load_userdict()#文件地址 注意编码
