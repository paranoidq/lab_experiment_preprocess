#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: extractor.py
@time: 16/3/8 22:18
"""

import os
import sys
import simplejson as json
import logging
import logging.handlers
import time
import datetime
import re
from collections import defaultdict
import jieba
import jieba.analyse
import jieba.posseg as posseg
import multiprocessing as mp
from operator import itemgetter
from preprocess import path_constants as constant
from preprocess import loader as loader

# logging.basicConfig(level=logging.DEBUG)

fh = logging.FileHandler('/Users/paranoidq/PycharmProjects/lab_experiment_preprocess/log/' + str(int(time.time())))
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)


formatter = logging.Formatter('%(asctime)s[%(levelname)s] - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger = logging.getLogger('extractor')
logger.addHandler(fh)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)


# logging.basicConfig(level=logging.DEBUG)
# logger = logging


def extract_init():

    # format = "%Y-%m-%d %H:%M:%S"
    # min = int(time.mktime(time.strptime('2013-9-1 00:00:00', format)))
    # max = int(time.mktime(time.strptime('2013-9-2 00:00:00', format)))

    user_map = {}
    tag_re = re.compile(r'#[^#*]+#')

    o_files = os.listdir(constant.data_src_path)
    files = (constant.data_src_path + f for f in o_files if f != '.DS_Store')
    for f in files:
        with open(f, encoding="UTF-8") as fin:
            logger.debug("Processing file: " + f)

            for num, line in enumerate(fin):
                line_json = json.loads(line)

                # 统计用户数量
                uid = line_json['user']
                retweeted_uid = line_json['retweeted_uid']
                if uid not in user_map:
                    user_map[uid] = dict()
                if retweeted_uid != 0 and retweeted_uid not in user_map:
                    user_map[retweeted_uid] = dict()

                text = line_json['text']
                tags = tag_re.findall(text)
                for tag in tags:
                    tag = tag.strip('\s+\?\!,#')
                    if len(tag) > 50:
                        continue
                    if tag in user_map[uid]:
                        user_map[uid][tag] += 1
                    else:
                        user_map[uid][tag] = 1

            # logging.debug("Processing file OK.\n")
            logger.debug("Processing file OK. Total user: " + str(len(user_map)) + "\n")

    with open(constant.user_tag_path, 'w+', encoding='utf-8') as fout:
        for id, tags in user_map.items():
            l = [tag + '|' + str(freq) for tag, freq in tags.items()]
            fout.write(str(id) + '#' + str(len(tags.keys())) + '#' + '#'.join(l) + '\n')
            # uid#tag数量#tag|提及次数#tag|提及次数, ...

    # # 统计tag分布的情况,即有n个tag的用户分别有多少个
    # tag_dict = dict()
    # tag_distribute = dict()
    # for id, tags in user_map.items():
    #     # 统计user的tag次数
    #     user_tag_count = len(tags.keys())
    #     if user_tag_count in tag_distribute:
    #         tag_distribute[user_tag_count] += 1
    #     else:
    #         tag_distribute[user_tag_count] = 1
    #     # 统计具体tag的总次数
    #     for tag, count in tags.items():
    #         if tag in tag_dict:
    #             tag_dict[tag] += count
    #         else:
    #             tag_dict[tag] = count
    #
    # distribute = sorted(tag_distribute.items(), key=itemgetter(0), reverse=False)
    # with open(constant.user_tagcount_distribute_path, 'w+', encoding='utf-8') as fout:
    #     for user_tag_count, user_count in distribute:
    #         fout.write(str(user_tag_count) + ',' + str(user_count) + '\n')
    # # 将tag按照出现的次数排序
    # tags = sorted(tag_dict.items(), key=itemgetter(1), reverse=True)
    # with open(constant.tag_path, 'w+', encoding='UTF-8') as fout:
    #     for tag, tag_count in tags:
    #         fout.write(tag + ',' + str(tag_count) + '\n')

    logger.debug("Processing tags OK\n")


def extract_network():
    network = dict()

    o_files = os.listdir(constant.data_src_path)
    files = (constant.data_src_path + f for f in o_files if f != '.DS_Store')

    for f in files:
        with open(f, encoding="UTF-8") as fin:
            logger.debug("Processing file: " + f)

            for num, line in enumerate(fin):
                line_json = json.loads(line)
                uid = line_json['user']
                retweeted_uid = line_json['retweeted_uid']
                message_type = line_json['message_type']

                if retweeted_uid == 0 or message_type == 4 or message_type == 1:  # 去除原创的微博和私信
                    continue
                if uid not in network:
                    edges = dict()
                    edges[retweeted_uid] = 1
                    network[uid] = edges
                else:
                    edges = network[uid]
                    if retweeted_uid not in edges:
                        edges[retweeted_uid] = 1
                    else:
                        edges[retweeted_uid] += 1

            logger.debug("Processing file OK.")

    with open(constant.network_path, 'w+', encoding='UTF-8') as fout:
        for uid, edges in network.items():
            # fout.write(str(uid) + "," + ",".join((str(u) for u in edges.keys())) + "\n")  # 这里忽略了转发的数量
            for u, freq in edges.items():
                fout.write(str(uid) + ',' + str(u) + ',' + str(freq) + '\n')

    pass


def extract_network_with_tagGt2():
    # 提取tag >= 2的用户
    users = dict()
    with open(constant.user_tag_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.split('#')
            uid = sp[0]
            tags_count = int(sp[1])
            tags_str_list = sp[1:]
            if tags_count >= 2:
                users[uid] = tags_str_list
    # # 写入user_tags_path2文件
    # with open(constant.user_tag_path2, 'w+', encoding='utf-8') as fout:
    #     for uid, tags_str_list in users.items():
    #         fout.write(uid + "#" + '#'.join(tags_str_list))

    network = loader.load_network(constant.network_path)
    # 根据user提取网络,必须满足条件的user才能存在于网络中,其余的user去除
    network2 = dict()
    for uid, edges in network.items():
        if uid in users:
            network2[uid] = dict()
            for u, strength in edges.items():
                if u in users:
                    network2[uid][u] = strength

    network = network2
    # 写入network_path2文件
    with open(constant.network_path2, 'w+', encoding='utf-8') as fout:
        for uid, edges in network.items():
            for u, freq in edges.items():
                fout.write(str(uid) + ',' + str(u) + ',' + str(freq) + '\n')


def extract_users(src_path, output_path):
    users = set()
    with open(src_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.split("#")
            uid = sp[0]
            users.add(uid)
    with open(output_path, 'w+', encoding='utf-8') as fout:
        for uid in users:
            fout.write(uid + '\n')


def extract_tags(user_tag_path, output_path):
    """
    根据user_tags文件提取所有的tag和对应的count
    """
    tags = dict()
    with open(user_tag_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.split('#')
            tags_str_list = sp[2:]
            for tag_str in tags_str_list:
                sp = tag_str.split('|')
                tag = ''
                if len(sp) > 2:
                    tag = "|".join(sp[:-1])
                else:
                    tag = sp[0]
                count = int(sp[-1])
                if tag in tags:
                    tags[tag] += count
                else:
                    tags[tag] = count
    tags = sorted(tags.items(), key=itemgetter(1), reverse=True)
    with open(output_path, 'w+', encoding='utf-8') as fout:
        for tag, count in tags:
            fout.write(tag + ',' + str(count) + '\n')


_allowPos = ('ns', 'n', 'nr', 'nt', 'nz', 'ng', 't', 'vn', 'an')
def worker(f):
    with open(constant.data_src_path + f, encoding="UTF-8") as fin:
        logger.debug("Processing file: " + f)
        with open(constant.words_seg_dir_path + f, 'w+', encoding='utf-8') as fout:
            for num, line in enumerate(fin):
                line_json = json.loads(line)
                uid = line_json['user']
                text = line_json['text']
                seg_tags = jieba.analyse.extract_tags(text, topK=20, allowPOS=_allowPos)
                line = str(uid) + "#" + "#".join(seg_tags) + "\n"
                fout.write(line)
        logger.debug("Processing file OK.\n")



def extract_from_text_with_segment():
    # jieba.enable_parallel(processnum=4)

    #user_seg_tags = dict()
    o_files = os.listdir(constant.data_src_path)
    manager = mp.Manager()
    pool = mp.Pool(mp.cpu_count())
    # files = (constant.data_src_path + f for f in o_files if f != '.DS_Store')
    for f in (ff for ff in o_files if ff != '.DS_Store' and ff != 'tiqu_part_aa' and ff != 'tiqu_part_ab'):
            pool.apply_async(worker, (f,))
    pool.close()
    pool.join()
            # logger.debug("Processing file: " + f)
            # with open(constant.user_seg_dir_path + f, 'w+', encoding='utf-8') as fout:
            #     for num, line in enumerate(fin):
            #         line_json = json.loads(line)
            #         uid = line_json['user']
            #         text = line_json['text']
            #
            #         # 提取关键词
            #         seg_tags = jieba.analyse.extract_tags(text, topK=20, allowPOS=_allowPos)
            #         # 写入行
            #         fout.write()
            #         # uid#tag|提及次数#tag|提及次数, ...
            # logger.debug("Processing file OK.\n")

def extract_user_words(output_path):

    user_words = dict()
    o_files = os.listdir(constant.data_src_path)
    files = (constant.words_seg_dir_path + f for f in o_files if f != '.DS_Store')
    for f in files:
        with open(f, 'r', encoding='utf-8') as fin:
            logger.debug('Processing words segment file: ' + f)
            for line in fin:
                sp = line.strip("\n").split("#")
                uid = int(sp[0])
                if uid not in user_words:
                    user_words[uid] = set()
                for word in sp[1:]:
                    if word != "":
                        user_words[uid].add(word)

    users = loader.load_users(constant.users_path)
    with open(output_path, 'w+', encoding='utf-8') as fout:
        for user in users:
            if user in user_words:
                fout.write(str(user) + "#" + str(len(user_words[user])) + "#" + "#".join(user_words[user]) + '\n')
            else:
                fout.write(str(user) + '#' + str(0) + "#" + '\n')

def extract_words(src_path, output_path):
    words = dict()
    with open(src_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.strip("\n").split("#")
            for word in sp[2:]:
                if word != "":
                    if word not in words:
                        words[word] = 1
                    else:
                        words[word] += 1
    words = sorted(words.items(), key=itemgetter(1), reverse=True)
    with open(output_path, 'w+', encoding='utf-8') as fout:
        for word, freq in words:
            fout.write(word + "," + str(freq) + '\n')







if __name__ == '__main__':
    # extract_user()
    # extract_network();
    # load_network()

    # extract_network_with_tagGt2()
    # extract_tags(constant.user_tag_path2, constant.tag_path2)

    # extract_from_text_with_segment()

    # extract_users(constant.user_tag_path, constant.users_path)

    # extract_user_words(constant.user_words_path)

    extract_words(constant.user_words_path, constant.words_path)


    pass

