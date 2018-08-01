#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：决策树实现和学习
from math import log
import operator


def calShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCount = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel] = 0
        labelCount[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCount:
        prob = float(labelCount[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, "no"],
               [0, 1, "no"],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVect in dataSet:
        if featVect[axis] == value:
            reduceFeatVect = featVect[:axis]
            reduceFeatVect.extend(featVect[axis + 1:])  # 寻找第axis个位置值为value的数据
            retDataSet.append(reduceFeatVect)
    return retDataSet


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1  # 获得特征数
    baseEntropy = calShannonEnt(dataSet)  # 计算原有数据集的信息熵
    bestInfoGain = 0.0
    beatFeature = -1
    for i in range(numFeatures):
        featList = [e[i] for e in dataSet]  # 得到所有的特征
        uniqueVals = set(featList)  # 特征去重
        newEntropy = 0.0
        for value in uniqueVals:  # 按照每个特征分割数据集
            newDataSet = splitDataSet(dataSet, i, value)
            prob = float(len(newDataSet)) / float(len(dataSet))  # 计算新划分的数据集占旧数据集的比例
            newEntropy += prob * calShannonEnt(newDataSet)  # 加权计算所有重新划分的数据集的信息熵
        infoGain = baseEntropy - newEntropy  # 计算信息增益，信息增益是信息熵的减少或者数据无序度的减少，通过计算信息增益
        # 可以比较哪一种划分方式使得划分过后的数据集混乱度最小，即划分的最合理
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            beatFeature = i
    return beatFeature


# 当叶子节点或者终止块中的分类结果不唯一时，使用多数表决的方法，即统计当前分类结果的类别数量，类别数量的多的为当前的分类
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    classList = [e[-1] for e in dataSet]
    if classList.count(classList[0]) == len(classList):  # 若当前节点的所有分类相同，则返回当前类别列表并退出递归
        return classList[0]
    if len(dataSet[0]) == 1:  # 若当前数据集的特征都已经使用完成，则返回投票选举的类别结果
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del (labels[bestFeat])
    featValue = [e[bestFeat] for e in dataSet]
    uniqueVals = set(featValue)
    for value in uniqueVals:
        subLabel = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabel)
    return myTree


def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


def storeTree(inputTree, fileName):
    import pickle
    fw = open(fileName, 'w')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(fileName):
    import pickle
    fr = open(fileName)
    return pickle.load(fr)
