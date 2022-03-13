# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 23:41:12 2019

@author: Mastermind
"""
import os
from datafetch import fetchClassic
from datafetch import fetchCensus


#Section5ALL_Hist
##www.bea.gov/histdata/Releases/GDP_and_PI/2012/Q1/Second_May-31-2012/Section5ALL_Hist.xls
##Metadata: `Section5ALL_Hist.xls`@[`dataset USA BEA Release 2010-08-05 Section5ALL_Hist.xls` Offsets `dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip`]'''
##'''Fixed Assets Series: K160021,  1951--1969'''
##sub_frame1 = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50900 Ann', 22, 3, 0)
def cd_original(frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb,  P.H. Douglas. A Theory of Production,  1928;
    frame.index: Period, 
    frame.iloc[:, 0]: Capital, 
    frame.iloc[:, 1]: Labor, 
    frame.iloc[:, 2]: Product
    '''
    functionDict = {'FigureA':'Chart I Progress in Manufacturing %d$-$%d (%d = 100)', 
                  'FigureB':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d = 100)', 
                  'FigureC':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average', 
                  'FigureD':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d'}
    X = frame.iloc[:, 0].div(frame.iloc[:, 1])
    Y = frame.iloc[:, 2].div(frame.iloc[:, 1])
    import scipy as sp
    X = sp.log(X)
    Y = sp.log(Y)
    f1p = sp.polyfit(X, Y, 1)
    a1, a0 = f1p ##Original: a1 = 0.25
    a0 = sp.exp(a0)
    PP = a0*(frame.iloc[:, 1]**(1-a1))*(frame.iloc[:, 0]**a1)
    PR = frame.iloc[:, 2].rolling(window = 3, center = True).mean()
    PPR = PP.rolling(window = 3, center = True).mean()
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(frame.index, frame.iloc[:, 0], label = 'Fixed Capital')
    axs[0].plot(frame.index, frame.iloc[:, 1], label = 'Labor Force')
    axs[0].plot(frame.index, frame.iloc[:, 2], label = 'Physical Product')
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Indexes')
    axs[0].set_title(functionDict['FigureA'] %(frame.index[0], frame.index[len(frame)-1], frame.index[0]))
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(frame.index, frame.iloc[:, 2], label = 'Actual Product')
    axs[1].plot(frame.index, PP, label = 'Computed Product,  $P\' = %fL^{%f}C^{%f}$' %(a0, 1-a1, a1))
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Production')
    axs[1].set_title(functionDict['FigureB'] %(frame.index[0], frame.index[len(frame)-1], frame.index[0]))
    axs[1].legend()
    axs[1].grid(True)
    axs[2].plot(frame.index, frame.iloc[:, 2]-PR, label = 'Deviations of $P$')
    axs[2].plot(frame.index, PP-PPR, '--', label = 'Deviations of $P\'$')
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage Deviation')
    axs[2].set_title(functionDict['FigureC'])
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(frame.index, PP.div(frame.iloc[:, 2])-1)
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage Deviation')
    axs[3].set_title(functionDict['FigureD'] %(frame.index[0], frame.index[len(frame)-1]))
    axs[3].grid(True)
    plt.tight_layout()
    plt.savefig('view.pdf', format = 'pdf', dpi = 900)
    plt.show()


def dataCombined():
    '''Most Up-To-Date Version'''
    '''US BEA Fixed Assets Series Tests'''
    '''Item 1.1'''
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    '''Item 1.2'''
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    '''Item 1.3'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    '''Item 1.4: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    '''Item 1.5'''
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    '''Item 2.1: Don't Use,  Use Item 1.1 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    '''Item 2.2: Don't Use,  Use Item 1.2 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    '''Item 2.3: Don't Use,  Use Item 1.3 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    '''Item 2.4'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    '''Item 2.5: Don't Use,  Use Item 1.5 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    '''Item 3.1: Don't Use,  Use Item 1.1 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    '''Item 3.2: Don't Use,  Use Item 1.2 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    '''Item 3.3: Don't Use,  Use Item 1.3 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    '''Item 3.4: Don't Use,  Use Item 2.4 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    '''Item 3.5: Don't Use,  Use Item 1.5 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    '''Item 4.1: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    '''Item 4.2: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    '''Item 4.3: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    '''Item 4.4: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    '''Item 4.5: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    '''Item 5.1: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    '''Item 5.2: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    '''Item 5.3: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    '''Item 5.4: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    '''Item 5.5: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    '''Item 6.1: Don't Use,  Use Item 1.1 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    '''Item 6.2: Don't Use,  Use Item 1.2 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    '''Item 6.3: Don't Use,  Use Item 1.3 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    '''Item 6.4: Don't Use,  Use Item 2.4 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    '''Item 6.5: Don't Use,  Use Item 1.5 Instead'''
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    '''Item 7.1: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    '''Item 7.2: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    '''Item 7.3: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    '''Item 7.4: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    '''Item 7.5: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    '''Item 8.1: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    '''Item 8.2: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    '''Item 8.3: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    '''Item 8.4: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    '''Item 8.5: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    '''Item 9.1: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'i3ptotl1es000')
    '''Item 9.2: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'icptotl1es000')
    '''Item 9.3: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k1ptotl1es000')
    '''Item 9.4: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'k3ptotl1es000')
    '''Item 9.5: Don't Use'''
    ##fetchBEA('beanipa20170823sfat.zip', 'kcptotl1es000')
    import pandas as pd
    semi_frameA = fetchBEA('dataset USA BEA NipaDataA.txt', 'A006RC')
    semi_frameB = fetchBEA('dataset USA BEA NipaDataA.txt', 'A006RD')
    semi_frameC = fetchBEA('dataset USA BEA NipaDataA.txt', 'A008RC')
    semi_frameD = fetchBEA('dataset USA BEA NipaDataA.txt', 'A008RD')
    semi_frameE = fetchBEA('dataset USA BEA NipaDataA.txt', 'A032RC')
    semi_frameF = fetchBEA('dataset USA BEA NipaDataA.txt', 'A191RA')
    semi_frameG = fetchBEA('dataset USA BEA NipaDataA.txt', 'A191RC')
    semi_frameH = fetchBEA('dataset USA BEA NipaDataA.txt', 'A191RX')
    sub_frameA = fetchBEA('dataset USA BEA NipaDataA.txt', 'H4313C')
    sub_frameB = fetchBEA('dataset USA BEA NipaDataA.txt', 'J4313C')
    sub_frameC = fetchBEA('dataset USA BEA NipaDataA.txt', 'A4313C')
    sub_frameD = fetchBEA('dataset USA BEA NipaDataA.txt', 'N4313C')
    semi_frameI = pd.concat([sub_frameA, sub_frameB, sub_frameC, sub_frameD], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD
    semi_frameI = semi_frameI.mean(1)
    semi_frameI = semi_frameI.to_frame(name = 'Labor')
    semi_frameJ = fetchBEA('dataset USA BEA NipaDataA.txt', 'W170RC')
    semi_frameK = fetchBEA('dataset USA BEA NipaDataA.txt', 'W170RX')
    '''Fixed Assets Series: K100701,  1951--1969'''
    sub_frameA = beaFetch(None, 'dataset USA BEA Release 2015-03-02 Section5ALL_Hist.xls', '51000 Ann', 1951, 1969, 70)
    '''Fixed Assets Series: K100701,  1969--2013'''
    sub_frameB = beaFetch(None, 'dataset USA BEA Release 2015-03-02 Section5all_xls.xls', '51000 Ann', 1969, 2013, 70)
    semi_frameL = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Investment in Fixed Assets,  Private,  i3ptotl1es000,  1901--2016'''
    semi_frameM = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section1ALL_xls.xls', '105 Ann', 1901, 2016, 3)
    '''Chain-Type Quantity Index for Investment in Fixed Assets,  Private,  icptotl1es000,  1901--2016'''
    semi_frameN = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section1ALL_xls.xls', '106 Ann', 1901, 2016, 3)
    '''Current-Cost Net Stock of Fixed Assets,  Private,  k1ptotl1es000,  1925--2016'''
    semi_frameO = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section1ALL_xls.xls', '101 Ann', 1925, 2016, 3)
    '''Historical-Cost Net Stock of Private Fixed Assets,  Private Fixed Assets,  k3ptotl1es000,  1925--2016'''
    semi_frameP = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '203 Ann', 1925, 2016, 1)
    '''Chain-Type Quantity Indexes for Net Stock of Fixed Assets,  Private,  kcptotl1es000,  1925--2016'''
    semi_frameQ = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section1ALL_xls.xls', '102 Ann', 1925, 2016, 3)
    semi_frameR = FRBMS()
    semi_frameS = FRBMS()
    semi_frameT = FRBMS()
    semi_frameU = pd.read_csv('dataset USA 0025PR.txt')
    semi_frameU.columns = semi_frameU.columns.str.title()
    semi_frameU = semi_frameU.set_index('Period')
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI, semi_frameJ, \
                           semi_frameK, semi_frameL, semi_frameM, semi_frameN, semi_frameO, \
                           semi_frameP, semi_frameQ, semi_frameR, semi_frameS, semi_frameT, \
                           semi_frameU], axis = 1, sort = True)
    return result_frame


def plotKZFB(source_frame):
    """Kolmogorov--Zurbenko Filter
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Series"""
    import pandas as pd
    import matplotlib.pyplot as plt
    """Data_frame for Kolmogorov--Zurbenko Filter Results"""
    result_frameA = source_frame
    """Data_frame for Kolmogorov--Zurbenko Filter Residuals"""
    result_frameB = pd.concat([source_frame.iloc[:, 0], source_frame.iloc[:, 0].rolling(window = 2).mean()], axis = 1, sort = False)
    result_frameB = pd.concat([result_frameB, (source_frame.iloc[:, 1]-source_frame.iloc[:, 1].shift(1)).div(source_frame.iloc[:, 1].shift(1))], axis = 1, sort = False)
    series = source_frame.iloc[:, 1]
    for i in range(1, 1+len(source_frame)//2):
        series = series.rolling(window = 2).mean()
        skz = series.shift(-(i//2))
        result_frameA = pd.concat([result_frameA, skz], axis = 1, sort = False)
        if i%2 ==0:
            result_frameB = pd.concat([result_frameB, (skz-skz.shift(1)).div(skz.shift(1))], axis = 1, sort = False)
        else:
            result_frameB = pd.concat([result_frameB, (skz.shift(-1)-skz).div(skz)], axis = 1, sort = False)
    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(result_frameA.iloc[:, 0], result_frameA.iloc[:, 1], label = 'Original Series')
    for i in range(2, 1+len(source_frame)//2):
        if i%2 ==0:
            plt.plot(result_frameA.iloc[:, 0].rolling(window = 2).mean(), result_frameA.iloc[:, i], label = '$KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frameA.iloc[:, 0], result_frameA.iloc[:, i], label = '$KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Kolmogorov$-$Zurbenko Filter Residuals')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(result_frameB.iloc[:, 1], result_frameB.iloc[:, 2], label = 'Residuals')
    for i in range(3, 2+len(source_frame)//2):
        if i%2 ==0:
            plt.plot(result_frameB.iloc[:, 1], result_frameB.iloc[:, i], label = '$\\delta KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frameB.iloc[:, 0], result_frameB.iloc[:, i], label = '$\\delta KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.show()


def fetchXLSM():
    '''Indexed'''
    import os
    import pandas as pd
    '''Nominal Investment Series: A006RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1968, 7)
    '''Nominal Investment Series: A006RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 7)
    semi_frameA = sub_frameA.append(sub_frameB)
    del sub_frameA, sub_frameB
    '''Nominal National income Series: A032RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10705 Ann', 1929, 1969, 16)
    '''Nominal National income Series: A032RC1,  1969--2011'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10705 Ann', 1969, 2011, 16)
    semi_frameB = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Nominal Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 1)
    '''Nominal Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 1)
    semi_frameC = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10106 Ann', 1929, 1969, 1)
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10106 Ann', 1969, 2012, 1)
    semi_frameD = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameE = pd.read_csv('dataset USA 0025PR.txt')
    semi_frameE.columns = semi_frameE.columns.str.title()
    semi_frameE = semi_frameE.set_index('Period')
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis = 1, sort = True).dropna(how = 'all')
    return result_frame


#def fetch(string):
#    """The GDELT Project"""
#    import os
#    import pandas as pd
#    source_frame = pd.read_csv('dataset World %s.export.csv' %(string),  sep = '\t')
#    print(source_frame.describe())
#fetch('20180822')
##'''https://stackoverflow.com/questions/32788526/python-scipy-kolmogorov-zurbenko-filter'''


##def kz(series,  window,  iterations):
##    """KZ filter implementation
##    series is a pandas series
##    window is the filter window m in the units of the data (m = 1+2q)
##    iterations is the number of times the moving average is evaluated
##    """
##    z = series.copy()
##    for i in range(iterations):
##        z = pd.rolling_mean(z,  window = window,  min_periods = 1,  center = True)
##    return z
    ##plt.savefig('NBER-CESmean.pdf', format = 'pdf', dpi = 900)
    ##plt.savefig('NBER-CESsum.pdf', format = 'pdf', dpi = 900)
#os.chdir('C:\\Projects')
#plt.figure(1).savefig('figure_1.pdf')
#plt.figure(2).savefig('figure_2.pdf')
#plt.figure(3).savefig('figure_3.pdf')
#plt.figure(4).savefig('figure_4.pdf')
'''Gross fixed capital formation Data Block'''
'''Not Clear: v62143969 - 380-0068 Gross fixed capital formation; Canada; Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial\
machinery and equipment (x 1, 000, 000) (quarterly,  1961-03-01 to 2017-09-01)'''
'''Not Clear: v62143990 - 380-0068 Gross fixed capital formation; Canada; Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial\
machinery and equipment (x 1, 000, 000) (quarterly,  1961-03-01 to 2017-09-01)'''
##fetchCANSIMQ('03800068', 'v62143969', True)
##fetchCANSIMQ('03800068', 'v62143990', True)
##fetchCANSIMGroupB('5245628780870031920', 3)
##fetchCANSIMGroupA('7931814471809016759', 241)
##fetchCANSIMGroupA('8448814858763853126', 81)
'''Not Clear'''
##frame = pd.read_csv('dataset CAN cansim-%s-eng-%s.csv'%(0310003, 7591839622055840674), skiprows=3)
##del frame
'''Unallocated'''
##'''Retrieve Series' Codes'''
#source_frame = pd.read_csv('beanipa20170823sfat.zip')
#source_frame = source_frame[~source_frame.iloc[:, 0].str.contains('Depreciation')]
#source_frame = source_frame[source_frame.iloc[:, 1].str.contains('Billions')]
#source_frame = source_frame[~source_frame.iloc[:, 1].str.contains('Years')]
'''Fixed Assets Series: k3n31gd1es000,  1947--2011'''
semi_frameC = BEASingle('dataset USA BEA SFAT Release 2012-08-15 SectionAll_xls.zip', 'Section3ALL_xls.xls', '303ES Ann', 68, 17, 9)
'''Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
sub_frameA = BEASingleXL('dataset USA BEA Release 2013-09-26 Section1All_Hist.xls', '10105 Ann', 44, 1, False)
'''Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
sub_frameB = BEASingleXL('dataset USA BEA Release 2013-09-26 Section1All_xls.xls', '10105 Ann', 47, 1, False)
semi_frameD = sub_frameA.append(sub_frameB).drop_duplicates()
del sub_frameA, sub_frameB
semi_frameD = semi_frameD.set_index('Period')


def approxPowerFunctionA(period, series, q1, q2, alpha):
    import pandas as pd
    result_frame = pd.Data_frame() ##Data_frame for Based Log-Linear Approximation Results
    result_frame = pd.concat([result_frame, period], axis = 1, sort = True)
    calcul_frame = [] ##Blank List for Calculation Results
    import math
    for i in range(len(period)):
        X01 = q1+q2*(1+period[i]-period[0])**alpha ##{RESULT}(Yhat) = Y0+A*(T-T0)**alpha
        X02 = (q1+q2*(1+period[i]-period[0])**alpha-series[i])**2 ##(Yhat-Y)**2
        X03 = (1+period[i]-period[0])**(alpha-1) ##(T-T0)**(alpha-1)
        X04 = (1+period[i]-period[0])**alpha ##(T-T0)**alpha
        X05 = ((1+period[i]-period[0])**alpha)*math.log(1+period[i]-period[0]) ##((T-T0)**alpha)*LN(T-T0)
        X06 = series[i]*(1+period[i]-period[0])**alpha ##Y*(T-T0)**alpha
        X07 = series[i]*((1+period[i]-period[0])**alpha)*math.log(1+period[i]-period[0]) ##Y*((T-T0)**alpha)*LN(T-T0)
        X08 = (1+period[i]-period[0])**(2*alpha) ##(T-T0)**(2*alpha)
        X09 = (1+period[i]-period[0])**(2*alpha)*math.log(1+period[i]-period[0]) ##(T-T0)**(2*alpha)*LN(T-T0)
        X10 = (1+period[i]-period[0])**(2*alpha-1) ##(T-T0)**(2*alpha-1)
        calcul_frame.append({'X01': X01,  'X02': X02,  'X03': X03,  'X04': X04,  'X05': X05,  'X06': X06,  'X07': X07,  'X08': X08,  'X09': X09,  'X10': X10})
    del X01, X02, X03, X04, X05, X06, X07, X08, X09, X10
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    z1, z2 = 0, 0
    for i in range(len(period)):
        z1 = (q1+q2*(1+period[i]-period[0])**alpha)/(1+i)+z1*i/(1+i)
        z2 = (q1+q2*(1+period[i]-period[0])**alpha-series[i])**2/(1+i)+z2*i/(1+i)
    print('Model Parameter: T0 = %d' %((period[0]-1)))
    print('Model Parameter: Y0 = %d' %(q1))
    print('Model Parameter: A = %f' %(q2))
    print('Model Parameter: alpha = %f' %(alpha))
    print('Estimator Result: Mean Value: %f' %(z1))
    print('Estimator Result: Mean Squared Deviation (MSD): %f' %(z2))
    print('Estimator Result: Root-Mean-Square Deviation (RMSD): %f' %(math.sqrt(z2)))


def approxPowerFunctionB(period, ser_in, ser_ou, p1, p2, p3, p4, alpha):
    import pandas as pd
    result_frame = pd.Data_frame() ##Data_frame for Approximation Results
    result_frame = pd.concat([result_frame, period], axis = 1, sort = True) ##Period
    calcul_frame = [] ##Blank List for Calculation Results
    for i in range(len(period)):
        X01 = ser_in[i] ##'{X}'
        X02 = p3+((p4-p3)/(p2-p1)**alpha)*(ser_in[i]-p1)**alpha ##'{RESULT}(Yhat) = U1+((U2-U1)/(TAU2-TAU1)**Alpha)*({X}-TAU1)**Alpha'
        X03 = (ser_ou[i]-(p3+((p4-p3)/(p2-p1)**alpha)*(ser_in[i]-p1)**alpha))**2 ##'(Yhat-Y)**2'
        X04 = abs(ser_ou[i]-(p3+((p4-p3)/(p2-p1)**alpha)*(ser_in[i]-p1)**alpha)) ##'ABS(Yhat-Y)'
        calcul_frame.append({'X01': X01,  'X02': X02,  'X03': X03,  'X04': X04})
    del X01, X02, X03, X04
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    z1, z2 = 0, 0
    for i in range(len(period)):
        z1 = (p3+((p4-p3)/(p2-p1)**alpha)*(ser_in[i]-p1)**alpha)/(1+i)+z1*i/(1+i)
        z2 = (ser_ou[i]-p3-((p4-p3)/(p2-p1)**alpha)*(ser_in[i]-p1)**alpha)**2/(1+i)+z2*i/(1+i)
    import math
    print('Model Parameter: TAU1 = %d' %(p1))
    print('Model Parameter: TAU2 = %d' %(p2))
    print('Model Parameter: U1 = %d' %(p3))
    print('Model Parameter: U2 = %d' %(p4))
    print('Model Parameter: Alpha = %f' %(alpha))
    print('Model Parameter: A: = (U2-U1)/(TAU2-TAU1)**Alpha = %f' %((p4-p3)/(p2-p1)**alpha))
    print('Estimator Result: Mean Value: %f' %(z1))
    print('Estimator Result: Mean Squared Deviation (MSD): %f' %(z2))
    print('Estimator Result: Root-Mean-Square Deviation (RMSD): %f' %(math.sqrt(z2)))


def approxPowerFunctionC(period, ser_in, ser_ou, p1, p2, p3, p4):
    import math
    alpha = math.log(p4/p3)/math.log(p1/p2)
    import pandas as pd
    result_frame = pd.Data_frame() ##Data_frame for Approximation Results
    result_frame = pd.concat([result_frame, period], axis = 1, sort = True) ##Period
    calcul_frame = [] ##Blank List for Calculation Results
    for i in range(len(period)):
        X01 = ser_in[i] ##'{X}'
        X02 = p3*(p1/ser_in[i])**alpha ##'{RESULT}{Hat}{Y} = Y1*(X1/{X})**Alpha'
        X03 = ser_ou[i]-p3*(p1/ser_in[i])**alpha ##'{Hat-1}{Y}'
        X04 = abs(ser_ou[i]-p3*(p1/ser_in[i])**alpha) ##'ABS({Hat-1}{Y})'
        X05 = (ser_ou[i]-p3*(p1/ser_in[i])**alpha)**2 ##'({Hat-1}{Y})**2'
        calcul_frame.append({'X01': X01,  'X02': X02,  'X03': X03,  'X04': X04,  'X05': X05})
    del X01, X02, X03, X04, X05
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    z1, z2 = 0, 0
    for i in range(len(period)):
        z1 = (p3*(p1/ser_in[i])**alpha)/(1+i)+z1*i/(1+i)
        z2 = (ser_ou[i]-p3*(p1/ser_in[i])**alpha)**2/(1+i)+z2*i/(1+i)
    print('Model Parameter: X1 = %f' %(p1))
    print('Model Parameter: X2 = %d' %(p2))
    print('Model Parameter: Y1 = %f' %(p3))
    print('Model Parameter: Y2 = %d' %(p4))
    print('Model Parameter: Alpha: = LN(Y2/Y1)/LN(X1/X2) = %f' %(alpha))
    print('Estimator Result: Mean Value: %f' %(z1))
    print('Estimator Result: Mean Squared Deviation (MSD): %f' %(z2))
    print('Estimator Result: Root-Mean-Square Deviation (RMSD): %f' %(math.sqrt(z2)))


def datasetCanada():
    '''Number 1. CANSIM Table 282-0012 Labour Force Survey Estimates (LFS),  employment by class of worker,  North American Industry Classification\
    System (NAICS) and sex'''
    '''Number 2. CANSIM Table 03790031'''
    '''Title: Gross domestic product (GDP) at basic prices,  by North American Industry Classification System (NAICS)'''
    '''Measure: monthly (dollars x 1, 000, 000)'''
    '''Number 3. CANSIM Table 03800068'''
    '''Title: Gross fixed capital formation'''
    '''Measure: quarterly (dollars x 1, 000, 000)'''
    '''Number 4. CANSIM Table 031-0004: Flows and stocks of fixed non-residential capital,  total all industries,  by asset,  provinces and territories, \
    annual (dollars x 1, 000, 000)'''
    '''Number 5. CANSIM Table 03790028'''
    '''Title: Gross domestic product (GDP) at basic prices,  by North American Industry Classification System (NAICS),  provinces and territories'''
    '''Measure: annual (percentage share)'''
    '''Number 6. CANSIM Table 03800001'''
    '''Title: Gross domestic product (GDP),  income-based,  *Terminated*'''
    '''Measure: quarterly (dollars x 1, 000, 000)'''
    '''Number 7. CANSIM Table 03800002'''
    '''Title: Gross domestic product (GDP),  expenditure-based,  *Terminated*'''
    '''Measure: quarterly (dollars x 1, 000, 000)'''
    '''Number 8. CANSIM Table 03800063'''
    '''Title: Gross domestic product,  income-based'''
    '''Measure: quarterly (dollars x 1, 000, 000)'''
    '''Number 9. CANSIM Table 03800064'''
    '''Title: Gross domestic product,  expenditure-based'''
    '''Measure: quarterly (dollars x 1, 000, 000)'''
    '''Number 10. CANSIM Table 03800069'''
    '''Title: Investment in inventories'''
    '''Measure: quarterly (dollars unless otherwise noted)'''
    '''---'''
    '''1.0. Labor Block: `v2523012`,  Preferred Over `v3437501` Which Is Quarterly'''
    '''`v2523012` - 282-0012 Labour Force Survey Estimates (LFS),  employment by class of worker,  North American Industry Classification System (NAICS)\
    and sex; Canada; Total employed,  all class of workers; Manufacturing; Both sexes (x 1, 000) (annual,  1987 to 2017)'''
    from datafetch import fetchCANSIM
    from datafetch import fetchCANSIMQ
    labor = fetchCANSIM('02820012', 'v2523012', True)
    '''1.1. Labor Block,  Alternative Option Not Used'''
    '''`v3437501` - 282-0011 Labour Force Survey estimates (LFS),  employment by class of worker,  North American Industry Classification System (NAICS)\
    and sex,  unadjusted for seasonality; Canada; Total employed,  all classes of workers; Manufacturing; Both sexes (x 1, 000) (monthly,  1987-01-01 to\
    2017-12-01)'''
    ##fetchCANSIMQ('02820011', 'v3437501', True)
    '''2.i. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
    `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    '''2.0. 2007 constant prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1, 000, 000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    '''Industrial machinery (x 1, 000, 000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    S = ['v43975603', 'v43977683', 'v43978099', 'v43978515', 'v43978931', 'v43979347', 'v43979763', 'v43980179', 'v43980595', 'v43976019', 'v43976435', 'v43976851', \
       'v43977267', 'v43975594', 'v43977674', 'v43978090', 'v43978506', 'v43978922', 'v43979338', 'v43979754', 'v43980170', 'v43980586', 'v43976010', 'v43976426', \
       'v43976842', 'v43977258']
    '''2.1. Fixed Assets Block,  Alternative Option Not Used'''
    '''2.1.1. Chained (2007) dollars'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1, 000, 000): `v43980803`, `v43981843`, `v43982051`, `v43982259`, `v43982467`, `v43982675`, `v43982883`, `v43983091`, `v43983299`, \
    `v43981011`, `v43981219`, `v43981427`, `v43981635`'''
    '''Industrial machinery (x 1, 000, 000): `v43980794`, `v43981834`, `v43982042`, `v43982250`, `v43982458`, `v43982666`, `v43982874`, `v43983082`, `v43983290`, \
    `v43981002`, `v43981210`, `v43981418`, `v43981626`'''
    ##AS1 = ['v43980803', 'v43981843', 'v43982051', 'v43982259', 'v43982467', 'v43982675', 'v43982883', 'v43983091', 'v43983299', 'v43981011', 'v43981219', 'v43981427', \
    ##     'v43981635', 'v43980794', 'v43981834', 'v43982042', 'v43982250', 'v43982458', 'v43982666', 'v43982874', 'v43983082', 'v43983290', 'v43981002', 'v43981210', \
    ##     'v43981418', 'v43981626']
    '''2.1.2. Current prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1, 000, 000): `v43975395`, `v43977475`, `v43977891`, `v43978307`, `v43978723`, `v43979139`, `v43979555`, `v43979971`, `v43980387`, \
    `v43975811`, `v43976227`, `v43976643`, `v43977059`'''
    '''Industrial machinery (x 1, 000, 000): `v43975386`, `v43977466`, `v43977882`, `v43978298`, `v43978714`, `v43979130`, `v43979546`, `v43979962`, `v43980378`, \
    `v43975802`, `v43976218`, `v43976634`, `v43977050`'''
    ##AS2 = ['v43975395', 'v43977475', 'v43977891', 'v43978307', 'v43978723', 'v43979139', 'v43979555', 'v43979971', 'v43980387', 'v43975811', 'v43976227', 'v43976643', \
    ##     'v43977059', 'v43975386', 'v43977466', 'v43977882', 'v43978298', 'v43978714', 'v43979130', 'v43979546', 'v43979962', 'v43980378', 'v43975802', 'v43976218', \
    ##     'v43976634', 'v43977050']
    capital = fetchCANSIMFA(fetchCANSIMSeries())
    '''3.i. Production Block: `v65201809`,  Preferred Over `v65201536` Which Is Quarterly'''
    '''3.0. Production Block: `v65201809`'''
    '''`v65201809` - 379-0031 Gross domestic product (GDP) at basic prices,  by North American Industry Classification System (NAICS); Canada; Trading-day\
    adjusted; 2007 constant prices; Manufacturing (x 1, 000, 000) (monthly,  1997-01-01 to 2017-10-01)'''
    product = fetchCANSIMQ('03790031', 'v65201809', True)
    '''3.1. Production Block: `v65201536`,  Alternative Option Not Used'''
    '''`v65201536` - 379-0031 Gross domestic product (GDP) at basic prices,  by North American Industry Classification System (NAICS); Canada; Seasonnaly\
    adjusted at annual rates; 2007 constant prices; Manufacturing (x 1, 000, 000) (monthly,  1997-01-01 to 2017-10-01)'''
    ##fetchCANSIMQ('03790031', 'v65201536', True)
    import pandas as pd
    result_frame = pd.concat([labor, capital, product], axis = 1, sort = True)
    result_frame = result_frame.dropna()
    result_frame.rename(columns = {'v2523012':'labor', 0:'capital', 'v65201809':'product'}, inplace=True)
    result_frame.to_csv('temporary.txt')
    del result_frame
    result_frame = pd.read_csv('temporary.txt')
    import os
    os.unlink('temporary.txt')
    return result_frame


def douglasTest(control, series):
    '''control from Original Dataset;
    series from Douglas Theory of Wages'''
    import pandas as pd
    if control =='CDT2S4':
        control_frame = fetchClassic('cobbdouglas.zip', 'CDT2S4') ## Total Fixed Capital in 1880 dollars (4)
    elif control =='J0014':
        control_frame = fetchCensus('census1949.zip', 'J0014', True)
    test_frame = fetchClassic('douglas.zip', series)
    if control =='J0014':
        control_frame.iloc[:, 0] = 100*control_frame.iloc[:, 0].div(control_frame.iloc[36, 0]) ## 1899 = 100
        control_frame.iloc[:, 0] = control_frame.iloc[:, 0].round(0)
    else:
        pass
    control_frame = pd.concat([control_frame, test_frame], axis = 1, sort = True)
    if control =='J0014':
        control_frame['dev'] = control_frame.iloc[:, 1]-control_frame.iloc[:, 0]
    elif control =='CDT2S4':
        control_frame['dev'] = control_frame.iloc[:, 0].div(control_frame.iloc[:, 1])
    else:
        pass
    control_frame = control_frame.dropna()
#    control_frame.plot(title = 'Cobb--Douglas Data Comparison', legend = True, grid = True)
    print(control_frame)


def options():
    '''The Revised Index of Physical Production for All Manufacturing In the United States,  1899--1926'''
    fetchClassic('douglas.zip', 'DT24AS01')
    '''Not Suitable: Total Capital (in millions of 1880 dollars)'''
    fetchClassic('douglas.zip', 'DT63AS01')
    '''Not Suitable: Annual Increase (in millions of 1880 dollars)'''
    fetchClassic('douglas.zip', 'DT63AS02')
    '''Not Suitable: Percentage Rate of Growth'''
    fetchClassic('douglas.zip', 'DT63AS03')


def douglasTest(control, series):
    '''control from Original Dataset;
    series from Douglas Theory of Wages'''
    import pandas as pd
    if control =='CDT2S4':
        control_frame = fetchClassic('cobbdouglas.zip', 'CDT2S4') ## Total Fixed Capital in 1880 dollars (4)
    elif control =='J0014':
        control_frame = fetchCensus('census1949.zip', 'J0014', True)
    test_frame = fetchClassic('douglas.zip', series)
    if control =='J0014':
        control_frame.iloc[:, 0] = 100*control_frame.iloc[:, 0]/control_frame.iloc[36, 0] ## 1899 = 100
        control_frame.iloc[:, 0] = control_frame.iloc[:, 0].round(0)
    else:
        pass
    control_frame = pd.concat([control_frame, test_frame], axis = 1, sort = True)
    if control =='J0014':
        control_frame['dev'] = control_frame.iloc[:, 1]-control_frame.iloc[:, 0]
    elif control =='CDT2S4':
        control_frame['dev'] = control_frame.iloc[:, 0]/control_frame.iloc[:, 1]
    else:
        pass
    print(control_frame)


def archivedCommonFetch():
    """Data Fetch"""
    import os
    import pandas as pd
#    from datafetch import BEASingle
#    from datafetch import BEASingleXL
#    from datafetch import FRBCU
#    from datafetch import labor
    """Fixed Assets Series: k1n31gd1es000,  1925--2016"""
    semi_frameA = BEASingle('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '401 Ann', 95, 12, 0)
    """Fixed Assets Series: k1ntotl1si000,  1925--2016"""
    semi_frameB = BEASingle('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '201 Ann', 95, 56, 0)
    """Fixed Assets Series: k3n31gd1es000,  1925--2016"""
    semi_frameC = BEASingle('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '403 Ann', 95, 12, 0)
    """Fixed Assets Series: k3ntotl1si000,  1925--2016"""
    semi_frameD = BEASingle('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '203 Ann', 95, 56, 24)
    """Fixed Assets Series: K160491,  1951--1969"""
    sub_frameA = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50900 Ann', 22, 54, 32)
    """Fixed Assets Series: K160491,  1969--2011"""
    sub_frameB = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50900 Ann', 46, 54, 32)
    semi_frameE = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameF = labor()
    """National Income: A032RC1,  1929--1969"""
    sub_frameA = BEASingleXL('dataset USA BEA Release 2015-03-02 Section1ALL_Hist.xls', '11200 Ann', 44, 1, False)
    """National Income: A032RC1,  1969--2013"""
    sub_frameB = BEASingleXL('dataset USA BEA Release 2015-03-02 Section1all_xls.xls', '11200 Ann', 48, 1, False)
    semi_frameG = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameG = semi_frameG.set_index('Period')
    """Nominal Gross Domestic Product Series: A191RC1,  1929--1969"""
    sub_frameA = BEASingleXL('dataset USA BEA Release 2015-03-02 Section1ALL_Hist.xls', '10105 Ann', 44, 1, False)
    """Nominal Gross Domestic Product Series: A191RC1,  1969--2014"""
    sub_frameB = BEASingleXL('dataset USA BEA Release 2015-03-02 Section1all_xls.xls', '10105 Ann', 49, 1, False)
    semi_frameH = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameH = semi_frameH.set_index('Period')
    """Real Gross Domestic Product Series: A191RX1,  1929--1969,  2009 = 100"""
    sub_frameA = BEASingleXL('dataset USA BEA Release 2015-03-02 Section1ALL_Hist.xls', '10106 Ann', 44, 1, False)
    """Real Gross Domestic Product Series: A191RX1,  1969--2014,  2009 = 100"""
    sub_frameB = BEASingleXL('dataset USA BEA Release 2015-03-02 Section1all_xls.xls', '10106 Ann', 49, 1, False)
    semi_frameI = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameI = semi_frameI.set_index('Period')
    """Nominal Gross Domestic Product Series: A191RC1,  1929--1969"""
    sub_frameA = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 44, 1, 0)
    """Nominal Gross Domestic Product Series: A191RC1,  1969--2012"""
    sub_frameB = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 47, 1, 0)
    semi_frameJ = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Deflator Gross Domestic Product,  A191RD3,  1929--1969,  2009 = 100"""
    sub_frameA = BEASingleXL('dataset USA BEA Release 2015-03-02 Section1ALL_Hist.xls', '10109 Ann', 44, 1, False)
    """Deflator Gross Domestic Product,  A191RD3,  1969--2014,  2009 = 100"""
    sub_frameB = BEASingleXL('dataset USA BEA Release 2015-03-02 Section1all_xls.xls', '10109 Ann', 49, 1, False)
    semi_frameK = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameK = semi_frameK.set_index('Period')
    semi_frameK.iloc[:, 0] = 100/semi_frameK.iloc[:, 0]
    """Real Gross Domestic Product Series: A191RX1,  1929--1969,  2005 = 100"""
    sub_frameA = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10106 Ann', 44, 1, 6)
    """Real Gross Domestic Product Series: A191RX1,  1969--2012,  2005 = 100"""
    sub_frameB = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10106 Ann', 47, 1, 6)
    semi_frameL = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    """Capacity Utilization Series: CAPUTL.B50001.A,  1967--2012"""
    semi_frameM = FRBCU()
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI, semi_frameJ, \
                           semi_frameK, semi_frameL, semi_frameM], axis = 1, sort = True)
    return result_frame


def archivedCombinedCapital():
#    from datafetch import archivedBEALabor
#    from datafetch import FRBCU
    '''Nominal Investment Series: A006RC1,  1929--1969'''
    sub_frameA = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 43, 7, 0) ##Through Year of 1968 Instead of 1969
    '''Nominal Investment Series: A006RC1,  1969--2012'''
    sub_frameB = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 47, 7, 0)
    semi_frameA = sub_frameA.append(sub_frameB)
    del sub_frameA, sub_frameB
    '''Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
    sub_frameA = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 44, 1, 0)
    '''Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
    sub_frameB = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 47, 1, 0)
    semi_frameB = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Real Gross Domestic Product Series: A191RX1,  1929--1969'''
    sub_frameA = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10106 Ann', 44, 1, 6)
    '''Real Gross Domestic Product Series: A191RX1,  1969--2012'''
    sub_frameB = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10106 Ann', 47, 1, 6)
    semi_frameC = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Capacity Utilization Series: CAPUTL.B50001.A,  1967--2012'''
    semi_frameD = FRBCU()
    '''U.S. Bureau of Economic Analysis,  Produced assets,  closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA],  retrieved from FRED,  Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/K160491A027NBEA,  August 23,  2018.
    http://www.bea.gov/data/economic-accounts/national
    https://fred.stlouisfed.org/series/K160491A027NBEA
    https://search.bea.gov/search?affiliate = u.s.bureauofeconomicanalysis&query = k160491'''
    '''Fixed Assets Series: K160021,  1951--1969'''
    sub_frameA = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50900 Ann', 22, 3, 0)
    '''Fixed Assets Series: K160021,  1969--2011'''
    sub_frameB = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50900 Ann', 46, 3, 0)
    semi_frameE = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Fixed Assets Series: K160491,  1951--1969'''
    sub_frameA = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50900 Ann', 22, 54, 0)
    '''Fixed Assets Series: K160491,  1969--2011'''
    sub_frameB = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50900 Ann', 46, 54, 0)
    semi_frameF = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameG = archivedBEALabor()
    '''Labor Series: A4601C0,  1929--1948'''
    sub_frameA = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section6ALL_Hist.xls', '60800A Ann', 23, 1, 10)
    '''Labor Series: A4601C0,  1948--1969'''
    sub_frameB = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section6ALL_Hist.xls', '60800B Ann', 25, 1, 7)
    '''Labor Series: A4601C0,  1969--1987'''
    sub_frameC = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60800B Ann', 22, 1, 7)
    '''Labor Series: A4601C0,  1987--2000'''
    sub_frameD = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60800C Ann', 17, 1, 13)
    '''Labor Series: A4601C0,  1998--2011'''
    sub_frameE = BEASingle('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60800D Ann', 17, 1, 23)
    semi_frameH = sub_frameA.append(sub_frameB).append(sub_frameC).append(sub_frameD).append(sub_frameE).drop_duplicates()
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, 
                           semi_frameF, semi_frameG, semi_frameH], axis = 1, sort = True).dropna(how = 'all')
    return result_frame


def BEASingle(zpfl, wrkbk, wrksht, clmn_0, clmn_1, ftr_0):
    '''Data _frame Fetching from Bureau of Economic Analysis Zip Archives'''
    '''clmn_0 = source_frame.shape[1]
    clmn_1: Number of Line +1 Where Series Code Is Presented'''
    import zipfile
    zf = zipfile.ZipFile(zpfl, 'r')
    import pandas as pd
    xl = pd.ExcelFile(zf.open(wrkbk))
    source_frame = pd.read_excel(xl, wrksht, usecols=range(2, clmn_0), skiprows=7, skipfooter = ftr_0)
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del source_frame
    result_frame = pd.read_csv('temporary.txt', usecols=[0, clmn_1], skiprows=1)
    result_frame.columns = result_frame.columns.to_series().replace({'^Unnamed: \d':'Period'}, regex = True)
    result_frame = result_frame.set_index('Period')
    import os
    os.unlink('temporary.txt')
    del zf, xl
    return result_frame


def BEASingleXL(wrkbk, wrksht, yr, ln, index):
    '''Data _frame Fetching from Bureau of Economic Analysis'''
    import os
    import pandas as pd
    xl = pd.ExcelFile(wrkbk)
    source_frame = pd.read_excel(xl, wrksht, usecols=range(2, yr), skiprows=7)
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del xl, source_frame
    result_frame = pd.read_csv('temporary.txt', usecols=[0, ln], skiprows=1)
    os.unlink('temporary.txt')
    result_frame.columns = result_frame.columns.to_series().replace({'^Unnamed: \d':\
                                                                 'Period'}, regex = True)
    if index:
        result_frame = result_frame.set_index('Period')
    return result_frame


os.chdir('D:')
douglasTest('J0014', 'DT24AS01')
douglasTest('CDT2S4', 'DT63AS01')