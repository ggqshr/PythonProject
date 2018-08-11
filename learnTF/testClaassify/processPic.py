#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：截取图片

import cv2
import sys
from PIL import Image
import numpy as np
import os

SAVE_DIR = "train"


def CatchUsbVideo(label, filename, sfilename):
    cap = cv2.imread(filename)# 读取文件
    h, w = cap.shape[0], cap.shape[1] # 获得高和宽
    grey = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY) # 变成灰度图
    blurred = cv2.GaussianBlur(grey, (9, 9), 0) # 高斯模糊
    mask = np.zeros((h + 2, w + 2), np.uint8) # 设置mask
    cv2.floodFill(blurred, mask, (w - 1, h - 1), (255, 255, 255), (2, 2, 2), (3, 3, 3), 8)
    gradX = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=3)
    closed = cv2.dilate(closed, None, iterations=3)
    # 显示图像并等待10毫秒按键输入，输入‘q’退出程序

    (_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.cv2.boxPoints(rect))
    # draw a bounding box arounded the detected barcode and display the image
    # cv2.drawContours(cap, [box], -1, color, 3)
    # cv2.imshow('s',cap)
    # cv2.waitKey(0)
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    cropImg = cap[y1:y1 + hight, x1:x1 + width]
    if not os.path.exists(os.path.join(SAVE_DIR, label)):
        os.mkdir(os.path.join(SAVE_DIR, label))
    sava_dir = os.path.join(SAVE_DIR, label, sfilename)
    print(sava_dir)
    cv2.imwrite(sava_dir, cropImg, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    # cv2.imshow("Image", cropImg)
    #
    # cv2.imshow(window_name, cap)
    # c = cv2.waitKey(10)
    # if c & 0xFF == ord('q'):
    #     break

    # 释放摄像头并销毁所有窗口
    # cap.release()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    baseDir = os.walk("train")
    fileListWithDir = []
    for x in baseDir:
        fileListWithDir.append(x)
    alllabel = fileListWithDir[0][1]  # 获得所有的标签
    for fileDir, _, fileList in fileListWithDir[1:]:
        label = fileDir.split("\\")[1]
        for file in fileList:
            # print(label,os.path.join(fileDir,file))
            CatchUsbVideo(label, os.path.join(fileDir, file), file)
