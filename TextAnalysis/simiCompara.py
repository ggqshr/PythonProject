#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：文本相似度比较 将doc3和doc1与doc2分别比较，最后输出他们的相似度
import gensim as gm
import numpy
import jieba
from collections import defaultdict as df

doc1 = 'C:/Users/ggq/Desktop/dragon.txt'
doc2 = 'C:/Users/ggq/Desktop/mentang.txt'
# 要比较的文本
doc3 = 'C:/Users/ggq/Desktop/jiushen.txt'

d1 = open(doc1).read()
d2 = open(doc2).read()
d3 = open(doc3).read()

data1 = jieba.cut(d1)
data2 = jieba.cut(d2)
data3 = jieba.cut(d3)

data11 = ''
for i in data1:
    data11 += i + ' '
data22 = ''
for i in data2:
    data22 += i + ' '
data33 = ''
for i in data3:
    data33 += i + ' '
new_doc = data33

document = [data11, data22]

texts = [[word for word in d.split()] for d in document]

frequence = df(int) #构造词典
for text in texts:
    print text
    for token in text:
        frequence[token] += 1

dic = gm.corpora.Dictionary(texts)
dic.save("C:/Users/ggq/Desktop/wenben.txt")

# 变为稀疏向量
new_vec = dic.doc2bow(new_doc.split())
# 进一步处理
corpus = [dic.doc2bow(text) for text in texts]

tfidf = gm.models.TfidfModel(corpus)
# 得到特征数
ll = len(dic.token2id.keys())
index = gm.similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=ll)
# 得到相似性
sim = index[tfidf[new_vec]]
