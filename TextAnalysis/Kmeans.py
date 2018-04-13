#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：kmeans测试
import pandas as pda
import numpy as np
import matplotlib.pylab as pl
from sklearn.cluster import Birch
from sklearn.cluster import KMeans
import pymysql

# 测试一下聚类
'''
fname = r'C:\Users\ggq\Desktop\lesson.csv'
dataf = pda.read_csv(fname, encoding='gbk')
x = dataf.iloc[:, 1:5].as_matrix()
kms = KMeans(n_clusters=3)  # 聚为多少类,多少线程，最大循环
y = kms.fit_predict(x)
print y
'''
# 聚类京东电脑

sql = 'select * from jdcomputer limit 1000'
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123', db='sql_text', charset='gbk')
dataf = pda.read_sql(sql, conn)
x = dataf.iloc[:, 2:4].as_matrix()
kms = KMeans(n_clusters=3)
y = kms.fit_predict(x)
for i in xrange(0, len(y)):
    if y[i] == 0:
        pl.plot(dataf.loc[i:i + 1, 'price'], dataf.loc[i:i + 1, 'commit'], '*r', 'o')
    if y[i] == 1:
        pl.plot(dataf.loc[i:i + 1, 'price'], dataf.loc[i:i + 1, 'commit'], 'sg', 'o')
    if y[i] == 2:
        pl.plot(dataf.loc[i:i + 1, 'price'], dataf.loc[i:i + 1, 'commit'], 'pk', 'o')
pl.show()
