# -*- coding: utf-8 -*-
'''
Created on Tue Mar 10 22:29:22 2020

Thesis Project

@author: Alexander Mikhailov
'''
import os
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
import scipy.special
from mpl_toolkits.mplot3d import Axes3D
from pandas.plotting import autocorrelation_plot
from pandas.plotting import bootstrap_plot
from pandas.plotting import lag_plot
from scipy import signal
from scipy import stats
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


def base_dict(source):
    '''Returns Dictionary for Series from Douglas's & Kendrick's Databases'''
    series_dict = pd.read_csv(source, usecols=range(3, 5))
    series_dict = series_dict.drop_duplicates()
    series_dict = series_dict[series_dict.columns[[1, 0]]]
    series_dict = series_dict.sort_values('vector')
    series_dict = series_dict.reset_index(drop = True)
    return series_dict


def beaFetch(source, wrkbk, wrksht, start, finish, line):
    '''Data _frame Fetching from Bureau of Economic Analysis Zip Archives'''
    '''
    source: Name of Zip Archive, 
    wrkbk: Name of Excel File within Zip Archive, 
    wrksht: Name of Worksheet within Excel File within Zip Archive, 
    boundary: 4+<Period_Finish>-<Period_Start>, 
    line: Line'''
    boundary = 4-start+finish
    if source == None:
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
    '''`dataset USA BEA NipaDataA.txt`: U.S. Bureau of Economic Analysis
    Archived: https://www.bea.gov/National/FAweb/Details/Index.html
    https://www.bea.gov//national/FA2004/DownSS2.asp,  Accessed May 26,  2018'''
    if source == 'beanipa20131202.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source == 'beanipa20150302section5.zip': ##Not Used
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source == 'beanipa20150501.zip':
        source_frame = pd.read_csv(source, usecols=range(14, 18))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
        source_frame = source_frame[source_frame.iloc[:, 2] == 0]
        source_frame = source_frame[source_frame.columns[[0, 1, 3]]]
    elif source == 'dataset USA BEA NipaDataA.txt':
        source_frame = pd.read_csv(source, thousands = ', ')
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source == 'beanipa20131202sfat.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    elif source == 'beanipa20170823sfat.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11))
        source_frame.columns = source_frame.columns.str.title()
        source_frame.rename(columns = {'Value':string}, inplace=True)
    else:
        pass
    result_frame = source_frame[source_frame.iloc[:, 0] == string]
    del source_frame
    result_frame = result_frame[result_frame.columns[[1, 2]]]
    result_frame = result_frame.reset_index(drop = True)
    result_frame = result_frame.set_index('Period')
    result_frame.to_csv('temporary.txt')
    del result_frame
    result_frame = pd.read_csv('temporary.txt')
    os.unlink('temporary.txt')
    result_frame = result_frame.set_index('Period')
    if source == 'beanipa20170823sfat.zip':
        result_frame = result_frame.round(3)
    else:
        pass
    result_frame = result_frame.drop_duplicates()
    return result_frame


def fetchCANSIM(source, vector, index):
    '''Data _frame Fetching from CANSIM Zip Archives
    Should Be [x 7 columns]
    index == True -- indexed by `Period`;
    index == False -- not indexed by `Period`'''
    source_frame = pd.read_csv('dataset CAN {}-eng.zip'.format(source))
    source_frame = source_frame[source_frame.Vector == vector]
    if source == '03800106':
        source_frame = source_frame[source_frame.columns[[0, 5]]]
    elif source == '03800566':
        source_frame = source_frame[source_frame.columns[[0, 5]]]
    elif source == '02820011':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '02820012':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03790031':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03800068':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    else:
        source_frame = source_frame[source_frame.columns[[0, 6]]] ##Should Be [x 7 columns]
    source_frame.rename(columns = {'Ref_Date':'Period', 'Value':vector}, inplace=True)
    source_frame.iloc[:, 1] = pd.to_numeric(source_frame.iloc[:, 1])
    source_frame.to_csv('dataset CAN {} {}.csv'.format(source, vector), index = False)
    if index:
        source_frame = source_frame.set_index('Period')
        os.unlink('dataset CAN {} {}.csv'.format(source, vector))
        return source_frame
    else:
        del source_frame
        result_frame = pd.read_csv('dataset CAN {} {}.csv'.format(source, vector))
        os.unlink('dataset CAN {} {}.csv'.format(source, vector))
        return result_frame


def fetchCANSIMFA(sequence):
    '''Fetch `Series Sequence` from CANSIM Table 031-0004: Flows and stocks of fixed non-residential capital,  total all industries,  by asset,  provinces\
    and territories,  annual (dollars x 1, 000, 000)'''
    source_frame = pd.read_csv('dataset CAN 00310004-eng.zip')
    source_frame = source_frame.loc[source_frame['Vector'].isin(sequence)]
    source_frame = source_frame[source_frame.iloc[:, 8]! = '..']
    source_frame = source_frame[source_frame.columns[[6, 0, 8]]]
    tables = source_frame.iloc[:, 0].unique()
    tables = pd.Series(tables)
    i = 0 ##Counter
    for table in tables:
        current_frame = source_frame[source_frame.iloc[:, 0] == table]
        current_frame = current_frame[current_frame.columns[[1, 2]]]
        current_frame.iloc[:, 1] = current_frame.iloc[:, 1].astype(float)
        current_frame.rename(columns = {'Ref_Date':'Period', 'Value':table}, inplace=True)
        current_frame = current_frame.drop_duplicates()
        current_frame = current_frame.reset_index(drop = True)
        current_frame = current_frame.set_index('Period')
        if i == 0:
            result_frame = current_frame
        elif i> = 1:
            result_frame = pd.concat([current_frame, result_frame], axis = 1, sort = True)
        del current_frame
        i+ = 1
    result_frame = result_frame.sum(axis = 1)
    return result_frame


def fetchCANSIMQ(source, vector, index):
    '''Data _frame Fetching from Quarterly Data within CANSIM Zip Archives
    Should Be [x 7 columns]
    index == True -- indexed by `Period`;
    index == False -- not indexed by `Period`'''
    source_frame = pd.read_csv('dataset CAN {}-eng.zip'.format(source))
    source_frame = source_frame[source_frame.Vector == vector]
    if source == '02820011':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '02820012':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03790031':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    elif source == '03800068':
        source_frame = source_frame[source_frame.columns[[0, 7]]]
    else:
        source_frame = source_frame[source_frame.columns[[0, 6]]] ##Should Be [x 7 columns]
    source_frame.rename(columns = {'Value':vector}, inplace=True)
    source_frame['Period'], source_frame['Q'] = source_frame.iloc[:, 0].str.split('/').str
    source_frame = source_frame[source_frame.columns[[2, 1]]]
    source_frame.iloc[:, 0] = source_frame.iloc[:, 0].astype(int)
    source_frame.iloc[:, 1] = pd.to_numeric(source_frame.iloc[:, 1])
    if (source == '03800084' and vector == 'v62306938'):
        source_frame = source_frame.groupby('Period').sum()
    elif (source == '03790031' and vector == 'v65201536'):
        source_frame = source_frame.groupby('Period').mean()
    elif (source == '03790031' and vector == 'v65201809'):
        source_frame = source_frame.groupby('Period').sum()
    else:
        source_frame = source_frame.groupby('Period').mean()
    if index:
        return source_frame
    else:
        source_frame.to_csv('temporary.txt')
        del source_frame
        result_frame = pd.read_csv('temporary.txt')
        os.unlink('temporary.txt')
        return result_frame


def fetchCANSIMSeries():
    '''Fetch `Series Sequence` from CANSIM Table 031-0004: Flows and stocks of fixed non-residential capital,  total all industries,  by asset, \
    provinces and territories,  annual (dollars x 1, 000, 000)'''
    source_frame = pd.read_csv('dataset CAN 00310004-eng.zip')
    source_frame = source_frame[source_frame.iloc[:, 2].str.contains('2007 constant prices')]
    source_frame = source_frame[source_frame.iloc[:, 4] == 'Geometric (infinite) end-year net stock']
    source_frame = source_frame[source_frame.iloc[:, 5].str.contains('Industrial')]
    source_frame = source_frame[source_frame.columns[[6]]]
    source_frame = source_frame.drop_duplicates()
    slist = source_frame.iloc[:, 0].values.tolist()
    return slist


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


def fetchCensusDescription(source, string):
    '''Retrieve Series Description U.S. Bureau of the Census'''
    source_frame = pd.read_csv(source, usecols=[0, 1, 3, 4, 5, 6, 8], low_memory = False)
    source_frame = source_frame[source_frame.iloc[:, 6] == string]
    source_frame.drop_duplicates(inplace=True)
    if source_frame.iloc[0, 2] == 'no_details':
        if source_frame.iloc[0, 5] == 'no_details':
            if source_frame.iloc[0, 4] == 'no_details':
                description = '{}'.format(source_frame.iloc[0, 3])
            else:
                description = '{} -\n{}'.format(source_frame.iloc[0, 3], source_frame.iloc[0, 4])
        else:
            description = '{} -\n{} -\n{}'.format(source_frame.iloc[0, 3], source_frame.iloc[0, 4], source_frame.iloc[0, 5])
    else:
        if source_frame.iloc[0, 5] == 'no_details':
            if source_frame.iloc[0, 4] == 'no_details':
                description = '{}; {}'.format(source_frame.iloc[0, 3], source_frame.iloc[0, 2])
            else:
                description = '{} -\n{}; {}'.format(source_frame.iloc[0, 3], source_frame.iloc[0, 4], source_frame.iloc[0, 2])
        else:
            description = '{} -\n{} -\n{}; {}'.format(source_frame.iloc[0, 3], source_frame.iloc[0, 4], source_frame.iloc[0, 5], source_frame.iloc[0, 2])
    return description


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


def fetchMCB(string, index):
    '''Data _frame Fetching from McConnell C.R. & Brue S.L.'''
    source_frame = pd.read_csv('mcConnellBrue.zip', usecols=range(1, 4))
    source_frame = source_frame[source_frame.iloc[:, 0] == string]
    source_frame = source_frame[source_frame.columns[[1, 2]]]
    source_frame.columns = source_frame.columns.str.title()
    source_frame = source_frame.sort_values('Period')
    source_frame = source_frame.reset_index(drop = True)
    if index:
        source_frame = source_frame.set_index('Period')
        return source_frame
    else:
        source_frame.to_csv('temporary.txt', index = False)
        del source_frame
        result_frame = pd.read_csv('temporary.txt')
        os.unlink('temporary.txt')
        return result_frame


def indexswitch(source_frame):
    source_frame.to_csv('temporary.txt')
    del source_frame
    result_frame = pd.read_csv('temporary.txt')
    os.unlink('temporary.txt')
    return result_frame


def savezip(result_frame, string):
    import zipfile
    result_frame.to_csv('{}.csv'.format(string), index = False, encoding = 'utf-8')
    del result_frame
    archive = zipfile.ZipFile('{}.zip'.format(string), 'w')
    archive.write('{}.csv'.format(string), compress_type = zipfile.ZIP_DEFLATED)
    archive.close()
    os.unlink('{}.csv'.format(string))
    del archive


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


def archivedDataCombined():
    '''Version: 02 December 2013'''
    '''Nominal Investment Series: A006RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1968, 7)
    '''Nominal Investment Series: A006RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 7)
    semi_frameA = sub_frameA.append(sub_frameB)
    del sub_frameA, sub_frameB
    '''Implicit Price Deflator Series: A006RD3,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10109 Ann', 1929, 1969, 7)
    '''Implicit Price Deflator Series: A006RD3,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10109 Ann', 1969, 2012, 7)
    semi_frameB = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Gross private domestic investment -- Nonresidential: A008RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 9)
    '''Gross private domestic investment -- Nonresidential: A008RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 9)
    semi_frameC = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD3,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10109 Ann', 1929, 1969, 9)
    '''Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD3,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10109 Ann', 1969, 2012, 9)
    semi_frameD = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Nominal National income Series: A032RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10705 Ann', 1929, 1969, 16)
    '''Nominal National income Series: A032RC1,  1969--2011'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10705 Ann', 1969, 2011, 16)
    semi_frameE = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Gross Domestic Product,  2005 = 100: B191RA3,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10103 Ann', 1929, 1969, 1)
    '''Gross Domestic Product,  2005 = 100: B191RA3,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10103 Ann', 1969, 2012, 1)
    semi_frameF = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Nominal Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 1)
    '''Nominal Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 1)
    semi_frameG = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10106 Ann', 1929, 1969, 1)
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10106 Ann', 1969, 2012, 1)
    semi_frameH = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Labor Series'''
    semi_frameI = archivedBEALabor()
    '''Gross Domestic Investment,  W170RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50100 Ann', 1929, 1968, 22)
    '''Gross Domestic Investment,  W170RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50100 Ann', 1969, 2012, 22)
    semi_frameJ = sub_frameA.append(sub_frameB)
    del sub_frameA, sub_frameB
    '''Gross Domestic Investment,  W170RX1,  1967--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50206 Ann', 1967, 1969, 1)
    '''Gross Domestic Investment,  W170RX1,  1969--2011'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50206 Ann', 1969, 2011, 1)
    semi_frameK = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''`K160491` Replaced with `K10070` in `dataCombined()`'''
    '''Fixed Assets Series: K160491,  1951--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50900 Ann', 1951, 1969, 49)
    '''Fixed Assets Series: K160491,  1969--2011'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50900 Ann', 1969, 2011, 49)
    semi_frameL = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Investment in Fixed Assets and Consumer Durable Goods,  Private,  i3ptotl1es000,  1901--2011'''
    semi_frameM = beaFetch('dataset USA BEA SFAT Release 2012-08-15 SectionAll_xls.zip', 'Section1ALL_xls.xls', '105 Ann', 1901, 2011, 3)
    '''Chain-Type Quantity Indexes for Investment in Fixed Assets and Consumer Durable Goods,  Private,  icptotl1es000,  1901--2011'''
    semi_frameN = beaFetch('dataset USA BEA SFAT Release 2012-08-15 SectionAll_xls.zip', 'Section1ALL_xls.xls', '106 Ann', 1901, 2011, 3)
    '''Current-Cost Net Stock of Fixed Assets and Consumer Durable Goods,  Private,  k1ptotl1es000,  1925--2011'''
    semi_frameO = beaFetch('dataset USA BEA SFAT Release 2012-08-15 SectionAll_xls.zip', 'Section1ALL_xls.xls', '101 Ann', 1925, 2011, 3)
    '''Historical-Cost Net Stock of Private Fixed Assets,  Equipment and Software,  and Structures by Type,  Private fixed assets,  k3ptotl1es000,  1925--2011'''
    semi_frameP = beaFetch('dataset USA BEA SFAT Release 2012-08-15 SectionAll_xls.zip', 'Section2ALL_xls.xls', '203 Ann', 1925, 2011, 1)
    '''Chain-Type Quantity Indexes for Net Stock of Private Fixed Assets,  Equipment and Software,  and Structures by Type,  Private fixed assets,  kcptotl1es000,  1925--2011'''
    semi_frameQ = beaFetch('dataset USA BEA SFAT Release 2012-08-15 SectionAll_xls.zip', 'Section2ALL_xls.xls', '202 Ann', 1925, 2011, 1)
    semi_frameR = pd.read_csv('dataset USA 0022M1.txt')
    semi_frameR.columns = semi_frameR.columns.str.title()
    semi_frameR = semi_frameR.set_index('Period')
    semi_frameS = fetchCensus('census1975.zip', 'X0414', True)
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


def archivedSet():
    base = 54 ##Year 2005
    semi_frameA = BLSCPIU()
    semi_frameA = semi_frameA.set_index('Period')
    '''Nominal Investment Series: A006RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1968, 7)
    '''Nominal Investment Series: A006RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 7)
    semi_frameB = sub_frameA.append(sub_frameB)
    del sub_frameA, sub_frameB
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10106 Ann', 1929, 1969, 1)
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10106 Ann', 1969, 2012, 1)
    semi_frameC = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''`K160491` Replaced with `K10070` in `dataCombined()`'''
    '''Fixed Assets Series: K160491,  1951--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50900 Ann', 1951, 1969, 49)
    '''Fixed Assets Series: K160491,  1969--2011'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50900 Ann', 1969, 2011, 49)
    semi_frameD = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    source_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD], axis = 1, sort = True).dropna()
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD
    '''Deflator,  2005 = 100'''
    source_frame['def'] = sp.cumprod(1+source_frame.iloc[:, 0])
    source_frame.iloc[:, 4] = source_frame.iloc[:, 4].rdiv(source_frame.iloc[base, 4])
    '''Investment,  2005 = 100'''
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 4]
    '''Capital,  2005 = 100'''
    source_frame['cap'] = source_frame.iloc[:, 3]*source_frame.iloc[:, 4]
    '''Capital Retirement Ratio'''
    source_frame['rto'] = 1+(1*source_frame.iloc[:, 5]-source_frame.iloc[:, 6].shift(-1)).div(source_frame.iloc[:, 6])
    result_frameA = source_frame[source_frame.columns[[5, 2, 6, 7]]]
    result_frameB = source_frame[source_frame.columns[[7]]]
    result_frameA = indexswitch(result_frameA).dropna()
    result_frameB = indexswitch(result_frameB).dropna()
    return result_frameA, result_frameB, base


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


def BLSCPIU():
    '''BLS CPI-U Price Index Fetch'''
    source_frame = pd.read_csv('dataset USA BLS cpiai.txt', sep = '\s+', skiprows=16)
    psm = source_frame.iloc[:, 1:13].mean(1) #source_frame.loc[:, 'Jan.':'Dec.']
    prt = source_frame.iloc[:, 1:13].prod(1)
    prt = prt**(1/12)
    result_frame = pd.concat([source_frame.iloc[:, 0], psm, prt], axis = 1, sort = True)
    result_frame.columns = ['Period', 'mean', 'sqroot']
    result_frame['mean_less_sqroot'] = result_frame.iloc[:, 1]-result_frame.iloc[:, 2]
    result_frame['dec_on_dec'] = (source_frame.iloc[:, 12]-source_frame.iloc[:, 12].shift(1)).div(source_frame.iloc[:, 12].shift(1))
    result_frame['mean_on_mean'] = (result_frame.iloc[:, 1]-result_frame.iloc[:, 1].shift(1)).div(result_frame.iloc[:, 1].shift(1))
    result_frame = result_frame[result_frame.columns[[0, 5]]]
    result_frame = result_frame.dropna()
    result_frame.to_csv('temporary.txt', index = False)
    del result_frame
    result_frame = pd.read_csv('temporary.txt')
    os.unlink('temporary.txt')
    return result_frame


def cobbDouglasCapitalDeflator():
    '''Fixed Assets Deflator,  2009 = 100'''
    base = [84, 177, 216] ##2009,  1970,  2009
    '''Combine L2,  L15,  E7,  E23,  E40,  E68 & P107/P110'''
    '''Bureau of Labor Statistics
    Data Not Used As It Covers Only Years of 1998--2017'''
    '''Results:
    fetchCensus('census1949.zip', 'L0036', True) Offset with fetchCensus('census1975.zip', 'E0183', True)
    fetchCensus('census1949.zip', 'L0038', True) Offset with fetchCensus('census1975.zip', 'E0184', True)
    fetchCensus('census1949.zip', 'L0039', True) Offset with fetchCensus('census1975.zip', 'E0185', True)
    fetchCensus('census1975.zip', 'E0052', True) Offset With fetchCensus('census1949.zip', 'L0002', True)'''
    '''Cost-Of-Living Indexes'''
    '''E183: Federal Reserve Bank,  1913 = 100'''
    '''E184: Burgess,  1913 = 100'''
    '''E185: Douglas,  1890-99 = 100'''
    sub_frameA = fetchClassic('cobbdouglas.zip', 'CDT2S1')
    sub_frameB = fetchClassic('cobbdouglas.zip', 'CDT2S3')
    sub_frameC = fetchCensus('census1949.zip', 'L0001', True)
    sub_frameD = fetchCensus('census1949.zip', 'L0002', True)
    sub_frameE = fetchCensus('census1949.zip', 'L0015', True)
    sub_frameF = fetchCensus('census1949.zip', 'L0037', True)
    sub_frameG = fetchCensus('census1975.zip', 'E0007', True)
    sub_frameH = fetchCensus('census1975.zip', 'E0008', True)
    sub_frameI = fetchCensus('census1975.zip', 'E0009', True)
    sub_frameJ = fetchCensus('census1975.zip', 'E0023', True)
    sub_frameK = fetchCensus('census1975.zip', 'E0040', True)
    sub_frameL = fetchCensus('census1975.zip', 'E0068', True)
    sub_frameM = fetchCensus('census1975.zip', 'E0183', True)
    sub_frameN = fetchCensus('census1975.zip', 'E0184', True)
    sub_frameO = fetchCensus('census1975.zip', 'E0185', True)
    sub_frameP = fetchCensus('census1975.zip', 'E0186', True)
    sub_frameQ = fetchCensus('census1975.zip', 'P0107', True)
    sub_frameR = fetchCensus('census1975.zip', 'P0110', True)
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
    semi_frameA = fetchClassic('cobbdouglas.zip', 'CDT3S1') ## Average Number Employed (in thousands)
    semi_frameB = fetchCensus('census1949.zip', 'D0069', True)
    semi_frameC = fetchCensus('census1949.zip', 'J0004', True)
    semi_frameD = fetchCensus('census1975.zip', 'D0130', True)
    semi_frameE = fetchCensus('census1975.zip', 'P0005', True)
    semi_frameF = fetchCensus('census1975.zip', 'P0062', True)
    sub_frameA = fetchBEA('dataset USA BEA NipaDataA.txt', 'H4313C')
    sub_frameB = fetchBEA('dataset USA BEA NipaDataA.txt', 'J4313C')
    sub_frameC = fetchBEA('dataset USA BEA NipaDataA.txt', 'A4313C')
    sub_frameD = fetchBEA('dataset USA BEA NipaDataA.txt', 'N4313C')
    semi_frameG = pd.concat([sub_frameA, sub_frameB, sub_frameC, sub_frameD], axis = 1, sort = True)
    del sub_frameA, sub_frameB, sub_frameC, sub_frameD
    semi_frameG = semi_frameG.mean(1)
    semi_frameG = semi_frameG.to_frame(name = 'BEA')
    semi_frameH = fetchClassic('kendrick.zip', 'KTD02S02')
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


def cobbDouglasProductExtension():
    base = [109, 149] ##1899,  1939
    '''Bureau of the Census,  1949,  Page 179,  J13: National Bureau of Economic Research Index of Physical Output,  All Manufacturing Industries.'''
    semi_frameA = fetchCensus('census1949.zip', 'J0013', True)
    '''Bureau of the Census,  1949,  Page 179,  J14: Warren M. Persons,  Index of Physical Production of Manufacturing'''
    semi_frameB = fetchCensus('census1949.zip', 'J0014', True)
    '''Bureau of the Census,  1975,  Page 667,  P17: Edwin Frickey Index of Manufacturing Production'''
    semi_frameC = fetchCensus('census1975.zip', 'P0017', True)
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


def dataCombined():
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


def dataFetchA():
    base = 28 ##1980
    result_frame = fetchMCB('Валовой внутренний продукт,  млрд долл. США', True)
    result_frame = indexswitch(result_frame[base:])
    return result_frame


def dataFetchB():
    base = 28 ##1980
    semi_frameA = fetchMCB('Ставка прайм-рейт,  %', True)
    semi_frameA.rename(columns = {'Value': 'PrimeRate'}, inplace=True)
    semi_frameB = fetchMCB('Национальный доход,  млрд долл. США', True)
    semi_frameB.rename(columns = {'Value': 'A032RC1'}, inplace=True)
    result_frame = pd.concat([semi_frameA, semi_frameB], axis = 1, sort = True)
    del semi_frameA, semi_frameB
    result_frame = indexswitch(result_frame[base:])
    return result_frame


def dataFetchC():
    base = 28 ##1980
    semi_frameA = fetchMCB('Ставка прайм-рейт,  %', True)
    semi_frameA.rename(columns = {'Value': 'PrimeRate'}, inplace=True)
    semi_frameB = fetchMCB('Валовой объем внутренних частных инвестиций,  млрд долл. США', True)
    semi_frameB.rename(columns = {'Value': 'A006RC1'}, inplace=True)
    result_frame = pd.concat([semi_frameA, semi_frameB], axis = 1, sort = True)
    del semi_frameA, semi_frameB
    result_frame = indexswitch(result_frame[base:])
    return result_frame


def dataFetchCensusA():
    '''Census Manufacturing Indexes,  1899 = 100'''
    base = 39 ##1899 = 100
    '''HSUS 1949 Page 179,  J13'''
    semi_frameA = fetchCensus('census1949.zip', 'J0013', True)
    '''HSUS 1949 Page 179,  J14: Warren M. Persons,  Index Of Physical Production Of Manufacturing'''
    semi_frameB = fetchCensus('census1949.zip', 'J0014', True)
    '''HSUS 1975 Page 667,  P17: Edwin Frickey Series,  Indexes of Manufacturing Production'''
    semi_frameC = fetchCensus('census1975.zip', 'P0017', True)
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC], axis = 1, sort = True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].div(result_frame.iloc[base, 1]/100)
    return result_frame, base


def dataFetchCensusBA():
    '''Returns Nominal Million-Dollar Capital,  Including Structures & Equipment,  Series'''
    from scipy import signal
    semi_frameA = fetchCensus('census1949.zip', 'J0149', True) ##Nominal
    semi_frameB = fetchCensus('census1949.zip', 'J0150', True) ##Nominal
    semi_frameC = fetchCensus('census1949.zip', 'J0151', True) ##Nominal
    semi_frameD = fetchCensus('census1975.zip', 'P0107', True) ##Nominal
    semi_frameE = fetchCensus('census1975.zip', 'P0108', True) ##Nominal
    semi_frameF = fetchCensus('census1975.zip', 'P0109', True) ##Nominal
    semi_frameG = fetchCensus('census1975.zip', 'P0110', True) ##1958 = 100
    semi_frameH = fetchCensus('census1975.zip', 'P0111', True) ##1958 = 100
    semi_frameI = fetchCensus('census1975.zip', 'P0112', True) ##1958 = 100
    semi_frameJ = fetchCensus('census1975.zip', 'P0113', True) ##Nominal
    semi_frameK = fetchCensus('census1975.zip', 'P0114', True) ##Nominal
    semi_frameL = fetchCensus('census1975.zip', 'P0115', True) ##Nominal
    semi_frameM = fetchCensus('census1975.zip', 'P0116', True) ##1958 = 100
    semi_frameN = fetchCensus('census1975.zip', 'P0117', True) ##1958 = 100
    semi_frameO = fetchCensus('census1975.zip', 'P0118', True) ##1958 = 100
    semi_frameP = fetchCensus('census1975.zip', 'P0119', True) ##1958 = 100
    semi_frameQ = fetchCensus('census1975.zip', 'P0120', True) ##1958 = 100
    semi_frameR = fetchCensus('census1975.zip', 'P0121', True) ##1958 = 100
    semi_frameS = fetchCensus('census1975.zip', 'P0122', True) ##1958 = 100
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI, semi_frameJ, \
                           semi_frameK, semi_frameL, semi_frameM, semi_frameN, semi_frameO, \
                           semi_frameP, semi_frameQ, semi_frameR, semi_frameS], axis = 1, sort = True)
    result_frame = result_frame[12:]
    for i in range(3, 19):
        result_frame = blnTomln(result_frame, i)
    result_frame['total'] = result_frame.iloc[:, [0, 3]].mean(1)
    result_frame['structures'] = result_frame.iloc[:, [1, 4]].mean(1)
    result_frame['equipment'] = result_frame.iloc[:, [2, 5]].mean(1)
    '''Scipy Signal Wiener Filter,  Non-Linear Low-Pass Filter'''
    result_frame.iloc[:, 19] = signal.wiener(result_frame.iloc[:, 19]).round()
    result_frame.iloc[:, 20] = signal.wiener(result_frame.iloc[:, 20]).round()
    result_frame.iloc[:, 21] = signal.wiener(result_frame.iloc[:, 21]).round()
    result_frame = result_frame[result_frame.columns[[19, 20, 21]]]
    return result_frame


def dataFetchCensusBB():
    '''Returns Census Fused Capital Deflator'''
    semi_frameA = fetchCensus('census1975.zip', 'P0107', True) ##Nominal
    semi_frameB = fetchCensus('census1975.zip', 'P0108', True) ##Nominal
    semi_frameC = fetchCensus('census1975.zip', 'P0109', True) ##Nominal
    semi_frameD = fetchCensus('census1975.zip', 'P0110', True) ##1958 = 100
    semi_frameE = fetchCensus('census1975.zip', 'P0111', True) ##1958 = 100
    semi_frameF = fetchCensus('census1975.zip', 'P0112', True) ##1958 = 100
    semi_frameG = fetchCensus('census1975.zip', 'P0113', True) ##Nominal
    semi_frameH = fetchCensus('census1975.zip', 'P0114', True) ##Nominal
    semi_frameI = fetchCensus('census1975.zip', 'P0115', True) ##Nominal
    semi_frameJ = fetchCensus('census1975.zip', 'P0116', True) ##1958 = 100
    semi_frameK = fetchCensus('census1975.zip', 'P0117', True) ##1958 = 100
    semi_frameL = fetchCensus('census1975.zip', 'P0118', True) ##1958 = 100
    source_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                          semi_frameF, semi_frameG, semi_frameH, semi_frameI, semi_frameJ, \
                          semi_frameK, semi_frameL], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, semi_frameF, semi_frameG, \
        semi_frameH, semi_frameI, semi_frameJ, semi_frameK, semi_frameL
    source_frame['pur_total'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 3])
    source_frame['pur_structures'] = source_frame.iloc[:, 1].div(source_frame.iloc[:, 4])
    source_frame['pur_equipment'] = source_frame.iloc[:, 2].div(source_frame.iloc[:, 5])
    source_frame['dep_total'] = source_frame.iloc[:, 6].div(source_frame.iloc[:, 9])
    source_frame['dep_structures'] = source_frame.iloc[:, 7].div(source_frame.iloc[:, 10])
    source_frame['dep_equipment'] = source_frame.iloc[:, 8].div(source_frame.iloc[:, 11])
    source_frame = source_frame[16:]
    semi_frameA = processing(source_frame, 12)
    semi_frameB = processing(source_frame, 13)
    semi_frameC = processing(source_frame, 14)
    semi_frameD = processing(source_frame, 15)
    semi_frameE = processing(source_frame, 16)
    semi_frameF = processing(source_frame, 17)
    interim_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                          semi_frameF], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, semi_frameF
    interim_frame['census_fused'] = interim_frame.mean(1)
    result_frame = interim_frame[interim_frame.columns[[6]]]
    return result_frame


def dataFetchCensusC():
    '''Census Primary Metals & Railroad-Related Products Manufacturing Series'''
    base = [15, 20, 49] ## 1875 = 100,  1880 = 100,  1909 = 100
    semi_frameA = fetchCensus('census1975.zip', 'P0262', True)
    semi_frameB = fetchCensus('census1975.zip', 'P0265', True)
    semi_frameC = fetchCensus('census1975.zip', 'P0266', True)
    semi_frameD = fetchCensus('census1975.zip', 'P0267', True)
    semi_frameE = fetchCensus('census1975.zip', 'P0268', True)
    semi_frameF = fetchCensus('census1975.zip', 'P0269', True)
    semi_frameG = fetchCensus('census1975.zip', 'P0293', True)
    semi_frameH = fetchCensus('census1975.zip', 'P0294', True)
    semi_frameI = fetchCensus('census1975.zip', 'P0295', True)
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI], axis = 1, sort = True)
    result_frame.iloc[:, 0] = result_frame.iloc[:, 0].div(result_frame.iloc[base[0], 0]/100)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].div(result_frame.iloc[base[0], 1]/100)
    result_frame.iloc[:, 2] = result_frame.iloc[:, 2].div(result_frame.iloc[base[0], 2]/100)
    result_frame.iloc[:, 3] = result_frame.iloc[:, 3].div(result_frame.iloc[base[0], 3]/100)
    result_frame.iloc[:, 4] = result_frame.iloc[:, 4].div(result_frame.iloc[base[0], 4]/100)
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(result_frame.iloc[base[2], 5]/100)
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(result_frame.iloc[base[1], 6]/100)
    result_frame.iloc[:, 7] = result_frame.iloc[:, 7].div(result_frame.iloc[base[0], 7]/100)
    result_frame.iloc[:, 8] = result_frame.iloc[:, 8].div(result_frame.iloc[base[0], 8]/100)
    return result_frame, base


def dataFetchCensusE():
    '''Census Total Immigration Series'''
    semi_frameAA = fetchCensus('census1975.zip', 'C0091', True)
    semi_frameAB = fetchCensus('census1975.zip', 'C0092', True)
    semi_frameAC = fetchCensus('census1975.zip', 'C0093', True)
    semi_frameAD = fetchCensus('census1975.zip', 'C0094', True)
    semi_frameAE = fetchCensus('census1975.zip', 'C0095', True)
    semi_frameAF = fetchCensus('census1975.zip', 'C0096', True)
    semi_frameAG = fetchCensus('census1975.zip', 'C0097', True)
    semi_frameAH = fetchCensus('census1975.zip', 'C0098', True)
    semi_frameAI = fetchCensus('census1975.zip', 'C0099', True)
    semi_frameAJ = fetchCensus('census1975.zip', 'C0100', True)
    semi_frameAK = fetchCensus('census1975.zip', 'C0101', True)
    semi_frameAL = fetchCensus('census1975.zip', 'C0103', True)
    semi_frameAM = fetchCensus('census1975.zip', 'C0104', True)
    semi_frameAN = fetchCensus('census1975.zip', 'C0105', True)
    semi_frameAO = fetchCensus('census1975.zip', 'C0106', True)
    semi_frameAP = fetchCensus('census1975.zip', 'C0107', True)
    semi_frameAQ = fetchCensus('census1975.zip', 'C0108', True)
    semi_frameAR = fetchCensus('census1975.zip', 'C0109', True)
    semi_frameAS = fetchCensus('census1975.zip', 'C0111', True)
    semi_frameAT = fetchCensus('census1975.zip', 'C0112', True)
    semi_frameAU = fetchCensus('census1975.zip', 'C0113', True)
    semi_frameAV = fetchCensus('census1975.zip', 'C0114', True)
    semi_frameAW = fetchCensus('census1975.zip', 'C0115', True)
    semi_frameAX = fetchCensus('census1975.zip', 'C0117', True)
    semi_frameAY = fetchCensus('census1975.zip', 'C0118', True)
    semi_frameAZ = fetchCensus('census1975.zip', 'C0119', True)
    result_frame = pd.concat([semi_frameAA, semi_frameAB, semi_frameAC, semi_frameAD, semi_frameAE, \
                              semi_frameAF, semi_frameAG, semi_frameAH, semi_frameAI, semi_frameAJ, \
                              semi_frameAK, semi_frameAL, semi_frameAM, semi_frameAN, semi_frameAO, \
                              semi_frameAP, semi_frameAQ, semi_frameAR, semi_frameAS, semi_frameAT, \
                              semi_frameAU, semi_frameAV, semi_frameAW, semi_frameAX, semi_frameAY, \
                              semi_frameAZ], axis = 1, sort = True)
    del semi_frameAA, semi_frameAB, semi_frameAC, semi_frameAD, semi_frameAE, \
        semi_frameAF, semi_frameAG, semi_frameAH, semi_frameAI, semi_frameAJ, \
        semi_frameAK, semi_frameAL, semi_frameAM, semi_frameAN, semi_frameAO, \
        semi_frameAP, semi_frameAQ, semi_frameAR, semi_frameAS, semi_frameAT, \
        semi_frameAU, semi_frameAV, semi_frameAW, semi_frameAX, semi_frameAY, \
        semi_frameAZ
    result_frame['C89'] = result_frame.sum(1)
    result_frame = result_frame[result_frame.columns[[result_frame.shape[1]-1]]]
    return result_frame


def dataFetchCensusF():
    '''Census Employment Series'''
    semi_frameA = fetchCensus('census1975.zip', 'D0085', True)
    semi_frameB = fetchCensus('census1975.zip', 'D0086', True)
    semi_frameC = fetchCensus('census1975.zip', 'D0796', True)
    semi_frameD = fetchCensus('census1975.zip', 'D0797', True)
    semi_frameE = fetchCensus('census1975.zip', 'D0977', True)
    semi_frameF = fetchCensus('census1975.zip', 'D0982', True)
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF], axis = 1, sort = True)
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, semi_frameF
    result_frame['workers'] = result_frame.iloc[:, 0].div(result_frame.iloc[:, 1]/100)
    result_frame.iloc[:, 4].fillna(result_frame.iloc[:25, 4].mean(), inplace=True)
    result_frame.iloc[:, 5].fillna(result_frame.iloc[:25, 5].mean(), inplace=True)
    return result_frame


def dataFetchCensusG():
    '''Census Gross National Product Series'''
    semi_frameAA = fetchCensus('census1975.zip', 'F0003', True)
    semi_frameAB = fetchCensus('census1975.zip', 'F0004', True)
    result_frame = pd.concat([semi_frameAA, semi_frameAB], axis = 1, sort = True)
    del semi_frameAA, semi_frameAB
    result_frame = result_frame[2:]
    result_frame = result_frame.div(result_frame.iloc[0, :]/100)
    return result_frame


def dataFetchCensusI():
    '''Census Foreign Trade Series'''
    semi_frameAA = fetchCensus('census1975.zip', 'U0001', True)
    semi_frameAB = fetchCensus('census1975.zip', 'U0008', True)
    result_frameA = pd.concat([semi_frameAA, semi_frameAB], axis = 1, sort = True)
    del semi_frameAA, semi_frameAB
    semi_frameAA = fetchCensus('census1975.zip', 'U0187', True)
    semi_frameAB = fetchCensus('census1975.zip', 'U0188', True)
    semi_frameAC = fetchCensus('census1975.zip', 'U0189', True)
    result_frameB = pd.concat([semi_frameAA, semi_frameAB, semi_frameAC], axis = 1, sort = True)
    del semi_frameAA, semi_frameAB, semi_frameAC
    semi_frameAA = fetchCensus('census1975.zip', 'U0319', True)
    semi_frameAB = fetchCensus('census1975.zip', 'U0320', True)
    semi_frameAC = fetchCensus('census1975.zip', 'U0321', True)
    semi_frameAD = fetchCensus('census1975.zip', 'U0322', True)
    semi_frameAE = fetchCensus('census1975.zip', 'U0323', True)
    semi_frameAF = fetchCensus('census1975.zip', 'U0325', True)
    semi_frameAG = fetchCensus('census1975.zip', 'U0326', True)
    semi_frameAH = fetchCensus('census1975.zip', 'U0327', True)
    semi_frameAI = fetchCensus('census1975.zip', 'U0328', True)
    semi_frameAJ = fetchCensus('census1975.zip', 'U0330', True)
    semi_frameAK = fetchCensus('census1975.zip', 'U0331', True)
    semi_frameAL = fetchCensus('census1975.zip', 'U0332', True)
    semi_frameAM = fetchCensus('census1975.zip', 'U0333', True)
    semi_frameAN = fetchCensus('census1975.zip', 'U0334', True)
    semi_frameAO = fetchCensus('census1975.zip', 'U0337', True)
    semi_frameAP = fetchCensus('census1975.zip', 'U0338', True)
    semi_frameAQ = fetchCensus('census1975.zip', 'U0339', True)
    semi_frameAR = fetchCensus('census1975.zip', 'U0340', True)
    semi_frameAS = fetchCensus('census1975.zip', 'U0341', True)
    semi_frameAT = fetchCensus('census1975.zip', 'U0343', True)
    semi_frameAU = fetchCensus('census1975.zip', 'U0344', True)
    semi_frameAV = fetchCensus('census1975.zip', 'U0345', True)
    semi_frameAW = fetchCensus('census1975.zip', 'U0346', True)
    semi_frameAX = fetchCensus('census1975.zip', 'U0348', True)
    semi_frameAY = fetchCensus('census1975.zip', 'U0349', True)
    semi_frameAZ = fetchCensus('census1975.zip', 'U0350', True)
    semi_frameBA = fetchCensus('census1975.zip', 'U0351', True)
    semi_frameBB = fetchCensus('census1975.zip', 'U0352', True)
    result_frameC = pd.concat([semi_frameAA, semi_frameAB, semi_frameAC, semi_frameAD, semi_frameAE, \
                            semi_frameAF, semi_frameAG, semi_frameAH, semi_frameAI, semi_frameAJ, \
                            semi_frameAK, semi_frameAL, semi_frameAM, semi_frameAN, semi_frameAO, \
                            semi_frameAP, semi_frameAQ, semi_frameAR, semi_frameAS, semi_frameAT, \
                            semi_frameAU, semi_frameAV, semi_frameAW, semi_frameAX, semi_frameAY, \
                            semi_frameAZ, semi_frameBA, semi_frameBB], axis = 1, sort = True)
    del semi_frameAA, semi_frameAB, semi_frameAC, semi_frameAD, semi_frameAE, \
        semi_frameAF, semi_frameAG, semi_frameAH, semi_frameAI, semi_frameAJ, \
        semi_frameAK, semi_frameAL, semi_frameAM, semi_frameAN, semi_frameAO, \
        semi_frameAP, semi_frameAQ, semi_frameAR, semi_frameAS, semi_frameAT, \
        semi_frameAU, semi_frameAV, semi_frameAW, semi_frameAX, semi_frameAY, \
        semi_frameAZ, semi_frameBA, semi_frameBB
    result_frameC['Exports'] = result_frameC.iloc[:, 0:14].sum(1)
    result_frameC['Imports'] = result_frameC.iloc[:, 14:28].sum(1)
    return result_frameA, result_frameB, result_frameC


def dataFetchCensusJ():
    '''Census Money Supply Aggregates'''
    base = 48 ## 1915 = 100
    semi_frameAA = fetchCensus('census1975.zip', 'X0410', True)
    semi_frameAB = fetchCensus('census1975.zip', 'X0414', True)
    semi_frameAC = fetchCensus('census1975.zip', 'X0415', True)
    result_frame = pd.concat([semi_frameAA, semi_frameAB, semi_frameAC], axis = 1, sort = True)
    del semi_frameAA, semi_frameAB, semi_frameAC
    result_frame = result_frame.div(result_frame.iloc[base, :]/100)
    return result_frame, base


def datasetCanada():
    '''A. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
    `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    '''2007 constant prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1, 000, 000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    '''Industrial machinery (x 1, 000, 000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    capital = fetchCANSIMFA(fetchCANSIMSeries())
    '''B. Labor Block: `v2523012`,  Preferred Over `v3437501` Which Is Quarterly'''
    '''`v2523012` - 282-0012 Labour Force Survey Estimates (LFS),  employment by class of worker,  North American Industry Classification System (NAICS)\
    and sex; Canada; Total employed,  all class of workers; Manufacturing; Both sexes (x 1, 000) (annual,  1987 to 2017)'''
    labor = fetchCANSIM('02820012', 'v2523012', True)
    '''C. Production Block: `v65201809`'''
    '''`v65201809` - 379-0031 Gross domestic product (GDP) at basic prices,  by North American Industry Classification System (NAICS); Canada; Trading-day\
    adjusted; 2007 constant prices; Manufacturing (x 1, 000, 000) (monthly,  1997-01-01 to 2017-10-01)'''
    product = fetchCANSIMQ('03790031', 'v65201809', True)
    result_frame = pd.concat([capital, labor, product], axis = 1, sort = True)
    result_frame = result_frame.dropna()
    result_frame.rename(columns = {0:'capital', 'v2523012':'labor', 'v65201809':'product'}, inplace=True)
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


def douglasPreprocessing():
    '''Douglas Data Preprocessing'''
    semi_frameA = fetchClassic('douglas.zip', 'DT19AS03')
    semi_frameB = fetchClassic('douglas.zip', 'DT19AS02')
    semi_frameC = fetchClassic('douglas.zip', 'DT19AS01')
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC], axis = 1, sort = True)
    result_frame = result_frame.div(result_frame.iloc[9, :])
    return result_frame


def fetchCapital():
    '''Series Not Used - `k3ntotl1si000`'''
    semi_frameA = fetchClassic('cobbdouglas.zip', 'CDT2S1') ##Annual Increase in Terms of Cost Price (1)
    semi_frameB = fetchClassic('cobbdouglas.zip', 'CDT2S3') ##Annual Increase in Terms of 1880 dollars (3)
    semi_frameC = fetchClassic('cobbdouglas.zip', 'CDT2S4') ##Total Fixed Capital in 1880 dollars (4)
    '''Fixed Assets: k1n31gd1es000,  1925--2016,  Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    semi_frameD = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '401 Ann', 1925, 2016, 9)
    '''Not Used: Fixed Assets: k3n31gd1es000,  1925--2016,  Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    semi_frameE = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '403 Ann', 1925, 2016, 9)
    semi_frameF = fetchCensus('census1975.zip', 'P0107', True)
    semi_frameG = fetchCensus('census1975.zip', 'P0110', True)
    semi_frameH = fetchCensus('census1975.zip', 'P0119', True)
    '''Kendrick J.W.,  Productivity Trends in the United States,  Page 320'''
    semi_frameI = fetchClassic('kendrick.zip', 'KTA15S08')
    '''Douglas P.H.,  Theory of Wages,  Page 332'''
    semi_frameJ = fetchClassic('douglas.zip', 'DT63AS01')
    '''FRB Data'''
    semi_frameK = FRBFA()
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF, semi_frameG, semi_frameH, semi_frameI, semi_frameJ, \
                           semi_frameK], axis = 1, sort = True)
    return result_frame


def fetchINFCF():
    '''Retrieve Yearly Price Rates from `infcf16652007.zip`'''
    source_frame = pd.read_csv('infcf16652007.zip', usecols=range(4, 7))
    series = source_frame.iloc[:, 0].unique()
    i = 0
    for ser in series:
        current_frame = source_frame[source_frame.iloc[:, 0] == ser]
        current_frame = current_frame[current_frame.columns[[1, 2]]]
        current_frame.columns = current_frame.columns.str.title()
        current_frame.rename(columns = {'Value':ser}, inplace=True)
        current_frame = current_frame.set_index('Period')
        current_frame.iloc[:, 0] = current_frame.iloc[:, 0].rdiv(1)
        current_frame = -pricesInverseSingle(current_frame) ## Put '-' Is the Only Way to Comply with the Rest of Study
        if i == 0:
            result_frame = current_frame
        elif i> = 1:
            result_frame = pd.concat([result_frame, current_frame], axis = 1, sort = True)
        del current_frame
        i+ = 1
    result_frame = result_frame[result_frame.columns[range(14)]]
    result_frame['cpiu_fused'] = result_frame.mean(1)
    result_frame = result_frame[result_frame.columns[[14]]]
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


def FRBMS():
    '''Indexed Money Stock Measures (H.6) Series:
    https://www.federalreserve.gov/datadownload/Download.aspx?rel = h6&series = 5398d8d1734b19f731aba3105eb36d47&filetype = csv&label = include&layout = seriescolumn&from = 01/01/1959&to = 12/31/2018'''
    source_frame = pd.read_csv('dataset USA FRB_H6.csv', skiprows=5, usecols=range(2))
    source_frame.columns = source_frame.columns.to_series().replace({'[ .:;@_]':''}, regex = True)
    source_frame['Period'], source_frame['Mnth'] = source_frame['TimePeriod'].str.split('-').str
    source_frame = source_frame[source_frame.columns[[2, 1]]]
    source_frame = source_frame.groupby('Period').mean()
    source_frame.to_csv('temporary.txt')
    del source_frame
    result_frame = pd.read_csv('temporary.txt')
    os.unlink('temporary.txt')
    result_frame = result_frame.set_index('Period')
    return result_frame


def localFetch():
    '''Nominal Investment Series: A006RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1968, 7)
    '''Nominal Investment Series: A006RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 7)
    semi_frameA = sub_frameA.append(sub_frameB)
    del sub_frameA, sub_frameB
    '''Nominal Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 1)
    '''Nominal Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 1)
    semi_frameB = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10106 Ann', 1929, 1969, 1)
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10106 Ann', 1969, 2012, 1)
    semi_frameC = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameD = FRBCU()
    '''`K160491` Replaced with `K10070` in `dataCombined()`'''
    '''Fixed Assets Series: K160491,  1951--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section5ALL_Hist.xls', '50900 Ann', 1951, 1969, 49)
    '''Fixed Assets Series: K160491,  1969--2011'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section5all_xls.xls', '50900 Ann', 1969, 2011, 49)
    semi_frameE = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    semi_frameF = archivedBEALabor()
    result_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, \
                           semi_frameF], axis = 1, sort = True)
    return result_frame


def preprocessingA(source_frame):
    source_frame = source_frame[source_frame.columns[[0, 4, 6, 7]]]
    source_frame = source_frame.dropna()
    source_frame = source_frame.div(source_frame.iloc[0, :])
    source_frame = indexswitch(source_frame)
    return source_frame


def preprocessingB(source_frame):
    source_frame = source_frame[source_frame.columns[[0, 6, 7, 20]]]
    source_frame = source_frame.dropna()
    source_frame = indexswitch(source_frame)
    return source_frame


def preprocessingC(source_frame):
    source_frameProduction = source_frame[source_frame.columns[[0, 6, 7]]]
    source_frameProduction = source_frameProduction.dropna()
    source_frameProduction = source_frameProduction.div(source_frameProduction.iloc[0, :])
    source_frameMoney = source_frame.iloc[:, 18:20]
    source_frameMoney = source_frameMoney.mean(1)
    source_frameMoney = pd.Data_frame(source_frameMoney, columns = ['M1']) ##Convert Series to Dataframe
    source_frameMoney = source_frameMoney.dropna()
    source_frameMoney = source_frameMoney.div(source_frameMoney.iloc[0, :])
    result_frame = pd.concat([source_frameProduction, source_frameMoney], axis = 1)
    result_frame = result_frame.dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    result_frame = indexswitch(result_frame)
    return result_frame


def preprocessingD(source_frame):
    source_frame = source_frame[source_frame.columns[[0, 1, 2, 3, 7]]]
    source_frame = source_frame.dropna()
    source_frame = indexswitch(source_frame)
    return source_frame


def preprocessingE(source_frame):
    '''Works on Result of `archivedDataCombined`'''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 0]*source_frame.iloc[:, 7].div(source_frame.iloc[:, 6])
    '''`Real` Capital'''
    source_frame['cap'] = source_frame.iloc[:, 11]*source_frame.iloc[:, 7].div(source_frame.iloc[:, 6])
    '''Nominal DataSet'''
    nominal_frame = source_frame[source_frame.columns[[0, 6, 11]]].dropna()
    '''`Real` DataSet'''
    real_frame = source_frame[source_frame.columns[[21, 7, 22]]].dropna()
    return nominal_frame, real_frame


def preprocessingF(testing_frame):
    '''testing_frame: Test _frame'''
    '''Control _frame'''
    control_frame = pd.read_csv('dataset USA Reference RU Kurenkov Yu.V..csv')
    control_frame = control_frame.set_index('Period')
    '''Data Fetch'''
    '''Production'''
    semi_frameAA = control_frame[control_frame.columns[[0]]]
    semi_frameAB = testing_frame[testing_frame.columns[[7]]].dropna()
    semi_frameAC = FRBIP()
    result_frameA = pd.concat([semi_frameAA, semi_frameAB, semi_frameAC], axis = 1, sort = True)
    result_frameA = result_frameA.div(result_frameA.iloc[31, :]/100)
    '''Labor'''
    semi_frameBA = control_frame[control_frame.columns[[1]]]
    semi_frameBB = testing_frame[testing_frame.columns[[8]]].dropna()
    result_frameB = pd.concat([semi_frameBA, semi_frameBB], axis = 1, sort = True)
    '''Capital'''
    semi_frameCA = control_frame[control_frame.columns[[2]]]
    semi_frameCB = testing_frame[testing_frame.columns[[11]]].dropna()
    result_frameC = pd.concat([semi_frameCA, semi_frameCB], axis = 1, sort = True)
    result_frameC = result_frameC.div(result_frameC.iloc[1, :]/100)
    '''Capacity Utilization'''
    semi_frameDA = control_frame[control_frame.columns[[3]]]
    semi_frameDB = FRBCU()
    result_frameD = pd.concat([semi_frameDA, semi_frameDB], axis = 1, sort = True)
    return result_frameA, result_frameB, result_frameC, result_frameD


def updatedSet():
    semi_frameA = fetchBEA('dataset USA BEA NipaDataA.txt', 'A006RC')
    semi_frameB = fetchBEA('dataset USA BEA NipaDataA.txt', 'A006RD')
    semi_frameC = fetchBEA('dataset USA BEA NipaDataA.txt', 'A191RC')
    semi_frameD = fetchBEA('dataset USA BEA NipaDataA.txt', 'A191RX')
    '''Fixed Assets: kcn31gd1es000,  1925--2016,  Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    semi_frameE = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '402 Ann', 1925, 2016, 9)
    '''Not Used: Fixed Assets: k3n31gd1es000,  1925--2016,  Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    semi_frameF = beaFetch('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section4ALL_xls.xls', '403 Ann', 1925, 2016, 9)
    source_frame = pd.concat([semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, semi_frameF], axis = 1, sort = True).dropna()
    del semi_frameA, semi_frameB, semi_frameC, semi_frameD, semi_frameE, semi_frameF
    base = 58 ##Year 2009
    '''Investment,  2009 = 100'''
    source_frame['inv'] = source_frame.iloc[base, 0]*source_frame.iloc[:, 1].div(100)
    '''Capital,  2009 = 100'''
    source_frame['cap'] = 1000*source_frame.iloc[base, 5]*source_frame.iloc[:, 4].div(100)
    '''Capital Retirement Ratio'''
    source_frame['rto'] = 1+(1*source_frame.iloc[:, 6]-source_frame.iloc[:, 7].shift(-1)).div(source_frame.iloc[:, 7])
    result_frameA = source_frame[source_frame.columns[[6, 3, 7, 8]]]
    result_frameB = source_frame[source_frame.columns[[8]]]
    result_frameA = indexswitch(result_frameA).dropna()
    result_frameB = indexswitch(result_frameB).dropna()
    return result_frameA, result_frameB, base


def blnTomln(source_frame, column):
    '''Convert Series in Billions of Dollars to Series in Millions of Dollars'''
    source_frame.iloc[:, column] = 1000*source_frame.iloc[:, column]
    return source_frame


def capital(source_frame, A, B, C, D, Pi):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Investment, 
    source_frame.iloc[:, 2]: Production, 
    source_frame.iloc[:, 3]: Capital, 
    source_frame.iloc[:, 4]: Capital Retirement, 
    A: S - Gross Fixed Investment to Gross Domestic Product Ratio - Absolute Term over Period, 
    B: S - Gross Fixed Investment to Gross Domestic Product Ratio - Slope over Period, 
    C: Λ - Fixed Assets Turnover Ratio - Absolute Term over Period, 
    D: Λ - Fixed Assets Turnover Ratio - Slope over Period, 
    Pi: Investment to Capital Conversion Ratio
    '''
    series = source_frame.iloc[:, 3].shift(1)*(1+(B*source_frame.iloc[:, 0].shift(1)+A)*(D*source_frame.iloc[:, 0].shift(1)+C)*Pi-source_frame.iloc[:, 4].shift(1))
    return series


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


def MSplineEA(source_frame, intervals, k):
    '''Exponential Spline,  Type A
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Target Series, 
    intervals: Number of Intervals, 
    k: Interpolation Knots'''
    A, K, S = [], [], []
    for j in range(intervals): ##Coefficient Section
        A.append(((source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[0], 0])*sp.log(source_frame.iloc[k[j], 1])-(source_frame.iloc[k[j], 0]-source_frame.iloc[k[0], 0])*sp.log(source_frame.iloc[k[1+j], 1]))/(source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0]))
        if j == 0:
            K.append((sp.log(source_frame.iloc[k[1+j], 1])-sp.log(source_frame.iloc[k[j], 1]))/(source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0]))
        else:
            K.append(K[j-1]+sp.log(source_frame.iloc[k[1+j], 1])/(source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0])-\
                     (source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j-1], 0])*sp.log(source_frame.iloc[k[j], 1])/((source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0])*(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0]))+\
                     sp.log(source_frame.iloc[k[j-1], 1])/(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0]))
        if j == intervals-1: ##Spline Section
            for i in range(k[j], 1+k[1+j]):
                S.append(sp.exp(A[j]+K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0])))
        else:
            for i in range(k[j], k[1+j]):
                S.append(sp.exp(A[j]+K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0])))
    S = pd.Data_frame(S, columns = ['Spline']) ##Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis = 1, sort = True)
    return K, result_frame


def MSplineEB(source_frame, intervals, k):
    '''Exponential Spline,  Type B
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Target Series, 
    intervals: Number of Intervals, 
    k: Interpolation Knots'''
    K, S = [], []
    for j in range(intervals): ##Coefficient Section
        K.append((sp.log(source_frame.iloc[k[1+j], 1])-sp.log(source_frame.iloc[k[j], 1]))/(source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0]))
        if j == intervals-1: ##Spline Section
            for i in range(k[j], 1+k[1+j]):
                S.append(source_frame.iloc[k[j], 1]*sp.exp(K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0])))
        else:
            for i in range(k[j], k[1+j]):
                S.append(source_frame.iloc[k[j], 1]*sp.exp(K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0])))
    S = pd.Data_frame(S, columns = ['Spline']) ##Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis = 1, sort = True)
    return K, result_frame


def MSplineLA(source_frame, intervals, k):
    '''Linear Spline,  Type A
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Target Series, 
    intervals: Number of Intervals, 
    k: Interpolation Knots'''
    A, K, S = [], [], []
    for j in range(intervals):
        A.append(((source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[0], 0])*source_frame.iloc[k[j], 1]-(source_frame.iloc[k[j], 0]-source_frame.iloc[k[0], 0])*source_frame.iloc[k[1+j], 1])/(source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0]))
        if j == 0:
            K.append((source_frame.iloc[k[1+j], 1]-source_frame.iloc[k[j], 1])/(source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0]))
        else:
            K.append(K[j-1]+source_frame.iloc[k[1+j], 1]/(source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0])-\
                     (source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j-1], 0])*source_frame.iloc[k[j], 1]/((source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0])*(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0]))+\
                     source_frame.iloc[k[j-1], 1]/(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0]))
        if j == intervals-1:
            for i in range(k[j], 1+k[1+j]):
                S.append(A[j]+K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0]))
        else:
            for i in range(k[j], k[1+j]):
                S.append(A[j]+K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0]))
    S = pd.Data_frame(S, columns = ['Spline']) ##Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis = 1, sort = True)
    return K, result_frame


def MSplineLB(source_frame, intervals, k):
    '''Linear Spline,  Type B
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Target Series, 
    intervals: Number of Intervals, 
    k: Interpolation Knots'''
    K, S = [], []
    for j in range(intervals):
        K.append((source_frame.iloc[k[1+j], 1]-source_frame.iloc[k[j], 1])/(source_frame.iloc[k[1+j], 0]-source_frame.iloc[k[j], 0]))
        if j == intervals-1:
            for i in range(k[j], 1+k[1+j]):
                S.append(source_frame.iloc[k[j], 1]+K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0]))
        else:
            for i in range(k[j], k[1+j]):
                S.append(source_frame.iloc[k[j], 1]+K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0]))
    S = pd.Data_frame(S, columns = ['Spline']) ##Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis = 1, sort = True)
    return K, result_frame


def MSplineLLS(source_frame, intervals, k):
    '''Linear Spline,  Linear Regression Kernel
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Target Series, 
    intervals: Number of Intervals, 
    k: Interpolation Knots'''
    A, K, S = [], [], []
    for j in range(intervals):
        S1, S2, S3, S4 = 0, 0, 0, 0 ##X, Y, X**2, XY ##Summarize
        if j == intervals-1:
            for i in range(k[j], 1+k[1+j]):
                S1+ = source_frame.iloc[i, 0]
                S2+ = source_frame.iloc[i, 1]
                S3+ = (source_frame.iloc[i, 0])**2
                S4+ = source_frame.iloc[i, 0]*source_frame.iloc[i, 1]
            A.append(((1+k[1+j]-k[j])*S4-S1*S2)/((1+k[1+j]-k[j])*S3-S1**2))
        else:
            for i in range(k[j], k[1+j]):
                S1+ = source_frame.iloc[i, 0]
                S2+ = source_frame.iloc[i, 1]
                S3+ = (source_frame.iloc[i, 0])**2
                S4+ = source_frame.iloc[i, 0]*source_frame.iloc[i, 1]
            if j == 0:
                A.append((S2*S3-S1*S4)/((k[1+j]-k[j])*S3-S1**2))
            A.append(((k[1+j]-k[j])*S4-S1*S2)/((k[1+j]-k[j])*S3-S1**2))
    for j in range(intervals):
        if j == 0:
            K.append(A[j])
        else:
            K.append(K[j-1]+(A[j]-A[1+j])*source_frame.iloc[k[j], 0])
        if j == intervals-1:
            for i in range(k[j], 1+k[1+j]):
                S.append(K[j]+A[1+j]*source_frame.iloc[i, 0])
        else:
            for i in range(k[j], k[1+j]):
                S.append(K[j]+A[1+j]*source_frame.iloc[i, 0])
    S = pd.Data_frame(S, columns = ['Spline']) ##Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis = 1, sort = True)
    return A, result_frame


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


def approxPowerFunctionA(source_frame, q1, q2, alpha):
    '''
    source_frame.iloc[:, 0]: Regressor: = Period, 
    source_frame.iloc[:, 1]: Regressand, 
    q1, q2, alpha: Parameters
    '''
    result_frame = source_frame.iloc[:, 0] ##Data_frame for Based Log-Linear Approximation Results
    calcul_frame = [] ##Blank List for Calculation Results
    import math
    for i in range(len(source_frame)):
        XAA = q1+q2*(1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha ##{RESULT}(Yhat) = Y0+A*(T-T0)**alpha
        XBB = (q1+q2*(1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha-source_frame.iloc[i, 1])**2 ##(Yhat-Y)**2
        XCC = (1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(alpha-1) ##(T-T0)**(alpha-1)
        XDD = (1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha ##(T-T0)**alpha
        XEE = ((1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha)*math.log(1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0]) ##((T-T0)**alpha)*LN(T-T0)
        XFF = source_frame.iloc[i, 1]*(1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha ##Y*(T-T0)**alpha
        XGG = source_frame.iloc[i, 1]*((1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha)*math.log(1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0]) ##Y*((T-T0)**alpha)*LN(T-T0)
        XHH = (1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(2*alpha) ##(T-T0)**(2*alpha)
        XII = (1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(2*alpha)*math.log(1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0]) ##(T-T0)**(2*alpha)*LN(T-T0)
        XJJ = (1+source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(2*alpha-1) ##(T-T0)**(2*alpha-1)
        calcul_frame.append({'XAA': XAA,  'XBB': XBB,  'XCC': XCC,  'XDD': XDD,  'XEE': XEE,  'XFF': XFF,  'XGG': XGG,  'XHH': XHH,  'XII': XII,  'XJJ': XJJ})
    del XAA, XBB, XCC, XDD, XEE, XFF, XGG, XHH, XII, XJJ
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    Z = q1+q2*(1+source_frame.iloc[:, 0]-source_frame.iloc[0, 0])**alpha
    from sklearn.metrics import mean_squared_error
    print('Model Parameter: T0 = {}'.format((source_frame.iloc[0, 0]-1)))
    print('Model Parameter: Y0 = {}'.format(q1))
    print('Model Parameter: A = {:.4f}'.format(q2))
    print('Model Parameter: Alpha = {:.4f}'.format(alpha))
    print('Estimator Result: Mean Value: {:, .4f}'.format(sp.mean(Z)))
    print('Estimator Result: Mean Squared Deviation,  MSD: {:, .4f}'.format(mean_squared_error(source_frame.iloc[:, 1], Z)))
    print('Estimator Result: Root-Mean-Square Deviation,  RMSD: {:, .4f}'.format(math.sqrt(mean_squared_error(source_frame.iloc[:, 1], Z))))


def approxPowerFunctionB(source_frame, q1, q2, q3, q4, alpha):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Regressor, 
    source_frame.iloc[:, 2]: Regressand, 
    q1, q2, q3, q4, alpha: Parameters
    '''
    result_frame = source_frame.iloc[:, 0] ##Data_frame for Approximation Results
    calcul_frame = [] ##Blank List for Calculation Results
    for i in range(len(source_frame)):
        XAA = source_frame.iloc[i, 1] ##'{X}'
        XBB = q3+((q4-q3)/(q2-q1)**alpha)*(source_frame.iloc[i, 1]-q1)**alpha ##'{RESULT}(Yhat) = U1+((U2-U1)/(TAU2-TAU1)**Alpha)*({X}-TAU1)**Alpha'
        XCC = (source_frame.iloc[i, 2]-(q3+((q4-q3)/(q2-q1)**alpha)*(source_frame.iloc[i, 1]-q1)**alpha))**2 ##'(Yhat-Y)**2'
        XDD = abs(source_frame.iloc[i, 2]-(q3+((q4-q3)/(q2-q1)**alpha)*(source_frame.iloc[i, 1]-q1)**alpha)) ##'ABS(Yhat-Y)'
        calcul_frame.append({'XAA': XAA,  'XBB': XBB,  'XCC': XCC,  'XDD': XDD})
    del XAA, XBB, XCC, XDD
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    Z = q3+((q4-q3)/(q2-q1)**alpha)*(source_frame.iloc[:, 1]-q1)**alpha
    import math
    from sklearn.metrics import mean_squared_error
    print('Model Parameter: TAU1 = {}'.format(q1))
    print('Model Parameter: TAU2 = {}'.format(q2))
    print('Model Parameter: U1 = {}'.format(q3))
    print('Model Parameter: U2 = {}'.format(q4))
    print('Model Parameter: Alpha = {:.4f}'.format(alpha))
    print('Model Parameter: A: = (U2-U1)/(TAU2-TAU1)**Alpha = {:, .4f}'.format((q4-q3)/(q2-q1)**alpha))
    print('Estimator Result: Mean Value: {:, .4f}'.format(sp.mean(Z)))
    print('Estimator Result: Mean Squared Deviation,  MSD: {:, .4f}'.format(mean_squared_error(source_frame.iloc[:, 2], Z)))
    print('Estimator Result: Root-Mean-Square Deviation,  RMSD: {:, .4f}'.format(math.sqrt(mean_squared_error(source_frame.iloc[:, 2], Z))))


def approxPowerFunctionC(source_frame, q1, q2, q3, q4):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Regressor, 
    source_frame.iloc[:, 2]: Regressand, 
    q1, q2, q3, q4: Parameters
    '''
    import math
    alpha = math.log(q4/q3)/math.log(q1/q2)
    result_frame = source_frame.iloc[:, 0] ##Data_frame for Approximation Results
    calcul_frame = [] ##Blank List for Calculation Results
    for i in range(len(source_frame)):
        XAA = source_frame.iloc[i, 1] ##'{X}'
        XBB = q3*(q1/source_frame.iloc[i, 1])**alpha ##'{RESULT}{Hat}{Y} = Y1*(X1/{X})**Alpha'
        XCC = source_frame.iloc[i, 2]-q3*(q1/source_frame.iloc[i, 1])**alpha ##'{Hat-1}{Y}'
        XDD = abs(source_frame.iloc[i, 2]-q3*(q1/source_frame.iloc[i, 1])**alpha) ##'ABS({Hat-1}{Y})'
        XEE = (source_frame.iloc[i, 2]-q3*(q1/source_frame.iloc[i, 1])**alpha)**2 ##'({Hat-1}{Y})**2'
        calcul_frame.append({'XAA': XAA,  'XBB': XBB,  'XCC': XCC,  'XDD': XDD,  'XEE': XEE})
    del XAA, XBB, XCC, XDD, XEE
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    Z = q3*(source_frame.iloc[:, 1].rdiv(q1))**alpha
    import math
    from sklearn.metrics import mean_squared_error
    print('Model Parameter: X1 = {:.4f}'.format(q1))
    print('Model Parameter: X2 = {}'.format(q2))
    print('Model Parameter: Y1 = {:.4f}'.format(q3))
    print('Model Parameter: Y2 = {}'.format(q4))
    print('Model Parameter: Alpha: = LN(Y2/Y1)/LN(X1/X2) = {:.4f}'.format(alpha))
    print('Estimator Result: Mean Value: {:, .4f}'.format(sp.mean(Z)))
    print('Estimator Result: Mean Squared Deviation,  MSD: {:, .4f}'.format(mean_squared_error(source_frame.iloc[:, 2], Z)))
    print('Estimator Result: Root-Mean-Square Deviation,  RMSD: {:, .4f}'.format(math.sqrt(mean_squared_error(source_frame.iloc[:, 2], Z))))


def errorMetrics(source_frame):
    '''Error Metrics Module'''
    DX = (source_frame.iloc[:, 2]-source_frame.iloc[:, 1]).div(source_frame.iloc[:, 1])
    DX = DX.abs()
    C = sp.mean(DX)
    print('Criterion,  C: {:.6f}'.format(C))


def resultsDeliveryA(intervals, coefficients):
    '''Results Delivery Module
    intervals (1+N): 1+Number of Intervals
    coefficients: A-Coefficients'''
    for i in range(1+intervals):
        print('Model Parameter: A{:02d} = {:.6f}'.format(i, coefficients[i]))


def resultsDeliveryK(intervals, coefficients):
    '''Results Delivery Module
    intervals: Number of Intervals
    coefficients: K-Coefficients'''
    for i in range(intervals):
        print('Model Parameter: K{:02d} = {:.6f}'.format(1+i, coefficients[i]))


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


def capitalAcquisitions(source_frame):
    '''
    source_frame.iloc[:, 0]: Period
    source_frame.iloc[:, 1]: Nominal Investment
    source_frame.iloc[:, 2]: Nominal Production
    source_frame.iloc[:, 3]: Real Production
    source_frame.iloc[:, 4]: Maximum Real Production
    source_frame.iloc[:, 5]: Nominal Capital
    source_frame.iloc[:, 6]: Labor
    '''
    i = len(source_frame)-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 3])>1:
        i- = 1
        base = i ##Basic Year
    '''Calculate Static Values'''
    XAA = source_frame.iloc[:, 3].div(source_frame.iloc[:, 5]) ##Fixed Assets Turnover Ratio
    XBB = source_frame.iloc[:, 1].div(source_frame.iloc[:, 3]) ##Investment to Gross Domestic Product Ratio,  (I/Y)/(I0/Y0)
    XCC = source_frame.iloc[:, 5].div(source_frame.iloc[:, 6]) ##Labor Capital Intensity
    XDD = source_frame.iloc[:, 3].div(source_frame.iloc[:, 6]) ##Labor Productivity
    XBB = XBB.div(XBB[0])
    XCC = XCC.div(XCC[0])
    XDD = XDD.div(XDD[0])
    XEE = sp.log(XCC) ##Log Labor Capital Intensity,  LN((K/L)/(K0/L0))
    XFF = sp.log(XDD) ##Log Labor Productivity,  LN((Y/L)/(Y0/L0))
    XGG = source_frame.iloc[:, 4].div(source_frame.iloc[:, 5]) ##Max: Fixed Assets Turnover Ratio
    XHH = source_frame.iloc[:, 1].div(source_frame.iloc[:, 4]) ##Max: Investment to Gross Domestic Product Ratio
    XII = source_frame.iloc[:, 4].div(source_frame.iloc[:, 6]) ##Max: Labor Productivity
    XHH = XHH.div(XHH[0])
    XII = XII.div(XII[0])
    XJJ = sp.log(XII) ##Max: Log Labor Productivity
    XEE = pd.Data_frame(XEE, columns = ['XEE']) ##Convert List to Dataframe
    XFF = pd.Data_frame(XFF, columns = ['XFF']) ##Convert List to Dataframe
    XJJ = pd.Data_frame(XJJ, columns = ['XJJ']) ##Convert List to Dataframe
    '''Calculate Dynamic Values'''
    N = int(input('Define Number of Line Segments for Pi: ')) ##Number of Periods
    if N> = 1:
        print('Number of Periods Provided: {}'.format(N))
        pi, knt = [], [] ##Pi Switch Points & Pi
        knt.append(0)
        i = 0
        if N == 1:
            knt.append(len(source_frame)-1)
            pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1+i]-1, 0]))))
        elif N> = 2:
            while i<N:
                if i == N-1:
                    knt.append(len(source_frame)-1)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1+i]-1, 0]))))
                    i+ = 1
                else:
                    y = int(input('Select Row for Year,  Should Be More Than {}: = {}: '.format(0, source_frame.iloc[0, 0])))
                    if y>knt[i]:
                        knt.append(y)
                        pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1+i], 0]))))
                        i+ = 1
        else:
            print('Error')
        XKK = []
        for i in range(1):
            XKK.append(sp.nan)
        if N == 1:
            j = 0
            for i in range(knt[j], knt[1+j]):
                XKK.append(source_frame.iloc[1+i, 5]-source_frame.iloc[i, 5]+pi[j]*source_frame.iloc[1+i, 1]) ##Estimate: GCF[-] or CA[+]
        else:
            for j in range(N):
                if j == N-1:
                    for i in range(knt[j], knt[1+j]):
                        XKK.append(source_frame.iloc[1+i, 5]-source_frame.iloc[i, 5]+pi[j]*source_frame.iloc[1+i, 1]) ##Estimate: GCF[-] or CA[+]
                else:
                    for i in range(knt[j], knt[1+j]):
                        XKK.append(source_frame.iloc[1+i, 5]-source_frame.iloc[i, 5]+pi[j]*source_frame.iloc[1+i, 1]) ##Estimate: GCF[-] or CA[+]
        XKK = pd.Data_frame(XKK, columns = ['XKK']) ##Convert List to Dataframe
        result_frame = pd.Data_frame(source_frame.iloc[:, 0], columns = ['Period'])
        result_frame = pd.concat([result_frame, XAA, XBB, XCC, XDD, XEE, XFF, XGG, XHH, XII, XJJ, XKK], axis = 1)
        result_frame.columns = ['Period', 'XAA', 'XBB', 'XCC', 'XDD', 'XEE', 'XFF', 'XGG', 'XHH', 'XII', 'XJJ', 'XKK']
        '''
        `-` Gross Capital Formation
        `+` Capital Acquisitions
        '''
        for i in range(N):
            if i == N-1:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1+i]-1, 0], pi[i]))
            else:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1+i], 0], pi[i]))
        plt.figure(1)
        plt.plot(XCC, XDD)
        plt.plot(XCC, XII)
        plt.title('Labor Productivity,  Observed & Max,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Labor Capital Intensity')
        plt.ylabel('Labor Productivity,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(2)
        plt.plot(XEE, XFF)
        plt.plot(XEE, XJJ)
        plt.title('Log Labor Productivity,  Observed & Max,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Log Labor Capital Intensity')
        plt.ylabel('Log Labor Productivity,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(3)
        plt.plot(source_frame.iloc[:, 0], XAA)
        plt.plot(source_frame.iloc[:, 0], XGG)
        plt.title('Fixed Assets Turnover ($\\lambda$),  Observed & Max,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Period')
        plt.ylabel('Fixed Assets Turnover ($\\lambda$),  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(4)
        plt.plot(source_frame.iloc[:, 0], XBB)
        plt.plot(source_frame.iloc[:, 0], XHH)
        plt.title('Investment to Gross Domestic Product Ratio, \nObserved & Max,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(5)
        plt.plot(source_frame.iloc[:, 0], XKK)
        plt.title('Gross Capital Formation (GCF) or\nCapital Acquisitions (CA),  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Period')
        plt.ylabel('GCF or CA,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.show()
    else:
        print('N> = 1 is Required,  N = {} Was Provided'.format(N))


def capitalRetirement(source_frame):
    '''
    source_frame.iloc[:, 0]: Period
    source_frame.iloc[:, 1]: Nominal Investment
    source_frame.iloc[:, 2]: Nominal Production
    source_frame.iloc[:, 3]: Real Production
    source_frame.iloc[:, 4]: Nominal Capital
    source_frame.iloc[:, 5]: Labor
    '''
    '''Define Basic Year for Deflator'''
    i = len(source_frame)-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 3])>1:
        i- = 1
        base = i ##Basic Year
    '''Calculate Static Values'''
    YAA = source_frame.iloc[:, 4].div(source_frame.iloc[:, 5])
    YAA = sp.log(YAA.div(YAA[0])) ##Log Labor Capital Intensity,  LN((K/L)/(K0/L0))
    YBB = source_frame.iloc[:, 3].div(source_frame.iloc[:, 5])
    YBB = sp.log(YBB.div(YBB[0])) ##Log Labor Productivity,  LN((Y/L)/(Y0/L0))
    YCC = source_frame.iloc[:, 1].div(source_frame.iloc[:, 3])
    YCC = YCC.div(YCC[0]) ##Investment to Gross Domestic Product Ratio,  (I/Y)/(I0/Y0)
    YDD = source_frame.iloc[:, 3].div(source_frame.iloc[:, 4]) ##Fixed Assets Turnover Ratio
    YAA = pd.Data_frame(YAA, columns = ['YAA']) ##Convert List to Dataframe
    YBB = pd.Data_frame(YBB, columns = ['YBB']) ##Convert List to Dataframe
    N = int(input('Define Number of Line Segments for Pi: ')) ##Number of Periods
    if N> = 1:
        print('Number of Periods Provided: {}'.format(N))
        pi, knt = [], [] ##Pi Switch Points & Pi
        knt.append(0)
        i = 0
        if N == 1:
            knt.append(len(source_frame)-1)
            pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[:, 0][knt[1+i]]))))
        elif N> = 2:
            while i<N:
                if i == N-1:
                    knt.append(len(source_frame)-1)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1+i], 0]))))
                    i+ = 1
                else:
                    y = int(input('Select Row for Year: '))
                    if y>knt[i]:
                        knt.append(y)
                        pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1+i], 0]))))
                        i+ = 1
        else:
            print('Error')
        YEE = []
        YFF = []
        YEE.append(sp.nan) ##Fixed Assets Retirement Value
        YFF.append(sp.nan) ##Fixed Assets Retirement Ratio
        '''Calculate Dynamic Values'''
        if N == 1:
            j = 0
            for i in range(knt[j], knt[1+j]):
                YEE.append(source_frame.iloc[i, 4]-source_frame.iloc[1+i, 4]+pi[j]*source_frame.iloc[i, 1]) ##Fixed Assets Retirement Value
                YFF.append((source_frame.iloc[i, 4]-source_frame.iloc[1+i, 4]+pi[j]*source_frame.iloc[i, 1])/source_frame.iloc[1+i, 4]) ##Fixed Assets Retirement Ratio
        else:
            for j in range(N):
                if j == N-1:
                    for i in range(knt[j], knt[1+j]):
                        YEE.append(source_frame.iloc[i, 4]-source_frame.iloc[1+i, 4]+pi[j]*source_frame.iloc[i, 1]) ##Fixed Assets Retirement Value
                        YFF.append((source_frame.iloc[i, 4]-source_frame.iloc[1+i, 4]+pi[j]*source_frame.iloc[i, 1])/source_frame.iloc[1+i, 4]) ##Fixed Assets Retirement Ratio
                else:
                    for i in range(knt[j], knt[1+j]):
                        YEE.append(source_frame.iloc[i, 4]-source_frame.iloc[1+i, 4]+pi[j]*source_frame.iloc[i, 1]) ##Fixed Assets Retirement Value
                        YFF.append((source_frame.iloc[i, 4]-source_frame.iloc[1+i, 4]+pi[j]*source_frame.iloc[i, 1])/source_frame.iloc[1+i, 4]) ##Fixed Assets Retirement Ratio
        YEE = pd.Data_frame(YEE, columns = ['YEE']) ##Convert List to Dataframe
        YFF = pd.Data_frame(YFF, columns = ['YFF']) ##Convert List to Dataframe
        result_frame = pd.Data_frame(source_frame.iloc[:, 0], columns = ['Period'])
        result_frame = pd.concat([result_frame, YAA, YBB, YCC, YDD, YEE, YFF], axis = 1, sort = True)
        result_frame.columns = ['Period', 'YAA', 'YBB', 'YCC', 'YDD', 'YEE', 'YFF']
        result_frame['YGG'] = result_frame['YFF']-result_frame['YFF'].mean()
        result_frame['YGG'] = result_frame['YGG'].abs()
        result_frame['YHH'] = result_frame['YFF']-result_frame['YFF'].shift(1)
        result_frame['YHH'] = result_frame['YHH'].abs()
        for i in range(N):
            if i == N-1:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1+i], 0], pi[i]))
            else:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1+i], 0], pi[i]))
        plt.figure(1)
        plt.title('Product,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Product,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0],  source_frame.iloc[:, 3])
        plt.grid(True)
        plt.figure(2)
        plt.title('Capital,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Capital,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0],  source_frame.iloc[:, 4])
        plt.grid(True)
        plt.figure(3)
        plt.title('Fixed Assets Turnover ($\\lambda$),  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Fixed Assets Turnover ($\\lambda$),  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0],  source_frame.iloc[:, 3].div(source_frame.iloc[:, 4]))
        plt.grid(True)
        plt.figure(4)
        plt.title('Investment to Gross Domestic Product Ratio,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], YCC)
        plt.grid(True)
        plt.figure(5)
        plt.title('$\\alpha(t)$,  Fixed Assets Retirement Ratio,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('$\\alpha(t)$,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], YFF)
        plt.grid(True)
        plt.figure(6)
        plt.title('Fixed Assets Retirement Ratio to Fixed Assets Retirement Value,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('$\\alpha(t)$,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.ylabel('Fixed Assets Retirement Value,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.plot(YFF, YEE)
        plt.grid(True)
        plt.figure(7)
        plt.title('Labor Capital Intensity,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Labor Capital Intensity,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.ylabel('Labor Productivity,  {} = 100'.format(source_frame.iloc[base, 0]))
        plt.plot(sp.exp(YAA), sp.exp(YBB))
        plt.grid(True)
        plt.show()
    else:
        print('N> = 1 is Required,  N = {} Was Provided'.format(N))


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


def cd_modified(source_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb,  P.H. Douglas. A Theory of Production,  1928 & P.H. Douglas. The Theory of Wages,  1934;
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Capital, 
    source_frame.iloc[:, 1]: Labor, 
    source_frame.iloc[:, 2]: Product
    '''
    functionDict = {'FigureA':'Chart 15 Relative Increase in Capital,  Labor,  and Physical Product in Manufacturing Industries of Massachussets,  %d$-$%d (%d = 100)', 
                'FigureB':'Chart 16 Theoretical and Actual Curves of Production,  Massachusetts,  %d$-$%d (%d = 100)', 
                'FigureC':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines,  Massachusetts\nTrend Lines = 3 Year Moving Average', 
                'FigureD':'Chart 17 The Percentage Deviations of the Computed Product ($P\'$) from the Actual Product ($P$) in Massachusetts Manufacturing,  %d$-$%d', 
                'priceyear':1899}
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
    plt.title(functionDict['FigureA'] %(source_frame.index[0], source_frame.index[len(source_frame)-1], functionDict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.index, source_frame.iloc[:, 2], label = 'Actual Product')
    plt.plot(source_frame.index, PP, label = 'Computed Product,  $P\' = {:, .4f}L^{{{:, .4f}}}C^{{{:, .4f}}}$'.format(a0, 1-a1, a1))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(functionDict['FigureB'] %(source_frame.index[0], source_frame.index[len(source_frame)-1], functionDict['priceyear']))
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


def cd_canada(source_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb,  P.H. Douglas. A Theory of Production,  1928;
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Capital, 
    source_frame.iloc[:, 1]: Labor, 
    source_frame.iloc[:, 2]: Product
    '''
    functionDict = {'FigureA':'Chart I Progress in Manufacturing %d$-$%d (%d = 100)', 
                'FigureB':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d = 100)', 
                'FigureC':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines = 3 Year Moving Average', 
                'FigureD':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d', 
                'priceyear':2007}
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
    plt.title(functionDict['FigureA'] %(source_frame.index[0], source_frame.index[len(source_frame)-1], functionDict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.index, source_frame.iloc[:, 2], label = 'Actual Product')
    plt.plot(source_frame.index, PP, label = 'Computed Product,  $P\' = {:, .4f}L^{{{:, .4f}}}C^{{{:, .4f}}}$'.format(a0, 1-a1, a1))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(functionDict['FigureB'] %(source_frame.index[0], source_frame.index[len(source_frame)-1], functionDict['priceyear']))
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


def dataFetchPlottingA(source_frame):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Gross Domestic Investment, 
    source_frame.iloc[:, 2]: National Income, 
    source_frame.iloc[:, 3]: Nominal Gross Domestic Product, 
    source_frame.iloc[:, 4]: Real Gross Domestic Product
    '''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 4].div(source_frame.iloc[:, 3])
    '''`Real` Production'''
    source_frame['prd'] = source_frame.iloc[:, 2]*source_frame.iloc[:, 4].div(source_frame.iloc[:, 3])
    plt.figure()
    plt.title('Gross Private Domestic Investment & National Income,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5], label = 'Gross Private Domestic Investment')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 6], label = 'National Income')
    plt.xlabel('Period')
    plt.ylabel('Index')
    source_frame.iloc[:, 0] = (source_frame.iloc[:, 0].shift(-1)+source_frame.iloc[:, 0])/2
    X = (source_frame.iloc[:, 5].shift(-1)+source_frame.iloc[:, 5])/2
    Y = (source_frame.iloc[:, 6].shift(-1)+source_frame.iloc[:, 6])/2
    plt.plot(source_frame.iloc[:, 0], X, '--', source_frame.iloc[:, 0], Y, '--')
    plt.grid()
    plt.legend()
    plt.show()


def dataFetchPlottingB(source_frame):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Gross Domestic Investment, 
    source_frame.iloc[:, 2]: Nominal Gross Domestic Product, 
    source_frame.iloc[:, 3]: Real Gross Domestic Product, 
    source_frame.iloc[:, 4]: Prime Rate
    '''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])
    plt.figure()
    plt.plot(source_frame.iloc[:, 4], source_frame.iloc[:, 5])
    plt.title('Gross Private Domestic Investment,  A006RC,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Percentage')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.show()


def dataFetchPlottingC(source_frame):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Gross Domestic Investment, 
    source_frame.iloc[:, 2]: Nominal Gross Domestic Product, 
    source_frame.iloc[:, 3]: Real Gross Domestic Product, 
    source_frame.iloc[:, 4]: M1
    '''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3], label = 'Real Gross Domestic Product')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5], label = '`Real` Gross Domestic Investment')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 4], label = 'Money Supply')
    plt.title('Indexes,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def dataFetchPlottingCensusD(series):
    '''series: List for Series'''
    for i in range(len(series)):
        title = fetchCensusDescription('census1975.zip', series[i])
        print('`{}` {}'.format(series[i], title))
    result_frame = fetchCensus('census1975.zip', series[0], True)
    result_frame = result_frame.div(result_frame.iloc[0, :]/100)
    for i in range(1, len(series)):
        current_frame = fetchCensus('census1975.zip', series[i], True)
        current_frame = current_frame.div(current_frame.iloc[0, :]/100)
        result_frame = pd.concat([result_frame, current_frame], axis = 1, sort = True)
        del current_frame
    plt.figure()
    plt.semilogy(result_frame)
    plt.title('Series P 231$-$300. Physical Output of Selected Manufactured Commodities: {}$-${}'.format(result_frame.index[0], result_frame.index[len(result_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend(series)
    plt.show()


def dataFetchPlottingCensusH():
    '''Census 1975,  Land in Farms'''
    result_frame = fetchCensus('census1975.zip', 'K0005', True)
    plt.figure()
    plt.plot(result_frame.index, result_frame.iloc[:, 0])
    plt.title('Land in Farms')
    plt.xlabel('Period')
    plt.ylabel('1, 000 acres')
    plt.grid()
    plt.show()


def dataFetchPlottingCensusK():
    '''Census Financial Markets & Institutions Series'''
    series = ['X0410', 'X0411', 'X0412', 'X0413', 'X0414', 'X0415', 'X0416', 'X0417', 'X0418', \
            'X0419', 'X0420', 'X0421', 'X0422', 'X0423', 'X0580', 'X0581', 'X0582', 'X0583', \
            'X0584', 'X0585', 'X0586', 'X0587', 'X0610', 'X0611', 'X0612', 'X0613', 'X0614', \
            'X0615', 'X0616', 'X0617', 'X0618', 'X0619', 'X0620', 'X0621', 'X0622', 'X0623', \
            'X0624', 'X0625', 'X0626', 'X0627', 'X0628', 'X0629', 'X0630', 'X0631', 'X0632', \
            'X0633', 'X0741', 'X0742', 'X0743', 'X0744', 'X0745', 'X0746', 'X0747', 'X0748', \
            'X0749', 'X0750', 'X0751', 'X0752', 'X0753', 'X0754', 'X0755', 'X0879', 'X0880', \
            'X0881', 'X0882', 'X0883', 'X0884', 'X0885', 'X0886', 'X0887', 'X0888', 'X0889', \
            'X0890', 'X0891', 'X0892', 'X0893', 'X0894', 'X0895', 'X0896', 'X0897', 'X0898', \
            'X0899', 'X0900', 'X0901', 'X0902', 'X0903', 'X0904', 'X0905', 'X0906', 'X0907', \
            'X0908', 'X0909', 'X0910', 'X0911', 'X0912', 'X0913', 'X0914', 'X0915', 'X0916', \
            'X0917', 'X0918', 'X0919', 'X0920', 'X0921', 'X0922', 'X0923', 'X0924', 'X0925', \
            'X0926', 'X0927', 'X0928', 'X0929', 'X0930', 'X0931', 'X0932', 'X0947', 'X0948', \
            'X0949', 'X0950', 'X0951', 'X0952', 'X0953', 'X0954', 'X0955', 'X0956']
    for i in range(len(series)):
        current_frame = fetchCensus('census1975.zip', series[i], True)
        current_frame = current_frame.div(current_frame.iloc[0, :]/100)
        title = fetchCensusDescription('census1975.zip', series[i])
        plt.figure(1+i)
        plt.plot(current_frame.index, current_frame.iloc[:, 0], label = '{}'.format(series[i]))
        plt.title('{},  {}$-${}'.format(title, current_frame.index[0], current_frame.index[len(current_frame)-1]))
        plt.xlabel('Period')
        plt.ylabel('Percentage')
        plt.grid(True)
        plt.legend()
        plt.show()
        del current_frame


def dataFetchPlottingD(source_frame):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Gross Domestic Investment, 
    source_frame.iloc[:, 2]: Gross Domestic Investment Price Index, 
    source_frame.iloc[:, 3]: Fixed Investment, 
    source_frame.iloc[:, 4]: Fixed Investment Price Index, 
    source_frame.iloc[:, 5]: Real Gross Domestic Product
    '''
    i = len(source_frame.iloc[:, 0])-1
    while abs(source_frame.iloc[i, 2]-100)>0.1:
        i- = 1
        base = i ##Basic Year
    '''Real Investment,  Billions'''
    source_frame['inv'] = source_frame.iloc[base, 1]*source_frame.iloc[:, 2].div(100*1000)
    '''Real Fixed Investment,  Billions'''
    source_frame['fnv'] = source_frame.iloc[base, 3]*source_frame.iloc[:, 4].div(100*1000)
    source_frame.iloc[:, 5] = source_frame.iloc[:, 5].div(1000)
    plt.figure(1)
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 6], label = 'Real Gross Private Domestic Investment $GPDI$')
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 7], color = 'red', label = 'Real Gross Private Fixed Investment,  Nonresidential $GPFI(n)$')
    plt.title('Real Indexes,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5])
    plt.title('Real Gross Domestic Product $GDP$,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 6], source_frame.iloc[:, 5])
    plt.title('$GPDI$ & $GPFI(n)$,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.iloc[:, 7], source_frame.iloc[:, 5])
    plt.title('$GPFI(n)$ & $GDP$,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame.iloc[:, 0])-1, 0]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.show()


def plotApproxLinear(source_frame):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Real Values for Price Deflator, 
    source_frame.iloc[:, 2]: Nominal Values for Price Deflator, 
    source_frame.iloc[:, 3]: Regressor, 
    source_frame.iloc[:, 4]: Regressand
    '''
    i = len(source_frame)-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 1])>1:
        i- = 1
        base = i ##Basic Year
    D = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]) ##Deflator
    result_frame = source_frame.iloc[:, 0] ##Data_frame for Based Linear Approximation Results
    calcul_frame = [] ##Blank List for Calculation Results
    for i in range(len(source_frame)):
        X = source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0])
        Y = source_frame.iloc[i, 4]*D[i]/(source_frame.iloc[0, 4]*D[0])
        calcul_frame.append({'X': X, 'Y': Y})
    del X, Y
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    S1, S2, S3, S4 = 0, 0, 0, 0 ##X, Y, X**2, XY ##Summarize
    for i in range(len(source_frame)):
        S1+ = source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0])
        S2+ = source_frame.iloc[i, 4]*D[i]/(source_frame.iloc[0, 4]*D[0])
        S3+ = (source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0]))**2
        S4+ = source_frame.iloc[i, 3]*source_frame.iloc[i, 4]*(D[i])**2/(source_frame.iloc[0, 3]*source_frame.iloc[0, 4]*(D[0]**2))
    '''Approximation'''
    A0 = (S2*S3-S1*S4)/(len(source_frame)*S3-S1**2)
    A1 = (len(source_frame)*S4-S1*S2)/(len(source_frame)*S3-S1**2)
    calcul_frame = [] ##Blank List for Calculation Results
    for i in range(len(source_frame)):
        Y = A0+A1*source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0])
        calcul_frame.append({'YH': Y})
    del Y
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    print('Period From: {} Through: {}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    print('Prices: {} = 100'.format(source_frame.iloc[base, 0]))
    print('Model: Yhat = {:.4f}+{:.4f}*X'.format(A0, A1))
    print('Model Parameter: A0 = {:.4f}'.format(A0))
    print('Model Parameter: A1 = {:.4f}'.format(A1))
    plt.figure()
    plt.title('$Y(X)$,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Gross Private Domestic Investment,  $X(\\tau)$,  {} = 100,  {} = 100'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0]))
    plt.ylabel('Gross Domestic Product,  $Y(\\tau)$,  {} = 100,  {} = 100'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0]))
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 2])
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 3], label = '$\\hat Y = {:.4f}+{:.4f}X$'.format(A0, A1))
    plt.grid(True)
    plt.legend()
    plt.show()


def plotApproxLogLinear(source_frame):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Real Values for Price Deflator, 
    source_frame.iloc[:, 2]: Nominal Values for Price Deflator, 
    source_frame.iloc[:, 3]: Regressor, 
    source_frame.iloc[:, 4]: Regressand
    '''
    i = len(source_frame)-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 1])>1:
        i- = 1
        base = i ##Basic Year
    D = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]) ##Deflator
    result_frame = source_frame.iloc[:, 0] ##Data_frame for Based Log-Linear Approximation Results
    calcul_frame = [] ##Blank List for Calculation Results
    import math
    for i in range(len(source_frame)):
        X = math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3])
        Y = math.log(source_frame.iloc[i, 4])+math.log(D[i])-math.log(source_frame.iloc[0, 4])-math.log(D[0])
        calcul_frame.append({'X': X, 'Y': Y})
    del X, Y
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    S1, S2, S3, S4 = 0, 0, 0, 0 ##Summarize
    for i in range(len(source_frame)):
        S1+ = math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3])
        S2+ = math.log(source_frame.iloc[i, 4])+math.log(D[i])-math.log(source_frame.iloc[0, 4])-math.log(D[0])
        S3+ = (math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3]))**2
        S4+ = (math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3]))*(math.log(D[i])+math.log(source_frame.iloc[i, 4])-math.log(D[0])-math.log(source_frame.iloc[0, 4]))
    '''Approximation'''
    A0 = (S2*S3-S1*S4)/(len(source_frame)*S3-S1**2)
    A1 = (len(source_frame)*S4-S1*S2)/(len(source_frame)*S3-S1**2)
    calcul_frame = [] ##Blank List for Calculation Results
    for i in range(len(source_frame)):
        Y = A0+A1*(math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3])) ##Yhat
        calcul_frame.append({'YH': Y})
    del Y
    calcul_frame = pd.Data_frame(calcul_frame) ##Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis = 1, sort = True)
    del calcul_frame
    print('Period From: {} Through: {}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    print('Prices: {} = 100'.format(source_frame.iloc[base, 0]))
    print('Model: Yhat = {:.4f}+{:.4f}*Ln(X)'.format(A0, A1))
    print('Model Parameter: A0 = {:.4f}'.format(A0))
    print('Model Parameter: A1 = {:.4f}'.format(A1))
    plt.figure()
    plt.title('$Y(X)$,  {} = 100,  {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Logarithm Prime Rate,  $X(\\tau)$,  {} = 100'.format(source_frame.iloc[0, 0]))
    if source_frame.columns[4][:7] == 'A032RC1':
        desc = 'National Income'
    elif source_frame.columns[4][:7] == 'A191RC1':
        desc = 'Gross Domestic Product'
    plt.ylabel('Logarithm {},  $Y(\\tau)$,  {} = 100,  {} = 100'.format(desc, source_frame.iloc[base, 0], source_frame.iloc[0, 0]))
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 2])
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 3], label = '$\\hat Y = {:.4f}+{:.4f}X$'.format(A0, A1))
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


def plotBuiltin(module):
    source_frame = pd.read_csv('datasetAutocorrelation.txt')
    source_frame = source_frame[source_frame.columns[[1, 0, 2]]]
    series = source_frame.iloc[:, 0].sort_values().unique()
    del source_frame
    for i in range(len(series)):
        current = fetchWorldBank('datasetAutocorrelation.txt', series[i])
        plt.figure(1+i)
        module(current.iloc[:, 1])
        plt.grid(True)
        del current
    del series
    source_frame = pd.read_csv('CHN_TUR_GDP.zip')
    source_frame = source_frame[source_frame.columns[[1, 0, 2]]]
    series = source_frame.iloc[:, 0].sort_values().unique()
    del source_frame
    for i in range(len(series)):
        current = fetchWorldBank('CHN_TUR_GDP.zip', series[i])
        plt.figure(5+i)
        module(current.iloc[:, 1])
        plt.grid(True)
        del current
    del series
    plt.show()


def plotCapitalModelling(source_frame, base):
    '''
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Investment, 
    source_frame.iloc[:, 2]: Production, 
    source_frame.iloc[:, 3]: Capital, 
    source_frame.iloc[:, 4]: Capital Retirement
    '''
    QS = sp.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]), 1)
    QL = sp.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 2].div(source_frame.iloc[:, 3]), 1)
    '''Gross Fixed Investment to Gross Domestic Product Ratio'''
    S = QS[1]+QS[0]*source_frame.iloc[:, 0]
    '''Fixed Assets Turnover'''
    L = QL[1]+QL[0]*source_frame.iloc[:, 0]
    KA = capital(source_frame, QS[1], QS[0], QL[1], QL[0], 0.875)
    KB = capital(source_frame, QS[1], QS[0], QL[1], QL[0], 1)
    KC = capital(source_frame, QS[1], QS[0], QL[1], QL[0], 1.125)
    plt.figure(1)
    plt.title('Fixed Assets Turnover ($\\lambda$) for the US,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 2].div(source_frame.iloc[:, 3]), label = '$\\lambda$')
    if QL[0]<0:
        plt.plot(source_frame.iloc[:, 0], L, label = '$\\lambda = {1:, .4f}\\ {0:, .4f}\\times t$'.format(QL[0], QL[1]))
    else:
        plt.plot(source_frame.iloc[:, 0], L, label = '$\\lambda = {1:, .4f} + {0:, .4f} \\times t$'.format(QL[0], QL[1]))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Gross Fixed Investment as Percentage of GDP ($S$) for the US,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]), label = '$S$')
    if QS[0]<0:
        plt.plot(source_frame.iloc[:, 0], S, label = '$S = {1:, .4f}\\ {0:, .4f}\\times t$'.format(QS[0], QS[1]))
    else:
        plt.plot(source_frame.iloc[:, 0], S, label = '$S = {1:, .4f} + {0:, .4f} \\times t$'.format(QS[0], QS[1]))
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.title('$\\alpha$ for the US,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-2, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 4], label = '$\\alpha$')
    plt.grid(True)
    plt.legend()
    plt.figure(4)
    plt.title('$K$ for the US,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-2, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars,  {} = 100'.format(source_frame.iloc[base, 0]))
    plt.semilogy(source_frame.iloc[:, 0], KA, label = '$K\\left(\\pi = \\frac{7}{8}\\right)$')
    plt.semilogy(source_frame.iloc[:, 0], KB, label = '$K\\left(\\pi = 1\\right)$')
    plt.semilogy(source_frame.iloc[:, 0], KC, label = '$K\\left(\\pi = \\frac{9}{8}\\right)$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotDiscreteFourier(source_frame, precision = 10):
    '''
    source_frame.iloc[:, 0]: Period;
    source_frame.iloc[:, 1]: Series
    Discrete Fourier Transform based on Simpson's Rule
    '''
    f1p = sp.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1], 1)
    LX = f1p[1]+f1p[0]*source_frame.iloc[:, 0]
    Q = [] ##Blank List for Fourier Coefficients
    for i in range(1+precision):
        c = 2*(source_frame.iloc[:, 1]-LX)*sp.cos(2*sp.pi*i*(source_frame.iloc[:, 0]-source_frame.iloc[0, 0]).div(len(source_frame)))
        s = 2*(source_frame.iloc[:, 1]-LX)*sp.sin(2*sp.pi*i*(source_frame.iloc[:, 0]-source_frame.iloc[0, 0]).div(len(source_frame)))
        Q.append({'cos': c.mean(),  'sin': s.mean()})
    del c, s
    Q = pd.Data_frame(Q) ##Convert List to Dataframe
    Q['cos'][0] = Q['cos'][0]/2
    EX = pd.Data_frame(1, index = range(1+len(source_frame)), columns = ['EX'])
    EX = Q['cos'][0]
    plt.figure()
    plt.title('$\\alpha$ for the US,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 1], label = '$\\alpha$')
    for i in range(1, 1+precision):
        EX = EX+Q['cos'][i]*sp.cos(2*sp.pi*i*(source_frame.iloc[:, 0]-source_frame.iloc[0, 0]).div(len(source_frame)))+Q['sin'][i]*sp.sin(2*sp.pi*i*(source_frame.iloc[:, 0]-source_frame.iloc[0, 0]).div(len(source_frame)))
        plt.plot(source_frame.iloc[:, 0], LX+EX, label = '$FT_{{{:02}}}(\\alpha)$'.format(i))
    plt.grid(True)
    plt.legend()
    plt.show()


def plotDouglas(source, dictionary, num, start, stop, step, title, measure, label = None):
    '''
    source: Source Database, 
    dictionary: Dictionary of Series Codes to Series Titles from Source Database, 
    num: Plot Number, 
    start: Start Series Code, 
    stop: Stop Series Code, 
    step: Step for Series Codes, 
    title: Plot Title, 
    measure: Dimenstion for Series, 
    label: Additional Sublabels'''
    plt.figure(num)
    for i in range(start, stop, step):
        plt.plot(fetchClassic(source, dictionary.iloc[i, 0]), label = dictionary.iloc[i, 1])
    plt.title(title)
    plt.xlabel('Period')
    plt.ylabel(measure)
    plt.grid(True)
    if label == None:
        plt.legend()
    else:
        plt.legend(label)


def plotElasticity(source):
    '''
    source.iloc[:, 0]: Period, 
    source.iloc[:, 1]: Real Values for Price Deflator, 
    source.iloc[:, 2]: Nominal Values for Price Deflator, 
    source.iloc[:, 3]: Focused Series
    '''
    if source.columns[3] == 'A032RC1':
        desc = 'National Income'
    else:
        desc = 'Series'
    i = len(source)-1
    while abs(source.iloc[i, 2]-source.iloc[i, 1])>1:
        i- = 1
        base = i
    source['ser'] = source.iloc[:, 1]*source.iloc[:, 3].div(source.iloc[:, 2])
    source['sma'] = source.iloc[:, 4].rolling(window = 2).mean() ##source['sma'] = (source.iloc[:, 4]+source.iloc[:, 4].shift(1))/2
    source['ela'] = 2*(source.iloc[:, 4]-source.iloc[:, 4].shift(1)).div(source.iloc[:, 4]+source.iloc[:, 4].shift(1))
    source['elb'] = (source.iloc[:, 4].shift(-1)-source.iloc[:, 4].shift(1)).div(2*source.iloc[:, 4])
    source['elc'] = 2*(source.iloc[:, 4].shift(-1)-source.iloc[:, 4].shift(1)).div(source.iloc[:, 4].shift(1)+2*source.iloc[:, 4]+source.iloc[:, 4].shift(-1))
    source['eld'] = (-source.iloc[:, 4].shift(1)-source.iloc[:, 4]+source.iloc[:, 4].shift(-1)+source.iloc[:, 4].shift(-2)).div(2*source.iloc[:, 4]+2*source.iloc[:, 4].shift(-1))
    result_frame = source[source.columns[[0, 4, 5, 6, 7, 8, 9]]]
    plt.figure(1)
    plt.title('{},  {},  {} = 100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars,  {} = 100'.format(result_frame.iloc[base, 0]))
    plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 1], label = '{}'.format(source.columns[3]))
    plt.plot(result_frame.iloc[:, 0].rolling(window = 2).mean(), result_frame.iloc[:, 2], label = 'A032RC1,  Rolling Mean,  Window = 2')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Elasticity: {},  {},  {} = 100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(result_frame.iloc[:, 0].rolling(window = 2).mean(), result_frame.iloc[:, 3], label = '$\\overline{E}_{T+\\frac{1}{2}}$')
    plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 4], label = '$E_{T+1}$')
    plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 5], label = '$\\overline{E}_{T+1}$')
    plt.plot(result_frame.iloc[:, 0].rolling(window = 2).mean(), result_frame.iloc[:, 6], label = '$\\overline{\\epsilon(E_{T+\\frac{1}{2}})}$')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.title('Elasticity: {},  {},  {} = 100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.xlabel('{},  {},  {} = 100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.ylabel('Elasticity: {},  {},  {} = 100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 6], label = '$\\frac{\\epsilon(X)}{X}$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotGrowthElasticity(source_frame):
    '''Growth Elasticity Plotting
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Series
    '''
    resultList = [] ##Create List Results
    for i in range(len(source_frame)-3):
        '''
        `Period`: Period,  Centered
        `ValueA`: Value,  Centered
        `ValueB`: Value,  Growth Rate
        `ValueC`: Value,  Elasticity
        '''
        resultList.append({'Period': (source_frame.iloc[1+i, 0]+source_frame.iloc[2+i, 0])/2, \
                           'ValueA': (source_frame.iloc[1+i, 1]+source_frame.iloc[2+i, 1])/2, \
                           'ValueB': (source_frame.iloc[2+i, 1]-source_frame.iloc[i, 1])/(source_frame.iloc[i, 1]+source_frame.iloc[1+i, 1]), \
                           'ValueC': (source_frame.iloc[2+i, 1]+source_frame.iloc[3+i, 1]-source_frame.iloc[i, 1]-source_frame.iloc[1+i, 1])/(source_frame.iloc[i, 1]+source_frame.iloc[1+i, 1]+source_frame.iloc[2+i, 1]+source_frame.iloc[3+i, 1])})
    result_frame = pd.Data_frame(resultList) ##Convert List to Dataframe
    del resultList
    result_frame = result_frame.set_index('Period')
    plt.figure()
    result_frame.iloc[:, 1].plot(label = 'Growth Rate')
    result_frame.iloc[:, 2].plot(label = 'Elasticity Rate')
    plt.title('Growth & Elasticity Rates')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotKZF(source_frame):
    '''Kolmogorov--Zurbenko Filter
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Series'''
    import scipy.special
    '''Data_frame for Kolmogorov--Zurbenko Filter Results'''
    result_frameA = source_frame
    '''Data_frame for Kolmogorov--Zurbenko Filter Residuals'''
    result_frameB = pd.concat([source_frame.iloc[:, 0], source_frame.iloc[:, 0].rolling(window = 2).mean()], axis = 1, sort = False)
    result_frameB = pd.concat([result_frameB, (source_frame.iloc[:, 1]-source_frame.iloc[:, 1].shift(1)).div(source_frame.iloc[:, 1].shift(1))], axis = 1, sort = False)
    for k in range(1, 1+len(source_frame)//2):
        cap = 'col{:02d}'.format(k)
        result_frameA[cap] = sp.nan
        for j in range(1, 1+len(source_frame)-k):
            vkz = 0
            for i in range(1+k):
                vkz+ = result_frameA.iloc[i+j-1, 1]*scipy.special.binom(k, i)/(2**k)
            result_frameA.iloc[i+j-(k//2)-1, 1+k] = vkz
        if k%2 == 0:
            result_frameB = pd.concat([result_frameB, (source_frame.iloc[:, 1+k]-source_frame.iloc[:, 1+k].shift(1)).div(source_frame.iloc[:, 1+k].shift(1))], axis = 1, sort = False)
        else:
            result_frameB = pd.concat([result_frameB, (source_frame.iloc[:, 1+k].shift(-1)-source_frame.iloc[:, 1+k]).div(source_frame.iloc[:, 1+k])], axis = 1, sort = False)
    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(result_frameA.iloc[:, 0], result_frameA.iloc[:, 1], label = 'Original Series')
    for i in range(2, 1+len(source_frame)//2):
        if i%2 == 0:
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
        if i%2 == 0:
            plt.plot(result_frameB.iloc[:, 1], result_frameB.iloc[:, i], label = '$\\delta KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frameB.iloc[:, 0], result_frameB.iloc[:, i], label = '$\\delta KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
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
    plt.plot(source_frame.index, PP, label = '$\\hat Y = %fX^{%f},  R^2 = %.4f$' %(sp.exp(yp1p[1]), yp1p[0], r20))
    plt.plot(source_frame.index, YAA, label = '$\\hat P_{%d}(X) = %.2f+%.2fX,  R^2 = %.4f$' %(1, yl1p[1], yl1p[0], r21))
    plt.plot(source_frame.index, YBB, label = '$\\hat P_{%d}(X) = %.2f+%.2fX %.2fX^2,  R^2 = %.4f$' %(2, yl2p[2], yl2p[1], yl2p[0], r22))
    plt.plot(source_frame.index, YCC, label = '$\\hat P_{%d}(X) = %.2f+%.2fX %.2fX^2+%.2fX^3,  R^2 = %.4f$' %(3, yl3p[3], yl3p[2], yl3p[1], yl3p[0], r23))
    plt.plot(source_frame.index, YDD, label = '$\\hat P_{%d}(X) = %.2f+%.2fX %.2fX^2+%.2fX^3 %.2fX^4,  R^2 = %.4f$' %(4, yl4p[4], yl4p[3], yl4p[2], yl4p[1], yl4p[0], r24))
    plt.title('Labor Capital Intensity & Labor Productivity,  {}$-${}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.plot(source_frame.index, DPP, ':', label = '$\\|\\frac{\\hat Y-Y}{Y}\\|,  \\bar S = %.4f$' %(100*DPP.mean()) +'%')
    plt.plot(source_frame.index, DYAA, ':', label = '$\\|\\frac{\\hat P_{%d}(X)-Y}{Y}\\|,  \\bar S = %.4f$' %(1, 100*DYAA.mean()) +'%')
    plt.plot(source_frame.index, DYBB, ':', label = '$\\|\\frac{\\hat P_{%d}(X)-Y}{Y}\\|,  \\bar S = %.4f$' %(2, 100*DYBB.mean()) +'%')
    plt.plot(source_frame.index, DYCC, ':', label = '$\\|\\frac{\\hat P_{%d}(X)-Y}{Y}\\|,  \\bar S = %.4f$' %(3, 100*DYCC.mean()) +'%')
    plt.plot(source_frame.index, DYDD, ':', label = '$\\|\\frac{\\hat P_{%d}(X)-Y}{Y}\\|,  \\bar S = %.4f$' %(4, 100*DYDD.mean()) +'%')
    plt.title('Deltas of Labor Capital Intensity & Labor Productivity,  {}$-${}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotPearsonRTest(source_frame):
    '''Left-Side & Right-Side Rolling Means' Calculation & Plotting
    source_frame.index: Period, 
    source_frame.iloc[:, 0]: Series'''
    from scipy import stats
    result_frame = pd.Data_frame(columns = ['window'])
    for i in range(1+len(source_frame)//2):
        '''Shift Mean Values to Left'''
        L_frame = source_frame.iloc[:, 0].rolling(window = 1+i).mean().shift(-i)
        '''Shift Mean Values to Right'''
        R_frame = source_frame.iloc[:, 0].rolling(window = 1+i).mean()
        numerator = stats.pearsonr(source_frame.iloc[:, 0][R_frame.notna()].tolist(), R_frame.dropna().tolist())[0]
        denominator = stats.pearsonr(source_frame.iloc[:, 0][L_frame.notna()].tolist(), L_frame.dropna().tolist())[0]
        result_frame = result_frame.append({'window':numerator/denominator}, ignore_index = True)
    '''Plot 'Window' to 'Right-Side to Left-Side Pearson R'''
    plt.figure()
    plt.title('Right-Side to Left-Side Pearson R Ratio')
    plt.xlabel('`Window`')
    plt.ylabel('Index')
    plt.plot(result_frame, label = 'Right-Side to Left-Side Pearson R Ratio')
    plt.grid(True)
    plt.legend()
    plt.show()


def plotRMF(source_frame):
    '''
    source_frame.iloc[:, 0]: Period;
    source_frame.iloc[:, 1]: Series
    Rolling Mean Filter'''
    plt.figure(1)
    plt.title('Moving Average {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    source_frame['sma'] = source_frame.iloc[:, 1].rolling(window = 1, center = True).mean()
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 2], label = '$Y$')
    '''Smoothed Series Calculation'''
    for i in range(1, len(source_frame)//2):
        source_frame.iloc[:, 2] = source_frame.iloc[:, 1].rolling(window = 1+i, center = True).mean()
        if i%2 == 0:
            plt.plot(0.5+source_frame.iloc[:, 0], source_frame.iloc[:, 2], label = '$\\bar Y_{{m = {}}}$'.format(i))
        else:
            plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 2], label = '$\\bar Y_{{m = {}}}$'.format(i))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Moving Average Deviations {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Deviations ($\\delta$),  Percent')
    source_frame['del'] = (source_frame.iloc[:, 1].rolling(window = 1, center = True).mean().shift(-1)-source_frame.iloc[:, 1].rolling(window = 1, center = True).mean()).div(source_frame.iloc[:, 1].rolling(window = 1, center = True).mean())
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 3], label = '$\\delta(Y)$')
    '''Deviations Calculation'''
    for i in range(1, len(source_frame)//2):
        source_frame.iloc[:, 3] = (source_frame.iloc[:, 1].rolling(window = 1+i, center = True).mean().shift(-1)-source_frame.iloc[:, 1].rolling(window = 1+i, center = True).mean()).div(source_frame.iloc[:, 1].rolling(window = 1+i, center = True).mean())
        if i%2 == 0:
            plt.plot(0.5+source_frame.iloc[:, 0], source_frame.iloc[:, 3], label = '$\\delta(\\bar Y_{{m = {}}})$'.format(i))
        else:
            plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3], label = '$\\delta(\\bar Y_{{m = {}}})$'.format(i))
    plt.grid(True)
    plt.legend()
    plt.show()


def plotSES(source_frame, window, step):
    '''Single Exponential Smoothing
    Robert Goodell Brown,  1956
    source_frame.iloc[:, 0]: Period, 
    source_frame.iloc[:, 1]: Series'''
    '''Average of Window-First Entries'''
    S = source_frame.iloc[:window, 1].mean()
    '''Data_frame for Exponentially Smoothed Series'''
    smooth_frame = pd.Data_frame(source_frame.iloc[:, 0])
    '''Data_frame for Deltas of Exponentially Smoothed Series'''
    deltas_frame = pd.Data_frame(0.5+source_frame.iloc[:(len(source_frame)-1), 0])
    delta = (source_frame.iloc[:, 1].shift(-1)-source_frame.iloc[:, 1]).div(source_frame.iloc[:, 1].shift(-1))
    delta = delta[:(len(delta)-1)]
    deltas_frame = pd.concat([deltas_frame, delta], axis = 1, sort = False)
    plt.figure()
    plt.title('Deltas of Exponentially Smoothed Series')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 1], label = 'Original Series')
    k = 0
    while True:
        k+ = 1
        alpha = 0.25+step*(k-1)
        ses, dse = [], []
        ses.append(alpha*source_frame.iloc[0, 1]+(1-alpha)*S)
        for i in range(1, len(source_frame)):
            ses.append(alpha*source_frame.iloc[i, 1]+(1-alpha)*ses[i-1])
            dse.append((ses[i]-ses[i-1])/ses[i-1])
            cap = 'col{:02d}'.format(k)
        ses = pd.Data_frame(ses, columns = [cap])
        dse = pd.Data_frame(dse, columns = [cap])
        smooth_frame = pd.concat([smooth_frame, ses], axis = 1, sort = False)
        deltas_frame = pd.concat([deltas_frame, dse], axis = 1, sort = False)
        plt.plot(source_frame.iloc[:, 0], ses, label = 'Smoothing: $w = {},  \\alpha = {:, .2f}$'.format(window, alpha))
        del ses, dse
        if k> = 0.5+0.75/step: ## 0.25+step*(k-0.5)> = 1
            break
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
    plt.title('Model: $\\hat Y = %f+%f\\times X$,  %d$-$%d' %(coef1, coef2, source_frame.index[0], source_frame.index[len(source_frame)-1]))
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
    plt.title('Model: $\\ln(\\hat Y) = %f+%f\\times \\ln(X)$,  %d$-$%d' %(coef1, coef2, source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('$\\hat Y = \\ln(Labor\ Productivity)$,  $X = \\ln(Labor\ Capital\ Intensity)$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plottingCensusA(source_frame, base):
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], label = 'Fabricant S.,  Shiskin J.,  NBER')
    plt.plot(source_frame.iloc[:, 1], color = 'red', linewidth = 4, label = 'W.M. Persons')
    plt.plot(source_frame.iloc[:, 2], label = 'E. Frickey')
    plt.axvline(x = source_frame.index[base], linestyle = ':')
    plt.title('US Manufacturing Indexes Of Physical Production Of Manufacturing,  {} = 100'.format(source_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plottingCensusB(capital_frame, deflator_frame):
    '''Census Manufacturing Fixed Assets Series'''
    plt.figure(1)
    plt.semilogy(capital_frame.iloc[:, 0], label = 'Total')
    plt.semilogy(capital_frame.iloc[:, 1], label = 'Structures')
    plt.semilogy(capital_frame.iloc[:, 2], label = 'Equipment')
    plt.title('Manufacturing Fixed Assets,  {}$-${}'.format(capital_frame.index[0], capital_frame.index[len(capital_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(deflator_frame)
    plt.title('Census Fused Capital Deflator,  {}$-${}'.format(deflator_frame.index[0], deflator_frame.index[len(deflator_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.show()


def plottingCensusC(source_frame, base):
    plt.figure(1)
    plt.semilogy(source_frame.index, source_frame.iloc[:, 1], label = 'P265 - Raw Steel Produced - Total,  {} = 100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 2], label = 'P266 - Raw Steel Produced - Bessemer,  {} = 100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 3], label = 'P267 - Raw Steel Produced - Open Hearth,  {} = 100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 4], label = 'P268 - Raw Steel Produced - Crucible,  {} = 100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 5], label = 'P269 - Raw Steel Produced - Electric and All Other,  {} = 100'.format(source_frame.index[base[2]]))
    plt.axvline(x = source_frame.index[base[0]], linestyle = ':')
    plt.axvline(x = source_frame.index[base[2]], linestyle = ':')
    plt.title('Steel Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.semilogy(source_frame.index, source_frame.iloc[:, 0], label = 'P262 - Rails Produced,  {} = 100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 6], label = 'P293 - Locomotives Produced,  {} = 100'.format(source_frame.index[base[1]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 7], label = 'P294 - Railroad Passenger Cars Produced,  {} = 100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 8], label = 'P295 - Railroad Freight Cars Produced,  {} = 100'.format(source_frame.index[base[0]]))
    plt.axvline(x = source_frame.index[base[0]], linestyle = ':')
    plt.axvline(x = source_frame.index[base[1]], linestyle = ':')
    plt.title('Rails & Cars Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plottingCensusE(source_frame):
    plt.figure()
    plt.plot(source_frame.index, source_frame.iloc[:, 0])
    plt.title('Total Immigration,  {}$-${}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Period')
    plt.ylabel('People')
    plt.grid()
    plt.show()


def plottingCensusFA(source_frame):
    plt.figure(1)
    source_frame.iloc[:, 1].plot()
    plt.title('Unemployment,  Percent of Civilian Labor Force')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 2], label = 'Bureau of Labour')
    plt.plot(source_frame.iloc[:, 3], label = 'Wolman')
    plt.title('All Manufacturing,  Average Full-Time Weekly Hours,  1890-1899 = 100')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.figure(3)
    source_frame.iloc[:, 6].plot()
    plt.title('Implicit Number of Workers')
    plt.xlabel('Period')
    plt.ylabel('Persons')
    plt.grid()
    plt.show()


def plottingCensusFB(source_frame):
    fig,  axA  =  plt.subplots()
    color  =  'tab:red'
    axA.set_xlabel('Period')
    axA.set_ylabel('Number',  color = color)
    axA.plot(source_frame.index,  source_frame.iloc[:, 4],  color = color,  label = 'Stoppages')
    axA.set_title('Work Conflicts')
    axA.grid()
    axA.legend(loc = 2)
    axA.tick_params(axis = 'y',  labelcolor = color)
    axB  =  axA.twinx()
    color  =  'tab:blue'
    axB.set_ylabel('1, 000 People',  color = color)
    axB.plot(source_frame.index,  source_frame.iloc[:, 5],  color = color,  label = 'Workers Involved')
    axB.legend(loc = 1)
    axB.tick_params(axis = 'y',  labelcolor = color)
    fig.tight_layout()
    plt.show()


def plottingCensusG(source_frame):
    plt.figure()
    plt.plot(source_frame.index, source_frame.iloc[:, 0], label = 'Gross National Product')
    plt.plot(source_frame.index, source_frame.iloc[:, 1], label = 'Gross National Product Per Capita')
    plt.title('Gross National Product,  Prices {} = 100,  {} = 100'.format(1958, source_frame.index[0]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plottingCensusI(source_frameA, source_frameB, source_frameC):
    plt.figure(1)
    plt.plot(source_frameA.iloc[:, 0], label = 'Exports,  U1')
    plt.plot(source_frameA.iloc[:, 1], label = 'Imports,  U8')
    plt.plot(source_frameA.iloc[:, 0].sub(source_frameA.iloc[:, 1]), label = 'Net Exports')
    plt.title('Exports & Imports of Goods and Services,  {}$-${}'.format(source_frameA.index[0], source_frameA.index[len(source_frameA)-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(source_frameB.iloc[:, 0], label = 'Exports,  U187')
    plt.plot(source_frameB.iloc[:, 1], label = 'Imports,  U188')
    plt.plot(source_frameB.iloc[:, 2], label = 'Net Exports,  U189')
    plt.title('Total Merchandise,  Gold and Silver,  {}$-${}'.format(source_frameB.index[0], source_frameB.index[len(source_frameB)-1]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.plot(source_frameC.iloc[:, 0].sub(source_frameC.iloc[:, 14]), label = 'America-Canada')
    plt.plot(source_frameC.iloc[:, 1].sub(source_frameC.iloc[:, 15]), label = 'America-Cuba')
    plt.plot(source_frameC.iloc[:, 2].sub(source_frameC.iloc[:, 16]), label = 'America-Mexico')
    plt.plot(source_frameC.iloc[:, 3].sub(source_frameC.iloc[:, 17]), label = 'America-Brazil')
    plt.plot(source_frameC.iloc[:, 4].sub(source_frameC.iloc[:, 18]), label = 'America-Other')
    plt.plot(source_frameC.iloc[:, 5].sub(source_frameC.iloc[:, 19]), label = 'Europe-United Kingdom')
    plt.plot(source_frameC.iloc[:, 6].sub(source_frameC.iloc[:, 20]), label = 'Europe-France')
    plt.plot(source_frameC.iloc[:, 7].sub(source_frameC.iloc[:, 21]), label = 'Europe-Germany')
    plt.plot(source_frameC.iloc[:, 8].sub(source_frameC.iloc[:, 22]), label = 'Europe-Other')
    plt.plot(source_frameC.iloc[:, 9].sub(source_frameC.iloc[:, 23]), label = 'Asia-Mainland China')
    plt.plot(source_frameC.iloc[:, 10].sub(source_frameC.iloc[:, 24]), label = 'Asia-Japan')
    plt.plot(source_frameC.iloc[:, 11].sub(source_frameC.iloc[:, 25]), label = 'Asia-Other')
    plt.plot(source_frameC.iloc[:, 12].sub(source_frameC.iloc[:, 26]), label = 'Australia and Oceania-All')
    plt.plot(source_frameC.iloc[:, 13].sub(source_frameC.iloc[:, 27]), label = 'Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(4)
    plt.plot(source_frameC.iloc[:, 0].sub(source_frameC.iloc[:, 14]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'America-Canada')
    plt.plot(source_frameC.iloc[:, 1].sub(source_frameC.iloc[:, 15]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'America-Cuba')
    plt.plot(source_frameC.iloc[:, 2].sub(source_frameC.iloc[:, 16]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'America-Mexico')
    plt.plot(source_frameC.iloc[:, 3].sub(source_frameC.iloc[:, 17]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'America-Brazil')
    plt.plot(source_frameC.iloc[:, 4].sub(source_frameC.iloc[:, 18]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'America-Other')
    plt.plot(source_frameC.iloc[:, 5].sub(source_frameC.iloc[:, 19]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'Europe-United Kingdom')
    plt.plot(source_frameC.iloc[:, 6].sub(source_frameC.iloc[:, 20]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'Europe-France')
    plt.plot(source_frameC.iloc[:, 7].sub(source_frameC.iloc[:, 21]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'Europe-Germany')
    plt.plot(source_frameC.iloc[:, 8].sub(source_frameC.iloc[:, 22]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'Europe-Other')
    plt.plot(source_frameC.iloc[:, 9].sub(source_frameC.iloc[:, 23]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'Asia-Mainland China')
    plt.plot(source_frameC.iloc[:, 10].sub(source_frameC.iloc[:, 24]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'Asia-Japan')
    plt.plot(source_frameC.iloc[:, 11].sub(source_frameC.iloc[:, 25]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'Asia-Other')
    plt.plot(source_frameC.iloc[:, 12].sub(source_frameC.iloc[:, 26]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'Australia and Oceania-All')
    plt.plot(source_frameC.iloc[:, 13].sub(source_frameC.iloc[:, 27]).div(source_frameC.iloc[:, 28].sub(source_frameC.iloc[:, 29])), label = 'Africa-All')
    plt.title('Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plottingCensusJ(source_frame, base):
    plt.figure()
    plt.semilogy(source_frame.index, source_frame.iloc[:, 0], label = 'Currency Held by the Public')
    plt.semilogy(source_frame.index, source_frame.iloc[:, 1], label = 'M1 Money Supply (Currency Plus Demand Deposits)')
    plt.semilogy(source_frame.index, source_frame.iloc[:, 2], label = 'M2 Money Supply (M1 Plus Time Deposits)')
    plt.axvline(x = source_frame.index[base], linestyle = ':')
    plt.title('Currency Dynamics,  {} = 100'.format(source_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plottingE(source_frame):
    '''
    source_frame.iloc[:, 0]: Investment, 
    source_frame.iloc[:, 1]: Production, 
    source_frame.iloc[:, 2]: Capital
    '''
    '''Investment to Production Ratio'''
    source_frame['S'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    '''Fixed Assets Turnover Ratio'''
    source_frame['L'] = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2])
    QS = sp.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1], 1)
    QL = sp.polyfit(source_frame.iloc[:, 1], source_frame.iloc[:, 2], 1)
    source_frame['RS'] = QS[1]+QS[0]*source_frame.iloc[:, 0]
    source_frame['RL'] = QL[1]+QL[0]*source_frame.iloc[:, 2]
    plt.figure()
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 1])
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 5])
    plt.title('Investment to Production Ratio,  {}$-${}'.format(source_frame.index[0], source_frame.index[len(source_frame)-1]))
    plt.xlabel('Investment,  Billions of Dollars')
    plt.ylabel('Gross Domestic Product,  Billions of Dollars')
    plt.grid(True)
    plt.legend(['$P(I)$', '$\\hat P(I) = %.4f+%.4f I$' %(QS[1], QS[0])])
    print(source_frame.iloc[:, 3].describe())
    print(QS)
    print(source_frame.iloc[:, 4].describe())
    print(QL)
    plt.show()


def plottingF(source_frameA, source_frameB, source_frameC, source_frameD):
    '''
    source_frameA: Production _frame, 
    source_frameB: Labor _frame, 
    source_frameC: Capital _frame, 
    source_frameD: Capacity Utilization _frame'''
    base = [31, 1]
    '''Plotting'''
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(source_frameA.index, source_frameA.iloc[:, 0], label = 'Kurenkov Data,  {} = 100'.format(source_frameA.index[base[0]]))
    axs[0].plot(source_frameA.index, source_frameA.iloc[:, 1], label = 'BEA Data,  {} = 100'.format(source_frameA.index[base[0]]))
    axs[0].plot(source_frameA.index, source_frameA.iloc[:, 2], label = 'FRB Data,  {} = 100'.format(source_frameA.index[base[0]]))
    axs[0].set_title('Production')
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Percentage')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(source_frameB.index, source_frameB.iloc[:, 0], label = 'Kurenkov Data')
    axs[1].plot(source_frameB.index, source_frameB.iloc[:, 1], label = 'BEA Data')
    axs[1].set_title('Labor')
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Thousands of Persons')
    axs[1].legend()
    axs[1].grid(True)
    '''Revised Capital'''
    axs[2].plot(source_frameC.index, source_frameC.iloc[:, 0], label = 'Kurenkov Data,  {} = 100'.format(source_frameC.index[base[1]]))
    axs[2].plot(source_frameC.index, source_frameC.iloc[:, 1], label = 'BEA Data,  {} = 100'.format(source_frameC.index[base[1]]))
    axs[2].set_title('Capital')
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage')
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(source_frameD.index, source_frameD.iloc[:, 0], label = 'Kurenkov Data')
    axs[3].plot(source_frameD.index, source_frameD.iloc[:, 1], label = 'FRB Data')
    axs[3].set_title('Capacity Utilization')
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage')
    axs[3].legend()
    axs[3].grid(True)
    fig.set_size_inches(10., 20.)


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
    plt.plot(source_frame.iloc[:, 0], K1, label = '$\\hat K_{l} = %.2f %.2f t,  R^2 = %.4f$' %(kl1p[1], kl1p[0], r21))
    plt.plot(source_frame.iloc[:, 0], K2, label = '$\\hat K_{e} = \\exp (%.2f %.2f t),  R^2 = %.4f$' %(ke1p[1], ke1p[0], r22))
    plt.title('Fixed Assets Turnover Approximation,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 0], DK1, ':', label = '$\\|\\frac{\\hat K_{l}-K}{K}\\|,  \\bar S = %.4f$' %(100*DK1.mean()) +'%')
    plt.plot(source_frame.iloc[:, 0], DK2, ':', label = '$\\|\\frac{\\hat K_{e}-K}{K}\\|,  \\bar S = %.4f$' %(100*DK2.mean()) +'%')
    plt.title('Deltas of Fixed Assets Turnover Approximation,  {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[len(source_frame)-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def complexCensus(source_frame):
    plotPearsonRTest(source_frame)
    source_frame = indexswitch(source_frame)
    plotKZF(source_frame)
    plotSES(source_frame, 5, 0.1)
    del source_frame


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


def processingSpline(source_frame, kernelModule, deliveryModule):
    source_frame.columns = ['Period', 'Original']
    N = int(input('Define Number of Interpolation Intervals: ')) ##Number of Periods
    if N> = 2:
        print('Number of Periods Provided: {}'.format(N))
        knt = [] ##Switch Points
        knt.append(0)
        i = 0
        if N == 1:
            knt.append(len(source_frame)-1)
        elif N> = 2:
            while i<N:
                if i == N-1:
                    knt.append(len(source_frame)-1)
                    i+ = 1
                else:
                    y = int(input('Select Row for Year: '))-1
                    if y>knt[i]:
                        knt.append(y)
                        i+ = 1
        else:
            print('Error') ##Should Never Happen
        K, result_frame = kernelModule(source_frame, N, knt)
        deliveryModule(N, K)
        errorMetrics(result_frame)
        plt.figure()
        plt.scatter(result_frame.iloc[:, 0], result_frame.iloc[:, 1])
        plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 2], color = 'red', label = '$s_{%d}(\\tau)$' %(0, ))
        gonogo = input('Does the Resulting Value Need an Improvement?,  Y: ')
        if gonogo == 'Y':
            Q = []
            assert len(knt) == 1+N
            for i in range(len(knt)):
                Q.append(float(input('Correction of Knot {:02d}: '.format(1+i))))
            modified = source_frame.iloc[:, 1].copy() ##Series Modification
            for i in range(len(knt)):
                modified[knt[i]] = Q[i]*modified[knt[i]]
            del K, result_frame
            source_frame = pd.concat([source_frame.iloc[:, 0], modified], axis = 1, sort = True)
            source_frame.columns = ['Period', 'Original']
            K, result_frame = kernelModule(source_frame, N, knt)
            deliveryModule(N, K)
            errorMetrics(result_frame)
            plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 2], color = 'g', label = '$s_{%d}(\\tau)$' %(1, ))
            plt.grid(True)
            plt.legend()
            plt.show()
        else:
            plt.grid(True)
            plt.legend()
            plt.show()
            pass
    else:
        print('N> = 2 is Required,  N = {} Was Provided'.format(N))


print(__doc__)
'''Subproject I. Approximation'''
'''
`plotApproxLinear`: Linear Approximation, 
`plotApproxLogLinear`: Log-Linear Approximation, 
`approxPowerFunctionA`: Power Function Approximation, 
`approxPowerFunctionB`: Power Function Approximation, 
`approxPowerFunctionC`: Power Function Approximation
'''
source_frame = archivedDataCombined()
result_frameA = source_frame[source_frame.columns[[7, 6, 0, 6]]]
result_frameA = result_frameA.dropna()
result_frameA = indexswitch(result_frameA)
result_frameB = source_frame[source_frame.columns[[7, 6, 20, 4]]]
result_frameB = result_frameB.dropna()
result_frameB = indexswitch(result_frameB)
result_frameC = source_frame[source_frame.columns[[7, 6, 20, 6]]]
result_frameC = result_frameC.dropna()
result_frameC = indexswitch(result_frameC)
plotApproxLinear(result_frameA)
plotApproxLogLinear(result_frameB)
plotApproxLogLinear(result_frameC)
del source_frame
source_frame = dataFetchA()
approxPowerFunctionA(source_frame, 2800, 0.01, 0.5)
del source_frame
source_frame = dataFetchB()
approxPowerFunctionB(source_frame, 4, 12, 9000, 3000, 0.87)
del source_frame
source_frame = dataFetchC()
approxPowerFunctionC(source_frame, 1.5, 19, 1.7, 1760)
del source_frame, result_frameA, result_frameB, result_frameC
'''Subproject II. Capital'''
'''
Project: Fixed Assets Dynamics Modelling:
Fixed Assets Turnover Linear Approximation
Gross Fixed Investment to Gross Domestic Product Ratio Linear Approximation
Alpha: Investment to Capital Conversion Ratio Dynamics
Original Result on Archived Data: {s1;s2} = {-7.28110931679034e-05;0.302917968959722}
Original Result on Archived Data: {λ1;λ2} = {-0.000413347827690062;1.18883834418742}
'''
result_frameA, result_frameB, A = archivedSet()
result_frameC, result_frameD, B = updatedSet()
plotCapitalModelling(result_frameA, A)
plotCapitalModelling(result_frameC, B)
'''Project: Discrete Fourier Transform based on Simpson's Rule Applied to Fixed Assets of the US'''
plotDiscreteFourier(result_frameB)
plotDiscreteFourier(result_frameD)
del result_frameA, result_frameB, result_frameC, result_frameD
'''Subproject III. Capital Interactive'''
'''
Alpha: Capital Retirement Ratio
Pi: Investment to Capital Conversion Ratio
**************************************************
Project: Interactive Capital Acquisitions
**************************************************
Option 1
    Define Number of Line Segments for Pi: 1
    Number of Periods Provided: 1
    Pi for Period from 1968 to 2010: 0
Option 2
    Define Number of Line Segments for Pi: 1
    Number of Periods Provided: 1
    Pi for Period from 1968 to 2010: 1
Option 3
    Define Number of Line Segments for Pi: 2
    Number of Periods Provided: 2
    Pi for Period from 1968 to 1981: 1
    Pi for Period from 1982 to 2010: 0
Option 4
    Define Number of Line Segments for Pi: 4
    Number of Periods Provided: 4
    Pi for Period from 1968 to 1981: 1
    Pi for Period from 1982 to 1991: 0.537711622818944
    Pi for Period from 1992 to 2001: 0.815869779361117
    Pi for Period from 2002 to 2010: 0.956084835528969
**************************************************
Project: Interactive Capital Retirement
**************************************************
Option 1
    Define Number of Line Segments for Pi: 1
    Number of Periods Provided: 1
    Define Pi for Period from 1951 to 2011: 0
Option 2
    Define Number of Line Segments for Pi: 2
    Number of Periods Provided: 2
    Select Row for Year: 52
    Define Pi for Period from 1951 to 2003: 1
    Define Pi for Period from 2003 to 2011: 1.4
Option 3
    Define Number of Line Segments for Pi: 2
    Number of Periods Provided: 2
    Select Row for Year: 11
    Define Pi for Period from 1951 to 1962: 0.0493299706940006
    Define Pi for Period from 1962 to 2011: 0.0168837249983057
'''
result_frame = localFetch()
'''Nominal Investment'''
result_frame['IRU'] = result_frame.iloc[:, 0]*result_frame.iloc[:, 2].div(result_frame.iloc[:, 1])
'''Nominal Product'''
result_frame['PNU'] = result_frame.iloc[:, 1]
'''Real Product'''
result_frame['PRU'] = result_frame.iloc[:, 2]
'''Maximum Nominal Product'''
result_frame['PNM'] = result_frame.iloc[:, 1].div(result_frame.iloc[:, 3]/100)
'''Maximum Real Product'''
result_frame['PRM'] = result_frame.iloc[:, 2].div(result_frame.iloc[:, 3]/100)
'''Labor'''
result_frame.rename(columns = {'Labor':'LUU'}, inplace=True)
'''Fixed Assets,  End-Period'''
result_frame['CRU'] = result_frame.iloc[:, 4]*result_frame.iloc[:, 2].div(result_frame.iloc[:, 1])
result_frameA = result_frame[result_frame.columns[[6, 7, 8, 10, 11, 5]]].dropna()
result_frameB = result_frame[result_frame.columns[[6, 7, 8, 11, 5]]].dropna()
result_frameC = result_frame[result_frame.columns[[6, 9, 10, 11, 5]]].dropna()
result_frameA = indexswitch(result_frameA)
result_frameB = indexswitch(result_frameB)
result_frameC = indexswitch(result_frameC)
capitalAcquisitions(result_frameA)
capitalRetirement(result_frameB)
capitalRetirement(result_frameC)
del result_frame, result_frameA, result_frameB, result_frameC
'''Subproject IV. Cobb--Douglas'''
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
del source_frame, result_frameA, result_frameB, result_frameC, result_frameD, result_frameE, result_frameF, result_frameG, result_frameH, result_frameI
'''Subproject V. Cobb--Douglas CAN'''
'''First Figure: Exact Correspondence with `Note INTH05 2014-07-10.docx`'''
source_frame = datasetCanada()
source_frame = source_frame.div(source_frame.iloc[0, :])
cd_canada(source_frame)
cobbDouglas3D(source_frame)
del source_frame
'''Subproject VI. Elasticity'''
source_frame = archivedDataCombined()
result_frameA = source_frame[source_frame.columns[[7, 6, 4]]]
result_frameB = source_frame[source_frame.columns[[4]]]
result_frameA = result_frameA.dropna()
result_frameB = result_frameB.dropna()
result_frameA = indexswitch(result_frameA)
result_frameB = indexswitch(result_frameB)
plotElasticity(result_frameA)
plotGrowthElasticity(result_frameB)
del source_frame, result_frameA, result_frameB
'''Subproject VII. MSpline'''
'''Makeshift Splines'''
result_frame = cobbDouglasPreprocessing()
result_frame['turnover'] = result_frame.iloc[:, 2].div(result_frame.iloc[:, 0]) ## Fixed Assets Turnover
result_frame = result_frame[result_frame.columns[[5]]]
result_frame = indexswitch(result_frame)
'''Option 1'''
processingSpline(result_frame, MSplineLLS, resultsDeliveryA)
'''Option 2.1.1'''
processingSpline(result_frame, MSplineEA, resultsDeliveryK)
'''Option 2.1.2'''
processingSpline(result_frame, MSplineEB, resultsDeliveryK)
'''Option 2.2.1'''
processingSpline(result_frame, MSplineLA, resultsDeliveryK)
'''Option 2.2.2'''
processingSpline(result_frame, MSplineLB, resultsDeliveryK)
del result_frame
'''Subproject VIII. Multiple'''
source_frame = cobbDouglasPreprocessing()
source_frame['lab_cap_int'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
source_frame['lab_product'] = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])
result_frameA = source_frame[source_frame.columns[[0]]]
result_frameB = source_frame[source_frame.columns[[1]]]
result_frameC = source_frame[source_frame.columns[[2]]]
result_frameD = source_frame[source_frame.columns[[5]]]
result_frameE = source_frame[source_frame.columns[[6]]]
complexCensus(result_frameA)
complexCensus(result_frameB)
complexCensus(result_frameC)
complexCensus(result_frameD)
complexCensus(result_frameE)
del source_frame, result_frameA, result_frameB, result_frameC, result_frameD, result_frameE
series = ['D0004', 'D0130', 'F0003', 'F0004', 'P0110', 'U0001', 'U0008', 'X0414', 'X0415']
for i in range(len(series)):
    print('Processing {}'.format(series[i]))
    source_frame = fetchCensus('census1975.zip', series[i], True)
    plotPearsonRTest(source_frame)
    del source_frame
    source_frame = fetchCensus('census1975.zip', series[i], False)
    plotKZF(source_frame)
    plotSES(source_frame, 5, 0.1)
    del source_frame
'''Subproject IX. USA BEA'''
source_frameA = archivedDataCombined()
source_frameB = dataCombined()
'''Project: Initial Version Dated: 05 October 2012'''
result_frameAB = preprocessingA(source_frameA)
result_frameAC = preprocessingA(source_frameB)
dataFetchPlottingA(result_frameAB)
dataFetchPlottingA(result_frameAC)
'''Project: Initial Version Dated: 23 November 2012'''
result_frameBB = preprocessingB(source_frameA)
result_frameBC = preprocessingB(source_frameB)
dataFetchPlottingB(result_frameBB)
dataFetchPlottingB(result_frameBC)
'''Project: Initial Version Dated: 16 June 2013'''
result_frameCB = preprocessingC(source_frameA)
result_frameCC = preprocessingC(source_frameB)
dataFetchPlottingC(result_frameCB)
dataFetchPlottingC(result_frameCC)
'''Project: Initial Version Dated: 15 June 2015'''
result_frameD = preprocessingD(source_frameB)
dataFetchPlottingD(result_frameD)
'''Project: Initial Version Dated: 17 February 2013'''
result_frameEA, result_frameEB = preprocessingE(source_frameA)
plottingE(result_frameEA)
plottingE(result_frameEB)
'''Project: BEA Data Compared with Kurenkov Yu.V. Data'''
result_frameFA, result_frameFB, result_frameFC, result_frameFD = preprocessingF(source_frameA)
plottingF(result_frameFA, result_frameFB, result_frameFC, result_frameFD)
del result_frameAB, result_frameAC, result_frameBB, result_frameBC, result_frameCB, result_frameCC, result_frameD, result_frameEA, result_frameEB, result_frameFA, result_frameFB, result_frameFC, result_frameFD, source_frameA, source_frameB
'''Subproject X. USA Census'''
result_frame, base = dataFetchCensusA()
plottingCensusA(result_frame, base)
capital = dataFetchCensusBA()
deflator = dataFetchCensusBB()
plottingCensusB(capital, deflator)
result_frame, base = dataFetchCensusC()
plottingCensusC(result_frame, base)
'''Census Production Series'''
series = ['P0248', 'P0249', 'P0250', 'P0251', 'P0262', 'P0265', 'P0266', 'P0267', 'P0268', \
        'P0269', 'P0293', 'P0294', 'P0295']
alternative = ['P0231', 'P0232', 'P0233', 'P0234', 'P0235', 'P0236', 'P0237', 'P0238', \
             'P0239', 'P0240', 'P0241', 'P0244', 'P0247', 'P0248', 'P0249', 'P0250', \
             'P0251', 'P0252', 'P0253', 'P0254', 'P0255', 'P0256', 'P0257', 'P0258', \
             'P0259', 'P0260', 'P0261', 'P0262', 'P0263', 'P0264', 'P0265', 'P0266', \
             'P0267', 'P0268', 'P0269', 'P0270', 'P0271', 'P0277', 'P0279', 'P0281', \
             'P0282', 'P0283', 'P0284', 'P0286', 'P0288', 'P0290', 'P0293', 'P0294', \
             'P0295', 'P0296', 'P0297', 'P0298', 'P0299', 'P0300']
dataFetchPlottingCensusD(series)
result_frame = dataFetchCensusE()
plottingCensusE(result_frame)
result_frame = dataFetchCensusF()
plottingCensusFA(result_frame)
plottingCensusFB(result_frame)
result_frame = dataFetchCensusG()
plottingCensusG(result_frame)
dataFetchPlottingCensusH()
result_frameA, result_frameB, result_frameC = dataFetchCensusI()
plottingCensusI(result_frameA, result_frameB, result_frameC)
result_frame, base = dataFetchCensusJ()
plottingCensusJ(result_frame, base)
dataFetchPlottingCensusK()
del capital, deflator, result_frame, result_frameA, result_frameB, result_frameC, base, series, alternative
'''Subproject XI. USA Census J14'''
plotGrowthElasticity(fetchCensus('census1949.zip', 'J0014', False))
plotRMF(fetchCensus('census1949.zip', 'J0014', False))
'''Subproject XII. USA Douglas Kendrick'''
'''Douglas European Demographics & Growth of US Capital'''
series_dict = base_dict('douglas.zip')
titles_deu = ['Germany Birth Rate', 'Germany Death Rate', 'Germany Net Fertility Rate', 'Prussia Birth Rate', 'Prussia Death Rate', 'Prussia Net Fertility Rate']
titles_eur = ['Sweden', 'Norway', 'Denmark', 'England & Wales', 'France', 'Germany', 'Prussia', 'Switzerland', 'Italy']
titles = ['Table I Indexes of Physical Production,  1899 = 100 [1899$-$1926]', 
        'Table II Wholesale Price Indexes,  1899 = 100 [1899$-$1928]', 
        'Table III Exchange Value = Ratio of Wholesale Prices to General Price Level: Nine Groups and Manufacturing [1899$-$1928]', 
        'Table IV Relative Total Value Product for Nine Groups and All Manufacturing [1899$-$1926]', 
        'Table V Employment Index: Nine Industries and Manufacturing,  1899$-$1927', 
        'Table VI Value Product Per Employee: Nine Industries and Manufacturing,  1899$-$1926', 
        'Table VII Index of Money Wages: Nine Groups and Manufacturing,  1899$-$1927', 
        'Table VIII Index of Real Wages: Nine Groups and Manufacturing,  1899$-$1926', 
        'Table 19 The Movement of Labor,  Capital,  and Product In\nMassachusetts Manufacturing,  1890$-$1926,  1899 = 100', 
        'Table 24 The Revised Index of Physical Production for\nAll Manufacturing in the United States,  1899$-$1926', 
        'Chart 67. Birth,  Death,  and Net Fertility Rates in Sweden,  1750$-$1931\nTable XXV Birth,  Death and Net Fertility Rates for Sweden,  1750$-$1931, \nSource: Computed from data given in the Statistisk ?rsbok for Sverige.', 
        'Chart 68. Birth,  Death,  and Net Fertility Rates in Norway,  1801$-$1931\nTable XXVI Birth,  Death and Net Fertility Rates for Norway,  1801$-$1931, \nSource: Statistisk ?rbok for Kongeriket Norge.', 
        'Chart 69. Birth,  Death,  and Net Fertility Rates in Denmark,  1800$-$1931\nTable XXVII Birth,  Death and Net Fertility Rates for Denmark,  1800$-$1931, \nSource: Danmarks Statistik,  Statistisk Aarbog.', 
        'Chart 70. Birth,  Death,  and Net Fertility Rates in Great Britain,  1850$-$1932\nTable XXVIII Birth,  Death and Net Fertility Rates for England and Wales,  1850$-$1932, \nSource: Statistical Abstract for the United Kingdom.', 
        'Chart 71. Birth,  Death,  and Net Fertility Rates in France,  1801$-$1931\nTable XXIX Birth,  Death and Net Fertility Rates for France,  1801$-$1931, \nSource: Statistique generale de la France: Mouvement de la Population.', 
        'Chart 72$\'$. Birth,  Death,  and Net Fertility Rates in Germany,  1871$-$1931\nTable XXX Birth,  Death And Net Fertility Rates For:\n(A) Germany,  1871$-$1931\n(B) Prussia,  1816$-$1930\nSource: Statistisches Jahrbuch fur das Deutsche Reich.', 
        'Chart 73. Birth,  Death,  and Net Fertility Rates in Switzerland,  1871$-$1931\nTable XXXI Birth,  Death and Net Fertility Rates for Switzerland,  1871$-$1931, \nSource: Statistisches Jahrbuch der Schweiz.', 
        'Chart 74. Birth,  Death,  and Net Fertility Rates in Italy,  1862$-$1931\nTable XXXII Birth,  Death and Net Fertility Rates for Italy,  1862$-$1931, \nSource: Annuario Statistico Italiano.', 
        'Table 62 Estimated Total British Capital In Terms of the 1865 Price Level\nInvested Inside and Outside the United Kingdom by Years From\n1865 to 1909,  and Rate of Growth of This Capital', 
        'Table 63 Growth of Capital in the United States,  1880$-$1922', 
        'Birth Rates by Countries']
plotDouglas('douglas.zip', series_dict, 1, 0, 12, 1, titles[0], 'Percentage')
plotDouglas('douglas.zip', series_dict, 2, 12, 23, 1, titles[1], 'Percentage')
plotDouglas('douglas.zip', series_dict, 3, 23, 34, 1, titles[2], 'Percentage')
plotDouglas('douglas.zip', series_dict, 4, 34, 45, 1, titles[3], 'Percentage')
plotDouglas('douglas.zip', series_dict, 5, 45, 55, 1, titles[4], 'Percentage')
plotDouglas('douglas.zip', series_dict, 6, 55, 66, 1, titles[5], 'Percentage')
plotDouglas('douglas.zip', series_dict, 7, 66, 76, 1, titles[6], 'Percentage')
plotDouglas('douglas.zip', series_dict, 8, 76, 86, 1, titles[7], 'Percentage')
plotDouglas('douglas.zip', series_dict, 9, 86, 89, 1, titles[8], 'Percentage')
plotDouglas('douglas.zip', series_dict, 10, 89, 90, 1, titles[9], 'Percentage')
plotDouglas('douglas.zip', series_dict, 11, 90, 93, 1, titles[10], 'Rate Per 1000')
plotDouglas('douglas.zip', series_dict, 12, 93, 96, 1, titles[11], 'Rate Per 1000')
plotDouglas('douglas.zip', series_dict, 13, 96, 99, 1, titles[12], 'Rate Per 1000')
plotDouglas('douglas.zip', series_dict, 14, 99, 102, 1, titles[13], 'Rate Per 1000')
plotDouglas('douglas.zip', series_dict, 15, 102, 105, 1, titles[14], 'Rate Per 1000')
plotDouglas('douglas.zip', series_dict, 16, 105, 111, 1, titles[15], 'Rate Per 1000', titles_deu)
plotDouglas('douglas.zip', series_dict, 17, 111, 114, 1, titles[16], 'Rate Per 1000')
plotDouglas('douglas.zip', series_dict, 18, 114, 117, 1, titles[17], 'Rate Per 1000')
plotDouglas('douglas.zip', series_dict, 19, 117, 121, 1, titles[18], 'Mixed')
plotDouglas('douglas.zip', series_dict, 20, 121, 124, 1, titles[19], 'Millions of Dollars')
plotDouglas('douglas.zip', series_dict, 21, 90, 115, 3, titles[20], 'Births Rate Per 1000 People', titles_eur)
plt.show()
del series_dict, titles_deu, titles_eur, titles
'''Douglas Production Function'''
result_frame = douglasPreprocessing()
cd_modified(result_frame)
'''Kendrick Macroeconomic Series'''
series_dict = base_dict('kendrick.zip')
titles = ['Table A-I Gross And Net National Product,  Adjusted Kuznets Concepts,  Peacetime And National Security Version,  1869$-$1957 (Millions Of 1929 Dollars)', 
        'Table A-IIa Gross National Product,  Commerce Concept,  Derivation From Kuznets Estimates,  1869$-$1957 (Millions Of 1929 Dollars)', 
        'Table A-IIb Gross National Product,  Commerce Concept,  Derivation From Kuznets Estimates,  1869$-$1929; And Reconciliation With Kuznets Estimates,  1937,  1948,  And 1953 (Millions Of Current Dollars)', 
        'Table A-III National Product,  Commerce Concept,  By Sector,  1869$-$1957 (Millions Of 1929 Dollars)', 
        'Table A-VI National Economy. Persons Engaged,  By Major Sector,  1869$-$1957 (Thousands)', 
        'Table A-X National Economy: Manhours,  By Major Sector,  1869$-$1957 (Millions)', 
        'Table A-XV National Economy: Real Capital Stocks,  By Major Sector,  1869$-$1957 (Millions Of 1929 Dollars)', 
        'Table A-XVI Domestic Economy And Private Sectors: Real Capital Stocks,  By Major Type,  1869$-$1953 (Millions Of 1929 Dollars)', 
        'Table A-XIX National Economy: Real Net Product,  Inputs,  And Productivity Ratios,  Kuznets Concept,  National Security Version,  1869$-$1957 (1929 = 100)', 
        'Table A-XXII Private Domestic Economy. Real Gross Product,  Inputs,  And Productivity Ratios,  Commerce Concept,  1869$-$1957 (1929 = 100)', 
        'Table A-XXII: Supplement Private Domestic Economy: Productivity Ratios Based On Unweighted Inputs,  1869$-$1957 (1929 = 100)', 
        'Table A-XXIII Private Domestic Nonfarm Economy: Real Gross Product,  Inputs,  And Productivity Ratios,  Commerce Concept,  1869$-$1957 (1929 = 100)', 
        'Table D-II. Manufacturing: Output,  Labor Inputs,  and Labor Productivity Ratios,  1869-1957 (1929 = 100)']
plotDouglas('kendrick.zip', series_dict, 1, 0, 8, 1, titles[0], 'Millions Of 1929 Dollars')
plotDouglas('kendrick.zip', series_dict, 2, 8, 19, 1, titles[1], 'Millions Of 1929 Dollars')
plotDouglas('kendrick.zip', series_dict, 3, 19, 30, 1, titles[2], 'Millions Of Current Dollars')
plotDouglas('kendrick.zip', series_dict, 4, 30, 38, 1, titles[3], 'Millions Of 1929 Dollars')
plotDouglas('kendrick.zip', series_dict, 5, 38, 46, 1, titles[4], 'Thousands')
plotDouglas('kendrick.zip', series_dict, 6, 46, 54, 1, titles[5], 'Millions')
plotDouglas('kendrick.zip', series_dict, 7, 54, 60, 1, titles[6], 'Millions Of 1929 Dollars')
plotDouglas('kendrick.zip', series_dict, 8, 60, 72, 1, titles[7], 'Millions Of 1929 Dollars')
plotDouglas('kendrick.zip', series_dict, 9, 72, 84, 1, titles[8], 'Percentage')
plotDouglas('kendrick.zip', series_dict, 10, 84, 96, 1, titles[9], 'Percentage')
plotDouglas('kendrick.zip', series_dict, 11, 96, 100, 1, titles[10], 'Percentage')
plotDouglas('kendrick.zip', series_dict, 12, 100, 111, 1, titles[11], 'Percentage')
plotDouglas('kendrick.zip', series_dict, 13, 111, 118, 1, titles[12], 'Percentage')
plt.show()
del series_dict, titles