#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：用贝叶斯算法预测课程销量
import pandas as pda
import numpy as np
import bayes

fname = r'C:\Users\ggq\Desktop\lesson.csv'
dataf = pda.read_csv(fname, encoding='gbk')
traindata = dataf.loc[:, u'实战':u'是否提供资料']
label = dataf.loc[:, u'销量']
tdata = [list(x) for x in traindata.values]
labels = [x for x in label.values]
bys = bayes.Bayes()
bys.fit(tdata, labels)
testdata = [1, -1, 1, -1]
#批量测试
for i in xrange(0, len(tdata)):
    thisdata = tdata[i]
    thisresult = label[i]
    print '结果是', thisresult, '预测的结果是', bys.btest(thisdata, [1, -1])
