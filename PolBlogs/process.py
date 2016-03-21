#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: process.py
@time: 16/3/18 21:57
"""

from PolBlogs import loader
from PolBlogs import constant
import os


def process():

    id2words = None
    uid2feats = None
    edges = None
    id2items = None

    stops = loader.load_stop_words(constant.stop_words_path)
    en_stops = loader.load_enhanced_stops(constant.enhanced_stops_path)
    stops = stops.union(en_stops)

    # 过滤stop words
    id2words = loader.load_id2words(constant.id2wordspath)
    filtered_words = dict()
    for _id, word in id2words.items():
        if word not in stops:
            filtered_words[_id] = word
    id2words = filtered_words

    # 过滤feature中的stop words
    uid2feats = dict()
    with open(constant.feat_src_path, 'r', encoding='utf-8') as fin:
        with open(constant.feat_path, 'w+', encoding='utf-8') as fout:
            for uid, line in enumerate(fin):
                sp = line.strip('\n').split(",")
                uid2feats[uid] = set()
                for featno, fit in enumerate(sp):
                    if fit == "1" and featno in id2words:
                        uid2feats[uid].add(featno)
                fout.write(','.join((str(x) for x in sorted(uid2feats[uid]))) + '\n')


    # 生成items
    id2items = id2words  # 直接用id2words即可,表征边的两个点相同的word

    # 生成trans, 并写入文件
    edges = loader.load_edges(constant.edges_path)
    with open(constant.trans_path, 'w+', encoding='utf-8') as fout:
        for u1, u2 in edges:
            trans = set()
            u1feats = uid2feats[u1]
            u2feats = uid2feats[u2]
            for feat in u1feats.intersection(u2feats):
                trans.add(int(feat))
            trans = sorted(trans)
            fout.write(','.join(str(x) for x in trans) + '\n')

    # 产生pattern
    # 增加过滤词
    # os.system('/Users/paranoidq/316-data/polblogs/fpgrowth -q1 -m1 -n1 -s90 -v\"|%a\" ' +
    #            trans_path + ' ' + pats_path)
    os.system('/Users/paranoidq/316-data/polblogs/fpgrowth -tm -q1 -m2 -s50 -v\"|%a\" ' +
              constant.trans_path + ' ' + constant.pats_path)
    with open(constant.pats_path, 'r', encoding='utf-8') as fin:
        with open(constant.pats_repr_path, 'w+', encoding='utf-8') as fout:
            for line in fin:
                sp = line.strip('\n').split('|')
                support = sp[-1]
                items = sp[0].split(' ')
                for item_id in items:
                    fout.write(id2items[int(item_id)] + '|')
                    # fout.write(id2items[int(item_id)])
                fout.write(str(support) + '\n')
                # fout.write('\n')



if __name__ == '__main__':
    process()





