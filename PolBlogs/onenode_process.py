#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: onenode_process.py
@time: 16/3/19 16:13
"""



def load_edges():
    path = '/Users/paranoidq/316-data/polblogs/edges'
    edges = dict()
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.strip('\n').split(',')
            u1 = int(sp[0])
            u2 = int(sp[1])
            if u1 not in edges:
                edges[u1] = set()
            edges[u1].add(u2)
    edges = sorted(edges.items(), key= lambda x: len(x[1]), reverse=True)
    for u, es in edges:
        print(str(u) + ',' + str(len(es)) + '\n')


load_edges()