# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:17:13 2020

@author: Mastermind
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp


def beaFetch(source, wrkbk, wrksht, start, finish, line):
    '''Data _frame Fetching from Bureau of Economic Analysis Zip Archives'''
    '''
    source: Name of Zip Archive, 
    wrkbk: Name of Excel File within Zip Archive, 
    wrksht: Name of Worksheet within Excel File within Zip Archive, 
    boundary: 4+<Period_Finish>-<Period_Start>, 
    line: Line'''
    boundary = 4-start+finish
    if source ==None:
        xl = pd.ExcelFile(wrkbk)
    else:
        import zipfile
        zf = zipfile.ZipFile(source, 'r')
        xl = pd.ExcelFile(zf.open(wrkbk))
        del zf
    source_frame = pd.read_excel(xl, wrksht, usecols=range(2, boundary), skiprows=7)
    source_frame.dropna(inplace=True)
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del xl, source_frame
    result_frame = pd.read_csv('temporary.txt', usecols=[0, line], skiprows=1)
    os.unlink('temporary.txt')
    result_frame.columns = result_frame.columns.to_series().replace({'^Unnamed: \d':'Period'}, regex = True)
    result_frame = result_frame.set_index('Period')
    return result_frame


def fetchBEA(source, string):
    '''`dataset-usa-bea-NipaDataA.txt`: U.S. Bureau of Economic Analysis
    Archived: https://www.bea.gov/National/FAweb/Details/Index.html
    https://www.bea.gov//national/FA2004/DownSS2.asp,  Accessed May 26,  2018'''
    if source =='beanipa20131202.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source =='beanipa20150302section5.zip': ##Not Used
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source =='beanipa20150501.zip':
        source_frame = pd.read_csv(source, usecols=range(14, 18))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
        source_frame = source_frame[source_frame.iloc[:, 2] ==0]
        source_frame = source_frame[source_frame.columns[[0, 1, 3]]]
    elif source =='dataset-usa-bea-NipaDataA.txt':
        source_frame = pd.read_csv(source, thousands = ', ')
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source =='beanipa20131202sfat.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source =='beanipa20170823sfat.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    else:
        pass
    result_frame = source_frame[source_frame.iloc[:, 0] ==string]
    del source_frame
    result_frame = result_frame[result_frame.columns[[1, 2]]]
    result_frame = result_frame.reset_index(drop = True)
    result_frame = result_frame.set_index('Period')
    result_frame.to_csv('temporary.txt')
    del result_frame
    result_frame = pd.read_csv('temporary.txt')
    os.unlink('temporary.txt')
    result_frame = result_frame.set_index('Period')
    if source =='beanipa20170823sfat.zip':
        result_frame = result_frame.round(3)
    else:
        pass
    result_frame = result_frame.drop_duplicates()
    return result_frame


def fetchClassic(source, string):
    if source =='brown.zip':
        source_frame = pd.read_csv(source, skiprows=4, usecols=range(3, 6))
        source_frame.rename(columns = {'Данные по отработанным человеко-часам заимствованы из: Kendrick,  op. cit.,  pp. 311-313,  Table A. 10.':'series', 
                                    'Unnamed: 4':'period', 
                                    'Unnamed: 5':'value'}, inplace=True)
    elif source =='dataset-usa-cobb-douglas.zip':
        source_frame = pd.read_csv(source, usecols=range(5, 8))
    elif source =='douglas.zip':
        source_frame = pd.read_csv(source, usecols=range(4, 7))
    elif source =='dataset-usa-kendrick.zip':
        source_frame = pd.read_csv(source, usecols=range(4, 7))
    result_frame = source_frame[source_frame.iloc[:, 0] ==string]
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
    if source =='dataset-usa-census1975.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11), dtype = {'vector':str, 'period':str, 'value':str})
    else:
        source_frame = pd.read_csv(source, usecols=range(8, 11))
    source_frame = source_frame[source_frame.iloc[:, 0] ==string]
    source_frame = source_frame[source_frame.columns[[1, 2]]]
    if source =='dataset-usa-census1975.zip':
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


def pricesInverseSingle(source_frame):
    '''Intent: Returns Prices Icrement Series from Cumulative Deflator Series;
    source: pandas Data_frame'''
    D = source_frame.iloc[:, 0].div(source_frame.iloc[:, 0].shift(1))-1
    return D


def processing(source_frame, col):
    interim_frame = source_frame[source_frame.columns[[col]]]
    interim_frame = interim_frame.dropna()
    result_frame = pricesInverseSingle(interim_frame)
    result_frame = result_frame.dropna()
    return result_frame


def indexswitch(source_frame):
    source_frame.to_csv('temporary.txt')
    del source_frame
    result_frame = pd.read_csv('temporary.txt')
    os.unlink('temporary.txt')
    return result_frame


def cobbDouglasPreprocessing():
    '''Original Cobb--Douglas Data Preprocessing'''
    semi_frameA = fetchClassic('dataset-usa-cobb-douglas.zip', 'CDT2S4') ## Total Fixed Capital in 1880 dollars (4)
    semi_frameB = fetchClassic('dataset-usa-cobb-douglas.zip', 'CDT3S1') ## Average Number Employed (in thousands)
    semi_frameC = fetchCensus('dataset-usa-census1949.zip', 'J0014', True)
    semi_frameD = fetchCensus('dataset-usa-census1949.zip', 'J0013', True)
    semi_frameE = fetchClassic('douglas.zip', 'DT24AS01') ## The Revised Index of Physical Production for All Manufacturing In the United States,  1899--1926
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE
    result_frame = result_frame.dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def archivedBEALabor():
    '''Labor Series: H4313C0,  1929--1948'''
    semi_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section6ALL_Hist.xls', '60500A Ann', 1929, 1948, 14)
    '''Labor Series: J4313C0,  1948--1969'''
    semi_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section6ALL_Hist.xls', '60500B Ann', 1948, 1969, 13)
    '''Labor Series: J4313C0,  1969--1987'''
    semi_frameC = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60500B Ann', 1969, 1987, 13)
    '''Labor Series: A4313C0,  1987--2000'''
    semi_frameD = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60500C Ann', 1987, 2000, 13)
    '''Labor Series: N4313C0,  1998--2011'''
    semi_frameE = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60500D Ann', 1998, 2011, 13)
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE
    result_frame = result_frame.mean(1)
    result_frame = result_frame.to_frame(name = 'Labor')
    return result_frame


def BEALabor():
    '''Labor Series: H4313C0,  1929--1948'''
    semi_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section6ALL_Hist.xls', '60500A Ann', 1929, 1948, 14)
    '''Labor Series: J4313C0,  1948--1969'''
    semi_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section6ALL_Hist.xls', '60500B Ann', 1948, 1969, 13)
    '''Labor Series: J4313C0,  1969--1987'''
    semi_frameC = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60500B Ann', 1969, 1987, 13)
    '''Labor Series: A4313C0,  1987--2000'''
    semi_frameD = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60500C Ann', 1987, 2000, 13)
    '''Labor Series: N4313C0,  1998--2011'''
    semi_frameE = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section6all_xls.xls', '60500D Ann', 1998, 2011, 13)
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE
    result_frame = result_frame.mean(1)
    result_frame = result_frame.to_frame(name = 'Labor')
    return result_frame


def FRBCU():
    '''Indexed Capacity Utilization Series: CAPUTL.B50001.A,  1967--2012
    CAPUTL.B50001.A Fetching'''
    source_frame = pd.read_csv('dataset USA FRB_G17_All_Annual 2013-06-23.csv', skiprows=1, usecols=range(5, 100))
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del source_frame
    source_frame = pd.read_csv('temporary.txt', skiprows=1)
    os.unlink('temporary.txt')
    source_frame.columns = source_frame.columns.to_series().replace({'[ .:;@_]':''}, regex = True)
    result_frame = source_frame[['SeriesName', 'CAPUTLB50001A']]
    del source_frame
    result_frame = result_frame.dropna()
    result_frame = result_frame.reset_index(drop = True)
    result_frame.rename(columns = {'SeriesName':'Period'}, inplace=True)
    result_frame.iloc[:, 0] = result_frame.iloc[:, 0].astype(int)
    result_frame = result_frame.set_index('Period')
    return result_frame


def FRBIP():
    '''Indexed Manufacturing Series: FRB G17 IP,  AIPMA_SA_IX,  1919--2018'''
    source_frame = pd.read_csv('dataset USA FRB US3_IP 2018-09-02.csv', skiprows=7)
    source_frame.columns = source_frame.columns.to_series().replace({'[ .:;@_]':''}, regex = True)
    source_frame['Period'], source_frame['Mnth'] = source_frame['Unnamed0'].str.split('-').str
    source_frame = source_frame.groupby('Period').mean()
    source_frame.to_csv('temporary.txt')
    del source_frame
    result_frame = pd.read_csv('temporary.txt', usecols=[0, 3])
    os.unlink('temporary.txt')
    result_frame = result_frame.set_index('Period')
    return result_frame


def FRBFA():
    '''Returns _frame of Manufacturing Fixed Assets Series,  Billion USD:
    result_frame.iloc[:, 0]: Nominal;
    result_frame.iloc[:, 1]: Real
    '''
    source_frame = pd.read_csv('dataset USA FRB invest_capital.csv', skiprows=4, skipfooter = 688, engine = 'python')
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del source_frame
    source_frame = pd.read_csv('temporary.txt', skiprows=1)
    os.unlink('temporary.txt')
    source_frame.columns = source_frame.columns.to_series().replace({'Manufacturing':'Period'})
    source_frame = source_frame.set_index('Period')
    source_frame['FRB_nominal'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 2].div(1000*source_frame.iloc[:, 0])+source_frame.iloc[:, 4]*source_frame.iloc[:, 5].div(1000*source_frame.iloc[:, 3])
    source_frame['FRB_real'] = source_frame.iloc[:, 2].div(1000)+source_frame.iloc[:, 5].div(1000)
    result_frame = source_frame[source_frame.columns[[6, 7]]]
    return result_frame


def FRBFADEF():
    '''Returns _frame of Deflator for Manufacturing Fixed Assets Series,  Index:
    result_frame.iloc[:, 0]: Deflator
    '''
    source_frame = pd.read_csv('dataset USA FRB invest_capital.csv', skiprows=4, skipfooter = 688, engine = 'python')
    source_frame = source_frame.T
    source_frame.to_csv('temporary.txt')
    del source_frame
    source_frame = pd.read_csv('temporary.txt', skiprows=1)
    os.unlink('temporary.txt')
    source_frame.columns = source_frame.columns.to_series().replace({'Manufacturing':'Period'})
    source_frame = source_frame.set_index('Period')
    source_frame['fa_def_frb'] = (source_frame.iloc[:, 1]+source_frame.iloc[:, 4]).div(source_frame.iloc[:, 0]+source_frame.iloc[:, 3])
    result_frame = source_frame[source_frame.columns[[6]]]
    return result_frame


def fetchINFCF():
    '''Retrieve Yearly Price Rates from `infcf16652007.zip`'''
    source_frame = pd.read_csv('infcf16652007.zip', usecols=range(4, 7))
    series = source_frame.iloc[:, 0].unique()
    i = 0
    for ser in series:
        current_frame = source_frame[source_frame.iloc[:, 0] ==ser]
        current_frame = current_frame[current_frame.columns[[1, 2]]]
        current_frame.columns = current_frame.columns.str.title()
        current_frame.rename(columns = {'Value':ser}, inplace=True)
        current_frame = current_frame.set_index('Period')
        current_frame.iloc[:, 0] = current_frame.iloc[:, 0].rdiv(1)
        current_frame = -pricesInverseSingle(current_frame) ## Put '-' Is the Only Way to Comply with the Rest of Study
        if i ==0:
            result_frame = current_frame
        elif i> = 1:
            result_frame = pd.concat([result_frame, current_frame], axis = 1, sort = True)
        del current_frame
        i+ = 1
    result_frame = result_frame[result_frame.columns[range(14)]]
    result_frame['cpiu_fused'] = result_frame.mean(1)
    result_frame = result_frame[result_frame.columns[[14]]]
    return result_frame


def RMF(source_frame, k = 1):
    '''Rolling Mean Filter
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Series
    '''
    series = source_frame.iloc[:, 1]
    result_frame = source_frame
    for i in range(1, 1+k):
        rmf = series.rolling(window = 1+i, center = True).mean()
        result_frame = pd.concat([result_frame, rmf], axis = 1, sort = True)
    odd_frame = result_frame.iloc[:, 0]
    even_frame = result_frame.iloc[:, 0].rolling(window = 2).mean()
    for i in range(1, 2+k, 2):
        odd_frame = pd.concat([odd_frame, result_frame.iloc[:, i]], axis = 1, sort = True)
    for i in range(2, 2+k, 2):
        even_frame = pd.concat([even_frame, result_frame.iloc[:, i]], axis = 1, sort = True)
    even_frame = even_frame.dropna(how = 'all').reset_index(drop = True)
    odd_frame = odd_frame.set_index('Period')
    even_frame = even_frame.set_index('Period')
    return odd_frame, even_frame


def KZF(source_frame, k = 1):
    '''Kolmogorov--Zurbenko Filter
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Series
    '''
    series = source_frame.iloc[:, 1]
    result_frame = source_frame
    for i in range(1, 1+k):
        series = series.rolling(window = 2).mean()
        skz = series.shift(-(i//2))
        result_frame = pd.concat([result_frame, skz], axis = 1, sort = True)
    odd_frame = result_frame.iloc[:, 0]
    even_frame = result_frame.iloc[:, 0].rolling(window = 2).mean()
    for i in range(1, 2+k, 2):
        odd_frame = pd.concat([odd_frame, result_frame.iloc[:, i]], axis = 1, sort = True)
    for i in range(2, 2+k, 2):
        even_frame = pd.concat([even_frame, result_frame.iloc[:, i]], axis = 1, sort = True)
    even_frame = even_frame.dropna(how = 'all').reset_index(drop = True)
    odd_frame = odd_frame.set_index('Period')
    even_frame = even_frame.set_index('Period')
    return odd_frame, even_frame


def SES(source_frame, window = 5, alpha = 0.5):
    '''Single Exponential Smoothing
    Robert Goodell Brown,  1956
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Series
    '''
    S = source_frame.iloc[:window, 1]
    S = S.mean() ##Average of Window-First Entries
    ses = []
    ses.append(alpha*source_frame.iloc[0, 1]+(1-alpha)*S)
    for i in range(1, len(source_frame)):
        ses.append(alpha*source_frame.iloc[i, 1]+(1-alpha)*ses[i-1])
    cap = 'ses{:02d}_{:, .6f}'.format(window, alpha)
    ses = pd.Data_frame(ses, columns = [cap])
    result_frame = pd.concat([source_frame, ses], axis = 1, sort = True)
    result_frame = result_frame.set_index('Period')
    return result_frame


def fetchCapital():
    '''Series Not Used - `k3ntotl1si000`'''
    semi_frameA = fetchClassic('dataset-usa-cobb-douglas.zip', 'CDT2S1') ##Annual Increase in Terms of Cost Price (1)
    semi_frameB = fetchClassic('dataset-usa-cobb-douglas.zip', 'CDT2S3') ##Annual Increase in Terms of 1880 dollars (3)
    semi_frameC = fetchClassic('dataset-usa-cobb-douglas.zip', 'CDT2S4') ##Total Fixed Capital in 1880 dollars (4)
    '''Fixed Assets: k1n31gd1es000,  1925--2016,  Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    semi_frameD = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '401 Ann', 1925, 2016, 9)
    '''Not Used: Fixed Assets: k3n31gd1es000,  1925--2016,  Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    semi_frameE = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '403 Ann', 1925, 2016, 9)
    semi_frameF = fetchCensus('dataset-usa-census1975.zip', 'P0107', True)
    semi_frameG = fetchCensus('dataset-usa-census1975.zip', 'P0110', True)
    semi_frameH = fetchCensus('dataset-usa-census1975.zip', 'P0119', True)
    '''Kendrick J.W.,  Productivity Trends in the United States,  Page 320'''
    semi_frameI = fetchClassic('dataset-usa-kendrick.zip', 'KTA15S08')
    '''Douglas P.H.,  Theory of Wages,  Page 332'''
    semi_frameJ = fetchClassic('douglas.zip', 'DT63AS01')
    '''FRB Data'''
    semi_frameK = FRBFA()
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI, semi_frameJ, \
                           semi_frameK], axis = 1, sort = True)
    return result_frame


def cobbDouglasCapitalExtension():
    '''Existing Capital Dataset'''
    source_frame = fetchCapital()
    '''Convert Capital Series into Current (Historical) Prices'''
    source_frame['nominal_cbb_dg'] = source_frame.iloc[:, 0]*source_frame.iloc[:, 2].div(1000*source_frame.iloc[:, 1])
    source_frame['nominal_census'] = source_frame.iloc[:, 5]*source_frame.iloc[:, 7].div(source_frame.iloc[:, 6])
    source_frame['nominal_dougls'] = source_frame.iloc[:, 0]*source_frame.iloc[:, 9].div(1000*source_frame.iloc[:, 1])
    source_frame['nominal_kndrck'] = source_frame.iloc[:, 5]*source_frame.iloc[:, 8].div(1000*source_frame.iloc[:, 6])
    source_frame.iloc[:, 15] = source_frame.iloc[66, 6]*source_frame.iloc[:, 15].div(source_frame.iloc[66, 5])
    '''Douglas P.H. -- Kendrick J.W. (Blended) Series'''
    source_frame['nominal_doug_kndrck'] = source_frame.iloc[:, 14:16].mean(1)
    '''Cobb C.W.,  Douglas P.H. -- FRB (Blended) Series'''
    source_frame['nominal_cbb_dg_frb'] = source_frame.iloc[:, [12, 10]].mean(1)
    '''Capital Structure Series: `Cobb C.W.,  Douglas P.H. -- FRB (Blended) Series` to `Douglas P.H. -- Kendrick J.W. (Blended) Series`'''
    source_frame['struct_ratio'] = source_frame.iloc[:, 17].div(source_frame.iloc[:, 16])
    '''Filling the Gaps within Capital Structure Series'''
    source_frame.iloc[6:36, 18].fillna(source_frame.iloc[36, 18], inplace=True)
    source_frame.iloc[36:, 18].fillna(0.275, inplace=True)
    '''Patch Series `Douglas P.H. -- Kendrick J.W. (Blended) Series` Multiplied by `Capital Structure Series`'''
    source_frame['nominal_patch'] = source_frame.iloc[:, 16]*source_frame.iloc[:, 18]
    '''`Cobb C.W.,  Douglas P.H. -- FRB (Blended) Series` Patched with `Patch Series`'''
    source_frame['nominal_extended'] = source_frame.iloc[:, [17, 19]].mean(1)
    source_frame = source_frame[source_frame.columns[[20]]]
    source_frame.dropna(inplace=True)
    return source_frame


def cobbDouglasCapitalDeflator():
    '''Fixed Assets Deflator,  2009 = 100'''
    base = [84, 177, 216] ##2009,  1970,  2009
    '''Combine L2,  L15,  E7,  E23,  E40,  E68 & P107/P110'''
    '''Bureau of Labor Statistics
    Data Not Used As It Covers Only Years of 1998--2017'''
    '''Results:
    fetchCensus('dataset-usa-census1949.zip', 'L0036', True) Offset with fetchCensus('dataset-usa-census1975.zip', 'E0183', True)
    fetchCensus('dataset-usa-census1949.zip', 'L0038', True) Offset with fetchCensus('dataset-usa-census1975.zip', 'E0184', True)
    fetchCensus('dataset-usa-census1949.zip', 'L0039', True) Offset with fetchCensus('dataset-usa-census1975.zip', 'E0185', True)
    fetchCensus('dataset-usa-census1975.zip', 'E0052', True) Offset With fetchCensus('dataset-usa-census1949.zip', 'L0002', True)'''
    '''Cost-Of-Living Indexes'''
    '''E183: Federal Reserve Bank,  1913 = 100'''
    '''E184: Burgess,  1913 = 100'''
    '''E185: Douglas,  1890-99 = 100'''
    sub_frameA = fetchClassic('dataset-usa-cobb-douglas.zip', 'CDT2S1')
    sub_frameB = fetchClassic('dataset-usa-cobb-douglas.zip', 'CDT2S3')
    sub_frameC = fetchCensus('dataset-usa-census1949.zip', 'L0001', True)
    sub_frameD = fetchCensus('dataset-usa-census1949.zip', 'L0002', True)
    sub_frameE = fetchCensus('dataset-usa-census1949.zip', 'L0015', True)
    sub_frameF = fetchCensus('dataset-usa-census1949.zip', 'L0037', True)
    sub_frameG = fetchCensus('dataset-usa-census1975.zip', 'E0007', True)
    sub_frameH = fetchCensus('dataset-usa-census1975.zip', 'E0008', True)
    sub_frameI = fetchCensus('dataset-usa-census1975.zip', 'E0009', True)
    sub_frameJ = fetchCensus('dataset-usa-census1975.zip', 'E0023', True)
    sub_frameK = fetchCensus('dataset-usa-census1975.zip', 'E0040', True)
    sub_frameL = fetchCensus('dataset-usa-census1975.zip', 'E0068', True)
    sub_frameM = fetchCensus('dataset-usa-census1975.zip', 'E0183', True)
    sub_frameN = fetchCensus('dataset-usa-census1975.zip', 'E0184', True)
    sub_frameO = fetchCensus('dataset-usa-census1975.zip', 'E0185', True)
    sub_frameP = fetchCensus('dataset-usa-census1975.zip', 'E0186', True)
    sub_frameQ = fetchCensus('dataset-usa-census1975.zip', 'P0107', True)
    sub_frameR = fetchCensus('dataset-usa-census1975.zip', 'P0110', True)
    sub_frameS = FRBFADEF()
    sub_frameQ = sub_frameQ[22:]
    sub_frameR = sub_frameR[22:]
    basis_frame = pd.concat([sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, \
                          sub_frameF, sub_frameG, sub_frameH, sub_frameI, sub_frameJ, \
                          sub_frameK, sub_frameL, sub_frameM, sub_frameN, sub_frameO, \
                          sub_frameP, sub_frameQ, sub_frameR, sub_frameS], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, sub_frameF, sub_frameG, \
        sub_frameH, sub_frameI, sub_frameJ, sub_frameK, sub_frameL, sub_frameM, sub_frameN, \
        sub_frameO, sub_frameP, sub_frameQ, sub_frameR, sub_frameS
    basis_frame['fa_def_cd'] = basis_frame.iloc[:, 0].div(basis_frame.iloc[:, 1])
    basis_frame['fa_def_cn'] = basis_frame.iloc[:, 16].div(basis_frame.iloc[:, 17])
    '''Cobb--Douglas'''
    semi_frameA = processing(basis_frame, 19)
    '''Bureau of Economic Analysis'''
    '''Fixed Assets: k1n31gd1es000,  1925--2016,  Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    sub_frameA = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '401 Ann', 1925, 2016, 9)
    '''Fixed Assets: kcn31gd1es000,  1925--2016,  Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    sub_frameB = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '402 Ann', 1925, 2016, 9)
    '''Not Used: Not Used: Fixed Assets: k3n31gd1es000,  1925--2016,  Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    sub_frameC = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '403 Ann', 1925, 2016, 9)
    '''Not Used: Fixed Assets: k3ntotl1si000,  1925--2016,  Table 2.3. Historical-Cost Net Stock of Private Fixed Assets,  Equipment,  Structures,  and Intellectual Property Products by Type'''
    sub_frameD = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '203 Ann', 1925, 2016, 48)
    '''Not Used: mcn31gd1es000,  1925--2016,  Table 4.5. Chain-Type Quantity Indexes for Depreciation of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    sub_frameE = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '405 Ann', 1925, 2016, 9)
    '''Not Used: mcntotl1si000,  1925--2016,  Table 2.5. Chain-Type Quantity Indexes for Depreciation of Private Fixed Assets,  Equipment,  Structures,  and Intellectual Property Products by Type'''
    sub_frameF = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '205 Ann', 1925, 2016, 48)
    '''Real Values'''
    semi_frameB = pd.concat([sub_frameA, sub_frameB], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, sub_frameF
    semi_frameB['ppi_bea'] = 100*semi_frameB.iloc[:, 0].div(semi_frameB.iloc[base[0], 0]*semi_frameB.iloc[:, 1])
    semi_frameB.iloc[:, 2] = processing(semi_frameB, 2)
    semi_frameB = semi_frameB[semi_frameB.columns[[2]]]
    '''Bureau of the Census'''
    '''Correlation Test:
    `kendall_frame = result_frame.corr(method = 'kendall')`
    `pearson_frame = result_frame.corr(method = 'pearson')`
    `spearman_frame = result_frame.corr(method = 'spearman')`
    Correlation Test Result: kendall & pearson & spearman: L2,  L15,  E7,  E23,  E40,  E68'''
    sub_frameA = processing(basis_frame, 3)
    sub_frameB = processing(basis_frame, 4)
    sub_frameC = processing(basis_frame, 6)
    sub_frameD = processing(basis_frame, 9)
    sub_frameE = processing(basis_frame, 10)
    sub_frameF = processing(basis_frame, 11)
    sub_frameG = processing(basis_frame, 20)
    semi_frameC = pd.concat([sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, \
                          sub_frameF, sub_frameG], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD, sub_frameE, sub_frameF, sub_frameG
    semi_frameC['ppi_census_fused'] = semi_frameC.mean(1)
    semi_frameC = semi_frameC[semi_frameC.columns[[7]]]
    '''Federal Reserve'''
    semi_frameD = processing(basis_frame, 18)
    '''Robert C. Sahr,  2007'''
    semi_frameE = fetchINFCF()
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE
    result_frame = result_frame[128:]
    result_frame['def_cum_bea'] = sp.cumprod(1+result_frame.iloc[:, 1])
    result_frame['def_cum_cen'] = sp.cumprod(1+result_frame.iloc[:, 2])
    result_frame['def_cum_frb'] = sp.cumprod(1+result_frame.iloc[:, 3])
    result_frame['def_cum_sah'] = sp.cumprod(1+result_frame.iloc[:, 4])
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(result_frame.iloc[base[1], 5])
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(result_frame.iloc[base[1], 6])
    result_frame.iloc[:, 7] = result_frame.iloc[:, 7].div(result_frame.iloc[base[1], 7])
    result_frame.iloc[:, 8] = result_frame.iloc[:, 8].div(result_frame.iloc[base[1], 8])
    result_frame['def_cum_com'] = result_frame.iloc[:, [5, 6, 7]].mean(1)
    result_frame['fa_def_com'] = processing(result_frame, 9)
    result_frame.iloc[:, 9] = result_frame.iloc[:, 9].div(result_frame.iloc[base[2], 9])
    result_frame = result_frame[result_frame.columns[[9]]]
    result_frame.dropna(inplace=True)
    return result_frame


def cobbDouglasLaborExtension():
    '''Manufacturing Laborers` Series Comparison
    semi_frameA: Cobb C.W.,  Douglas P.H. Labor Series
    semi_frameB: Census Bureau 1949,  D69
    semi_frameC: Census Bureau 1949,  J4
    semi_frameD: Census Bureau 1975,  D130
    semi_frameE: Census Bureau 1975,  P5
    semi_frameF: Census Bureau 1975,  P62
    semi_frameG: Bureau of Economic Analysis,  H4313C & J4313C & A4313C & N4313C
    semi_frameH: J.W. Kendrick,  Productivity Trends in the United States,  Table D-II,  `Persons Engaged` Column,  pp. 465--466
    semi_frameI: Yu.V. Kurenkov
    Bureau of Labor Statistics
    Federal Reserve Board'''
    semi_frameA = fetchClassic('dataset-usa-cobb-douglas.zip', 'CDT3S1') ## Average Number Employed (in thousands)
    semi_frameB = fetchCensus('dataset-usa-dataset-usa-census1949.zip', 'D0069', True)
    semi_frameC = fetchCensus('dataset-usa-dataset-usa-census1949.zip', 'J0004', True)
    semi_frameD = fetchCensus('dataset-usa-census1975.zip', 'D0130', True)
    semi_frameE = fetchCensus('dataset-usa-census1975.zip', 'P0005', True)
    semi_frameF = fetchCensus('dataset-usa-census1975.zip', 'P0062', True)
    sub_frameA = fetchBEA('dataset-usa-bea-NipaDataA.txt', 'H4313C')
    sub_frameB = fetchBEA('dataset-usa-bea-NipaDataA.txt', 'J4313C')
    sub_frameC = fetchBEA('dataset-usa-bea-NipaDataA.txt', 'A4313C')
    sub_frameD = fetchBEA('dataset-usa-bea-NipaDataA.txt', 'N4313C')
    semi_frameG = pd.concat([sub_frameA, sub_frameB, sub_frameC, sub_frameD], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD
    semi_frameG = semi_frameG.mean(1)
    semi_frameG = semi_frameG.to_frame(name = 'BEA')
    semi_frameH = fetchClassic('dataset-usa-kendrick.zip', 'KTD02S02')
    semi_frameI = pd.read_csv('dataset USA Reference RU Kurenkov Yu.V..csv', usecols=[0, 2])
    semi_frameI = semi_frameI.set_index('Period')
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI], axis = 1, sort = True)
    result_frame['kendrick'] = result_frame.iloc[14, 0]*result_frame.iloc[:, 7].div(result_frame.iloc[14, 7])
    result_frame['labor'] = result_frame.iloc[:, [0, 1, 3, 6, 8, 9]].mean(1)
    result_frame = result_frame[result_frame.columns[[10]]]
    result_frame.dropna(inplace=True)
    result_frame = result_frame[2:]
    return result_frame


def cobbDouglasProductExtension():
    base = [109, 149] ##1899,  1939
    '''Bureau of the Census,  1949,  Page 179,  J13: National Bureau of Economic Research Index of Physical Output,  All Manufacturing Industries.'''
    semi_frameA = fetchCensus('dataset-usa-census1949.zip', 'J0013', True)
    '''Bureau of the Census,  1949,  Page 179,  J14: Warren M. Persons,  Index of Physical Production of Manufacturing'''
    semi_frameB = fetchCensus('dataset-usa-census1949.zip', 'J0014', True)
    '''Bureau of the Census,  1975,  Page 667,  P17: Edwin Frickey Index of Manufacturing Production'''
    semi_frameC = fetchCensus('dataset-usa-census1975.zip', 'P0017', True)
    '''The Revised Index of Physical Production for All Manufacturing In the United States,  1899--1926'''
    semi_frameD = fetchClassic('douglas.zip', 'DT24AS01')
    '''Federal Reserve,  AIPMASAIX'''
    semi_frameE = FRBIP()
    '''Joseph H. Davis Production Index'''
    semi_frameF = pd.read_excel('dataset USA Davis J.H. ip-total.xls', skiprows=4)
    semi_frameF.columns = ['Period', 'davis_index']
    semi_frameF = semi_frameF.set_index('Period')
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, semi_frameF], axis = 1, sort = True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].div(result_frame.iloc[base[0], 1]/100)
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(result_frame.iloc[base[0], 5]/100)
    result_frame['fused_classic'] = result_frame.iloc[:, [0, 1, 2, 3, 5]].mean(1)
    result_frame.iloc[:, 4] = result_frame.iloc[:, 4].div(result_frame.iloc[base[1], 4]/100)
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(result_frame.iloc[base[1], 6]/100)
    result_frame['fused'] = result_frame.iloc[:, [4, 6]].mean(1)
    result_frame = result_frame[result_frame.columns[[7]]]
    return result_frame


def datasetVersionA():
    '''Returns  result_frameA: Capital,  Labor,  Product;
                result_frameB: Capital,  Labor,  Product Adjusted to Capacity Utilisation'''
    '''Data Fetch Archived'''
    '''Fixed Assets: kcn31gd1es000,  1925--2016,  Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    semi_frameA = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '402 Ann', 1925, 2016, 9)
    '''Labor'''
    semi_frameB = archivedBEALabor()
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10106 Ann', 1929, 1969, 1)
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10106 Ann', 1969, 2012, 1)
    semi_frameC = sub_frameA.append(sub_frameB).drop_duplicates()
    '''Capacity Utilization Series: CAPUTL.B50001.A,  1967--2012'''
    semi_frameD = FRBCU()
    result_frameA = pd.concat([semi_frameA, semi_frameB, semi_frameC], axis = 1, sort = True).dropna()
    result_frameB = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD], axis = 1, sort = True).dropna()
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD
    result_frameB.iloc[:, 2] = result_frameB.iloc[:, 2].div(result_frameB.iloc[:, 3]/100)
    result_frameB = result_frameB[result_frameB.columns[[0, 1, 2]]]
    result_frameA = result_frameA.div(result_frameA.iloc[0, :])
    result_frameB = result_frameB.div(result_frameB.iloc[0, :])
    return result_frameA, result_frameB


def datasetVersionB():
    '''Returns  result_frameA: Capital,  Labor,  Product;
                result_frameB: Capital,  Labor,  Product;
                result_frameC: Capital,  Labor,  Product Adjusted to Capacity Utilisation'''
    base = 38 ##1967 = 100
    '''Data Fetch Revised'''
    '''Fixed Assets: kcn31gd1es000,  1925--2016,  Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    semi_frameA = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '402 Ann', 1925, 2016, 9)
    '''Labor'''
    semi_frameB = BEALabor()
    '''Manufacturing Series: FRB G17 IP,  AIPMA_SA_IX,  1919--2018'''
    semi_frameC = FRBIP()
    '''Capacity Utilization Series: CAPUTL.B50001.A,  1967--2012'''
    semi_frameD = FRBCU()
    result_frameA = pd.concat([semi_frameA, semi_frameB, semi_frameC], axis = 1, sort = True).dropna()
    result_frameB = result_frameA[base:]
    result_frameC = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD], axis = 1, sort = True).dropna()
    result_frameC.iloc[:, 2] = result_frameC.iloc[:, 2].div(result_frameC.iloc[:, 3]/100)
    result_frameC = result_frameC[result_frameC.columns[[0, 1, 2]]]
    result_frameA = result_frameA.div(result_frameA.iloc[0, :])
    result_frameB = result_frameB.div(result_frameB.iloc[0, :])
    result_frameC = result_frameC.div(result_frameC.iloc[0, :])
    return result_frameA, result_frameB, result_frameC


def datasetVersionC():
    '''Data Fetch'''
    '''Data Fetch for Capital'''
    capital_frameA = cobbDouglasCapitalExtension()
    '''Data Fetch for Capital Deflator'''
    capital_frameB = cobbDouglasCapitalDeflator()
    capital_frame = pd.concat([capital_frameA, capital_frameB], axis = 1, sort = True)
    capital_frame.dropna(inplace=True)
    capital_frame['capital_real'] = capital_frame.iloc[:, 0].div(capital_frame.iloc[:, 1])
    '''Data Fetch for Labor'''
    labor_frame = cobbDouglasLaborExtension()
    '''Data Fetch for Product'''
    product_frame = cobbDouglasProductExtension()
    result_frame = pd.concat([capital_frame.iloc[:, 2], labor_frame, product_frame], axis = 1, sort = True).dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def cd_original(source_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb,  P.H. Douglas. A Theory of Production,  1928;
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Capital, 
    source_frame.iloc[:, 1]: Labor, 
    source_frame.iloc[:, 2]: Product
    '''
    functionDict = {'FigureA':'Chart I Progress in Manufacturing %d$-$%d (%d = 100)', 
                'FigureB':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d = 100)', 
                'FigureC':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average', 
                'FigureD':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d'}
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])
    X = sp.log(X)
    Y = sp.log(Y)
    f1p = sp.polyfit(X, Y, 1)
    a1, a0 = f1p ##Original: a1 = 0.25
    a0 = sp.exp(a0)
    PP = a0*(source_frame.iloc[:, 1]**(1-a1))*(source_frame.iloc[:, 0]**a1)
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
    plt.plot(source_frame.index, PP, label = 'Computed Product,  $P\' = {:, .4f}L^{{{:, .4f}}}C^{{{:, .4f}}}$'.format(a0, 1-a1, a1))
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


def cobbDouglas3D(source_frame):
    '''Cobb--Douglas 3D-Plotting
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Capital, 
    source_frame.iloc[:, 1]: Labor, 
    source_frame.iloc[:, 2]: Product
    '''
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1], source_frame.iloc[:, 2])
    ax.set_xlabel('Capital')
    ax.set_ylabel('Labor')
    ax.set_zlabel('Production')
    plt.show()


def plotLabProdPolynomial(source_frame):
    '''Static Labor Productivity Approximation
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Capital, 
    source_frame.iloc[:, 1]: Labor, 
    source_frame.iloc[:, 2]: Product
    '''
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]) ##Labor Capital Intensity
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]) ##Labor Productivity
    '''Power Function: Labor Productivity'''
    yp1p = sp.polyfit(sp.log(X), sp.log(Y), 1)
    '''Polynomials 1,  2,  3 & 4: Labor Productivity'''
    yl1p = sp.polyfit(X, Y, 1)
    yl2p = sp.polyfit(X, Y, 2)
    yl3p = sp.polyfit(X, Y, 3)
    yl4p = sp.polyfit(X, Y, 4)
    PP = sp.exp(yp1p[1])*X**yp1p[0]
    YAA = yl1p[1]+yl1p[0]*X
    YBB = yl2p[2]+yl2p[1]*X+yl2p[0]*X**2
    YCC = yl3p[3]+yl3p[2]*X+yl3p[1]*X**2+yl3p[0]*X**3
    YDD = yl4p[4]+yl4p[3]*X+yl4p[2]*X**2+yl4p[1]*X**3+yl4p[0]*X**4
    '''Deltas'''
    DPP = sp.absolute((sp.exp(yp1p[1])*X**yp1p[0]-Y).div(Y))
    DYAA = sp.absolute((YAA-Y).div(Y))
    DYBB = sp.absolute((YBB-Y).div(Y))
    DYCC = sp.absolute((YCC-Y).div(Y))
    DYDD = sp.absolute((YDD-Y).div(Y))
    from sklearn.metrics import r2_score
    r20 = r2_score(Y, PP)
    r21 = r2_score(Y, YAA)
    r22 = r2_score(Y, YBB)
    r23 = r2_score(Y, YCC)
    r24 = r2_score(Y, YDD)
    plt.figure(1)
    plt.scatter(source_frame.index, Y, label = 'Labor Productivity')
    plt.plot(source_frame.index, PP, label = '$\\hat Y = {:.2f}X^{{{:.2f}}},  R^2 = {:.4f}$'.format(sp.exp(yp1p[1]), yp1p[0], r20))
    plt.plot(source_frame.index, YAA, label = '$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X,  R^2 = {:.4f}$'.format(1, yl1p[1], yl1p[0], r21))
    plt.plot(source_frame.index, YBB, label = '$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2,  R^2 = {:.4f}$'.format(2, yl2p[2], yl2p[1], yl2p[0], r22))
    plt.plot(source_frame.index, YCC, label = '$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3,  R^2 = {:.4f}$'.format(3, yl3p[3], yl3p[2], yl3p[1], yl3p[0], r23))
    plt.plot(source_frame.index, YDD, label = '$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3 {:.2f}X^4,  R^2 = {:.4f}$'.format(4, yl4p[4], yl4p[3], yl4p[2], yl4p[1], yl4p[0], r24))
    plt.title('Labor Capital Intensity & Labor Productivity,  {}$-${}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame.index, DPP, ':', label = '$\\|\\frac{{\\hat Y-Y}}{{Y}}\\|,  \\bar S = {:.4%}$'.format(DPP.mean()))
    plt.plot(source_frame.index, DYAA, ':', label = '$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|,  \\bar S = {:.4%}$'.format(1, DYAA.mean()))
    plt.plot(source_frame.index, DYBB, ':', label = '$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|,  \\bar S = {:.4%}$'.format(2, DYBB.mean()))
    plt.plot(source_frame.index, DYCC, ':', label = '$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|,  \\bar S = {:.4%}$'.format(3, DYCC.mean()))
    plt.plot(source_frame.index, DYDD, ':', label = '$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|,  \\bar S = {:.4%}$'.format(4, DYDD.mean()))
    plt.title('Deltas of Labor Capital Intensity & Labor Productivity,  {}$-${}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotSimpleLinear(source_frame, coef1, coef2, E):
    '''
    Labor Productivity on Labor Capital Intensity Plot;
    Predicted Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1], label = 'Original')
    plt.title('$Labor\ Capital\ Intensity$,  $Labor\ Productivity$ Relation,  {}$-${}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame.index, E, label = '$\\frac{Y}{Y_{0}} = %f\\frac{L}{L_{0}}+%f\\frac{K}{K_{0}}$' %(coef1, coef2))
    plt.title('Model: $\\hat Y = {:.4f}+{:.4f}\\times X$,  {}$-${}'.format(coef1, coef2, source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('$\\hat Y = Labor\ Productivity$,  $X = Labor\ Capital\ Intensity$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotSimpleLog(source_frame, coef1, coef2, E):
    '''
    Log Labor Productivity on Log Labor Capital Intensity Plot;
    Predicted Log Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1], label = 'Logarithm')
    plt.title('$\\ln(Labor\ Capital\ Intensity),  \\ln(Labor\ Productivity)$ Relation,  {}$-${}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('$\\ln(Labor\ Capital\ Intensity)$')
    plt.ylabel('$\\ln(Labor\ Productivity)$')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(source_frame.index, E, label = '$\\ln(\\frac{Y}{Y_{0}}) = %f+%f\\ln(\\frac{K}{K_{0}})+%f\\ln(\\frac{L}{L_{0}})$' %(coef1, coef2, 1-coef2))
    plt.title('Model: $\\ln(\\hat Y) = {:.4f}+{:.4f}\\times \\ln(X)$,  {}$-${}'.format(coef1, coef2, source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('$\\hat Y = \\ln(Labor\ Productivity)$,  $X = \\ln(Labor\ Capital\ Intensity)$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotTurnover(source_frame):
    '''Static Fixed Assets Turnover Approximation
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Capital, 
    source_frame.iloc[:, 2]: Product
    '''
    K = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]) ##Fixed Assets Turnover
    '''Linear: Fixed Assets Turnover'''
    kl1p = sp.polyfit(source_frame.iloc[:, 0], K, 1)
    '''Exponential: Fixed Assets Turnover'''
    ke1p = sp.polyfit(source_frame.iloc[:, 0], sp.log(K), 1)
    K1 = kl1p[1]+kl1p[0]*source_frame.iloc[:, 0]
    K2 = sp.exp(ke1p[1]+ke1p[0]*source_frame.iloc[:, 0])
    '''Deltas'''
    DK1 = sp.absolute((K1-K).div(K))
    DK2 = sp.absolute((K2-K).div(K))
    from sklearn.metrics import r2_score
    r21 = r2_score(K, K1)
    r22 = r2_score(K, K2)
    plt.figure(1)
    plt.plot(source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]), source_frame.iloc[:, 1])
    plt.title('Fixed Assets Volume to Fixed Assets Turnover,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Fixed Assets Turnover')
    plt.ylabel('Fixed Assets Volume')
    plt.grid(True)
    plt.figure(2)
    plt.scatter(source_frame.iloc[:, 0], K, label = 'Fixed Assets Turnover')
    plt.plot(source_frame.iloc[:, 0], K1, label = '$\\hat K_{{l}} = {:.2f} {:.2f} t,  R^2 = {:.4f}$'.format(kl1p[1], kl1p[0], r21))
    plt.plot(source_frame.iloc[:, 0], K2, label = '$\\hat K_{{e}} = \\exp ({:.2f} {:.2f} t),  R^2 = {:.4f}$'.format(ke1p[1], ke1p[0], r22))
    plt.title('Fixed Assets Turnover Approximation,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 0], DK1, ':', label = '$\\|\\frac{{\\hat K_{{l}}-K}}{{K}}\\|,  \\bar S = {:.4%}$'.format(DK1.mean()))
    plt.plot(source_frame.iloc[:, 0], DK2, ':', label = '$\\|\\frac{{\\hat K_{{e}}-K}}{{K}}\\|,  \\bar S = {:.4%}$'.format(DK2.mean()))
    plt.title('Deltas of Fixed Assets Turnover Approximation,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotBlockZero(source_frame):
    '''
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Capital, 
    source_frame.iloc[:, 1]: Labor, 
    source_frame.iloc[:, 2]: Product
    '''
    pd.options.mode.chained_assignment = None
    source_frame['lab_cap_int'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]) ## Labor Capital Intensity
    source_frame['lab_product'] = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]) ## Labor Productivity
    source_frame['log_lab_c'] = sp.log(source_frame.iloc[:, 0].div(source_frame.iloc[:, 1]))
    source_frame['log_lab_p'] = sp.log(source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]))
    result_frameA = source_frame[source_frame.columns[[3, 4]]]
    result_frameB = source_frame[source_frame.columns[[5, 6]]]
    A0, A1, EA = simpleLinearRegression(result_frameA)
    plotSimpleLinear(result_frameA, A0, A1, EA)
    B0, B1, EB = simpleLinearRegression(result_frameB)
    plotSimpleLog(result_frameB, B0, B1, EB)


def plotBlockOne(source_frame):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Capital, 
    source_frame.iloc[:, 2]: Labor, 
    source_frame.iloc[:, 3]: Product
    '''
    source_frame['lab_cap_int'] = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]) ##Labor Capital Intensity
    labcap_frame = source_frame[source_frame.columns[[0, 4]]]
    semi_frameA, semi_frameB = RMF(labcap_frame)
    semi_frameC, semi_frameD = KZF(labcap_frame)
    semi_frameE = SES(labcap_frame, 5, 0.25)
    semi_frameE = semi_frameE.iloc[:, 1]
    odd_frame = pd.concat([semi_frameA, semi_frameE], axis = 1, sort = True)
    even_frame = pd.concat([semi_frameB, semi_frameD], axis = 1, sort = True)
    plt.figure()
    odd_frame.iloc[:, 0].plot(linewidth = 3, label = 'Labor Capital Intensity')
    odd_frame.iloc[:, 1].plot(label = 'Single Exponential Smoothing,  Window = {},  Alpha = {:, .2f}'.format(5, 0.25))
    even_frame.iloc[:, 0].plot(label = 'Rolling Mean,  {}'.format(2))
    even_frame.iloc[:, 1].plot(label = 'Kolmogorov--Zurbenko Filter,  {}'.format(2))
    plt.title('Labor Capital Intensity: Rolling Mean Filter,  Kolmogorov--Zurbenko Filter &\n\
              Single Exponential Smoothing')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def plotBlockTwo(source_frame):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Capital, 
    source_frame.iloc[:, 2]: Labor, 
    source_frame.iloc[:, 3]: Product
    '''
    source_frame['lab_product'] = source_frame.iloc[:, 3].div(source_frame.iloc[:, 2]) ##Labor Productivity
    labpro_frame = source_frame[source_frame.columns[[0, 4]]]
    semi_frameA, semi_frameB = RMF(labpro_frame, 3)
    semi_frameC, semi_frameD = KZF(labpro_frame, 3)
    semi_frameC = semi_frameC.iloc[:, 1]
    semi_frameE = SES(labpro_frame, 5, 0.25)
    semi_frameE = semi_frameE.iloc[:, 1]
    semi_frameF = SES(labpro_frame, 5, 0.35)
    semi_frameF = semi_frameF.iloc[:, 1]
    semi_frameG = SES(labpro_frame, 5, 0.45)
    semi_frameG = semi_frameG.iloc[:, 1]
    odd_frame = pd.concat([semi_frameA, semi_frameC, semi_frameE, semi_frameF, semi_frameG], axis = 1, sort = True)
    even_frame = pd.concat([semi_frameB, semi_frameD], axis = 1, sort = True)
    plt.figure()
    odd_frame.iloc[:, 0].plot(linewidth = 3, label = 'Labor Productivity')
    odd_frame.iloc[:, 1].plot(label = 'Rolling Mean,  {}'.format(3))
    odd_frame.iloc[:, 2].plot(label = 'Kolmogorov--Zurbenko Filter,  {}'.format(3))
    odd_frame.iloc[:, 3].plot(label = 'Single Exponential Smoothing,  Window = {},  Alpha = {:, .2f}'.format(5, 0.25))
    odd_frame.iloc[:, 4].plot(label = 'Single Exponential Smoothing,  Window = {},  Alpha = {:, .2f}'.format(5, 0.35))
    odd_frame.iloc[:, 5].plot(label = 'Single Exponential Smoothing,  Window = {},  Alpha = {:, .2f}'.format(5, 0.45))
    even_frame.iloc[:, 0].plot(label = 'Rolling Mean,  {}'.format(2))
    even_frame.iloc[:, 1].plot(label = 'Rolling Mean,  {}'.format(4))
    even_frame.iloc[:, 2].plot(label = 'Kolmogorov--Zurbenko Filter,  {}'.format(2))
    even_frame.iloc[:, 3].plot(label = 'Kolmogorov--Zurbenko Filter,  {}'.format(4))
    plt.title('Labor Capital Intensity: Rolling Mean Filter,  Kolmogorov--Zurbenko Filter &\n\
              Single Exponential Smoothing')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def simpleLinearRegression(source_frame):
    '''Determining of Coefficients of Regression
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Regressor, 
    source_frame.iloc[:, 1]: Regressand
    '''
    '''Summarize'''
    S1 = sum(source_frame.iloc[:, 0])
    S2 = sum(source_frame.iloc[:, 1])
    S3 = sum((source_frame.iloc[:, 0])**2)
    S4 = sum(source_frame.iloc[:, 0]*source_frame.iloc[:, 1])
    '''Approximation'''
    A0 = (S2*S3-S1*S4)/(len(source_frame)*S3-S1**2)
    A1 = (len(source_frame)*S4-S1*S2)/(len(source_frame)*S3-S1**2)
    E = A0+A1*(source_frame.iloc[:, 0])
    MY = sp.mean(source_frame.iloc[:, 1])
    ESS = sum((source_frame.iloc[:, 1]-A0-A1*source_frame.iloc[:, 0])**2)
    TSS = sum((source_frame.iloc[:, 1]-MY)**2)
    R2 = 1-ESS/TSS
    '''Delivery Block'''
    print('Period From {} Through {}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    print('Model: Yhat = {:, .4f}+{:, .4f}*X'.format(A0, A1))
    print('Model Parameter: A0 = {:, .4f}'.format(A0))
    print('Model Parameter: A1 = {:, .4f}'.format(A1))
    print('Model Result: ESS = {:, .4f}; TSS = {:, .4f}; R**2 = {:, .4f}'.format(ESS, TSS, R2))
    return A0, A1, E


def complexCobbDouglas(source_frame):
    modified_frameA = indexswitch(source_frame)
    modified_frameB = source_frame[source_frame.columns[[0, 2]]]
    modified_frameB = indexswitch(modified_frameB)
    cd_original(source_frame)
    cobbDouglas3D(source_frame)
    plotLabProdPolynomial(source_frame)
    plotBlockZero(source_frame)
    plotBlockOne(modified_frameA)
    plotBlockTwo(modified_frameA)
    plotTurnover(modified_frameB)
    del source_frame
    del modified_frameA
    del modified_frameB


'''On Original Dataset'''
source_frame = cobbDouglasPreprocessing()
result_frameA = source_frame[source_frame.columns[[0, 1, 2]]]
result_frameB = source_frame[source_frame.columns[[0, 1, 3]]]
result_frameC = source_frame[source_frame.columns[[0, 1, 4]]]
'''On Expanded Dataset'''
result_frameD, result_frameE = datasetVersionA()
result_frameF, result_frameG, result_frameH = datasetVersionB()
result_frameI = datasetVersionC()
complexCobbDouglas(result_frameA)
complexCobbDouglas(result_frameB)
complexCobbDouglas(result_frameC)
'''No Capacity Utilization Adjustment'''
complexCobbDouglas(result_frameD)
'''Capacity Utilization Adjustment'''
complexCobbDouglas(result_frameE)
'''Option: 1929--2013,  No Capacity Utilization Adjustment'''
complexCobbDouglas(result_frameF)
'''Option: 1967--2013,  No Capacity Utilization Adjustment'''
complexCobbDouglas(result_frameG)
'''Option: 1967--2012,  Capacity Utilization Adjustment'''
complexCobbDouglas(result_frameH)
complexCobbDouglas(result_frameI)