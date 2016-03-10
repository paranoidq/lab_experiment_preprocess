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

import re

pattern = re.compile(r'(\d+),(\d+)(,.+)*')

text = '3607101537,20,藏地菌王之王|2,哈芙诺基赢美肌神器|2,欢乐开学季|2,一方茶水中秋茶月饼限时抢购|2,每日特价极速冲钻|2,大闹西游|2,中秋|2,茚象泉秋季护肤|2,99大聚惠|1,应用广场签到|1,91熊猫看书年会|2,转发疯抢云海人家高档茶具|2,2013湖北微博嘉年华|2,开心久久狂送钻石珍珠项链啦|2,9月15广州顶固家居工厂团购钜惠|1,曼都发型微信送好礼|1,茶|1,海外婚礼|2,视觉江苏|2,有奖转发|2'

g = pattern.match(text).groups()[-1]
print(g)
p2 = re.compile(r'[^,]+\|\d+')
s = p2.findall(g)

print(s)




