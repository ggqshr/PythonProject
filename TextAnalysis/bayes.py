#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：贝叶斯分类器实现
import numpy as np
import myknn


class Bayes:
    def __init__(self):
        self.length = -1  # 初始化长度
        self.labels = dict()  # 标签
        self.vector = dict()  # 向量

    def fit(self, dataSet, labels):  # 训练
        if len(dataSet) != len(labels):
            raise ValueError('您输入的测试数组跟类别数组长度不一致')  # 引发一个异常相当于throws
        self.length = len(dataSet[0])  # 测试数据特征值的长度
        labelNum = len(labels)  # 类别所有的数量
        noreaptenum = set(labels)  # 不重复的类别的数量
        for item in noreaptenum:
            self.labels[item] = float(labels.count(item)) / labelNum  # 当前类别占类别总数的比例
        for vec, label in zip(dataSet, labels):
            if label not in self.vector:
                self.vector[label] = []
            self.vector[label].append(vec)
        print u'训练结束'
        return self

    def btest(self, testdata, labelset):
        if self.length == -1:
            raise ValueError('还没有进行训练')
        # 计算testdata分别为各个类别的概率
        ibdict = dict()
        for thislb in labelset:
            p = float(1)
            alllabel = self.labels[thislb]
            allvector = self.vector[thislb]
            vnum = len(allvector)
            allvector = np.array(allvector).T
            for index in xrange(0, len(testdata)):
                vec = list(allvector[index])
                p *= float(vec.count(testdata[index])) / vnum
            ibdict[thislb] = p * alllabel
        thislabel = sorted(ibdict, key=lambda x: ibdict[x], reverse=True)[0]
        return thislabel


if __name__ == '__main__':
    trainarray, labels = myknn.gettraindata()
    testarr = myknn.datatoarray('C:/Users/ggq\\Desktop\\knn-digits\\testDigits\\5 _50.txt')
    by1 = Bayes()
    by1.fit(trainarray, labels)
    print by1.btest(testarr, labels)
