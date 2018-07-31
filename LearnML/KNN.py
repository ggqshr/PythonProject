#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：KNN算法实现
from numpy import *
import operator
import matplotlib.pylab as plt
from os import listdir


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]  # 获得训练数据的行数
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet  # 将传入的向量变成和已有数据一样的行数，然后逐行进行相减
    sqDiffMat = diffMat ** 2  # 将得到的结果进行平方
    sgDistances = sqDiffMat.sum(axis=1)  # 然后将同一行中的每一列进行相加
    distances = sgDistances ** 0.5  # 最后对数据进行开平方
    sortedDistIndicies = distances.argsort()  # 对数据进行排序，返回的是按照从小到大顺序进行排序后的数组下标
    classCount = {}
    for i in range(k):  # 开始遍历
        voteILabel = labels[sortedDistIndicies[i]]
        classCount[voteILabel] = classCount.get(voteILabel, 0) + 1  # 统计距离最近的几个点中出现次数最多的标签
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    arrayOlines = fr.readlines()
    numberLine = len(arrayOlines)
    returnMatrix = zeros((numberLine, 3))
    classLabelVector = []
    index = 0
    for line in arrayOlines:
        line = line.strip()
        listFormLine = line.split('\t')
        returnMatrix[index, :] = listFormLine[0:3]
        classLabelVector.append(int(listFormLine[-1]))
        index += 1
    return returnMatrix, classLabelVector


def autoNorm(dataSet):
    maxV = dataSet.max(0)
    minV = dataSet.min(0)
    ranges = maxV - minV
    nDataSet = zeros(dataSet.shape)
    m = dataSet.shape[0]
    nDataSet = dataSet - tile(minV, (m, 1))
    nDataSet = nDataSet / tile(ranges, (m, 1))
    return nDataSet, ranges, minV


def datinClassTest():
    hoRatio = 0.10
    dataMatrix, dataLabels = file2matrix("datingTestSet2.txt")
    normalData, ranges, minV = autoNorm(dataMatrix)
    m = normalData.shape[0]
    numTestCase = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestCase):
        classifyTestResult = classify(normalData[i, :], normalData[numTestCase:m, :], dataLabels[numTestCase:m], 3)
        print "the classifier came back with:%d,the real answer is:%d" % (classifyTestResult, dataLabels[i])
        if classifyTestResult != dataLabels[i]:
            errorCount += 1.0
        print "the total error rate is:%f" % (errorCount / float(numTestCase))


def image2Vector(filename):
    returnvector = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnvector[0, 32 * i + j] = int(lineStr[j])
    return returnvector


def handWriteClassTest():
    hwLabels = []
    trainDataFileList = listdir("trainingDigits")
    m = len(trainDataFileList)
    trainMatrix = zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainDataFileList[i]
        classLabel = int(fileNameStr.split('.')[0].split("_")[0])
        hwLabels.append(classLabel)
        trainMatrix[i, :] = image2Vector("trainingDigits/%s" % fileNameStr)
    testFileList = listdir("testDigits")
    errorCount = 0.0
    mtest = testFileList.__len__()
    for i in range(mtest):
        fileNameStr = testFileList[i]
        classLabel = int(fileNameStr.split(".")[0].split("_")[0])
        vector = image2Vector("testDigits/%s" % fileNameStr)
        classifyResult = classify(vector, trainMatrix, hwLabels, 3)
        print"the classifier came back with:%d，the real anawer is:%d" % (classifyResult, classLabel)
        if classifyResult != classLabel:
            errorCount += 1.0
    print "\nthe total error count is %d" % errorCount
    print "\nthe total error rate is %f" % (errorCount / float(mtest))


if __name__ == '__main__':
    handWriteClassTest()
    # m, l = file2matrix("./datingTestSet2.txt")
    # nD, ranges, minV = autoNorm(m)
    # print nD
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(m[:, 1], m[:, 2])
    # ax.scatter(m[:, 1], m[:, 2], 10 * array(l), 10 * array(l))
    # plt.show()
