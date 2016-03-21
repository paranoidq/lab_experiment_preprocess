#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: loader.py
@time: 16/3/17 20:34
"""


def load_stop_words(path):
    stops = set()
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            stops.add(line.strip("\n"))
    return stops

def load_enhanced_stops(path):
    stops = set()
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            stops.add(line.strip("\n"))
    return stops


def load_id2words(path):
    words = dict()
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.strip("\n").split(',')
            no = int(sp[0])
            word = sp[1]
            words[no] = word
    return words


def load_uid2features(path):
    user_feats = dict()
    with open(path, 'r', encoding='utf-8') as fin:
        for no, line in enumerate(fin):
            uid = no
            features = line.split(',')
            user_feats[uid] = set()  # set
            for feat in features:
                user_feats[uid].add(feat)
    return user_feats


def load_edges(path):
    edges = set()
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.strip('\n').split(',')
            u1 = int(sp[0])
            u2 = int(sp[1])
            edges.add((u1, u2))
    return edges


def load_trans(path):
    trans_set = dict()
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            trans = set()
            sp = line.strip('\n').split(',')
            trans.add((int(x) for x in sp))
            trans_set.append(trans)
    return trans_set


def load_patterns(path):
    pats = dict()
    with open(path, 'r', encoding='utf-8') as fin:
        for pat_id, line in enumerate(fin):
            pats = line.strip('\n').split('|')[0].split(' ')
            pats[pat_id] = set()
            for item_id in (int(x) for x in pats):
                pats[pat_id].add(item_id)
    return pats



