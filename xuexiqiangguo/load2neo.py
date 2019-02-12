#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作用：
from py2neo import Graph, Node, Relationship


def load_data():
    data = []
    f = open("./output.txt", encoding="utf-8")
    line = f.readline()
    while line.__len__() > 0:
        want_line = line.split("\t")[-1]
        want_line = want_line.replace("(", "").replace(")", "").replace("\n", "")
        line_data = want_line.split(",")
        print(line_data)
        data.append(line_data)
        line = f.readline()
    return data


graph = Graph('http://119.23.224.186:7474', username='neo4j', password='1129')

data = load_data()
d_dict = {}
for d in data:  # type:list
    a = Node("test2", name=d[0])
    if d[0] in d_dict:
        a = d_dict[d[0]]
    else:
        d_dict[d[0]] = a
        graph.create(a)
    b = Node("test2", name=d[2],size=10)
    if d[1] in d_dict:
        b = d_dict[d[1]]
    else:
        d_dict[d[1]] = b
        graph.create(b)
    r = Relationship(a, d[1], b)
    graph.create(r)
