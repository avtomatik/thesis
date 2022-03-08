# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:47:52 2020

@author: Mastermind
"""

def beaFetch(source, wrkbk, wrksht, start, finish, line):
    '''Data _frame Fetching from Bureau of Economic Analysis Zip Archives'''
    '''
    source: Name of Zip Archive, 
    wrkbk: Name of Excel File within Zip Archive, 
    wrksht: Name of Worksheet within Excel File within Zip Archive, 
    boundary: 4+<Period_Finish>-<Period_Start>, 
    line: Line'''
    import os
    import pandas as pd
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
def BLSCPIU():
    '''BLS CPI-U Price Index Fetch'''
    import pandas as pd
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
    result_frame = result_frame.set_index('Period')
    return result_frame
def data_bea_def():
    '''Intent: Returns Cumulative Price Index for Some Base Year from Certain Type BEA Deflator File'''
    import pandas as pd
    source_frame = pd.read_excel('dataset USA BEA GDPDEF.xls', skiprows=15)
    source_frame['DATE'] = source_frame['DATE'].astype(str)
    source_frame['Period'], source_frame['mnth'], source_frame['day'] = source_frame['DATE'].str.split('-').str
    source_frame = source_frame[source_frame.columns[[2, 1]]]
    source_frame = source_frame.groupby('Period').prod()**(1/4)
    return source_frame
def data_bea_gdp():
    import pandas as pd
    '''Nominal Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 1)
    '''Nominal Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 1)
    semi_frameA = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1929--1969'''
    sub_frameA = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10106 Ann', 1929, 1969, 1)
    '''Real Gross Domestic Product Series,  2005 = 100: A191RX1,  1969--2012'''
    sub_frameB = beaFetch('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10106 Ann', 1969, 2012, 1)
    semi_frameB = sub_frameA.append(sub_frameB).drop_duplicates()
    del sub_frameA, sub_frameB
    result_frame = pd.concat([semi_frameA, semi_frameB], axis = 1, sort = False)
    return result_frame
def direct(source_frame, base):
    '''Intent: Returns Cumulative Price Index for Base Year;
    source_frame.iloc[:, 0]: Growth Rate;
    base: Base Year'''
    import scipy as sp
    '''Cumulative Price Index'''
    source_frame['p_i'] = sp.cumprod(1+source_frame.iloc[:, 0])
    '''Cumulative Price Index for the Base Year'''
    source_frame['cpi'] = source_frame.iloc[:, 1].div(source_frame.iloc[base-source_frame.index[0], 1])
    result_frame = source_frame[source_frame.columns[[2]]]
    return result_frame
def inverse_single(source_frame):
    '''Intent: Returns Growth Rate from Cumulative Price Index for Some Base Year;
    source_frame.iloc[:, 0]: Cumulative Price Index for Some Base Year'''
    source_frame['gri'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 0].shift(1))-1
    result_frame = source_frame[source_frame.columns[[1]]].dropna()
    return result_frame
def inverse_double(source_frame):
    '''Intent: Returns Growth Rate from Nominal & Real Prices Series;
    source_frame.iloc[:, 0]: Nominal Prices;
    source_frame.iloc[:, 1]: Real Prices'''
    source_frame['cpi'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    source_frame['gri'] = source_frame.iloc[:, 2].div(source_frame.iloc[:, 2].shift(1))-1
    result_frame = source_frame[source_frame.columns[[3]]].dropna()
    return result_frame
def price_base(source_frame):
    '''Returns Base Year'''
    i = len(source_frame)-1
    while abs(source_frame.iloc[i, 0]-100)>1/1000:
##    while abs(source_frame.iloc[i, 0]-source_frame.iloc[i, 1])>10:
#    while abs(source_frame.iloc[i, 0]-source_frame.iloc[i, 1])>1:
        i- = 1
        base = i ##Basic Year
    base = source_frame.index[base]