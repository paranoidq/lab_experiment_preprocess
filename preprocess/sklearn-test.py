#!/usr/bin/env Python3
# -*- coding:utf-8 -*-

"""
@version: 0.1
@author: paranoidQ
@license: Apache Licence 
@contact: paranoid_qian@163.com
@file: sklearn-test.py
@time: 16/3/11 16:11
"""

from sklearn import datasets
from sklearn import cross_validation
from sklearn import metrics
from sklearn import svm
from sklearn.datasets import fetch_20newsgroups

# categories = ['alt.atheism', 'soc.religion.christian',
#                'comp.graphics', 'sci.med']
# twenty_train = fetch_20newsgroups(subset='train',
#      categories=categories, shuffle=True, random_state=42)
# print(twenty_train)


# metrics.precision_score()
 # >>> precision_score(y_true, y_pred, average=None)  # doctest: +ELLIPSIS
 #    array([ 0.66...,  0.        ,  0.        ])

iris = datasets.load_iris()
#print(iris)
# print(len(iris.target))
# print(iris.data)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(
     iris.data, iris.target, test_size=0.4, random_state=0)
clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
predicted = clf.predict(X_test)
print(metrics.classification_report(y_test, predicted,
     target_names=iris.target_names))

print(metrics.f1_score(y_test, predicted, average=None)[0])

# ShuffleSplit
"""
>>> ss = cross_validation.ShuffleSplit(5, n_iter=3, test_size=0.25,
...     random_state=0)
>>> for train_index, test_index in ss:
...     print("%s %s" % (train_index, test_index))
...
[1 3 4] [2 0]
[1 4 3] [0 2]
[4 0 2] [1 3]
"""


import numpy as np
from sklearn.cross_validation import KFold

kf = KFold(4, n_folds=2)
for train, test in kf:
    print("%s %s" % (train, test))


X = np.array([[0., 0.], [1., 1.], [-1., -1.], [2., 2.]])
y = np.array([0, 1, 0, 1])
X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]

X = np.append(X, [[3], [4], [5], [6]])

print(X)

