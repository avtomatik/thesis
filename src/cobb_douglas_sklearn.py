# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:32:51 2020

@author: Alexander Mikhailov
"""


import os

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import rfft
from sklearn.datasets import load_iris
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import (KFold, LeaveOneOut, LeavePOut,
                                     RepeatedKFold, ShuffleSplit,
                                     TimeSeriesSplit, cross_val_score,
                                     train_test_split)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
# =============================================================================
# Support Vector Machine
# =============================================================================
from sklearn.svm import SVC

from lib.collect import stockpile_cobb_douglas
from lib.transform import transform_cobb_douglas_sklearn


def plot_discrete_fourier_transform(array: np.ndarray) -> None:
    """
    Discrete Fourier Transform

    Parameters
    ----------
    array : np.ndarray
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    # =========================================================================
    # TODO: Refine It
    # =========================================================================
    plt.plot(
        array,
        label='Labor Productivity',
    )
    plt.plot(
        rfft(array),
        'r:',
        label='Fourier Transform',
    )
    plt.grid()
    plt.legend()
    plt.show()


DIR = "/home/green-machine/data_science/data/interim"
MAP_FIG = {
    'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
    'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
    'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
    'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
    'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
    'year_price': 1899,
}

os.chdir(DIR)

# plot_cobb_douglas(
#     *stockpile_cobb_douglas().pipe(transform_cobb_douglas_sklearn),
#     MAP_FIG
# )
print(*stockpile_cobb_douglas().pipe(transform_cobb_douglas_sklearn))


# _df = stockpile_cobb_douglas()
# print(_df)
# X, y = _df.pipe(transform_cobb_douglas_sklearn)
#


# =============================================================================
# TODO: Discrete Laplace Transform
# =============================================================================


# # =============================================================================
# # Elastic Net
# # =============================================================================
# las = Lasso(normalize=1)
# alphas = np.logspace(-5, 2, 1000)
# alphas, coefs, _ = las.path(X, y, alphas=alphas)
# fig, ax = plt.subplots()
# ax.plot(alphas, coefs.T)
# ax.set_yscale('log')
# ax.set_xlim(alphas.max(), alphas.min())
# plt.show()

# # =============================================================================
# # Cross Validation
# # =============================================================================
# # =============================================================================
# # K-Fold
# # =============================================================================


# # kf = KFold(n_splits=4)

# # =============================================================================
# # Repeated K-Fold
# # =============================================================================


# # random_state = 12883823
# # rkf = RepeatedKFold(n_splits=2, n_repeats=2, random_state=random_state)

# # =============================================================================
# # Leave One Out (LOO)
# # =============================================================================

# # loo = LeaveOneOut()

# # =============================================================================
# # Leave P Out (LPO)
# # =============================================================================


# # lpo = LeavePOut(p=2)

# # =============================================================================
# # Random Permutations Cross-Validation a.k.a. Shuffle & Split
# # =============================================================================


# # ss = ShuffleSplit(n_splits=2, test_size=.25, random_state=0)


# # =============================================================================
# # Time Series Split
# # =============================================================================
# # =============================================================================
# # X = np.column_stack(np.log(df.iloc[:, -2]))
# # =============================================================================
# tscv = TimeSeriesSplit(n_splits=3)
# plt.figure()
# plt.scatter(X, y)
# # =============================================================================
# # for _, (train, test) in enumerate(kf.split(X), start=1):
# #     k, b = np.polyfit(X[train], y[train], 1)
# #     Z = b + k*X
# #     plt.plot(X, Z, label=f'Test {_:02d}')
# #
# # for _, (train, test) in enumerate(rkf.split(X), start=1):
# #     k, b = np.polyfit(X[train], y[train], 1)
# #     Z = b + k*X
# #     plt.plot(X, Z, label=f'Test {_:02d}')
# #
# # for _, (train, test) in enumerate(loo.split(X), start=1):
# #     k, b = np.polyfit(X[train], y[train], 1)
# #     Z = b + k*X
# #     plt.plot(X, Z, label=f'Test {_:02d}')
# #
# # for _, (train, test) in enumerate(lpo.split(X), start=1):
# #     k, b = np.polyfit(X[train], y[train], 1)
# #     Z = b + k*X
# #     plt.plot(X, Z, label=f'Test {_:02d}')
# #
# # for _, (train, test) in enumerate(ss.split(X), start=1):
# #     k, b = np.polyfit(X[train], y[train], 1)
# #     Z = b + k*X
# #     plt.plot(X, Z, label=f'Test {_:02d}')
# # =============================================================================

# for _, (train, test) in enumerate(tscv.split(X), start=1):
#     k, b = np.polyfit(X[train], y[train], 1)
#     Z = b + k*X
#     plt.plot(X, Z, label=f'Test {_:02d}')

# # =============================================================================
# # b = np.exp(b)
# # =============================================================================

# k, b = np.polyfit(X, y, 1)
# Z = b + k*X
# plt.plot(X, Z, label='Test {:02d}'.format(0))
# plt.grid()
# plt.legend()
# plt.show()

# =============================================================================
# # =============================================================================
# # Cross Validation Alternative
# # =============================================================================

# X = np.transpose(np.atleast_2d(X))  # Required

# # =============================================================================
# # X = np.log(X)
# # =============================================================================
# y = np.log(y)
# loo = LeaveOneOut(y.shape[0])
# regr = LinearRegression()
# scores = cross_val_score(
#     regr, X, y, scoring='mean_squared_error', cv=loo,)
# print(scores.mean())


# lr = LinearRegression()
# lr.fit(X, y)

# r2 = r2_score(y, lr.predict(X))
# # =============================================================================
# # r2 = lr.score(X, y)
# # =============================================================================
# print('R2 (test data): {:.2}'.format(r2))

# kf = KFold(len(X), n_folds=4)
# # =============================================================================
# # p = np.zeros_like(y)
# # =============================================================================
# for train, test in kf:
#     lr.fit(X[train], y[train])
#     p[test] = lr.predict(X[test])
#     print(lr.predict(X))

# plt.figure(1)
# plt.scatter(X, y, label='Original')
# plt.scatter(p, y, label='Linear Fit')
# plt.title('Labor Capital Intensity & Labor Productivity, 1899--1922')
# plt.xlabel('Labor Capital Intensity')
# plt.ylabel('Labor Productivity')
# plt.grid()
# plt.legend()
# plt.show()
# =============================================================================

# =============================================================================
# Cross Validation: Here
# =============================================================================
# =============================================================================
# http://scikit-learn.org/stable/modules/cross_validation.html
# =============================================================================

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=.4, random_state=0
)
# =============================================================================
# SVC: Support Vector Classification
# =============================================================================
clf = SVC(kernel='linear', C=1).fit(X_train, y_train)

# =============================================================================
# Option 1
# =============================================================================
scores = cross_val_score(clf, iris.data, iris.target, cv=5)

# =============================================================================
# Option 2
# =============================================================================
scores = cross_val_score(clf, iris.data, iris.target, cv=5, scoring='f1_macro')
print('Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), 2 * scores.std()))

# =============================================================================
# Option 3
# =============================================================================
print(iris.data.shape[0])
cv = ShuffleSplit(n_splits=5, test_size=.3, random_state=0)
result = cross_val_score(clf, iris.data, iris.target, cv=cv)

# =============================================================================
# Option 4
# =============================================================================


def custom_cv_2folds(X):
    n = X.shape[0]
    _ = 1
    while _ <= 2:
        idx = np.range(n * (_ - 1) / 2, n * _ / s, dtype=int)
        yield idx, idx
        _ += 1


custom_cv = custom_cv_2folds(iris.data)
cross_val_score(clf, iris.data, iris.target, cv=custom_cv)

# =============================================================================
# Option 5
# =============================================================================
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=.4, random_state=0
)
scaler = StandardScaler().fit(X_train)
X_train_transformed = scaler.transform(X_train)
clf = SVC(C=1).fit(X_train_transformed, y_train)
X_test_transformed = scaler.transform(X_test)
result = clf.score(X_test_transformed, y_test)

# =============================================================================
# Option 6
# =============================================================================
cv = ShuffleSplit(n_splits=5, test_size=.3, random_state=0)
clf = make_pipeline(StandardScaler(), SVC(C=1))
result = cross_val_score(clf, iris.data, iris.target, cv=cv)

# =============================================================================
# Kolmogorov-Smirnov Test for Goodness of Fit
# =============================================================================
# scipy.stats.kstest
