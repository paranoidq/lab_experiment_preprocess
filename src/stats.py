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
from src import path_constants as constant
from src import loader as loader

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
    with open(constant.tagcount_distribute_path, 'w+', encoding='utf-8') as fout:
        for count, n in tag_distribute:
            fout.write(str(count) + ',' + str(n) + '\n')


""" 在extract_user中实现,提取tag之后直接统计
"""
def user_tagcount_distribute():
    pass


""" 统计全网中的degree分布情况
    无向图
"""
def network_degree_distribute(network_path, output_path):
    network = loader.load_network(network_path)

    network_degree = dict()  # uid - degree
    for uid, edges in network.items():
        network_degree[uid] = len(edges.keys())
        for u, _ in edges.items():
            if u in network_degree:
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


if __name__ == '__main__':
    # tagcount_distribute()
    # network_degree_distribute(loader.load_network(), constant.origin_network_degrees_path)
    network_degree_distribute(constant.network_path, constant.network_degrees_path)
    pass