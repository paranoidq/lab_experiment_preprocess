#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: process.py
@time: 16/3/17 14:24
"""
from PolBlogs import loader as loader
from operator import itemgetter

dir_path = "/Users/paranoidq/316-data/polblogs/"

def process():

    pass

def process_words():
    with open(dir_path+'words_src', 'r') as fin:
        with open(dir_path+'words', 'w+') as fout:
            for line in fin:
                line = line.strip('\'\n').strip('\'')
                fout.write(line + '\n')

def process_edges():
    with open(dir_path+'edges_src', 'r') as fin:
        with open(dir_path+'edges', 'w+') as fout:
            for _id, line in enumerate(fin):
                sp = line.split(',')
                for _iid, s in enumerate(sp):
                    if s == '1':
                        fout.write(str(_id) + ',' + str(_iid) + '\n')

def process_features():

    stops = loader.load_stop_words()
    id2words = loader.load_id2words()
    f_words = dict()

    for _id, word in id2words.items():
        if word not in stops:
            f_words[_id] = word

    src_path = dir_path + 'features_src'
    dest_path = dir_path + 'features'
    with open(dest_path, 'w+', encoding='utf-8') as fout:
        with open(src_path, 'r', encoding='utf-8') as fin:
            for uid, line in enumerate(fin):
                sp = line.strip('\n').split(",")
                l = list()
                for featno, fit in enumerate(sp):
                    if fit == "1" and featno in f_words: # 过滤stop words
                        l.append(str(featno))
                fout.write(','.join(l) + '\n')


def gen_word_pair():
    """
    1. 过滤words
    2. generate word pair
    """
    stops = loader.load_stop_words()
    id2words = loader.load_id2words()

    f_words = dict()

    for _id, word in id2words.items():
        if word not in stops:
            f_words[_id] = word

    path = dir_path + 'pair_words'
    # 一共四种可能性
    with open(path, 'w+', encoding='utf-8') as fout:
        for _id in f_words.keys():
            fout.write(str(_id) + ':' + "0,0" + '\n')
            fout.write(str(_id) + ':' + "0,1" + '\n')
            fout.write(str(_id) + ':' + "1,0" + '\n')
            fout.write(str(_id) + ':' + "1,1" + '\n')


def gen_f_words():
    stops = loader.load_stop_words()
    id2words = loader.load_id2words()

    f_words = dict()

    for _id, word in id2words.items():
        if word not in stops:
            f_words[_id] = word
    f_words = sorted(f_words.items(), key=itemgetter(0), reverse=False)
    with open(dir_path+'words_filtered', 'w+', encoding='utf-8') as fout:
        for _id, word in f_words:
            fout.write(str(_id) + "," + word + '\n')


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

    with open(pats_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.strip('\n').split('|')
            support = sp[-1]






if __name__ == '__main__':
    # process_words()
    # process_features()
    # gen_f_words()
    # gen_word_pair()
    # gen_trans()
    gen_pats()
    pass



