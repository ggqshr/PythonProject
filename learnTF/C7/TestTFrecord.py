#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：TFRecord例子
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

MNIST_DATA_DIR = "../C6/MNIST_DATA/"


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


mnist = input_data.read_data_sets(MNIST_DATA_DIR, dtype=tf.uint8, one_hot=True)
images = mnist.train.images
labels = mnist.train.labels
pixels = images.shape[1]
num_example = mnist.train.num_examples
filename = "recored/nn.record"
writer = tf.python_io.TFRecordWriter(filename)
for index in range(num_example):
    image_raw = images[index].tostring()
    example = tf.train.Example(features=tf.train.Features(feature={
        'pixels': _int64_feature(pixels),
        'label': _int64_feature(np.argmax(labels[index])),
        'image_raw': _bytes_feature(image_raw)
    }))
    writer.write(example.SerializeToString())
writer.close()
