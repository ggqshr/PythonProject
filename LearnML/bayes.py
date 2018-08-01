#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：朴素贝叶斯算法的实现
from numpy import *


def loadDataSet():  # 加载数据
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, classVec


# 基于原始单词构建单词表
def createVocabList(dataSet):
    vacabSet = set([])
    for document in dataSet:
        vacabSet = vacabSet | set(document)
    return list(vacabSet)


# 将输入的数据集根据构建的单词表转换为词向量
def setOfWords2Vec(vocabList, inoutset):  # 词集模型，每个单词只能出现一次
    returnVec = [0] * len(vocabList)
    for word in inoutset:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word %s is not in my Vocabulary!" % word
    return returnVec


def trainNBO(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)  # 文章的个数
    numWords = len(trainMatrix[0])  # 每篇文章单词的个数
    pAbusive = sum(trainCategory) / float(numTrainDocs)  # 计算类别是1的句子出现的概率
    p0Num = ones(numWords)  # 将所有单词出现次数初始化为1，防止后面计算时，相乘概率为0的情况发生
    p1Num = ones(numWords)
    p0Denom = p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]  # 矩阵相加，相同位置代表相同的单词是否出现，
            p1Denom += sum(trainMatrix[i])  # 计算句子中所有单词的数量
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num / p0Denom)  # 计算类别1中各个单词出现的次数
    p0Vect = log(p0Num / p0Denom)  # 计算类别2中
    return p0Vect, p1Vect, pAbusive


def classify(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)  # vec2Classify与类别1中每个单词出现的概率相乘，
    # 若vec2Classify出现了该单词，则该单词的概率会保留下来，若未出现该单词，则该单词的概率就会被置成0
    # 且此处使用的sum函数，因为在之前是将p0Vec变成了log(p0Vec)，所有其中的每个值都变成了E的对数，
    # 且对数想加就等于log(x*y)，所以此处使用的是sum函数，
    p0 = sum(vec2Classify * p0Vec) + log(1 - pClass1)
    if p0 > p1:
        return 0
    else:
        return 1


def testingNB():
    listOPosts, listClasses = loadDataSet()  # 加载数据
    myVocabList = createVocabList(listOPosts)  # 根据原始数据构建单词表
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))  # 将原始数据变为句子向量然后组合成为文章矩阵
    p0V, p1V, pAb = trainNBO(array(trainMat), array(listClasses))  # 更具训练数据获得各项单词在各个类别中出现的概率以及类别为1的概率
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classify(thisDoc, p0V, p1V, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classify(thisDoc, p0V, p1V, pAb)


# 将输入的数据集根据构建的单词表转换为词向量
def bagOfWords2Vec(vocabList, inoutset):  # 词袋模型，每个单词可以出现多次
    returnVec = [0] * len(vocabList)
    for word in inoutset:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            print "the word %s is not in my Vocabulary!" % word
    return returnVec


def textParse(bigString):
    import re
    listOfToken = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfToken if len(tok) > 2]


def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)  # create vocabulary
    trainingSet = range(50);
    testSet = []  # create test set
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])
    trainMat = [];
    trainClasses = []
    for docIndex in trainingSet:  # train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = trainNBO(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:  # classify the remaining items
        wordVector = bagOfWords2Vec(vocabList, docList[docIndex])
        if classify(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
            print "classification error", docList[docIndex]
    print 'the error rate is: ', float(errorCount) / len(testSet)
