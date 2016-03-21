#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: constant.py
@time: 16/3/18 21:43
"""
import os

base = "/Users/paranoidq/316-data/polblogs/"

stop_words_path = base + 'stopwords'
enhanced_stops_path = base + os.path.join('en_stops', 'en_stops_80')
id2wordspath = base + 'words'

feat_src_path = base + 'features_src'
feat_path = base + 'features'

edges_path = base + 'edges'

pats_path = base + 'patterns'
pats_repr_path = base + 'patterns_repr'

trans_path = base + 'trans'
pat_trans_path = base + 'pats_trans'
