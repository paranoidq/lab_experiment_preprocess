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

dir_path = constant.base

def preprocess_words():
    with open(dir_path+'words_src', 'r') as fin:
        with open(dir_path+'words', 'w+') as fout:
            for no, line in enumerate(fin):
                line = line.strip('\'\n').strip('\'')
                fout.write(str(no) + ',' + line + '\n')

def preprocess_edges():
    with open(dir_path+'edges_src', 'r') as fin:
        with open(dir_path+'edges', 'w+') as fout:
            for _id, line in enumerate(fin):
                sp = line.split(',')
                for _iid, s in enumerate(sp):
                    if s == '1':
                        fout.write(str(_id) + ',' + str(_iid) + '\n')

def process_features():
    """
    1. 加载并过滤stopwords
    2. 生成words, 并写入文件
    3. 根据words生成features
    :return:
    """
    stops = loader.load_stop_words()
    id2words = loader.load_id2words()
    f_words = dict()


    for _id, word in id2words.items():
        if word not in stops:
            f_words[_id] = word
    f_words = sorted(f_words.items(), key=itemgetter(0), reverse=False)
    # 将words写入文件
    with open(dir_path+'words_filtered', 'w+', encoding='utf-8') as fout:
        for _id, word in f_words:
            fout.write(str(_id) + "," + word + '\n')


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



if __name__ == '__main__':
    preprocess_words()
    # process_features()

    # with open(dir_path + 'features_src', 'r') as fin:
    #     for uid, line in enumerate(fin):
    #         sp = line.strip('\n').split(',')





