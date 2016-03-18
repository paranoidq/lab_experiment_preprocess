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


def load_stop_words():
    stops = set()
    path = "/Users/paranoidq/316-data/polblogs/stopwords"
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            stops.add(line.strip("\s\n"))
    return stops


def load_id2words():
    words = dict()
    path = '/Users/paranoidq/316-data/polblogs/words'
    with open(path, 'r', encoding='utf-8') as fin:
        for no, line in enumerate(fin):
            word = line.strip("\s\n")
            words[no] = word
    return words


def load_uid2features():
    user_feats = dict()
    path = '/Users/paranoidq/316-data/polblogs/features'
    with open(path, 'r', encoding='utf-8') as fin:
        for no, line in enumerate(fin):
            uid = no
            features = line.split(',')
            user_feats[uid] = set()  # set
            for feat in features:
                user_feats[uid].add(feat)
    return user_feats

def load_edges():
    path = '/Users/paranoidq/316-data/polblogs/edges'
    edges = list()
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.strip('\n').split(',')
            u1 = int(sp[0])
            u2 = int(sp[1])
            edges.append((u1, u2))
    return edges


def load_pairword2id():
    path = '/Users/paranoidq/316-data/polblogs/pair_words'
    pairwords2id = dict()
    with open(path, 'r', encoding='utf-8') as fin:
        for no, line in enumerate(fin):
            pairwords2id[line.strip('\n')] = no
    return pairwords2id


def load_id2pairword():
    path = '/Users/paranoidq/316-data/polblogs/pair_words'
    id2pairwords = dict()
    with open(path, 'r', encoding='utf-8') as fin:
        for no, line in enumerate(fin):
            id2pairwords[no] = line.strip('\n')
    return id2pairwords


def load_trans():
    path = '/Users/paranoidq/316-data/polblogs/trans'
    trans_set = list()
    with open(path, 'r', encoding='utf-8') as fin:
        for line in fin:
            trans = list()
            sp = line.strip('\n').split(',')
            trans.append((int(x) for x in sp))
            trans_set.append(trans)
    return trans_set

