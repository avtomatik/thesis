# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:32:51 2020

@author: Mastermind
"""


from sklearn import linear_model
import os
import numpy as np
import pandas as pd
from collect.lib import collect_cobb_douglas
from collect.lib import transform_cobb_douglas_sklearn
from plot.lib import plot_cobb_douglas


# =============================================================================
# Discrete Fourier Transform
# =============================================================================
# Z = rfft(X)
# plt.plot(X)
# plt.plot(Z, 'r:')
# plt.grid(True)
# plt.legend()
# plt.show()
# =============================================================================
# Discrete Laplace Transform
# =============================================================================
# =============================================================================
# Spectrum Representations:
# https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/spectrum_demo.html
# =============================================================================
DIR = '/media/alexander/321B-6A94'
MAP_FIG = {
    'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
    'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
    'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
    'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
    'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
    'year_price': 1899,
}
os.chdir(DIR)
plot_cobb_douglas(
    *transform_cobb_douglas_sklearn(collect_cobb_douglas()),
    MAP_FIG
)


# =============================================================================
# # =============================================================================
# # Elastic Net
# # =============================================================================
# las = Lasso(normalize=1)
# alphas = np.logspace(-5, 2, 1000)
# alphas, coefs, _ = las.path(X, Y, alphas=alphas)
# fig, ax = plt.subplots()
# ax.plot(alphas, coefs.T)
# ax.set_scale('log')
# ax.set_xlim(alphas.max(), alphas.min())
# plt.show()
# =============================================================================
# =============================================================================
# Cross Validation
# =============================================================================
# # # # # # # # # # # # # # # # >K-Fold
# # # # # # # # # # # # # # from sklearn.model_selection import KFold
# # # # # # # # # # # # # # kf = KFold(n_splits=4)
# # # # # # # # # # # # # # >Repeated K-Fold
# # # # # # # # # # # # from sklearn.model_selection import RepeatedKFold
# # # # # # # # # # # # random_state = 12883823
# # # # # # # # # # # # rkf = RepeatedKFold(n_splits=2, n_repeats=2, random_state=random_state)
# # # # # # # # # # # # >Leave One Out (LOO)
# # # # # # # # # # from sklearn.model_selection import LeaveOneOut
# # # # # # # # # # loo = LeaveOneOut()
# # # # # # # # >Leave P Out (LPO)
# # # # # # # # >Random Permutations Cross-Validation a.k.a. Shuffle & Split
# # # # # # from sklearn.model_selection import LeavePOut
# # # # # # lpo = LeavePOut(p=2)
# # # # from sklearn.model_selection import ShuffleSplit
# # # # ss = ShuffleSplit(n_splits=2, test_size=.25, random_state=0)
# # # # >Time Series Split
# from sklearn.model_selection import TimeSeriesSplit
# tscv = TimeSeriesSplit(n_splits=3)
# plt.figure()
# plt.scatter(X, Y)
# i = 0
# # # # # # # # # # # # for train, test in kf.split(X):
# # # # # # # # # # for train, test in rkf.split(X):
# # # # # # # # for train, test in loo.split(X):
# # # # # # for train, test in lpo.split(X):
# # # # for train, test in ss.split(X):
# for train, test in tscv.split(X):
#    i += 1
#    k, b = np.polyfit(X[train], Y[train], 1)
#    Z = b + k*X
#    plt.plot(X, Z, label='Test {:02d}'.format(i))
# # #    b = np.exp(b)
#
# k, b = np.polyfit(X, Y, 1)
# Z = b + k*X
# plt.plot(X, Z, label='Test {:02d}'.format(0))
# plt.grid(True)
# plt.legend()
# plt.show()
# =============================================================================
# Cross Validation Alternative
# =============================================================================
# # # X = np.transpose(np.atleast_2d(X)) # # Required
# # # print(X)
# # # from sklearn import cross_validation, linear_model
# # #
# # # # # X = np.log(X)
# # # Y = np.log(Y)
# # # loo = cross_validation.LeaveOneOut(len(Y))
# # # regr = linear_model.LinearRegression()
# # # scores = cross_validation.cross_val_score(regr, X, Y, scoring='mean_squared_error', cv=loo,)
# # # print(scores.mean())
# # # # # from sklearn.linear_model import LinearRegression
# # # # # lr = LinearRegression()
# # # # # lr.fit(X, Y)
# # # # # from sklearn.metrics import r2_score
# # # # # r2 = r2_score(Y, lr.predict(X)) # # r2 = lr.score(X, Y)
# # # # # print('R2 (test data): {:.2}'.format(r2))
# # # # # from sklearn.cross_validation import Kfold
# # # # # kf = Kfold(len(X), n_folds=4)
# # # # # # # p = np.zeros_like(Y)
# # # # # for train, test in kf:
# # # # #    lr.fit(X[train], Y[train])
# # # # #    p[test] = lr.predict(X[test])
# # # print(lr.predict(X))
# # # # # plt.figure(1)
# # # # # plt.scatter(X, Y, label='Original')
# # # # # plt.scatter(p, Y, label='Linear Fit')
# # # # # plt.title('Labor Capital Intensity & Labor Productivity, 1899--1922')
# # # # # plt.xlabel('Labor Capital Intensity')
# # # # # plt.ylabel('Labor Productivity')
# # # # # plt.grid(True)
# # # # # # # plt.legend()
# # # # # # # plt.show()
# =============================================================================
# http://scikit-learn.org/stable/modules/cross_validation.html
# =============================================================================

# from sklearn.model_selection import train_test_split
# from sklearn import datasets
# from sklearn import svm # # Support Vector Machine
# iris = datasets.load_iris()
# # # X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=.4, random_state=0)
# # # clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
# # # SVC: Support Vector Classification
# from sklearn.model_selection import cross_val_score
# clf = svm.SVC(kernel='linear', C=1)
# # # 1
# # # scores = cross_val_score(clf, iris.data, iris.target, cv=5)
# # # 2
# # # from sklearn import metrics
# # # scores = cross_val_score(clf, iris.data, iris.target, cv=5, scoring='f1_macro')
# # # print(scores)
# # # print('Accuracy: %0.2f (+/- %0.2f)' %(scores.mean(), 2*scores.std()))
# # # 3
# # # from sklearn.model_selection import ShuffleSplit
# # # # # print(iris.data.shape[0])
# # # cv = ShuffleSplit(n_splits=5, test_size=.3, random_state=0)
# # # result = cross_val_score(clf, iris.data, iris.target, cv=cv)
# # # print(result)
# # # 4
# # # def custom_cv_2folds(X):
# # #    n = X.shape[0]
# # #    i = 1
# # #    while i <= 2:
# # #        idx = np.range(n*(i-1)/2, n*i/s, dtype=int)
# # #        yield idx, idx
# # #        i += 1
# # # custom_cv = custom_cv_2folds(iris.data)
# # # cross_val_score(clf, iris.data, iris.target, cv=custom_cv)
# # # 5
# # # from sklearn import preprocessing
# # # X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=.4, random_state=0)
# # # scaler = preprocessing.StandardScaler().fit(X_train)
# # # X_train_transformed = scaler.transform(X_train)
# # # clf = svm.SVC(C=1).fit(X_train_transformed, y_train)
# # # X_test_transformed = scaler.transform(X_test)
# # # result = clf.score(X_test_transformed, y_test)
# # # print(result)
# # # 6
# # # from sklearn.model_selection import ShuffleSplit
# # # from sklearn.pipeline import make_pipeline
# # # from sklearn import preprocessing
# # # cv = ShuffleSplit(n_splits=5, test_size=.3, random_state=0)
# # # clf = make_pipeline(preprocessing.StandardScaler(), svm.SVC(C=1))
# # # result = cross_val_score(clf, iris.data, iris.target, cv=cv)
# # # print(result)
# =============================================================================
# Kolmogorov-Smirnov Test for Goodness of Fit
# =============================================================================
# scipy.stats.kstest
