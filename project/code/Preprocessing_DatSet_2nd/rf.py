# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 19:31:55 2022

@author: 박순혁
"""


import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from lightgbm import LGBMClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import RFECV, RFE


df = pd.read_excel('df_total.xlsx', na_values=['-OVER','+OVER'])
df.drop(['Series_Date','Series_Time','filename','Date_Time','Type','Type_num'], axis=1, inplace=True)
df.interpolate(inplace=True)

X = df.drop(['Heat_ON'],axis=1)
y = df['Heat_ON']


# SVC classifier 선택
svc = SVC(kernel="linear")
# REFCV로 Feature들을 반복적으로 제거해가면서 학습/평가 수행
rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(5),
              scoring='accuracy', verbose=2)
rfecv.fit(X, y)

print("Optimal number of features : %d" % rfecv.n_features_)

# Plot number of features VS. cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross validation score (nb of correct classifications)")
plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
plt.show()