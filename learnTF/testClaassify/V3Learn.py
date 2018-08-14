#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：V3模型学习

import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
from tensorflow.python.framework import graph_util

# Inception-V3模型瓶颈层的节点个数
BOTTLENECK_TENSOR_SIZE = 2048
# 瓶颈层输出的张量名称
BOTTLENECK_TENSOR_NAME = "pool_3/_reshape:0"
# 图像输入张量所对应的名称
JPEG_DATA_TENSOR_NAME = "DecodeJpeg/contents:0"

MODEL_DIR = "v3/"

MODEL_FILE = "classify_image_graph_def.pb"

CACHE_DIR = "tmp/bottleneck/"

INPUT_DATA = "train/"

VALIDATION_PERCENTAGE = 10

TEST_PERCENTAGE = 10

LEARN_RATE = 0.01
STEPS = 2000
BATCH = 100


# 创建图像列表，将图片数据读入到内存中，并按照文件夹名称分类
def create_image_lists(testing_percentage, validation_percentage):
    result = {}
    sub_dirs = [x[0] for x in os.walk(INPUT_DATA)]  # 获得数据目录下的所有目录名
    is_root_dir = True
    for sub_dir in sub_dirs:
        if is_root_dir:
            is_root_dir = False
            continue
        extensions = ['jpg', 'jpeg', 'JPG', 'JPEG']
        file_list = []
        dir_name = os.path.basename(sub_dir)
        for extension in extensions:
            file_glob = os.path.join(INPUT_DATA, dir_name, "*." + extension)
            file_list.extend(glob.glob(file_glob))
        if not file_list:
            continue
        label_name = dir_name.lower()
        trainning_image = []
        testing_image = []
        validation_imgae = []
        for file_name in file_list:
            base_name = os.path.basename(file_name)
            chance = np.random.randint(100)
            if chance < validation_percentage:
                validation_imgae.append(base_name)
            elif chance < (testing_percentage + validation_percentage):
                testing_image.append(base_name)
            else:
                trainning_image.append(base_name)
        result[label_name] = {
            'dir': dir_name,
            'training': trainning_image,
            'testing': testing_image,
            'validation': validation_imgae
        }
    return result


# 获取图像真实的物理地址
# 根据不同的类别和所属数据集返回
def get_image_path(image_list, image_dir, label_name, index, category):
    label_list = image_list[label_name]
    category_list = label_list[category]
    mod_index = index % len(category_list)
    base_name = category_list[mod_index]
    sub_dir = label_list['dir']
    full_path = os.path.join(image_dir, sub_dir, base_name)
    return full_path


def get_bolleneck_path(image_lists, label_name, index, category):
    return get_image_path(image_lists, CACHE_DIR, label_name, index, category) + '.txt'


def run_bottleneck_on_image(sess, image_data, image_data_tensor, bottleneck_tensor):
    bottleneck_values = sess.run(bottleneck_tensor, {image_data_tensor: image_data})
    bottleneck_values = np.squeeze(bottleneck_values)
    return bottleneck_values


def get_or_create_bottleneck(
        sess, image_lists, label_name, index, category, jpeg_data_tensor, bottleneck_tensor
):
    label_lists = image_lists[label_name]
    sub_dir = label_lists['dir']
    sub_dir_path = os.path.join(CACHE_DIR, sub_dir)
    if not os.path.exists(sub_dir_path):
        os.mkdir(sub_dir_path)
    bottleneck_path = get_bolleneck_path(image_lists, label_name, index, category)
    if not os.path.exists(bottleneck_path):
        image_path = get_image_path(image_lists, INPUT_DATA, label_name, index, category)
        image_data = gfile.FastGFile(image_path, 'rb').read()
        bottleneck_values = run_bottleneck_on_image(sess, image_data, jpeg_data_tensor, bottleneck_tensor)
        bottleneck_string = ",".join(str(x) for x in bottleneck_values)
        with open(bottleneck_path, 'w') as bottleneck_file:
            bottleneck_file.write(bottleneck_string)
    else:
        with open(bottleneck_path, 'r') as bottleneck_file:
            bottleneck_string = bottleneck_file.read()
        bottleneck_values = [float(x) for x in bottleneck_string.split(',')]
    return bottleneck_values


def get_random_cached_bottlenecks(
        sess, n_classes, image_lists, how_many, category,
        jpeg_data_tensor, bottleneck_tensor
):
    bottlenecks = []
    groud_truths = []
    for _ in range(how_many):
        label_index = random.randrange(n_classes)
        label_name = list(image_lists.keys())[label_index]
        image_index = random.randrange(65536)
        bottleneck = get_or_create_bottleneck(sess, image_lists, label_name, image_index, category,
                                              jpeg_data_tensor, bottleneck_tensor)
        groud_truth = np.zeros(n_classes, dtype=np.float32)
        groud_truth[label_index] = 1.0
        bottlenecks.append(bottleneck)
        groud_truths.append(groud_truth)
    return bottlenecks, groud_truths


def get_test_bottlenecks(sess, image_lists, n_classes, jpeg_data_tensor, bottleneck_tensor):
    bottlenecks = []
    groud_truths = []
    label_name_lists = list(image_lists.keys())
    for label_index, label_name in enumerate(label_name_lists):
        category = 'testing'
        for index, unused_base_name in enumerate(image_lists[label_name][category]):
            bottleneck = get_or_create_bottleneck(sess, image_lists, label_name, index, category, jpeg_data_tensor,
                                                  bottleneck_tensor)
            ground_truth = np.zeros(n_classes, dtype=np.float32)
            ground_truth[label_index] = 1.0
            bottlenecks.append(bottleneck)
            groud_truths.append(ground_truth)
    return bottlenecks, groud_truths


# 创建一个图，将从inception-v3模型中提取出来的变量放在创建的图中，在sess创建时传入，
# 确保能够将inception模型和新的全连接层串联起来，便于保存成pb文件。
def getGraph():
    graph = tf.Graph()
    with graph.as_default():
        with gfile.FastGFile(os.path.join(MODEL_DIR, MODEL_FILE), 'rb')as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(graph_def, name="",
                                                                      return_elements=[BOTTLENECK_TENSOR_NAME,
                                                                                       JPEG_DATA_TENSOR_NAME]
                                                                      )
    return graph, bottleneck_tensor, jpeg_data_tensor


# 创建最后一层全连接层
def get_train_(n_classes, bootleneck_input, ground_truth_input):
    regularizer = tf.contrib.layers.l2_regularizer(0.0001)
    with tf.name_scope('final_training_ops'):
        weights = tf.Variable(tf.truncated_normal([BOTTLENECK_TENSOR_SIZE, 1024], stddev=0.001))
        biases = tf.Variable(tf.zeros([1024]))
        logits = tf.nn.relu(tf.matmul(bootleneck_input, weights) + biases)
        weights1 = tf.Variable(tf.truncated_normal([1024, n_classes], stddev=0.001))
        biases1 = tf.Variable(tf.zeros([n_classes]))
        logits1 = tf.matmul(logits, weights1) + biases1
        final_tensor = tf.nn.softmax(logits1)
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits1, labels=ground_truth_input)
    cross_entropy_mean = tf.reduce_mean(cross_entropy)+regularizer(weights)
    train_step = tf.train.GradientDescentOptimizer(LEARN_RATE).minimize(cross_entropy_mean)
    with tf.name_scope('evaluation'):
        correct_prediction = tf.equal(tf.argmax(final_tensor, 1), tf.argmax(ground_truth_input, 1))
        evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    return train_step, evaluation_step


# 创建一个设置对象
def getconfig():
    config = tf.ConfigProto(allow_soft_placement=True)  # 允许在GPU上运行失败的计算转移到CPU上
    config.gpu_options.allow_growth = True  # 设置在一开始时不分配所有的GPU内存，而是随着需求自动增长
    config.gpu_options.per_process_gpu_memory_fraction = 0.9  # 设置允许使用的最大GPU内存
    return config


def get_placeHolder(n_classes, bottleneck_tensor, graph):
    # 使用placeholder_with_default函数将inception模型和新的全连接层串起来
    # 这样在保存时，如果使用gfile的方式即可将inception模型和新的模型一起保存起来
    # 但要注意placeholder_with_default函数传入的那个变量必须和生成的变量在一个图中，
    # 在同一个sess中使用的图是同一个，也可以自己创建图来控制，在sess创建的时候传入即可
    # 若使用saver的方式，即可不用使用placeholder_with_default函数，只需保证
    # inception 新的全连接层，以及saver使用的是一个sess，所以所有的图的信息都会保存到一个ckpt文件中
    with graph.as_default():
        bottlececk_input = tf.placeholder_with_default(bottleneck_tensor, [None, BOTTLENECK_TENSOR_SIZE],
                                                       name="BottleneckInput")
        ground_truth_input = tf.placeholder(tf.float32, [None, n_classes], name='GroundTruthInput')
    return bottlececk_input, ground_truth_input


# 保存成pb格式
# def main(_):
#     image_lists = create_image_lists(TEST_PERCENTAGE, VALIDATION_PERCENTAGE)
#     n_classes = len(image_lists.keys())  # 共有多少类别
#     graph, bottleneck_tensor, jpeg_data_tensor = getGraph()
#     bottlececk_input, ground_truth_input = get_placeHolder(n_classes, bottleneck_tensor, graph)
#     with tf.Session(config=getconfig(), graph=graph) as sess:
#
#         train_step, evaluation_step = get_train_(n_classes, bottlececk_input, ground_truth_input)
#         tf.global_variables_initializer().run()
#         for i in range(STEPS):
#             train_bottlenecks, train_ground_truth = get_random_cached_bottlenecks(sess,
#                                                                                   n_classes,
#                                                                                   image_lists,
#                                                                                   BATCH,
#                                                                                   'training',
#                                                                                   jpeg_data_tensor,
#                                                                                   bottleneck_tensor)
#             sess.run(train_step,
#                      feed_dict={
#                          bottlececk_input: train_bottlenecks,
#                          ground_truth_input: train_ground_truth
#                      })
#             if i % 100 == 0 or i + 1 == STEPS:
#                 validation_bottlenecks, validation_ground_truth = get_random_cached_bottlenecks(sess, n_classes,
#                                                                                                 image_lists, BATCH,
#                                                                                                 'validation',
#                                                                                                 jpeg_data_tensor,
#                                                                                                 bottleneck_tensor)
#                 validation_accuracy = sess.run(evaluation_step, feed_dict={
#                     bottlececk_input: validation_bottlenecks,
#                     ground_truth_input: validation_ground_truth
#                 })
#                 print("Step %d : validation accuracy on random sampled %d example = %.1f%%"
#                       % (i, BATCH, validation_accuracy * 100))
#         test_bottlenecks, test_ground_truth = get_test_bottlenecks(
#             sess, image_lists, n_classes, jpeg_data_tensor, bottleneck_tensor
#         )
#         test_accuracy = sess.run(evaluation_step, feed_dict={bottlececk_input: test_bottlenecks,
#                                                              ground_truth_input: test_ground_truth})
#         print('final test accuracy = %.1f%%' % (test_accuracy * 100))
#         constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph_def, output_node_names=[
#             'final_training_ops/Softmax'
#         ])
#         # 使用这种方式需要将原来的模型和新的模型串联起来，才能够保存在一个文件中，
#         with gfile.FastGFile("final.pb", 'wb') as f:
#             f.write(constant_graph.SerializeToString())

def main(_):
    image_lists = create_image_lists(TEST_PERCENTAGE, VALIDATION_PERCENTAGE)
    n_classes = len(image_lists.keys())  # 共有多少类别
    print(n_classes)
    with gfile.FastGFile(os.path.join(MODEL_DIR, MODEL_FILE), 'rb')as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(graph_def, name="",
                                                              return_elements=[BOTTLENECK_TENSOR_NAME,
                                                                               JPEG_DATA_TENSOR_NAME])
    bottlececk_input = tf.placeholder(tf.float32, [None, BOTTLENECK_TENSOR_SIZE],
                                      name="BottleneckInput")
    ground_truth_input = tf.placeholder(tf.float32, [None, n_classes], name='GroundTruthInput')
    train_step, evaluation_step = get_train_(n_classes, bottlececk_input, ground_truth_input)
    with tf.Session(config=getconfig()) as sess:
        saver = tf.train.Saver()
        tf.global_variables_initializer().run()
        for i in range(STEPS):
            train_bottlenecks, train_ground_truth = get_random_cached_bottlenecks(sess,
                                                                                  n_classes,
                                                                                  image_lists,
                                                                                  BATCH,
                                                                                  'training',
                                                                                  jpeg_data_tensor,
                                                                                  bottleneck_tensor)
            sess.run(train_step,
                     feed_dict={
                         bottlececk_input: train_bottlenecks,
                         ground_truth_input: train_ground_truth
                     })
            if i % 100 == 0 or i + 1 == STEPS:
                validation_bottlenecks, validation_ground_truth = get_random_cached_bottlenecks(sess, n_classes,
                                                                                                image_lists, BATCH,
                                                                                                'validation',
                                                                                                jpeg_data_tensor,
                                                                                                bottleneck_tensor)
                validation_accuracy = sess.run(evaluation_step, feed_dict={
                    bottlececk_input: validation_bottlenecks,
                    ground_truth_input: validation_ground_truth
                })
                print("Step %d : validation accuracy on random sampled %d example = %.1f%%"
                      % (i, BATCH, validation_accuracy * 100))
        test_bottlenecks, test_ground_truth = get_test_bottlenecks(
            sess, image_lists, n_classes, jpeg_data_tensor, bottleneck_tensor
        )
        test_accuracy = sess.run(evaluation_step, feed_dict={bottlececk_input: test_bottlenecks,
                                                             ground_truth_input: test_ground_truth})
        print('final test accuracy = %.1f%%' % (test_accuracy * 100))
        saver.save(sess, "ckpt/nn")


if __name__ == '__main__':
    tf.app.run()
