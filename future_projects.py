# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:32:51 2020

@author: Mastermind
"""
def fetchClassic(source, string):
    if source == 'brown.zip':
        source_frame = pd.read_csv(source, skiprows=4, usecols=range(3, 6))
        source_frame.rename(columns = {'Данные по отработанным человеко-часам заимствованы из: Kendrick,  op. cit.,  pp. 311-313,  Table A. 10.':'series', 
                                    'Unnamed: 4':'period', 
                                    'Unnamed: 5':'value'}, inplace=True)
    elif source == 'cobbdouglas.zip':
        source_frame = pd.read_csv(source, usecols=range(5, 8))
    elif source == 'douglas.zip':
        source_frame = pd.read_csv(source, usecols=range(4, 7))
    elif source == 'kendrick.zip':
        source_frame = pd.read_csv(source, usecols=range(4, 7))
    result_frame = source_frame[source_frame.iloc[:, 0] == string]
    del source_frame
    result_frame = result_frame[result_frame.columns[[1, 2]]]
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns = {'Value':string}, inplace=True)
    result_frame.iloc[:, 0] = result_frame.iloc[:, 0].astype(int)
    result_frame.iloc[:, 1] = pd.to_numeric(result_frame.iloc[:, 1], errors = 'coerce')
    result_frame = result_frame.dropna()
    result_frame = result_frame.sort_values('Period')
    result_frame = result_frame.set_index('Period')
    return result_frame
def fetchCensus(source, string, index):
    '''Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census,  Historical Statistics of the United States,  1789--1945,  Washington,  D.C.,  1949.
    U.S. Bureau of the Census. Historical Statistics of the United States,  Colonial Times to 1970,  Bicentennial Edition. Washington,  D.C.,  1975.'''
    if source == 'census1975.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11), dtype = {'vector':str, 'period':str, 'value':str})
    else:
        source_frame = pd.read_csv(source, usecols=range(8, 11))
    source_frame = source_frame[source_frame.iloc[:, 0] == string]
    source_frame = source_frame[source_frame.columns[[1, 2]]]
    if source == 'census1975.zip':
        source_frame.iloc[:, 0] = source_frame.iloc[:, 0].str[:4]
    else:
        pass
    source_frame.iloc[:, 1] = source_frame.iloc[:, 1].astype(float)
    source_frame.columns = source_frame.columns.str.title()
    source_frame.rename(columns = {'Value':string}, inplace=True)
    source_frame.iloc[:, 0] = source_frame.iloc[:, 0].astype(int)
    source_frame = source_frame.sort_values('Period')
    source_frame = source_frame.reset_index(drop = True)
    source_frame = source_frame.groupby('Period').mean()
    if index:
        return source_frame
    else:
        source_frame.to_csv('temporary.txt')
        del source_frame
        result_frame = pd.read_csv('temporary.txt')
        os.unlink('temporary.txt')
        return result_frame
def cobbDouglasPreprocessing():
    '''Original Cobb--Douglas Data Preprocessing'''
    semi_frameA = fetchClassic('cobbdouglas.zip', 'CDT2S4') ## Total Fixed Capital in 1880 dollars (4)
    semi_frameB = fetchClassic('cobbdouglas.zip', 'CDT3S1') ## Average Number Employed (in thousands)
    semi_frameC = fetchCensus('census1949.zip', 'J0014', True)
    semi_frameD = fetchCensus('census1949.zip', 'J0013', True)
    semi_frameE = fetchClassic('douglas.zip', 'DT24AS01') ## The Revised Index of Physical Production for All Manufacturing In the United States,  1899--1926
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE
    result_frame = result_frame.dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame
import os
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
source_frame = cobbDouglasPreprocessing()
X = sp.log(source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]))
Y = sp.log(source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]))
"""Discrete Fourier Transform"""
#from scipy.fftpack import fft,  rfft,  irfft
#Z  =  rfft(X)
#plt.plot(source_frame.index,  X)
#plt.plot(source_frame.index,  Z,  'r:')
#plt.grid(True)
#plt.legend()
#plt.show()
"""Discrete Laplace Transform"""
"""Spectrum Representations:
    https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/spectrum_demo.html"""
"""Lasso"""
def cdnewFeatures(source_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb,  P.H. Douglas. A Theory of Production,  1928;
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Capital, 
    source_frame.iloc[:, 1]: Labor, 
    source_frame.iloc[:, 2]: Product
    '''
    from sklearn.linear_model import Lasso
    from sklearn.linear_model import LassoCV
    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import Ridge    
    functionDict = {'FigureA':'Chart I Progress in Manufacturing %d$-$%d (%d = 100)', 
                  'FigureB':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d = 100)', 
                  'FigureC':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average', 
                  'FigureD':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d'}
    x = sp.log(source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]))
    y = sp.log(source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]))
    X = np.vstack((np.zeros((len(x),  1)).T,  x)).T
    las = Lasso(alpha = 0.01).fit(X,  y)
    reg = LinearRegression().fit(X,  y)
#    las = LassoCV(cv = 4,  random_state = 0).fit(X,  y)
    tik = Ridge(alpha = 0.01).fit(X,  y)
#    print('Lasso: a_0 = {0:.12f} & a_1 = {1:.12f}'.format(las.intercept_,   las.coef_[1]))
#    print('Linear Regression: a_0 = {0:.12f} & a_1 = {1:.12f}'.format(reg.intercept_,   reg.coef_[1]))
#    print('Ridge Regression: a_0 = {0:.12f} & a_1 = {1:.12f}'.format(tik.intercept_,   tik.coef_[1]))
    A = sp.exp(las.intercept_)
    PP = A*(source_frame.iloc[:, 1]**(1-las.coef_[1]))*(source_frame.iloc[:, 0]**las.coef_[1])
    PR = source_frame.iloc[:, 2].rolling(window = 3, center = True).mean()
    PPR = PP.rolling(window = 3, center = True).mean()
    plt.figure(1)
    plt.plot(source_frame.index, source_frame.iloc[:, 0], label = 'Fixed Capital')
    plt.plot(source_frame.index, source_frame.iloc[:, 1], label = 'Labor Force')
    plt.plot(source_frame.index, source_frame.iloc[:, 2], label = 'Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(functionDict['FigureA'] %(source_frame.index[0], source_frame.index[len(source_frame)-1], source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.index, source_frame.iloc[:, 2], label = 'Actual Product')
    plt.plot(source_frame.index, PP, label = 'Computed Product,  $P\' = %fL^{%f}C^{%f}$' %(A, 1-las.coef_[1], las.coef_[1]))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(functionDict['FigureB'] %(source_frame.index[0], source_frame.index[len(source_frame)-1], source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.index, source_frame.iloc[:, 2]-PR, label = 'Deviations of $P$')
    plt.plot(source_frame.index, PP-PPR, '--', label = 'Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(functionDict['FigureC'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.index, PP.div(source_frame.iloc[:, 2])-1)
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(functionDict['FigureD'] %(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.grid(True)
    plt.show()
cdnewFeatures(source_frame)
#from sklearn.linear_model import LassoCV
#reg = LassoCV(cv = 4,  random_state = 0).fit(X,  y)
#print(reg.score(X,  y))
#print(reg)
#print(reg.predict(X[:1, ]))

#from sklearn.linear_model import LinearRegression
#X
#y
#reg = LinearRegression().fit(X,  y)
#reg.score(X,  y)
#reg.coef_
#reg.intercept_

#from sklearn import linear_model
#clf = linear_model.Lasso(alpha = 0.000001)
#clf.fit([[0,  0],  [1,  2],  [2,  4]],  [0,  2,  4])
#print(clf.coef_)
#print(clf.intercept_)
#print(sp.polyfit([0,  1,  2],  [0,  2,  4],  1))
"""Elastic Net"""
from sklearn import linear_model
las = linear_model.Lasso(normalize = 1)
alphas = np.logspace(-5, 2, 1000)
alphas, coefs, _ = las.path(X, Y, alphas = alphas)
fig, ax = plt.subplots()
ax.plot(alphas, coefs.T)
ax.set_scale('log')
ax.set_xlim(alphas.max(), alphas.min())
plt.show()
"""Cross Validation"""
################>K-Fold
##############from sklearn.model_selection import KFold
##############kf = KFold(n_splits = 4)
##############>Repeated K-Fold
############from sklearn.model_selection import RepeatedKFold
############random_state = 12883823
############rkf = RepeatedKFold(n_splits = 2, n_repeats = 2, random_state = random_state)
############>Leave One Out (LOO)
##########from sklearn.model_selection import LeaveOneOut
##########loo = LeaveOneOut()
########>Leave P Out (LPO)
########>Random Permutations Cross-Validation a.k.a. Shuffle & Split
######from sklearn.model_selection import LeavePOut
######lpo = LeavePOut(p = 2)
####from sklearn.model_selection import ShuffleSplit
####ss = ShuffleSplit(n_splits = 2, test_size = 0.25, random_state = 0)
####>Time Series Split
#from sklearn.model_selection import TimeSeriesSplit
#tscv = TimeSeriesSplit(n_splits = 3)
#plt.figure()
#plt.scatter(X, Y)
#i = 0
############for train, test in kf.split(X):
##########for train, test in rkf.split(X):
########for train, test in loo.split(X):
######for train, test in lpo.split(X):
####for train, test in ss.split(X):
#for train, test in tscv.split(X):
#    i+ = 1
#    f1p = sp.polyfit(X[train], Y[train], 1)
#    a1, a0 = f1p
#    Z = a0+a1*X
#    plt.plot(X, Z, label = 'Test {:02d}'.format(i))
###    a0 = sp.exp(a0)
#    del f1p
#f1p = sp.polyfit(X, Y, 1)
#a1, a0 = f1p
#Z = a0+a1*X
#plt.plot(X, Z, label = 'Test {:02d}'.format(0))
#plt.grid(True)
#plt.legend()
#plt.show()
"""Cross Validation Alternative"""
###X = np.transpose(np.atleast_2d(X)) ## Required
###print(X)
###from sklearn import cross_validation,  linear_model
###
#####X = sp.log(X)
###Y = sp.log(Y)
###loo = cross_validation.LeaveOneOut(len(Y))
###regr = linear_model.LinearRegression()
###scores = cross_validation.cross_val_score(regr,  X,  Y,  scoring = 'mean_squared_error',  cv = loo, )
###print(scores.mean())
#####from sklearn.linear_model import LinearRegression
#####lr = LinearRegression()
#####lr.fit(X, Y)
#####from sklearn.metrics import r2_score
#####r2 = r2_score(Y, lr.predict(X)) ##r2 = lr.score(X, Y)
#####print("R2 (test data): {:.2}".format(r2))
#####from sklearn.cross_validation import Kfold
#####kf = Kfold(len(X),  n_folds = 4)
#######p = np.zeros_like(Y)
#####for train,  test in kf:
#####    lr.fit(X[train],  Y[train])
#####    p[test] = lr.predict(X[test])
###print(lr.predict(X))
#####plt.figure(1)
#####plt.scatter(X,  Y,  label = 'Original')
#####plt.scatter(p,  Y,  label = 'Linear Fit')
#####plt.title('Labor Capital Intensity & Labor Productivity,  1899--1922')
#####plt.xlabel('Labor Capital Intensity')
#####plt.ylabel('Labor Productivity')
#####plt.grid(True)
#######plt.legend()
#######plt.show()
###http://scikit-learn.org/stable/modules/cross_validation.html
#
#from sklearn.model_selection import train_test_split
#from sklearn import datasets
#from sklearn import svm ##Support Vector Machine
#iris = datasets.load_iris()
###X_train, X_test, y_train, y_test = train_test_split(iris.data,  iris.target,  test_size = 0.4,  random_state = 0)
###clf = svm.SVC(kernel = 'linear',  C = 1).fit(X_train,  y_train)
###SVC: Support Vector Classification
#from sklearn.model_selection import cross_val_score
#clf = svm.SVC(kernel = 'linear',  C = 1)
###1
###scores = cross_val_score(clf, iris.data, iris.target, cv = 5)
###2
###from sklearn import metrics
###scores = cross_val_score(clf, iris.data, iris.target, cv = 5, scoring = 'f1_macro')
###print(scores)
###print("Accuracy: %0.2f (+/- %0.2f)" %(scores.mean(), 2*scores.std()))
###3
###from sklearn.model_selection import ShuffleSplit
#####print(iris.data.shape[0])
###cv = ShuffleSplit(n_splits = 5, test_size = 0.3, random_state = 0)
###result = cross_val_score(clf, iris.data, iris.target, cv = cv)
###print(result)
###4
###def custom_cv_2folds(X):
###    n = X.shape[0]
###    i = 1
###    while i< = 2:
###        idx = np.range(n*(i-1)/2, n*i/s, dtype = int)
###        yield idx,  idx
###        i+ = 1
###custom_cv = custom_cv_2folds(iris.data)
###cross_val_score(clf, iris.data, iris.target, cv = custom_cv)
###5
###from sklearn import preprocessing
###X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size = 0.4, random_state = 0)
###scaler = preprocessing.StandardScaler().fit(X_train)
###X_train_transformed = scaler.transform(X_train)
###clf = svm.SVC(C = 1).fit(X_train_transformed, y_train)
###X_test_transformed = scaler.transform(X_test)
###result = clf.score(X_test_transformed, y_test)
###print(result)
###6
###from sklearn.model_selection import ShuffleSplit
###from sklearn.pipeline import make_pipeline
###from sklearn import preprocessing
###cv = ShuffleSplit(n_splits = 5, test_size = 0.3, random_state = 0)
###clf = make_pipeline(preprocessing.StandardScaler(),  svm.SVC(C = 1))
###result = cross_val_score(clf, iris.data, iris.target, cv = cv)
###print(result)
"""Kolmogorov-Smirnov Test for Goodness of Fit"""
#scipy.stats.kstest