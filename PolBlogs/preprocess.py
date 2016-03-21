#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: preprocess.py
@time: 16/3/17 14:24
"""
from PolBlogs import loader as loader
from PolBlogs import constant
from operator import itemgetter


def preprocess_words(src_path, path):
    with open(src_path, 'r') as fin:
        with open(path, 'w+') as fout:
            for no, line in enumerate(fin):
                line = line.strip('\'\n').strip('\'')
                fout.write(str(no) + ',' + line + '\n')

def preprocess_edges(src_path, path):
    with open(src_path, 'r') as fin:
        with open(path, 'w+') as fout:
            for _id, line in enumerate(fin):
                sp = line.split(',')
                for _iid, s in enumerate(sp):
                    if s == '1':
                        fout.write(str(_id) + ',' + str(_iid) + '\n')





