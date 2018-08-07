#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：了解损失函数对模型的影响
import tensorflow as tf
from numpy.random import RandomState

batch_size = 8

x = tf.placeholder(tf.float32, shape=(None, 2), name="x-input")
y_ = tf.placeholder(tf.float32, shape=(None, 1), name="y-input")

w1 = tf.Variable(tf.random_normal([2, 1], stddev=1, seed=1))
y = tf.matmul(x, w1)

loss_less = 10
loss_more = 1

loss = tf.reduce_sum(tf.where(tf.greater(y, y_), (y - y_) * loss_more, (y_ - y) * loss_less))
train_step = tf.train.AdadeltaOptimizer(0.001).minimize(loss)

rdm = RandomState()
dataSet_size = 128
X = rdm.rand(dataSet_size, 2)

Y = [[x1 + x2 + rdm.rand() / 10.0 - 0.05] for (x1, x2) in X]

with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    STEP = 5000
    for i in range(STEP):
        start = (i * batch_size) % dataSet_size
        end = min(start + batch_size, dataSet_size)
        sess.run(train_step, feed_dict={x: X[start:end], y_: Y[start:end]})
        print(sess.run(w1))
