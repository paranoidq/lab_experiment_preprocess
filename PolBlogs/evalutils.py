#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: evalutils.py
@time: 16/3/21 17:28
"""

from PolBlogs import loader
from PolBlogs import constant
import random

def random_gen_nolinks(uid2feats, edges, delta_count):
    """
    随机产生nolink的ins
    :param uid2feats:
    :param edges:
    :param delta_count: nolink 与 link的相对比例,80%表示nolink的ins数量是link的ins的80%
    :return:
    """
    trans = list()
    max_uid = len(uid2feats) - 1
    max_count = int(delta_count * len(edges))
    cur_count = 0
    while cur_count <= max_count:
        u1 = random.randint(0, max_uid)
        u2 = random.randint(0, max_uid)
        if u1 != u2 and (u1, u2) not in edges:
            u1feats = uid2feats[u1]
            u2feats = uid2feats[u2]
            ins = set()
            for feat in u1feats.intersection(u2feats):
                ins.add(int(feat))
            ins = sorted(ins)
            trans.append(ins)

            cur_count += 1
    return trans


def gen_pat_trans0(trans, pats):
    pat_trans = list()
    for ins in trans:
        pat_ins = set()
        for pat in pats:
            if pat.issubset(ins):
                pat_ins.add(pat)
        pat_trans.append(pat_ins)
    return pat_trans



def gen_pat_trans(trans, pats):

    link_trans = gen_pat_trans0(trans, pats)
    nolink_trans = gen_pat_trans0(
        random_gen_nolinks(loader.load_uid2features(), loader.load_edges(), 1), pats)

    # TODO






