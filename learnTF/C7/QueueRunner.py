#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：QueueRunner案例
import tensorflow as tf

queue = tf.FIFOQueue(100, 'float')
enqueue = queue.enqueue([tf.random_normal([1])])
qr = tf.train.QueueRunner(queue, [enqueue] * 5)
tf.train.add_queue_runner(qr)
out_tensor = queue.dequeue()
with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess,coord)
    for _ in range(3):
        print(sess.run(out_tensor)[0])
    coord.request_stop()
    coord.join(threads)
