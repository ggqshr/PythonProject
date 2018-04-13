#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：
import threading


class A(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print 'a'
        # threading.Thread.run(self)


class B(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print 'b'
        # threading.Thread.run(self)


if __name__ == '__main__':
    a = A()
    b = B()
    a.start()
    b.start()
