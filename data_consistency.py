# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 20:39:06 2020

@author: Mastermind
"""

# =============================================================================
# TODO: Refactor
# =============================================================================
import os
import pandas as pd
import zipfile
import matplotlib.pyplot as plt


def fetch_usa_bea(zpfl, wrkbk, wrksht, start, finish, line):
# =============================================================================
# Data Frame Fetching from Bureau of Economic Analysis Zip Archives
# =============================================================================
# =============================================================================
# zpfl: Name of Zip Archive, 
# wrkbk: Name of Excel File within Zip Archive, 
# wrksht: Name of Worksheet within Excel File within Zip Archive, 
# boundary: 4+<Period_Finish>-<Period_Start>, 
# line: Line
# =============================================================================
    boundary = 4-start+finish
    if zpfl == None:
        xl = pd.ExcelFile(wrkbk)
    else:
        with zipfile.ZipFile(zpfl, 'r') as z:
            xl = pd.ExcelFile(z.open(wrkbk))
    data_frame = pd.read_excel(xl, wrksht, usecols=range(2, boundary), skiprows=7)
    data_frame.dropna(inplace=True)
    data_frame = data_frame.T
    data_frame.to_csv('temporary.txt')
    del xl, data_frame
    result_frame = pd.read_csv('temporary.txt', usecols=[0, line], skiprows=1)
    os.unlink('temporary.txt')
    result_frame.columns = result_frame.columns.to_series().replace({'^Unnamed: \d':'Period'}, regex=True)
    result_frame = result_frame.set_index('Period')
    return result_frame


def fetch_can_quarterly(file_name, vector, index):
# =============================================================================
# Data Frame Fetching from Quarterly Data within CANSIM Zip Archives
# Should Be [x 7 columns]
# index == True -- indexed by `Period`;
# index == False -- not indexed by `Period`
# =============================================================================
    data_frame = pd.read_csv('dataset CAN {}-eng.zip'.format(file_name))
    data_frame = data_frame[data_frame.Vector == vector]
    if file_name == '02820011':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    elif file_name == '02820012':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    elif file_name == '03790031':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    elif file_name == '03800068':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    else:
        data_frame = data_frame[data_frame.columns[[0, 6]]] ##Should Be [x 7 columns]
    data_frame.rename(columns={'Value':vector}, inplace=True)
    data_frame['Period'], data_frame['Q'] = data_frame.iloc[:, 0].str.split('/').str
    data_frame = data_frame[data_frame.columns[[2, 1]]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = pd.to_numeric(data_frame.iloc[:, 1])
    if (file_name == '03800084' and vector == 'v62306938'):
        data_frame = data_frame.groupby('Period').sum()
    elif (file_name == '03790031' and vector == 'v65201536'):
        data_frame = data_frame.groupby('Period').mean()
    elif (file_name == '03790031' and vector == 'v65201809'):
        data_frame = data_frame.groupby('Period').sum()
    else:
        data_frame = data_frame.groupby('Period').mean()
    if index:
        return data_frame
    else:
        data_frame.to_csv('temporary.txt')
        del data_frame
        result_frame = pd.read_csv('temporary.txt')
        os.unlink('temporary.txt')
        return result_frame


def fetch_can_annually(file_name, vector, index):
# =============================================================================
# Data Frame Fetching from CANSIM Zip Archives
# Should Be [x 7 columns]
# index == True -- indexed by `Period`;
# index == False -- not indexed by `Period`
# =============================================================================
    data_frame = pd.read_csv('dataset CAN {}-eng.zip'.format(file_name))
    data_frame = data_frame[data_frame.Vector == vector]
    if file_name == '03800106':
        data_frame = data_frame[data_frame.columns[[0, 5]]]
    elif file_name == '03800566':
        data_frame = data_frame[data_frame.columns[[0, 5]]]
    elif file_name == '02820011':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    elif file_name == '02820012':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    elif file_name == '03790031':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    elif file_name == '03800068':
        data_frame = data_frame[data_frame.columns[[0, 7]]]
    else:
        data_frame = data_frame[data_frame.columns[[0, 6]]] ##Should Be [x 7 columns]
    data_frame.rename(columns={'Ref_Date':'Period', 'Value':vector}, inplace=True)
    data_frame.iloc[:, 1] = pd.to_numeric(data_frame.iloc[:, 1])
    data_frame.to_csv('dataset CAN {} {}.csv'.format(file_name, vector), index=False)
    if index:
        data_frame = data_frame.set_index('Period')
        os.unlink('dataset CAN {} {}.csv'.format(file_name, vector))
        return data_frame
    else:
        del data_frame
        result_frame = pd.read_csv('dataset CAN {} {}.csv'.format(file_name, vector))
        os.unlink('dataset CAN {} {}.csv'.format(file_name, vector))
        return result_frame


def fetch_can_group_A(file_name, row):
    data_frame = pd.read_csv('dataset CAN cansim{}.csv'.format(file_name), skiprows=row)
    if file_name == '7931814471809016759':
        data_frame.columns = data_frame.columns.to_series().replace({'[.:;@_]':''}, regex=True)
        data_frame['Q1 2014'] = data_frame['Q1 2014'].str.replace(';', '')
    else:
        pass
    data_frame = data_frame.T
    data_frame.to_csv('temporary.txt')
    del data_frame
    data_frame = pd.read_csv('temporary.txt', skiprows=1)
    os.unlink('temporary.txt')
    data_frame['qrtr'], data_frame['Period'] = data_frame.iloc[:, 0].str.split(' ').str
    data_frame = data_frame.groupby('Period').mean()
    return data_frame


def fetch_can_group_B(file_name, row):
    data_frame = pd.read_csv('dataset CAN cansim{}.csv'.format(file_name), skiprows=row)
    data_frame['mnth'], data_frame['Period'] = data_frame.iloc[:, 0].str.split('-').str
    result_frame = data_frame.groupby('Period').mean()
    del data_frame
    return result_frame


def BLSLNU(file_name):
# =============================================================================
# LNU04000000: Bureau of Labor Statistics Unemployment Rate
# =============================================================================
    series_id = 'LNU04000000'
    data_frame = pd.read_csv(file_name, sep='\t', low_memory=False)
    data_frame = data_frame[data_frame.iloc[:, 0].str.contains(series_id)]
    data_frame = data_frame[data_frame.iloc[:, 2] == 'M13']
    result_frame = data_frame[data_frame.columns[[1, 3]]]
    result_frame.rename(columns={'year':'period'}, inplace=True)
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns={'Value':series_id}, inplace=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].astype(float)
    return result_frame


def BLSPCUOMFG(file_name):
# =============================================================================
# PCUOMFG--OMFG--: Bureau of Labor Statistics Producer Price Index Manufacturing
# =============================================================================
    series_id = 'PCUOMFG--OMFG--'
    data_frame = pd.read_csv(file_name, sep='\t', low_memory=False)
    data_frame = data_frame[data_frame.iloc[:, 0].str.contains(series_id)]
    data_frame = data_frame[data_frame.iloc[:, 2] == 'M13']
    result_frame = data_frame[data_frame.columns[[1, 3]]]
    result_frame.rename(columns={'year':'period'}, inplace=True)
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns={'Value':series_id}, inplace=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].astype(float)
    return result_frame


def archivedCombinedCapitalTest():
    '''Data Test'''
    '''Nominal Investment Series: A006RC1,  1929--1969'''
    sub_frameA = fetch_usa_bea('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 7)
    '''Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
    sub_frameB = fetch_usa_bea('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 1)
    control_frame = pd.concat([sub_frameA, sub_frameB], axis=1, sort=True)
    del sub_frameA, sub_frameB
    '''Nominal Investment Series: A006RC1,  1929--1969'''
    sub_frameA = fetch_usa_bea('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 7)
    '''Nominal Gross Domestic Product Series: A191RC1,  1929--1969'''
    sub_frameB = fetch_usa_bea('dataset USA BEA Release 2013-01-31 SectionAll_xls_1929_1969.zip', 'Section1ALL_Hist.xls', '10105 Ann', 1929, 1969, 1)
    test_frame = pd.concat([sub_frameA, sub_frameB], axis=1, sort=True)
    del sub_frameA, sub_frameB
    if control_frame.equals(test_frame):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1929--1969')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')
    del control_frame, test_frame
    '''Nominal Investment Series: A006RC1,  1969--2012'''
    sub_frameA = fetch_usa_bea('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 7)
    '''Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
    sub_frameB = fetch_usa_bea('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 1)
    control_frame = pd.concat([sub_frameA, sub_frameB], axis=1, sort=True)
    del sub_frameA, sub_frameB
    '''Nominal Investment Series: A006RC1,  1969--2012'''
    sub_frameA = fetch_usa_bea('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 7)
    '''Nominal Gross Domestic Product Series: A191RC1,  1969--2012'''
    sub_frameB = fetch_usa_bea('dataset USA BEA Release 2013-01-31 SectionAll_xls_1969_2012.zip', 'Section1all_xls.xls', '10105 Ann', 1969, 2012, 1)
    test_frame = pd.concat([sub_frameA, sub_frameB], axis=1, sort=True)
    del sub_frameA, sub_frameB
    if control_frame.equals(test_frame):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1969--2012')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')
    del control_frame, test_frame


def fetchBEA(file_name, series_id):
# =============================================================================
# `dataset USA BEA NipaDataA.txt`: U.S. Bureau of Economic Analysis
# Archived: https://www.bea.gov/National/FAweb/Details/Index.html
# https://www.bea.gov//national/FA2004/DownSS2.asp, Accessed May 26, 2018
# =============================================================================
    if file_name == 'beanipa20131202.zip':
        data_frame = pd.read_csv(file_name, usecols=range(8, 11))
        data_frame.columns = data_frame.columns.str.title()
        data_frame.rename(columns={'Value':series_id}, inplace=True)
    elif file_name == 'beanipa20150302section5.zip': ##Not Used
        data_frame = pd.read_csv(file_name, usecols=range(8, 11))
        data_frame.columns = data_frame.columns.str.title()
        data_frame.rename(columns={'Value':series_id}, inplace=True)
    elif file_name == 'beanipa20150501.zip':
        data_frame = pd.read_csv(file_name, usecols=range(14, 18))
        data_frame.columns = data_frame.columns.str.title()
        data_frame.rename(columns={'Value':series_id}, inplace=True)
        data_frame = data_frame[data_frame.iloc[:, 2] == 0]
        data_frame = data_frame[data_frame.columns[[0, 1, 3]]]
    elif file_name == 'dataset USA BEA NipaDataA.txt':
        data_frame = pd.read_csv(file_name, thousands=', ')
        data_frame.rename(columns={'Value':series_id}, inplace=True)
    elif file_name == 'beanipa20131202sfat.zip':
        data_frame = pd.read_csv(file_name, usecols=range(8, 11))
        data_frame.columns = data_frame.columns.str.title()
        data_frame.rename(columns={'Value':series_id}, inplace=True)
    elif file_name == 'beanipa20170823sfat.zip':
        data_frame = pd.read_csv(file_name, usecols=range(8, 11))
        data_frame.columns = data_frame.columns.str.title()
        data_frame.rename(columns={'Value':series_id}, inplace=True)
    else:
        pass
    result_frame = data_frame[data_frame.iloc[:, 0] == series_id]
    del data_frame
    result_frame = result_frame[result_frame.columns[[1, 2]]]
    result_frame = result_frame.reset_index(drop=True)
    result_frame = result_frame.set_index('Period')
    result_frame.to_csv('temporary.txt')
    del result_frame
    result_frame = pd.read_csv('temporary.txt')
    os.unlink('temporary.txt')
    result_frame = result_frame.set_index('Period')
    if file_name == 'beanipa20170823sfat.zip':
        result_frame = result_frame.round(3)
    else:
        pass
    result_frame = result_frame.drop_duplicates()
    return result_frame


def lookup(data_frame):
    for i, series_id in enumerate(data_frame.columns):
        series = data_frame.iloc[:, i].sort_values().unique()
        print('{:*^50}'.format(series_id))
        print(series)


def retrieval(series_id):
    data_frame = pd.read_csv('beanipa20150501.zip')
    data_frame = data_frame[data_frame.iloc[:, 0].str.contains('Table 3.17. Selected Government Current and Capital Expenditures by Function')]
    data_frame = data_frame[data_frame.iloc[:, 7].str.contains(series_id)]
    lookup(data_frame)


def test_procedure(codes):
    semi_frame_A = fetchBEA('beanipa20150501.zip', codes[0])
    semi_frame_B = fetchBEA('beanipa20150501.zip', codes[1])
    semi_frame_C = fetchBEA('beanipa20150501.zip', codes[2])
    result_frame = pd.concat([semi_frame_A, semi_frame_B, semi_frame_C], axis=1, sort=True)
    del semi_frame_A, semi_frame_B, semi_frame_C
    result_frame['test'] = result_frame.iloc[:, 0]-result_frame.iloc[:, 1]-result_frame.iloc[:, 2]
    result_frame.iloc[:, 3].plot(grid=True)


def fetch_usa_bea_sfat(series_id):
# =============================================================================
# Retrieve Historical Manufacturing Series from BEA SFAT CSV File
# =============================================================================
    data_frame = pd.read_csv('beanipa20170823sfat.zip', low_memory=False)
    data_frame = data_frame[data_frame.iloc[:, 0].str.contains('Historical')]
    data_frame = data_frame[data_frame.iloc[:, 6].str.contains('Manufacturing')]
    data_frame = data_frame[data_frame.iloc[:, 8] == series_id]
    tables = data_frame.iloc[:, 0].unique()
    tables = pd.Series(tables)
    if len(tables) == 1:
        result_frame = data_frame[data_frame.iloc[:, 0] == tables[0]]
        result_frame = result_frame[result_frame.columns[[9, 10]]]
        result_frame.columns = result_frame.columns.str.title()
        result_frame.rename(columns={'Value':series_id}, inplace=True)
        result_frame = result_frame.reset_index(drop=True)
        result_frame = result_frame.set_index('Period')
    elif len(tables) >= 2:
        i = 0
        for table in tables:
            current_frame = data_frame[data_frame.iloc[:, 0] == table]
            current_frame = current_frame[current_frame.columns[[9, 10]]]
            current_frame.columns = current_frame.columns.str.title()
            current_frame.rename(columns={'Value':series_id}, inplace=True)            
            current_frame = current_frame.reset_index(drop=True)
            current_frame = current_frame.set_index('Period')
            if i == 0:
                result_frame = current_frame
            elif i >= 1:
                result_frame = pd.concat([result_frame, current_frame], axis=1, sort=True)
            del current_frame
            i += 1
    return result_frame


def subTestA(data_frame):
    data_frame['delta_sm'] = data_frame.iloc[:, 0]-data_frame.iloc[:, 3]-data_frame.iloc[:, 4]-data_frame.iloc[:, 5]
    data_frame.dropna(inplace=True)
    from pandas.plotting import autocorrelation_plot
    autocorrelation_plot(data_frame.iloc[:, 7])


def subTestB(data_frame):
#    data_frame['delta_eq'] = data_frame.iloc[:, 0]-data_frame.iloc[:, 6]
    data_frame['delta_eq'] = 2*(data_frame.iloc[:, 0]-data_frame.iloc[:, 6]).div(data_frame.iloc[:, 0]+data_frame.iloc[:, 6])
    data_frame.dropna(inplace=True)
    data_frame.iloc[:, 7].plot(grid=True)


def fetch_usa_bea_sfat_series():    
# =============================================================================
# Earlier Version of `k3n31gd1es000`
# =============================================================================
    control_frame = pd.read_csv('beanipaUnknownsfatk3n31gd1es000.zip')
    control_header = control_frame.iloc[:, 8].unique().tolist()[0]
    control_frame = control_frame[control_frame.columns[[9, 10]]]
    control_frame.columns = control_frame.columns.str.title()
    control_frame.rename(columns={'Value':control_header}, inplace=True)
    control_frame = control_frame.reset_index(drop=True)
    control_frame = control_frame.set_index('Period')
    semi_frame_A = fetch_usa_bea_sfat('k3n31gd1es000')
    semi_frame_B = fetch_usa_bea_sfat('k3n31gd1eq000')
    semi_frame_C = fetch_usa_bea_sfat('k3n31gd1ip000')
    semi_frame_D = fetch_usa_bea_sfat('k3n31gd1st000')
    test_frame = pd.concat([semi_frame_A, semi_frame_B, semi_frame_C, semi_frame_D], axis=1, sort=True)
    del semi_frame_A, semi_frame_B, semi_frame_C, semi_frame_D
    result_frame = pd.concat([test_frame, control_frame], axis=1, sort=True)
    return result_frame


def plot_canada_test(control, test):
    plt.figure()
    control.plot(logy=True)
    test.plot(logy=True)
    plt.title('Discrepancy')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.show()


def plot_nber(file_name, method):
    data_frame = pd.read_csv(file_name)
    if method == 'mean':
        data_frame = data_frame.groupby('year').mean()
        title = 'Mean NBER-CES'
    elif method == 'sum':
        data_frame = data_frame.groupby('year').sum()
        title = 'Sum NBER-CES'
    else:
        return
    if 'sic' in file_name:
        data_frame.drop(['sic'], axis=1, inplace=True)
    elif 'naics' in file_name:
        data_frame.drop(['naics'], axis=1, inplace=True)
    else:
        return
    plt.figure()
    for i, series_id in enumerate(data_frame.columns):
        plt.plot(data_frame.iloc[:, i], label=series_id)
        plt.title(title)
        plt.xlabel('Period')
        plt.ylabel('Dimension')
        plt.grid(True)
        plt.legend()
        plt.show()


def data_consistency_test_A():
    '''Project I: Canada Gross Domestic Product Data Comparison'''
    print(__doc__)
    '''Expenditure-Based Gross Domestic Product Series Used'''
    '''Income-Based Gross Domestic Product Series Not Used'''
    '''Series A Equals Series D,  However,  Series D Is Preferred Over Series A As It Is Yearly: v62307282 - 380-0066 Price indexes,  gross domestic product; Canada; Implicit price indexes; Gross domestic product at market prices (quarterly,  1961-03-01 to 2017-09-01)'''
    semi_frame_A = fetch_can_quarterly('03800066', 'v62307282', True)
    '''Series B Equals Both Series C & Series E,  However,  Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306896 - 380-0084 Gross domestic product at 2007 constant prices,  expenditure-based; Canada; Seasonally adjusted at annual rates; Gross domestic product at market prices (x 1, 000, 000) (quarterly,  1961-03-01 to 2017-09-01)'''
    semi_frame_B = fetch_can_quarterly('03800084', 'v62306896', True)
    '''Series C Equals Both Series B & Series E,  However,  Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306938 - 380-0084 Gross domestic product at 2007 constant prices,  expenditure-based; Canada; Unadjusted; Gross domestic product at market prices (x 1, 000, 000) (quarterly,  1961-03-01 to 2017-09-01)'''
    semi_frame_C = fetch_can_quarterly('03800084', 'v62306938', True)
    '''Series D Equals Series A,  However,  Series D Is Preferred Over Series A As It Is Yearly: v62471023 - 380-0102 Gross domestic product indexes; Canada; Implicit price indexes; Gross domestic product at market prices (annual,  1961 to 2016)'''
    semi_frame_D = fetch_can_annually('03800102', 'v62471023', True)
    '''Series E Equals Both Series B & Series C,  However,  Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62471340 - 380-0106 Gross domestic product at 2007 constant prices,  expenditure-based; Canada; Gross domestic product at market prices (x 1, 000, 000) (annual,  1961 to 2016)'''
    semi_frame_E = fetch_can_annually('03800106', 'v62471340', True)
    semi_frame_F = fetch_can_annually('03800518', 'v96411770', True)
    semi_frame_G = fetch_can_annually('03800566', 'v96391932', True)
    semi_frame_H = fetch_can_annually('03800567', 'v96730304', True)
    semi_frame_I = fetch_can_annually('03800567', 'v96730338', True)
    result_frame = pd.concat([semi_frame_A, semi_frame_B, semi_frame_C, semi_frame_D, semi_frame_E, \
                           semi_frame_F, semi_frame_G, semi_frame_H, semi_frame_I], axis=1, sort=True)
    result_frame = result_frame.dropna()
    SERA = result_frame.iloc[:, 0].div(result_frame.iloc[0, 0])
    SERB = result_frame.iloc[:, 4].div(result_frame.iloc[0, 4])
    SERC = result_frame.iloc[:, 5].div(result_frame.iloc[0, 5])
    SERD = result_frame.iloc[:, 7].div(result_frame.iloc[:, 6].div(result_frame.iloc[:, 5]/100))
    SERE = result_frame.iloc[:, 8].div(result_frame.iloc[0, 8])
    '''Option 1'''
    plot_canada_test(SERA, SERC)
    '''Option 2'''
    plot_canada_test(SERD, SERE)
    '''Option 3'''
    plot_canada_test(SERB, SERE)
    '''Option 4'''
    plot_canada_test(SERE.div(SERB), SERC)


def data_consistency_test_B():
    '''Project II: USA Fixed Assets Data Comparison'''
    print(__doc__)
    """Fixed Assets Series: k1ntotl1si000,  1925--2016"""
    semi_frame_A = fetch_usa_bea('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '201 Ann', 1925, 2016, 48)
    """Fixed Assets Series: kcntotl1si000,  1925--2016"""
    semi_frame_B = fetch_usa_bea('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '202 Ann', 1925, 2016, 48)
    """Not Used: Fixed Assets: k3ntotl1si000,  1925--2016,  Table 2.3. Historical-Cost Net Stock of Private Fixed Assets,  Equipment,  Structures,  and Intellectual Property Products by Type"""
    semi_frame_C = fetch_usa_bea('dataset USA BEA SFAT Release 2017-08-23 SectionAll_xls.zip', 'Section2ALL_xls.xls', '203 Ann', 1925, 2016, 48)
    result_frame = pd.concat([semi_frame_A, semi_frame_B, semi_frame_C], axis=1, sort=True)
    del semi_frame_A, semi_frame_B, semi_frame_C
    print(result_frame)


def data_consistency_test_C():
    '''Project III: USA BLS Unemployment Rate & Producer Price Index Manufacturing'''
    print(__doc__)
    '''LNU04000000: Bureau of Labor Statistics Unemployment Rate'''
    print(BLSLNU('dataset USA BLS 2015-02-23 ln.data.1.AllData'))
    '''LNU04000000: Bureau of Labor Statistics Unemployment Rate'''
    print(BLSLNU('dataset USA BLS 2017-07-06 ln.data.1.AllData'))
    '''PCUOMFG--OMFG--: Bureau of Labor Statistics Producer Price Index Manufacturing'''
    print(BLSPCUOMFG('dataset USA BLS pc.data.0.Current'))


def data_consistency_test_D():
    '''Project IV: USA Macroeconomic & Fixed Assets Data Tests'''
    print(__doc__)
    """Macroeconomic Data Tests"""
    """Tested: `A051RC1` != `A052RC1`+`A262RC1`"""
    test_procedure(['A051RC1', 'A052RC1', 'A262RC1'])
    """Tested: `Government` = `Federal`+`State and local`"""
    test_procedure(['A822RC1', 'A823RC1', 'A829RC1'])
    test_procedure(['A955RC1', 'A957RC1', 'A991RC1'])
    """Tested: `Federal` = `National defense`+`Nondefense`"""
    test_procedure(['A823RC1', 'A824RC1', 'A825RC1'])
    test_procedure(['A957RC1', 'A997RC1', 'A542RC1'])
    """Fixed Assets Data Tests"""
    result_frame = fetch_usa_bea_sfat_series()
    """Tested: `k3n31gd1es000` = `k3n31gd1eq000`+`k3n31gd1ip000`+`k3n31gd1st000`"""
#    subTestA(result_frame)
    """Comparison of `k3n31gd1es000` out of control_frame with `k3n31gd1es000` out of test_frame"""
#    subTestB(result_frame)
    """Future Project: Test Ratio of Manufacturing Fixed Assets to Overall Fixed Assets"""
    """To Do"""


def data_consistency_test_E():
    '''Project V: USA NBER Data Plotting'''
    print(__doc__)
    plot_nber('dataset USA NBER-CES MID sic5811.csv', 'mean')
    plot_nber('dataset USA NBER-CES MID sic5811.csv', 'sum')
    plot_nber('dataset USA NBER-CES MID naics5811.csv', 'mean')
    plot_nber('dataset USA NBER-CES MID naics5811.csv', 'sum')


data_consistency_test_A()
data_consistency_test_B()
data_consistency_test_C()
#data_consistency_test_D()
data_consistency_test_E()