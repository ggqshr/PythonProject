#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：练习模块的基本使用
import numpy as num
import matplotlib.pylab as mtlp
import pandas as pda

x = num.array([1, 2, 3])
y = num.array([[1, 2, 3], [2, 3, 4], [5, 6, 7]])

data = pda.Series([1, 2, 3], ['one', 'two', 'three'])

data1 = pda.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], index=['one', 'two', 'three'], columns=['one', 'two', 'three'])

# mtlp.plot(x, y[0])#加上o代表散点图 plot代表室折线图或者散点图

# mtlp.show()

nor = num.random.normal(1.0,100.0,10000)#生成符合正态分布规律的1到100之间的10000个数

mtlp.hist(nor)

mtlp.show()
