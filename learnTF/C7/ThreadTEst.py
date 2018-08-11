#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：多线程案例
import tensorflow as tf
import numpy as np
import threading
import time


def Myloop(coord: tf.train.Coordinator, worker_id):
    while not coord.should_stop():
        if np.random.rand() < 0.1:
            print("stoping from id %d\n" % worker_id)
            coord.request_stop()
        else:
            print("worker id is %d\n" % worker_id)
        time.sleep(1)


coord = tf.train.Coordinator()
treads = [threading.Thread(target=Myloop, args=(coord, i)) for i in range(5)]
for i in treads:
    i.start()
coord.join(treads)
