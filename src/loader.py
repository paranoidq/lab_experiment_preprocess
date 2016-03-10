#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: loader.py
@time: 16/3/10 18:42
"""

import re
from src import path_constants as constant


def load_tags(path):
    tags = dict()
    p = re.compile(r'(.*),(\d+)')
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            g = p.match(line)
            tag = g.group(1)
            tag_count = g.group(2)
            tags[tag] = int(tag_count)
    return tags


def load_network(path):
    network = dict()
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.split(',')
            user = sp[0]
            retweeted_uid = sp[1]
            strength = int(sp[2])  # 代表转发的次数

            if user in network:
                network[user][retweeted_uid] = strength
            else:
                network[user] = dict()
                network[user][retweeted_uid] = strength
    return network





