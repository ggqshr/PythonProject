#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：BP人工神经网络 实现 课程销量预测 和 手写体数字识别 使用python3.6 因keras需要依赖tensorflow 又tensorflow无对应2.6 的版本
"""
  流程
1.读取对应数据
2.keras.modles Sequential  / keras.layers.core 中 Dense 建立层  Activation 激活函数
3.建立模型
4.建立层 use Dense
5.设置激活函数 Activation
6.模型编译
7.fit训练（学习）
8.验证（测试）
"""
from keras.models import Sequential
from keras.layers.core import Dense, Activation
import pandas as pda
import myknn

# 课程销量预测
'''
fname = 'C:\\Users\\ggq\\Desktop\\lesson.csv'
dataf = pda.read_csv(fname, encoding='gbk')
x = dataf.iloc[:, 1:5].as_matrix().astype(int)  # 转为数组
y = dataf.iloc[:, 5:].as_matrix().astype(int)
model = Sequential()
# 创建输入层
model.add(Dense(10, input_dim=len(x[0])))  # input_dim 代表多少个特征
model.add(Activation('relu'))  # 激活函数名
# 创建输出层
model.add(Dense(1, input_dim=1))
model.add(Activation('sigmoid'))
# 模型的编译
model.compile(loss='binary_crossentropy', optimizer='adam')  # 损失函数，求解方法，模式
# 训练
model.fit(x, y, nb_epoch=10, batch_size=100)  # 自变量和因变量,学习的次数
# 预测
rst = model.predict_classes(x).reshape(len(x))
xx = 0
for i in range(0, len(x)):
    if rst[i] != y[i]:
        xx += 1
print(xx)
print(1 - xx / len(x))  # 求准确率
'''
# 手写体数字识别
trainarray, labels = myknn.gettraindata()
testarr = myknn.datatoarray('C:/Users/ggq\\Desktop\\knn-digits\\testDigits\\5_50.txt')
xf = pda.DataFrame(trainarray).as_matrix().astype('int')
yf = pda.DataFrame(labels).as_matrix().astype('int')
model = Sequential()
# 创建输入层
model.add(Dense(10, input_dim=len(xf[0])))  # 多少个节点 input_dim 代表多少个特征
model.add(Activation('relu'))  # 激活函数名
# 创建输出层
model.add(Dense(1, input_dim=10))
model.add(Activation('sigmoid'))
# 模型的编译
model.compile(loss='mean_squared_error', optimizer='adam')  # 损失函数，求解方法，模式
# 训练
model.fit(xf, yf, nb_epoch=100, batch_size=6)  # 自变量和因变量,学习的次数
# 预测
rst = model.predict_classes(xf).reshape(len(xf))
print(rst)
