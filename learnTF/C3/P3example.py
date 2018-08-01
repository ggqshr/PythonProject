#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：第三章例子练习
import tensorflow as tf

if __name__ == '__main__':
    w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
    w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))

    # x = tf.constant([[0.7, 0.9]]) #常量的形式，直接传入具体的值
    x = tf.placeholder(tf.float32, shape=(1, 2), name="input")  # placeholder的形式，在运行时在传入,
    # shape参数可以指定，也可以让框架自行推断，默认一行就是一轮迭代中需要输入的数据，多行数据就会迭代多次
    sess = tf.Session()
    init_op = tf.initialize_all_variables()
    sess.run(init_op)
    a = tf.matmul(x, w1)
    y = tf.matmul(a, w2)

    # print(sess.run(y))
    print(sess.run(y, feed_dict={x: [[0.7, 0.9], [0.7, 0.5]]}))  # 使用placeholder需要传入参数 可以传入
    sess.close()
