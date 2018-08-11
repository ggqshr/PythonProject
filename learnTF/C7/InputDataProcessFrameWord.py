#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：输入数据处理框架
import tensorflow as tf
from ProcessImage import *


def inference():
    pass


def calc_loss():
    pass


files = tf.train.match_filenames_once('path/to/data.tfrecords-*')
filename_queue = tf.train.string_input_producer(files, shuffle=False)

reader = tf.TFRecordReader()
_, serialized_example = reader.read(filename_queue)
features = tf.parse_single_example(
    serialized=serialized_example,
    features={
        "image": tf.FixedLenFeature([], tf.string),
        'label': tf.FixedLenFeature([], tf.int64),
        'height': tf.FixedLenFeature([], tf.int64),
        'width': tf.FixedLenFeature([], tf.int64),
        'channels': tf.FixedLenFeature([], tf.int64)
    }
)
image, label = features['image'], features['label']
height, width = features['height'], features['width']
channels = features['channels']

decodeed_image = tf.decode_raw(image, tf.uint8)
decodeed_image.set_shape([height, width, channels])

image_size = 299
distordted_image = preprocess_for_train(decodeed_image, image_size, image_size, None)

min_after_dequeue = 10000
batch_size = 100
capacity = min_after_dequeue + 3 * batch_size
image_batch, label_batch = tf.train.shuffle_batch([distordted_image, label], batch_size, capacity, min_after_dequeue)
# 定义神经网络的结构以及优化过程，
logit = inference(image_batch)
loss = calc_loss(logit, label_batch)
train_step = tf.train.GradientDescentOptimizer(learning_rate=1).minimize(loss)

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess, coord)
    TRAINING_ROUNDS = 1000  # 训练轮数
    for i in range(TRAINING_ROUNDS):
        sess.run(train_step)
    coord.request_stop()
    coord.join(threads)
