#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：第三章例子练习
import tensorflow as tf

if __name__ == '__main__':
    w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
    w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))

    x = tf.constant([[0.7, 0.9]])
    sess = tf.Session()

    sess.run(w1.initializer)
    sess.run(w2.initializer)
    a = tf.matmul(x, w1)
    y = tf.matmul(a, w2)

    print(sess.run(y))
    sess.close()
