#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：
import argparse
import os
import cv2
import numpy as np


def args_parse():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dir', required=True, help='dir to process')
    ap.add_argument("-o", "--output_dir", required=True,
                    help="output dir")
    ap.add_argument("-m", "--model", required=True, default='f', choices=['f', 'n'], type=str,
                    help="f representative floodFill n representative not floodFill")
    args = vars(ap.parse_args())
    return args


# 使用洪泛填充截图图像
def processImage(image, output_dir, avgs):
    print('processing image : %s,store to %s' % (image.split(os.path.sep)[-1], output_dir))
    cc = cv2.imread(image)
    cc = cv2.resize(cc, (320, 320), cv2.INTER_NEAREST)
    h, w = cc.shape[0], cc.shape[1]
    cap = cv2.cvtColor(cc.copy(), cv2.COLOR_BGR2GRAY)
    cap = cv2.GaussianBlur(cap, (9, 9), 0)
    if avgs['model'] is 'f':
        mask = np.zeros((h + 2, w + 2), np.uint8)  # 设置mask
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
    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    cropImg = cc[y1:y1 + hight, x1:x1 + width]
    if not os.path.exists(output_dir):  # 若目录不存在，就创建目录
        os.mkdir(output_dir)
    if os.path.isdir(output_dir):  # 如果输出目录是一个目录
        filename = 'resize' + image.split(os.path.sep)[-1]
        sava_dir = os.path.join(output_dir, filename)
        cv2.imwrite(sava_dir, cropImg, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    else:  # 若不是目录，就直接存储
        cv2.imwrite(output_dir, cropImg, [int(cv2.IMWRITE_JPEG_QUALITY), 80])


# 不使用洪泛填充
# def not_use_flood_fill(image: str, output_dir):
#     print('processing image : %s,store to %s' % (image.split(os.path.sep)[-1], output_dir))
#     cap = cv2.imread(image)
#     cap = cv2.resize(cap, (320, 320), cv2.INTER_NEAREST)
#     cap = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
#     cap = cv2.GaussianBlur(cap, (9, 9), 0)
#     gradX = cv2.Sobel(cap, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
#     gradY = cv2.Sobel(cap, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
#     gradient = cv2.subtract(gradX, gradY)
#     gradient = cv2.convertScaleAbs(gradient)
#     blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
#     (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
#     closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#     closed = cv2.erode(closed, None, iterations=3)
#     closed = cv2.dilate(closed, None, iterations=3)
#     (_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
#     rect = cv2.minAreaRect(c)
#     box = np.int0(cv2.cv2.boxPoints(rect))
#     Xs = [i[0] for i in box]
#     Ys = [i[1] for i in box]
#     x1 = min(Xs)
#     x2 = max(Xs)
#     y1 = min(Ys)
#     y2 = max(Ys)
#     hight = y2 - y1
#     width = x2 - x1
#     cropImg = cap[y1:y1 + hight, x1:x1 + width]
#     if os.path.isdir(output_dir):  # 如果输出目录是一个目录
#         if not os.path.exists(output_dir):  # 若目录不存在，就创建目录
#             os.mkdir(output_dir)
#         filename = 'resize' + image
#         sava_dir = os.path.join(output_dir, filename)
#         cv2.imwrite(sava_dir, cropImg, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
#     else:  # 若不是目录，就直接存储
#         cv2.imwrite(output_dir, cropImg, [int(cv2.IMWRITE_JPEG_QUALITY), 80])


def process_signal(file, output_dir, args):
    processImage(file, output_dir, args)


def processdir(dir, output_dir, args):
    # 遍历文件夹，对每个文件调用process-signal方法即可
    file_list = [x for x in os.walk(dir)]
    for dir_name, _, file_name in file_list:
        for file in file_name:
            process_signal(os.path.join(dir_name, file), output_dir, args)


if __name__ == '__main__':
    args = args_parse()
    output_dir = args['output_dir']
    input_dir = args['dir']
    if os.path.isdir(input_dir):
        processdir(input_dir, output_dir, args)
    else:
        process_signal(input_dir, output_dir, args)
