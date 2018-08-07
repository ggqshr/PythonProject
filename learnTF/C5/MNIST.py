#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：手写识别
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data")
batch_size = 100
print("Training data size:", mnist.train.num_examples)

print("Validating data size:", mnist.validation.num_examples)

print("Testing data size:", mnist.test.num_examples)

# print("Example training data:", mnist.train.images[0])

print("Example training data label:", mnist.train.labels[0])

xs, ys = mnist.train.next_batch(batch_size)

print("xs.shape:", xs.shape)
print("ys.shape", ys.shape)
