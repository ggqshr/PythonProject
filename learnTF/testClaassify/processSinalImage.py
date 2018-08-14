#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：处理单个照片
import tensorflow as tf
import sys


def process(filename):
    image_raw_data = tf.gfile.FastGFile(filename, 'rb').read()
    image_data = tf.image.decode_jpeg(image_raw_data)
    image = tf.image.convert_image_dtype(image_data, tf.float32)
    image = tf.image.resize_images(image, [440, 320], 2)
    image = tf.image.convert_image_dtype(image, tf.uint8)
    image = tf.image.encode_jpeg(image)
    with tf.Session() as sess:
        with tf.gfile.GFile("resize" + filename, 'wb') as f:
            f.write(image.eval())


if __name__ == '__main__':
    process(sys.argv[1])
