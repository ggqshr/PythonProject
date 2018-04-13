#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：决策树实战
import pandas as pda
from sklearn.tree import DecisionTreeClassifier as dtc  # 决策树
from sklearn.tree import export_graphviz as eg  # 可视化
from sklearn.externals.six import StringIO
import numpy as np

fname = 'C:\\Users\\ggq\\Desktop\\lesson.csv'
dataf = pda.read_csv(fname, encoding='gbk')
dataf[u'销量'][dataf[u'销量'] == u'高'] = 1
dataf[u'销量'][dataf[u'销量'] == u'低'] = -1
dataf[u'实战'][dataf[u'实战'] == u'是'] = 1
dataf[u'实战'][dataf[u'实战'] == u'否'] = -1
dataf[u'课时数'][dataf[u'课时数'] == u'多'] = 1
dataf[u'课时数'][dataf[u'课时数'] == u'少'] = -1
dataf[u'是否优惠'][dataf[u'是否优惠'] == u'是'] = 1
dataf[u'是否优惠'][dataf[u'是否优惠'] == u'否'] = -1
dataf[u'是否提供资料'][dataf[u'是否提供资料'] == u'是'] = 1
dataf[u'是否提供资料'][dataf[u'是否提供资料'] == u'否'] = -1
x = dataf.iloc[:, 1:5].as_matrix().astype(int)  # 转为数组
y = dataf.iloc[:, 5:].as_matrix().astype(int)
# 建立决策树
tree = dtc(criterion='entropy')
tree.fit(x, y)
# 直接验证
xx = np.array([[1, -1, -1, 1], [1, 1, 1, 1], [-1, 1, -1, 1]])
print tree.predict(xx)
# 可视化决策树
# feature_names = ('combat', 'num', 'promotion', 'data')
# with open('C:\\Users\\ggq\\Desktop\\lesson.dot', 'w') as file:
#     eg(tree, feature_names=feature_names, out_file=file)
