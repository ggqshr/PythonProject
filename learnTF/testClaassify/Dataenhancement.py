#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：增强图像数据
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import cv2
import numpy as np

data = []
label = []
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                         height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                         horizontal_flip=True, fill_mode="nearest")
i = 0
for x, y in aug.flow_from_directory('mytraindata', batch_size=20):
    data.extend(x)
    label.extend(y)
    i += 1
    if i == 1:
        break
train_x,test_x,train_y,test_y = train_test_split(data,label)
print()
# print('train data len : %d train label len : %d'%(len(train_x),len(train_y)))
# print('test data len : %d test label len : %d'%(len(test_x),len(test_y)))