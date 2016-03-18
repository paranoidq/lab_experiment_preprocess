#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: stats.py
@time: 16/3/10 18:20
"""
from operator import itemgetter
from preprocess import path_constants as constant
from preprocess import loader as loader

""" 统计每个tag出现的次数的分布情况
"""
def tagcount_distribute(tags_path, output_path):
    tags = loader.load_tags(tags_path)
    # tags = sorted(tags.items(), key=itemgetter(1), reverse=False)
    tag_distribute = dict()
    # 统计被提及n次的tag分布有多少个
    for tag, count in tags.items():
        if count in tag_distribute:
            tag_distribute[count] += 1
        else:
            tag_distribute[count] = 1
    tag_distribute = sorted(tag_distribute.items(), key=itemgetter(0), reverse=False)
    with open(output_path, 'w+', encoding='utf-8') as fout:
        for count, n in tag_distribute:
            fout.write(str(count) + ',' + str(n) + '\n')



def user_tagcount_distribute(user_tag_path, output_path):
    """
    统计用户拥有的tag数量的分布
    """
    user_tag_distribute = dict()
    with open(user_tag_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.split('#')
            uid = sp[0]
            tag_count = int(sp[1])
            if tag_count in user_tag_distribute:
                user_tag_distribute[tag_count] += 1
            else:
                user_tag_distribute[tag_count] = 1
    user_tag_distribute = sorted(user_tag_distribute.items(), key=itemgetter(0), reverse=False)
    with open(output_path, 'w+', encoding='utf-8') as fout:
        for tag_count, user_count in user_tag_distribute:
            fout.write(str(tag_count) + ',' + str(user_count) + '\n')

def user_words_distribute(user_words_path, output_path):
    """
    统计用户拥有的words数量的分布
    """
    user_words_distribute = dict()
    with open(user_words_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.split('#')
            uid = sp[0]
            word_count = int(sp[1])
            if word_count in user_words_distribute:
                user_words_distribute[word_count] += 1
            else:
                user_words_distribute[word_count] = 1
    user_words_distribute = sorted(user_words_distribute.items(), key=itemgetter(0), reverse=False)
    with open(output_path, 'w+', encoding='utf-8') as fout:
        for word_count, user_count in user_words_distribute:
            fout.write(str(word_count) + ',' + str(user_count) + '\n')


def network_degree_distribute(network_path, output_path, with_strength=False):
    """
    统计全网中的degree分布情况
    无向图
    """
    network = loader.load_network(network_path)

    network_degree = dict()  # uid - degree
    if with_strength:
        for uid, edges in network.items():
            uid_degree = 0
            for u, strength in edges.items():
                if u in network_degree:
                    network_degree[u] += strength
                else:
                    network_degree[u] = strength
                uid_degree += strength
            if uid in network_degree and u != uid:
                network_degree[uid] += uid_degree
            else:
                network_degree[uid] = uid_degree
    else:
        for uid, edges in network.items():
            network_degree[uid] = len(edges.keys())
            for u, _ in edges.items():
                if u in network_degree and u != uid:
                    network_degree[u] += 1
                else:
                    network_degree[u] = 1

    degree_distribute = dict()
    for uid, degree in network_degree.items():
        if degree in degree_distribute:
            degree_distribute[degree] += 1
        else:
            degree_distribute[degree] = 1
    degree_distribute = sorted(degree_distribute.items(), key=itemgetter(0), reverse=False)

    with open(output_path, 'w+', encoding='utf-8') as fout:
        for degree, user_count in degree_distribute:
            fout.write(str(degree) + ',' + str(user_count) + '\n')


def degree_tag_stats(network_path, user_tag_path, output_path):

    network = loader.load_network(network_path)
    degrees = dict()
    for uid, edges in network.items():
            degrees[uid] = len(edges.keys())
            for u, _ in edges.items():
                if u in degrees and u != uid:
                    degrees[u] += 1
                else:
                    degrees[u] = 1
    user_tags = dict()
    with open(user_tag_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            sp = line.split('#')
            uid = sp[0]
            tag_count = int(sp[1])
            user_tags[uid] = tag_count

    degree_tags = dict()
    for uid, degree in degrees.items():
        tag_count = user_tags[uid] if uid in user_tags else 0
        degree_tags[uid] = (degree, tag_count)

    degree_tags = sorted(degree_tags.items(), key=lambda t: t[1][0])
    with open(output_path, 'w+', encoding='utf-8') as fout:
        for k, t in degree_tags:
            fout.write(k + ',' + str(t[0]) + ',' + str(t[1]) + '\n')



if __name__ == '__main__':
    # tagcount_distribute()
    # network_degree_distribute(constant.network_path2, constant.network_degrees_withStrength_path2, with_strength=True)

    # tagcount_distribute(constant.tag_path2, constant.tagcount_distribute_path2)
    # user_tagcount_distribute(constant.user_words_path, constant.user_wordscount_distribute_path)
    # degree_tag_stats(constant.network_path2, constant.user_tag_path2, constant.degree_tag_path2)

    user_words_distribute(constant.user_words_path, constant.user_wordscount_distribute_path)
    pass