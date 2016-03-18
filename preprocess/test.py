#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: test.py
@time: 16/3/9 15:18
"""

import time
import logging
import logging.handlers



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

# logger.info('hi')



# network = dict()
#
# network[1] = dict()
# network[2] = dict()
#
# network[1][1] = 123
# network[1][2] = 1234
#
# print(','.join((str(u) for u in network[2].keys())))

d = {1:(4,2), 2:(2,3)}
d = sorted(d.items(), key=lambda t: t[1][0], reverse=False)




