#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：使用apriori算法计算学院购买课程的关联
import apriori as ap
import pandas as pda

fname = r'C:\Users\ggq\Desktop\kecheng.csv'  # 文件地址
dataf = pda.read_csv(fname, encoding='gbk', header=None)
# 转化数据
change = lambda x: pda.Series(1, index=x[pda.notnull(x)])  # 难点在这
data1 = map(change, dataf.as_matrix())
data = pda.DataFrame(list(data1)).fillna(0)

# 临界支持度，置信度
spt = 0.1
cfd = 0.3

ap.find_rule(data, spt, cfd, '&&')
