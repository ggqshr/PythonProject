#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：数据清洗
import numpy
import matplotlib.pylab as my
import pandas as pda

data = pda.read_csv("C:/Users/ggq/Desktop/jdcomputer.csv")
data['price'][data.price == -1] = 5488
data['price'][data.price == 0L] = 5488
data['price'][data.price > 10000] = 5488
data['commit'][data.commit > 2000] = 400
price = data.price
commit = data.commit
my.subplot(2,1,1)
my.plot(price, commit, 'o')
# 分布分析
pricemin = float(data['price'].min())
pricemax = float(data['price'].max())
commitmin = float(data['commit'].min())
commitmax = float(data['commit'].max())
pricedst = pricemax - pricemin
commitdst = commitmax - commitmin
pDst = pricedst / 24
cDst = commitdst / 24
pristy = numpy.arange(pricemin, pricemax, pDst)
comsty = numpy.arange(commitmin, commitmax, cDst)
my.subplot(2,2,3)
my.hist(data['price'].values, pristy)
my.subplot(2,2,4)
my.hist(data['commit'].values,comsty)
my.show()
