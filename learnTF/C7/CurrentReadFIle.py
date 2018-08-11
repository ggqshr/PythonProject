#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：多线程读文件
import tensorflow as tf

files = tf.train.match_filenames_once("path/to/data.tfrecords-*")
filename_queue = tf.train.string_input_producer(files, shuffle=False)

reader = tf.TFRecordReader()
_, serialized_example = reader.read(filename_queue)
features = tf.parse_single_example(
    serialized=serialized_example,
    features={
        'i': tf.FixedLenFeature([], tf.int64),
        'j': tf.FixedLenFeature([], tf.int64),
    }
)
# with tf.Session() as sess:
#     tf.local_variables_initializer().run()
#     print(sess.run(files))
#     coord = tf.train.Coordinator()
#     threads = tf.train.start_queue_runners(sess, coord)
#     for i in range(6):
#         print(sess.run([features['i'], features['j']]))
#     coord.request_stop()
#     coord.join(threads)


# 使用batch函数
example, label = features['i'], features['j']
batch_size = 3
# 组合样例的队列中最多可以存储的样例个数，这个队列如果太大，那么需要占用很多内存资源
# 如果太小，那么出队操作可能会因为没有数据而被阻塞，从而导致训练效率降低，一般来说
# 这个队列的大小会和每一个batch的大小相关，下面一行代码给出了设置队列大小的一种方式
capacity = 1000 + 3 * batch_size

# example_batch, label_batch = tf.train.batch(
#     [example, label], batch_size=batch_size, capacity=capacity
# )
#
# with tf.Session() as sess:
#     tf.local_variables_initializer().run()
#     coord = tf.train.Coordinator()
#     threads = tf.train.start_queue_runners(sess, coord)
#
#     for i in range(2):
#         cur_example_batch, cur_label_batch = sess.run([example_batch, label_batch])
#         print(cur_example_batch, cur_label_batch)
#     coord.request_stop()
#     coord.join(threads)

# 使用shuffle_batch函数
example, label = features['i'], features['j']

example_batch, label_batch = tf.train.shuffle_batch([example, label], batch_size, capacity, 30)

with tf.Session() as sess:
    tf.local_variables_initializer().run()
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess, coord)

    for i in range(2):
        cur_example_batch, cur_label_batch = sess.run([example_batch, label_batch])
        print(cur_example_batch, cur_label_batch)
    coord.request_stop()
    coord.join(threads)