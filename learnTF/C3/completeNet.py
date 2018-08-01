#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：完整的神经网络实现

import tensorflow as tf
from numpy.random import RandomState
with tf.device("/cpu:0"): # 可以设置使用的设备，选择gpu或者cpu
    # 定义训练数据batch的大小。
    batch_size = 8
    w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
    w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))

    x = tf.placeholder(tf.float32, shape=(None, 2), name="X-input")
    y_ = tf.placeholder(tf.float32, shape=(None, 1), name="y-input")

    # 定义神经网络前向传播的过程
    a = tf.matmul(x, w1)
    y = tf.matmul(a, w2)
    # 定义损失函数和反向传播的算法
    cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))
    train_step = tf.train.AdadeltaOptimizer(0.001).minimize(cross_entropy)

    rdm = RandomState(1)
    dataset_size = 128
    X = rdm.rand(dataset_size, 2)
    Y = [[int(x1 + x2 < 1)] for (x1, x2) in X]
    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        # 训练之前的值
        print(sess.run(w1))
        print(sess.run(w2))

        # 设定训练的轮数
        STEPS = 5000
        for i in range(STEPS):
            # 每次选取batch_size个样本进行训练
            start = (i * batch_size) % dataset_size
            end = min(start + batch_size, dataset_size)

            # 通过选取的样本训练神经网络并更新参数
            sess.run(train_step, feed_dict={x: X[start:end], y_: Y[start:end]})
            if i % 1000 == 0:
                total_cross_entropy = sess.run(cross_entropy, feed_dict={x: X, y_: Y})
                print("after %d trainning steps,cross_entropy on all data is %g" % (i, total_cross_entropy))
        # 训练之后的值，经过反向传播优化
        print(sess.run(w1))
        print(sess.run(w2))
