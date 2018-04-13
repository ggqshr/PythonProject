#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：knn算法实现 手写体识别
import operator

import numpy as num


def knn(k, testdata, traindata, labels):
    traindatasize = traindata.shape[0]  # 行数
    # 从列的方向去扩展
    testdata = testdata.astype('float64')
    diff = num.tile(testdata, (traindatasize, 1)) - traindata  # 差值
    sqdif = diff ** 2  # 平方
    sumcolumn = sqdif.sum(axis=1)  # 每一行的各列求和
    dist = sumcolumn ** 0.5  # 开方得到距离
    sortdist = dist.argsort()  # 排序
    diction = {}
    for i in range(0, k):
        vote = labels[sortdist[i]]
        diction[vote] = diction.get(vote, 0) + 1
    sortcount = sorted(diction.items(), key=operator.itemgetter(1), reverse=True)
    return sortcount[0][0]


from PIL import Image  # 图片处理


# 将图片转为txt
def transPic(fname):
    picdir = fname
    img = Image.open(picdir).resize((32, 32))
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img = img.rotate(90)
    fh = open("C:/Users/ggq/Desktop/pic.txt", 'a')
    # data = num.asarray(img)
    # num.savetxt("C:/Users/ggq/Desktop/pic.txt", data, fmt='%d', delimiter='')
    img.save('C:/Users/ggq/Desktop/pic1.png')  # 存储图片
    width = img.size[0]
    height = img.size[1]
    # 按照像素遍历
    for i in range(0, width):
        for j in range(0, height):
            color = img.getpixel((i, j))
            sumall = color[0] + color[1] + color[2]
            if sumall == 0:
                # 黑色
                print('1'),
                fh.write('1')
            else:
                # 白色
                print('0'),
                fh.write('0')
        print('\n')
        fh.write('\n')
    fh.close()
    img.close()


# 读取数据
def datatoarray(fname):
    arr = []
    fh = open(fname)
    for i in range(0, 32):
        thisline = fh.readline()
        for j in range(0, 32):
            arr.append(int(thisline[j]))
    return arr
    # arr = list(num.loadtxt(fname, dtype='str'))
    # arr = num.array([list(x) for x in arr]).reshape((1, 1024))
    # return arr


from os import listdir


# 截取文件名
def splitFname(fname):
    s = fname.split('.')[0].split('_')[0]
    return int(s)


# 读取训练数据
def gettraindata():
    label = []
    all_file = listdir('C:/Users/ggq/Desktop/knn-digits/trainingDigits')  # 得到文件夹下所有文件
    c = len(all_file)
    trainarray = num.zeros((c, 1024))
    for i in range(0, c):
        fname = all_file[i]
        thislable = splitFname(fname)
        label.append(thislable)
        trainarray[i, :] = datatoarray("C:/Users/ggq/Desktop/knn-digits/trainingDigits/" + fname)
    return trainarray, label


# 拿到训练集
def datatest():
    trainarr, lable = gettraindata()
    testlist = listdir("C:/Users/ggq/Desktop/knn-digits/testDigits")
    tnum = len(testlist)
    for i in range(0, tnum):
        thistestfile = testlist[i]
        testarr = datatoarray("C:/Users/ggq/Desktop/knn-digits/testDigits/" + thistestfile)
        rknn = knn(3, testarr, trainarr, lable)
        print(rknn)


if __name__ == '__main__':
    datatest()
