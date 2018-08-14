#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：
import tensorflow as tf
import numpy as np

PB_FILE_DIR = "final.pb"


def predictByPbFIle():
    with tf.gfile.FastGFile(PB_FILE_DIR, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name("final_training_ops/Softmax:0")
        imageData = tf.gfile.FastGFile("flower_photos/sunflowers/24459548_27a783feda.jpg", 'rb').read()
        predict = sess.run(softmax_tensor, feed_dict={"DecodeJpeg/contents:0": imageData})
        predict = np.squeeze(predict)
        print(predict)
        print(sess.run(tf.argmax(predict)))


def predictByCkptFIle():
    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state('ckpt/')
        saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path + '.meta')
        saver.restore(sess, ckpt.model_checkpoint_path)
        g = tf.get_default_graph()
        softmax_tensor = g.get_tensor_by_name("pool_3/_reshape:0")
        imageData = tf.gfile.FastGFile("resize20180812_165259.jpg", 'rb').read()
        botlleneck = sess.run(softmax_tensor, feed_dict={"DecodeJpeg/contents:0": imageData})
        predict = sess.run(g.get_tensor_by_name('final_training_ops/Softmax:0'),
                           feed_dict={g.get_tensor_by_name('BottleneckInput:0'): botlleneck})
        predict = np.squeeze(predict)
        print(predict)
        print(sess.run(tf.argmax(predict)))


if __name__ == '__main__':
    print("CKPT")
    predictByCkptFIle()
    # print("pb")
    # predictByPbFIle()
