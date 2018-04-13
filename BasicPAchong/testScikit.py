#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：机器学习
from sklearn import tree

feature = [[130, 0], [140, 0], [150, 1], [160, 1]]
label = [0, 0, 1, 1]
cls = tree.DecisionTreeClassifier()
cls = cls.fit(feature, label)
print cls.predict([[130, 0]])
