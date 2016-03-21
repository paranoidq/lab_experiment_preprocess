#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: eval.py
@time: 16/3/21 16:30
"""


import random
import numpy as np
from sklearn.cross_validation import KFold



def eval():
    trans = loader.load_trans(constant.trans_path)
    pats = loader.load_patterns(constant.pats_path)

    gen_pat_trans(trans, pats)

    #evaluate()



