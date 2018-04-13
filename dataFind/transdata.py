#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：数据转换
import numpy as num
import pandas as pda
import matplotlib.pylab as myl
import sklearn.decomposition as sd

data = pda.read_csv('C:/Users/ggq/Desktop/jdcomputer.csv')
data['price'][data.price == -1] = 6707
data['price'][data.price == 0] = 6707
price = data[['price']]
commit = data[['commit']]
d1 = pda.concat([price, commit], axis=1)  # 0是行 1是列
d1 = pda.DataFrame(d1)
# 离差标准化
d2 = (d1 - d1.min()) / (d1.max() - d1.min())
# 标准差标准化
d3 = (d1 - d1.mean()) / d1.std()
# 小数定标标准化
k = num.ceil(num.log10(d1.abs().max()))
d4 = d1 / 10 ** k
# 连续性数据离散化
# 等宽离散化
cc = commit['commit'].values
d5 = pda.cut(cc, 3, labels=['便宜', '时钟', '昂贵'])
#非等宽离散化
d6 = pda.cut(cc,[2,10,300,4000])
#属性构造
pc = data['commit']/data['price']
data[u'评价比'] = pc

#主成分分析
pca1 = sd.PCA()
pca1.fit(data[['price','commit',u'评价比']])
#返回特征量
pcmp = pca1.components_
#各个主成分中各自方差的百分比（贡献率）

#降维

pca2 = sd.PCA(2)
pca2.fit(data[['price','commit',u'评价比']])
trandata = pca2.transform(data[['price','commit',u'评价比']])#降维
# pca2.inverse_transform(data[['price','commit',u'评价比']])#恢复
