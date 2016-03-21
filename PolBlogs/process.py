#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: process.py
@time: 16/3/18 20:25
"""

from PolBlogs import loader
from PolBlogs import constant

dir_path = constant.base


def gen_items():
    """
    1. load 过滤过的item
    2. generate item
    """
    stops = loader.load_stop_words()
    id2words = loader.load_id2words()

    f_words = dict()

    for _id, word in id2words.items():
        if word not in stops:
            f_words[_id] = word

    path = dir_path + 'items'
    # # 一共四种可能性
    # with open(path, 'w+', encoding='utf-8') as fout:
    #     for _id in f_words.keys():
    #         fout.write(str(_id) + ':' + "0,0" + '\n')
    #         fout.write(str(_id) + ':' + "0,1" + '\n')
    #         fout.write(str(_id) + ':' + "1,0" + '\n')
    #         fout.write(str(_id) + ':' + "1,1" + '\n')
    # 考虑node的值相等作为item
    with open(path, 'w+', encoding='utf-8') as fout:
        for _id in f_words.keys():
            fout.write(str(_id) + '\n')


def gen_trans():
    uid2features = loader.load_uid2features()
    edges = loader.load_edges()
    pairwords2id = loader.load_pairword2id()
    with open(dir_path+'trans', 'w+', encoding='utf-8') as fout:
        for u1, u2 in edges:
            trans = set()
            u1feats = uid2features[u1]
            u2feats = uid2features[u2]
            for feat1 in u1feats:
                if feat1 in u2feats:
                    trans.add(pairwords2id[feat1.strip('\n')+':1,1'])
                else:
                    trans.add(pairwords2id[feat1.strip('\n')+':1,0'])
            for feat2 in u2feats:
                if feat2 in u1feats:
                    trans.add(pairwords2id[feat2.strip('\n')+':1,1'])
                else:
                    trans.add(pairwords2id[feat2.strip('\n')+':0,1'])
            trans = sorted(trans)
            fout.write(','.join(str(x) for x in trans) + '\n')

import os
def gen_pats():
    # subprocess.call('/Users/paranoidq/316-data/polblogs/fpgrowth', )
    os.system('/Users/paranoidq/316-data/polblogs/fpgrowth -x -tm -m2 -s90 -v\"|%a\" \
              /Users/paranoidq/316-data/polblogs/trans /Users/paranoidq/316-data/polblogs/patterns')
    pats_path = '/Users/paranoidq/316-data/polblogs/patterns'
    id2items = loader.load_id2pairword()
    id2words = loader.load_id2words()

    pats_rep_path = '/Users/paranoidq/316-data/polblogs/patterns_repr'
    with open(pats_path, 'r', encoding='utf-8') as fin:
        with open(pats_rep_path, 'w+', encoding='utf-8') as fout:
            for line in fin:
                sp = line.strip('\n').split('|')
                support = sp[-1]
                items = sp[0].split(' ')
                buff = []
                for item_id in (int(x) for x in items):
                    item = id2items[item_id]
                    sp = item.split(':')
                    word = id2words[int(sp[0])]
                    if sp[1] == '0,1':
                        buff.append((word, '@'))
                    elif sp[1] == '1,0':
                        buff.append(('@', word))
                    elif sp[1] == '1,1':
                        buff.append((word, word))
                for w1, w2 in buff:
                    fout.write(w1 + ',' + w2 + '|')
                fout.write(str(support) + '\n')



