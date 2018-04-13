#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用: 根据百度百科的文本相似度进行kmean聚类
import simifunc
import pandas as pda
import pymysql
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pylab as pl

if __name__ == '__main__':
    sql = 'select * from baike limit 300'
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123', db='sql_text', charset='utf8')
    data = pda.read_sql(sql, conn)
    ss = simifunc.Simi(data.content)
    ss.process()
    simm = ss.analysis(data.loc[0, 'content'])
    kms = KMeans(n_clusters=3)
    simm = np.array(simm)
    simm1 = simm.reshape(-1, 1)
    y = kms.fit_predict(simm1)
    for i in xrange(0, len(y)):
        if y[i] == 0:
            pl.plot(i, simm[i], '*r', 'o')
        if y[i] == 1:
            pl.plot(i, simm[i], 'sk', 'o')
        if y[i] == 2:
            pl.plot(i, simm[i], 'dg', 'o')
    pl.show()
