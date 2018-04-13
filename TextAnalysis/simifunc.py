#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：文本相似度分析的封装
import gensim as gm
import jieba


class Simi():
    dataf = None
    texts = None
    dic = None

    def __init__(self, dataf):
        self.dataf = dataf

    def process(self):
        document = []
        for d in self.dataf:
            ff = ''
            for dd in jieba.cut(d):
                ff += dd + ' '
            document.append(ff)
        self.texts = [[word for word in d.split()] for d in document]
        self.dic = gm.corpora.Dictionary(self.texts)

    def analysis(self, sim):
        data = jieba.cut(sim)
        dd = ''
        for i in data:
            dd += i + ' '
        new_vec = self.dic.doc2bow(dd.split())
        corpus = [self.dic.doc2bow(text) for text in self.texts]
        tfidf = gm.models.TfidfModel(corpus)
        # 得到特征数
        ll = len(self.dic.token2id.keys())
        index = gm.similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=ll)
        sim = index[tfidf[new_vec]]
        return [float(s) for s in sim]
