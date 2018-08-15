#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：
import cv2
import numpy as np
cap = cv2.imread('./20180811_085507.jpg')
cap = cv2.resize(cap, (320, 320), cv2.INTER_NEAREST)
h, w = cap.shape[0], cap.shape[1]
cc = cap.copy()
cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
cap = cv2.GaussianBlur(cap, (9, 9), 0)
mask = np.zeros((h + 2, w + 2), np.uint8) # 设置mask
cv2.floodFill(cap, mask, (w - 1, h - 1), (255, 255, 255), (2, 2, 2), (3, 3, 3), 8)
gradX = cv2.Sobel(cap, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(cap, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)
blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
(_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
closed = cv2.erode(closed, None, iterations=3)
closed = cv2.dilate(closed, None, iterations=3)
(_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
rect = cv2.minAreaRect(c)
box = np.int0(cv2.cv2.boxPoints(rect))
cv2.drawContours(cc, [box], -1, (0,255,0), 3)
cv2.imshow('s', cc)
cv2.waitKey(0)
cv2.destroyAllWindows()
