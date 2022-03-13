# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:46:08 2021

@author: Mastermind
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


def fetch_bea_from_url(url):
    '''Downloading zip file from url'''
    r = requests.get(url)
    with open(url.split('/')[-1], 'wb') as s:
        s.write(r.content)
    with open(url.split('/')[-1]) as f:
      data_frame = pd.read_csv(f, thousands = ',')
    print('{}: Complete'.format(url))
    return data_frame


def bea_fetch(source, wkbk, wkst, start, finish, line):
    '''Data Frame Fetching from Bureau of Economic Analysis Zip Archives'''
    '''
    source: Name of Zip Archive,
    wkbk: Name of Excel File within Zip Archive,
    wkst: Name of Worksheet within Excel File within Zip Archive,
    boundary: 4+<Period_Finish>-<Period_Start>,
    line: Line'''
    boundary = 4-start+finish
    if source == None:
        xl = pd.ExcelFile(wkbk)
        source_frame = pd.read_excel(xl, wkst, usecols=range(2, boundary),
                                     skiprows=7)
    else:
        import zipfile
        with zipfile.ZipFile(source, 'r') as zf:
            with pd.ExcelFile(zf.open(wkbk)) as xl:
                source_frame = pd.read_excel(xl, wkst, usecols=range(2, boundary),
                                             skiprows=7)
    source_frame.dropna(inplace=True)
    source_frame.columns = source_frame.columns.to_series().replace({'^Unnamed: \d':'Period'},
                                                                    regex=True)
    source_frame = source_frame.set_index('Period').transpose()
    source_frame.index.name = 'Period'
    source_frame = source_frame[source_frame.columns[[line-1]]]
    return source_frame


def fetch_bea_from_loaded(source_frame, string):
    '''`NipaDataA.txt`: U.S. Bureau of Economic Analysis'''
    source_frame.rename(columns = {'Value':string}, inplace=True)
    result_frame = source_frame[source_frame.iloc[:,0] == string]
    result_frame = result_frame[result_frame.columns[[1,2]]]
    result_frame = result_frame.reset_index(drop=True)
    result_frame = result_frame.set_index('Period')
    result_frame.reset_index(level=0, inplace=True)
    result_frame = result_frame.set_index('Period')
    return result_frame


def fetch_classic(source, string):
    if source == 'dataset-usa-cobb-douglas.zip':
        source_frame = pd.read_csv(source, usecols=range(5, 8))
    elif source == 'dataset-douglas.zip':
        source_frame = pd.read_csv(source, usecols=range(4, 7))
    elif source == 'dataset-usa-kendrick.zip':
        source_frame = pd.read_csv(source, usecols=range(4, 7))
    result_frame = source_frame[source_frame.iloc[:,0] == string]
    del source_frame
    result_frame = result_frame[result_frame.columns[[1,2]]]
    result_frame.columns = result_frame.columns.str.title()
    result_frame.rename(columns={'Value':string}, inplace=True)
    result_frame.iloc[:,0] = result_frame.iloc[:,0].astype(int)
    result_frame.iloc[:,1] = pd.to_numeric(result_frame.iloc[:,1], errors='coerce')
    result_frame = result_frame.dropna()
    result_frame = result_frame.sort_values('Period')
    result_frame = result_frame.set_index('Period')
    return result_frame


def fetch_census(source, string, index):
    '''Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census, Historical Statistics of the United States,\
        1789--1945, Washington, D.C., 1949.
    U.S. Bureau of the Census. Historical Statistics of the United States,\
        Colonial Times to 1970, Bicentennial Edition. Washington, D.C., 1975.'''
    if source == 'dataset-usa-census1975.zip':
        source_frame = pd.read_csv(source, usecols=range(8, 11),
                                   dtype={'vector':str, 'period':str, 'value':str})
    else:
        source_frame = pd.read_csv(source, usecols=range(8, 11))
    source_frame = source_frame[source_frame.iloc[:,0] == string]
    source_frame = source_frame[source_frame.columns[[1,2]]]
    if source == 'dataset-usa-census1975.zip':
        source_frame.iloc[:,0] = source_frame.iloc[:,0].str[:4]
    else:
        pass
    source_frame.iloc[:,1] = source_frame.iloc[:,1].astype(float)
    source_frame.columns = source_frame.columns.str.title()
    source_frame.rename(columns={'Value':string}, inplace=True)
    source_frame.iloc[:,0] = source_frame.iloc[:,0].astype(int)
    source_frame = source_frame.sort_values('Period')
    source_frame = source_frame.reset_index(drop=True)
    source_frame = source_frame.groupby('Period').mean()
    if index:
        return source_frame
    else:
        source_frame.reset_index(level=0, inplace=True)
        return source_frame


def prices_inverse_single(source_frame):
    '''Intent: Returns Prices Icrement Series from Cumulative Deflator Series;
    source: pandas DataFrame'''
    D = source_frame.iloc[:,0].div(source_frame.iloc[:,0].shift(1))-1
    return D


def processing(source_frame, col):
    interim_frame = source_frame[source_frame.columns[[col]]]
    interim_frame = interim_frame.dropna()
    result_frame = prices_inverse_single(interim_frame)
    result_frame = result_frame.dropna()
    return result_frame


def frb_ip():
    '''Indexed Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018'''
    source_frame = pd.read_csv('dataset-usa-frb-US3_IP 2018-09-02.csv',
                               skiprows=7)
    source_frame.columns = source_frame.columns.to_series().replace({'[ .:;@_]':''},
                                                                    regex=True)
    source_frame[['Period', 'Mnth']] = source_frame['Unnamed0'].str.split('-', n=1,
                                                                          expand=True)
    source_frame = source_frame.groupby('Period').mean()
    source_frame.index = pd.to_numeric(source_frame.index, errors='ignore',
                                       downcast='integer')
    result_frame = source_frame[['AIPMASAIX']].dropna()
    return result_frame


def frb_fa():
    '''Returns Frame of Manufacturing Fixed Assets Series, Billion USD:
    result_frame.iloc[:,0]: Nominal;
    result_frame.iloc[:,1]: Real
    '''
    source_frame = pd.read_csv('dataset-usa-frb-invest_capital.csv',
                               skiprows=4, skipfooter=688, engine='python')
    source_frame.columns = source_frame.columns.to_series().replace({'Manufacturing':'Period'})
    source_frame = source_frame.set_index(source_frame.columns[0]).transpose()
    source_frame['frb_nominal'] = \
    source_frame.iloc[:,1]*source_frame.iloc[:,2].div(1000*source_frame.iloc[:,0])+\
    source_frame.iloc[:,4]*source_frame.iloc[:,5].div(1000*source_frame.iloc[:,3])
    source_frame['frb_real'] = source_frame.iloc[:,2].div(1000)+\
    source_frame.iloc[:,5].div(1000)
    source_frame.index = pd.to_numeric(source_frame.index, errors='ignore',
                                       downcast='integer')
    result_frame = source_frame[source_frame.columns[[6,7]]]
    return result_frame


def frb_fa_def():
    '''Returns Frame of Deflator for Manufacturing Fixed Assets Series, Index:
    result_frame.iloc[:,0]: Deflator
    '''
    source_frame = pd.read_csv('dataset-usa-frb-invest_capital.csv',
                               skiprows=4, skipfooter=688, engine='python')
    source_frame.columns = source_frame.columns.to_series().replace({'Manufacturing':'Period'})
    source_frame = source_frame.set_index(source_frame.columns[0]).transpose()
    source_frame.index = pd.to_numeric(source_frame.index, errors='ignore',
                                       downcast='integer')
    source_frame['fa_def_frb'] = (source_frame.iloc[:,1]+source_frame.iloc[:,4]).div(source_frame.iloc[:,0]+source_frame.iloc[:,3])
    result_frame = source_frame[source_frame.columns[[6]]]
    return result_frame


def fetch_infcf():
    '''Retrieve Yearly Price Rates from `dataset-usa-infcf16652007.zip`'''
    source_frame = pd.read_csv('dataset-usa-infcf16652007.zip',
                               usecols=range(4,7))
    series = source_frame.iloc[:,0].unique()
    i = 0
    for ser in series:
        current_frame = source_frame[source_frame.iloc[:,0] == ser]
        current_frame = current_frame[current_frame.columns[[1,2]]]
        current_frame.columns = current_frame.columns.str.title()
        current_frame.rename(columns={'Value':ser}, inplace=True)
        current_frame = current_frame.set_index('Period')
        current_frame.iloc[:,0] = current_frame.iloc[:,0].rdiv(1)
        current_frame = -prices_inverse_single(current_frame) ## Put '-' Is the Only Way to Comply with the Rest of Study
        if i == 0:
            result_frame = current_frame
        elif i >= 1:
            result_frame = pd.concat([result_frame, current_frame],
                                     axis=1, sort=True)
        del current_frame
        i += 1
    result_frame = result_frame[result_frame.columns[range(14)]]
    result_frame['cpiu_fused'] = result_frame.mean(1)
    result_frame = result_frame[result_frame.columns[[14]]]
    return result_frame


def fetch_capital():
    '''Series Not Used - `k3ntotl1si00`'''
    semi_frame_a = fetch_classic('dataset-usa-cobb-douglas.zip', 'CDT2S1') ##Annual Increase in Terms of Cost Price (1)
    semi_frame_b = fetch_classic('dataset-usa-cobb-douglas.zip', 'CDT2S3') ##Annual Increase in Terms of 1880 dollars (3)
    semi_frame_c = fetch_classic('dataset-usa-cobb-douglas.zip', 'CDT2S4') ##Total Fixed Capital in 1880 dollars (4)
    loaded_frame = fetch_bea_from_url('https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt')
    '''Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net\
        Stock of Private Nonresidential Fixed Assets by Industry Group and\
            Legal Form of Organization'''
    semi_frame_d = fetch_bea_from_loaded(loaded_frame, 'k1n31gd1es00')
    '''Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3.\
        Historical-Cost Net Stock of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    semi_frame_e = fetch_bea_from_loaded(loaded_frame, 'k3n31gd1es00')
    semi_frame_f = fetch_census('dataset-usa-census1975.zip', 'P0107', True)
    semi_frame_g = fetch_census('dataset-usa-census1975.zip', 'P0110', True)
    semi_frame_h = fetch_census('dataset-usa-census1975.zip', 'P0119', True)
    '''Kendrick J.W., Productivity Trends in the United States, Page 320'''
    semi_frame_i = fetch_classic('dataset-usa-kendrick.zip', 'KTA15S08')
    '''Douglas P.H., Theory of Wages, Page 332'''
    semi_frame_j = fetch_classic('dataset-douglas.zip', 'DT63AS01')
    '''FRB Data'''
    semi_frame_k = frb_fa()
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,\
                              semi_frame_d, semi_frame_e, semi_frame_f,\
                              semi_frame_g, semi_frame_h, semi_frame_i,\
                              semi_frame_j, semi_frame_k], axis=1, sort=True)
    return result_frame


def cobb_douglas_capital_extension():
    '''Existing Capital Dataset'''
    source_frame = fetch_capital()
    '''Convert Capital Series into Current (Historical) Prices'''
    source_frame['nominal_cbb_dg'] = source_frame.iloc[:,0]*source_frame.iloc[:,2].div(1000*source_frame.iloc[:,1])
    source_frame['nominal_census'] = source_frame.iloc[:,5]*source_frame.iloc[:,7].div(source_frame.iloc[:,6])
    source_frame['nominal_dougls'] = source_frame.iloc[:,0]*source_frame.iloc[:,9].div(1000*source_frame.iloc[:,1])
    source_frame['nominal_kndrck'] = source_frame.iloc[:,5]*source_frame.iloc[:,8].div(1000*source_frame.iloc[:,6])
    source_frame.iloc[:,15] = source_frame.iloc[66,6]*source_frame.iloc[:,15].div(source_frame.iloc[66,5])
    '''Douglas P.H. -- Kendrick J.W. (Blended) Series'''
    source_frame['nominal_doug_kndrck'] = source_frame.iloc[:,14:16].mean(1)
    '''Cobb C.W., Douglas P.H. -- FRB (Blended) Series'''
    source_frame['nominal_cbb_dg_frb'] = source_frame.iloc[:,[12,10]].mean(1)
    '''Capital Structure Series: `Cobb C.W., Douglas P.H. -- FRB (Blended)\
        Series` to `Douglas P.H. -- Kendrick J.W. (Blended) Series`'''
    source_frame['struct_ratio'] = source_frame.iloc[:,17].div(source_frame.iloc[:,16])
    '''Filling the Gaps within Capital Structure Series'''
    source_frame.iloc[6:36,18].fillna(source_frame.iloc[36,18], inplace=True)
    source_frame.iloc[36:,18].fillna(0.275, inplace=True)
    '''Patch Series `Douglas P.H. -- Kendrick J.W. (Blended) Series`\
        Multiplied by `Capital Structure Series`'''
    source_frame['nominal_patch'] = source_frame.iloc[:,16].mul(source_frame.iloc[:,18])
    '''`Cobb C.W., Douglas P.H. -- FRB (Blended) Series` Patched with `Patch Series`'''
    source_frame['nominal_extended'] = source_frame.iloc[:,[17,19]].mean(1)
    source_frame = source_frame[source_frame.columns[[20]]]
    source_frame.dropna(inplace=True)
    return source_frame


def cobb_douglas_capital_deflator():
    '''Fixed Assets Deflator, 2009=100'''
    base = (84, 177, 216) ##2009, 1970, 2009
    '''Combine L2, L15, E7, E23, E40, E68 & P107/P110'''
    '''Bureau of Labor Statistics
    Data Not Used As It Covers Only Years of 1998--2017'''
    '''Results:
    fetch_census('dataset-usa-census1949.zip', 'L0036', True) Offset with\
        fetch_census('dataset-usa-census1975.zip', 'E0183', True)
    fetch_census('dataset-usa-census1949.zip', 'L0038', True) Offset with\
        fetch_census('dataset-usa-census1975.zip', 'E0184', True)
    fetch_census('dataset-usa-census1949.zip', 'L0039', True) Offset with\
        fetch_census('dataset-usa-census1975.zip', 'E0185', True)
    fetch_census('dataset-usa-census1975.zip', 'E0052', True) Offset With\
        fetch_census('dataset-usa-census1949.zip', 'L0002', True)'''
    '''Cost-Of-Living Indexes'''
    '''E183: Federal Reserve Bank, 1913=100'''
    '''E184: Burgess, 1913=100'''
    '''E185: Douglas, 1890-99=100'''
    sub_frame_a = fetch_classic('dataset-usa-cobb-douglas.zip', 'CDT2S1')
    sub_frame_b = fetch_classic('dataset-usa-cobb-douglas.zip', 'CDT2S3')
    sub_frame_c = fetch_census('dataset-usa-census1949.zip', 'L0001', True)
    sub_frame_d = fetch_census('dataset-usa-census1949.zip', 'L0002', True)
    sub_frame_e = fetch_census('dataset-usa-census1949.zip', 'L0015', True)
    sub_frame_f = fetch_census('dataset-usa-census1949.zip', 'L0037', True)
    sub_frame_g = fetch_census('dataset-usa-census1975.zip', 'E0007', True)
    sub_frame_h = fetch_census('dataset-usa-census1975.zip', 'E0008', True)
    sub_frame_i = fetch_census('dataset-usa-census1975.zip', 'E0009', True)
    sub_frame_j = fetch_census('dataset-usa-census1975.zip', 'E0023', True)
    sub_frame_k = fetch_census('dataset-usa-census1975.zip', 'E0040', True)
    sub_frame_l = fetch_census('dataset-usa-census1975.zip', 'E0068', True)
    sub_frame_m = fetch_census('dataset-usa-census1975.zip', 'E0183', True)
    sub_frame_n = fetch_census('dataset-usa-census1975.zip', 'E0184', True)
    sub_frame_o = fetch_census('dataset-usa-census1975.zip', 'E0185', True)
    sub_frame_p = fetch_census('dataset-usa-census1975.zip', 'E0186', True)
    sub_frame_q = fetch_census('dataset-usa-census1975.zip', 'P0107', True)
    sub_frame_r = fetch_census('dataset-usa-census1975.zip', 'P0110', True)
    sub_frame_s = frb_fa_def()
    sub_frame_q = sub_frame_q[22:]
    sub_frame_r = sub_frame_r[22:]
    basis_frame = pd.concat([sub_frame_a, sub_frame_b, sub_frame_c,\
                             sub_frame_d, sub_frame_e, sub_frame_f,\
                             sub_frame_g, sub_frame_h, sub_frame_i,\
                             sub_frame_j, sub_frame_k, sub_frame_l,\
                             sub_frame_m, sub_frame_n, sub_frame_o,\
                             sub_frame_p, sub_frame_q, sub_frame_r,\
                             sub_frame_s], axis=1, sort=True)
    del sub_frame_a, sub_frame_b, sub_frame_c, sub_frame_d, sub_frame_e,\
        sub_frame_f, sub_frame_g, sub_frame_h, sub_frame_i, sub_frame_j,\
        sub_frame_k, sub_frame_l, sub_frame_m, sub_frame_n, sub_frame_o,\
        sub_frame_p, sub_frame_q, sub_frame_r, sub_frame_s
    basis_frame['fa_def_cd'] = basis_frame.iloc[:,0].div(basis_frame.iloc[:,1])
    basis_frame['fa_def_cn'] = basis_frame.iloc[:,16].div(basis_frame.iloc[:,17])
    '''Cobb--Douglas'''
    semi_frame_a = processing(basis_frame, 19)
    '''Bureau of Economic Analysis'''
    loaded_frame = fetch_bea_from_url('https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt')
    '''Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net\
        Stock of Private Nonresidential Fixed Assets by Industry Group and\
            Legal Form of Organization'''
    sub_frame_a = fetch_bea_from_loaded(loaded_frame, 'k1n31gd1es00')
    '''Fixed Assets: kcn31gd1es00, 1925--2019, Table 4.2. Chain-Type Quantity\
        Indexes for Net Stock of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    sub_frame_b = fetch_bea_from_loaded(loaded_frame, 'kcn31gd1es00')
    '''Not Used: Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3.\
        Historical-Cost Net Stock of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    sub_frame_c = fetch_bea_from_loaded(loaded_frame, 'k3n31gd1es00')
    '''Not Used: Fixed Assets: k3ntotl1si00, 1925--2019, Table 2.3.\
        Historical-Cost Net Stock of Private Fixed Assets, Equipment,\
            Structures, and Intellectual Property Products by Type'''
    sub_frame_d = fetch_bea_from_loaded(loaded_frame, 'k3ntotl1si00')
    '''Not Used: mcn31gd1es00, 1925--2019, Table 4.5. Chain-Type Quantity\
        Indexes for Depreciation of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    sub_frame_e = fetch_bea_from_loaded(loaded_frame, 'mcn31gd1es00')
    '''Not Used: mcntotl1si00, 1925--2019, Table 2.5. Chain-Type Quantity\
        Indexes for Depreciation of Private Fixed Assets, Equipment,\
            Structures, and Intellectual Property Products by Type'''
    sub_frame_f = fetch_bea_from_loaded(loaded_frame, 'mcntotl1si00')
    '''Real Values'''
    semi_frame_b = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)
    del loaded_frame, sub_frame_a, sub_frame_b, sub_frame_c, sub_frame_d,\
        sub_frame_e, sub_frame_f
    semi_frame_b['ppi_bea'] = 100*semi_frame_b.iloc[:,0].div(semi_frame_b.iloc[base[0],0]*semi_frame_b.iloc[:,1])
    semi_frame_b.iloc[:,2] = processing(semi_frame_b, 2)
    semi_frame_b = semi_frame_b[semi_frame_b.columns[[2]]]
    '''Bureau of the Census'''
    '''Correlation Test:
    `kendall_frame = result_frame.corr(method='kendall')`
    `pearson_frame = result_frame.corr(method='pearson')`
    `spearman_frame = result_frame.corr(method='spearman')`
    Correlation Test Result: kendall & pearson & spearman: L2, L15, E7, E23, E40, E68'''
    sub_frame_a = processing(basis_frame, 3)
    sub_frame_b = processing(basis_frame, 4)
    sub_frame_c = processing(basis_frame, 6)
    sub_frame_d = processing(basis_frame, 9)
    sub_frame_e = processing(basis_frame, 10)
    sub_frame_f = processing(basis_frame, 11)
    sub_frame_g = processing(basis_frame, 20)
    semi_frame_c = pd.concat([sub_frame_a, sub_frame_b, sub_frame_c,\
                              sub_frame_d, sub_frame_e, sub_frame_f,\
                                  sub_frame_g], axis=1, sort=True)
    del sub_frame_a, sub_frame_b, sub_frame_c, sub_frame_d, sub_frame_e,\
        sub_frame_f, sub_frame_g
    semi_frame_c['ppi_census_fused'] = semi_frame_c.mean(1)
    semi_frame_c = semi_frame_c[semi_frame_c.columns[[7]]]
    '''Federal Reserve'''
    semi_frame_d = processing(basis_frame, 18)
    '''Robert C. Sahr, 2007'''
    semi_frame_e = fetch_infcf()
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,\
                              semi_frame_d, semi_frame_e], axis=1, sort=True)
    del semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e
    result_frame = result_frame[128:]
    result_frame['def_cum_bea'] = np.cumprod(1+result_frame.iloc[:,1])
    result_frame['def_cum_cen'] = np.cumprod(1+result_frame.iloc[:,2])
    result_frame['def_cum_frb'] = np.cumprod(1+result_frame.iloc[:,3])
    result_frame['def_cum_sah'] = np.cumprod(1+result_frame.iloc[:,4])
    result_frame.iloc[:,5] = result_frame.iloc[:,5].div(result_frame.iloc[base[1],5])
    result_frame.iloc[:,6] = result_frame.iloc[:,6].div(result_frame.iloc[base[1],6])
    result_frame.iloc[:,7] = result_frame.iloc[:,7].div(result_frame.iloc[base[1],7])
    result_frame.iloc[:,8] = result_frame.iloc[:,8].div(result_frame.iloc[base[1],8])
    result_frame['def_cum_com'] = result_frame.iloc[:,[5,6,7]].mean(1)
    result_frame['fa_def_com'] = processing(result_frame, 9)
    result_frame.iloc[:,9] = result_frame.iloc[:,9].div(result_frame.iloc[base[2],9])
    result_frame = result_frame[result_frame.columns[[9]]]
    result_frame.dropna(inplace=True)
    return result_frame


def cobb_douglas_labor_extension():
    base = 14 ##1899
    '''Manufacturing Laborers` Series Comparison
    semi_frame_a: Cobb C.W., Douglas P.H. Labor Series
    semi_frame_b: Census Bureau 1949, D69
    semi_frame_c: Census Bureau 1949, J4
    semi_frame_d: Census Bureau 1975, D130
    semi_frame_e: Census Bureau 1975, P5
    semi_frame_f: Census Bureau 1975, P62
    semi_frame_g: Bureau of Economic Analysis, H4313C & J4313C & A4313C & N4313C
    semi_frame_h: J.W. Kendrick, Productivity Trends in the United States,\
        Table D-II, `Persons Engaged` Column, pp. 465--466
    semi_frame_i: Yu.V. Kurenkov
    Bureau of Labor Statistics
    Federal Reserve Board'''
    semi_frame_a = fetch_classic('dataset-usa-cobb-douglas.zip', 'CDT3S1') ## Average Number Employed (in thousands)
    semi_frame_b = fetch_census('dataset-usa-census1949.zip', 'D0069', True)
    semi_frame_c = fetch_census('dataset-usa-census1949.zip', 'J0004', True)
    semi_frame_d = fetch_census('dataset-usa-census1975.zip', 'D0130', True)
    semi_frame_e = fetch_census('dataset-usa-census1975.zip', 'P0005', True)
    semi_frame_f = fetch_census('dataset-usa-census1975.zip', 'P0062', True)
    loaded_frame = fetch_bea_from_url('https://apps.bea.gov/national/Release/TXT/NipaDataA.txt')
    sub_frame_a = fetch_bea_from_loaded(loaded_frame, 'H4313C')
    sub_frame_b = fetch_bea_from_loaded(loaded_frame, 'J4313C')
    sub_frame_c = fetch_bea_from_loaded(loaded_frame, 'A4313C')
    sub_frame_d = fetch_bea_from_loaded(loaded_frame, 'N4313C')
    semi_frame_g = pd.concat([sub_frame_a, sub_frame_b, sub_frame_c, sub_frame_d],
                             axis=1, sort=True)
    del loaded_frame, sub_frame_a, sub_frame_b, sub_frame_c, sub_frame_d
    semi_frame_g = semi_frame_g.mean(1)
    semi_frame_g = semi_frame_g.to_frame(name='BEA')
    semi_frame_h = fetch_classic('dataset-usa-kendrick.zip', 'KTD02S02')
    semi_frame_i = pd.read_csv('dataset-usa-reference-ru-kurenkov-yu-v.csv',
                               usecols=[0,2])
    semi_frame_i = semi_frame_i.set_index('Period')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,\
                              semi_frame_d, semi_frame_e, semi_frame_f,\
                              semi_frame_g, semi_frame_h, semi_frame_i],
                             axis=1, sort=True)
    result_frame['kendrick'] = result_frame.iloc[base,0]*result_frame.iloc[:,7].div(result_frame.iloc[base,7])
    result_frame['labor'] = result_frame.iloc[:,[0,1,3,6,8,9]].mean(1)
    result_frame = result_frame[result_frame.columns[[10]]]
    result_frame.dropna(inplace=True)
    result_frame = result_frame[2:]
    return result_frame


def cobb_douglas_product_extension():
    base = (109, 149) ##1899, 1939
    '''Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic\
        Research Index of Physical Output, All Manufacturing Industries.'''
    semi_frame_a = fetch_census('dataset-usa-census1949.zip', 'J0013', True)
    '''Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of\
        Physical Production of Manufacturing'''
    semi_frame_b = fetch_census('dataset-usa-census1949.zip', 'J0014', True)
    '''Bureau of the Census, 1975, Page 667, P17: Edwin Frickey Index of\
        Manufacturing Production'''
    semi_frame_c = fetch_census('dataset-usa-census1975.zip', 'P0017', True)
    '''The Revised Index of Physical Production for All Manufacturing In the\
        United States, 1899--1926'''
    semi_frame_d = fetch_classic('dataset-douglas.zip', 'DT24AS01')
    '''Federal Reserve, AIPMASAIX'''
    semi_frame_e = frb_ip()
    '''Joseph H. Davis Production Index'''
    semi_frame_f = pd.read_excel('dataset-usa-davis-j-h-ip-total.xls', skiprows=4)
    semi_frame_f.columns = ['Period', 'davis_index']
    semi_frame_f = semi_frame_f.set_index('Period')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,\
                              semi_frame_d, semi_frame_e, semi_frame_f],
                             axis=1, sort=True)
    result_frame.iloc[:,1] = result_frame.iloc[:,1].div(result_frame.iloc[base[0],1]/100)
    result_frame.iloc[:,5] = result_frame.iloc[:,5].div(result_frame.iloc[base[0],5]/100)
    result_frame['fused_classic'] = result_frame.iloc[:,[0,1,2,3,5]].mean(1)
    result_frame.iloc[:,4] = result_frame.iloc[:,4].div(result_frame.iloc[base[1],4]/100)
    result_frame.iloc[:,6] = result_frame.iloc[:,6].div(result_frame.iloc[base[1],6]/100)
    result_frame['fused'] = result_frame.iloc[:,[4,6]].mean(1)
    result_frame = result_frame[result_frame.columns[[7]]]
    return result_frame


def dataset():
    '''Data Fetch'''
    '''Data Fetch for Capital'''
    capital_frame_a = cobb_douglas_capital_extension()
    '''Data Fetch for Capital Deflator'''
    capital_frame_b = cobb_douglas_capital_deflator()
    capital_frame = pd.concat([capital_frame_a, capital_frame_b], axis=1, sort=True)
    capital_frame.dropna(inplace=True)
    capital_frame['capital_real'] = capital_frame.iloc[:,0].div(capital_frame.iloc[:,1])
    '''Data Fetch for Labor'''
    labor_frame = cobb_douglas_labor_extension()
    '''Data Fetch for Product'''
    product_frame = cobb_douglas_product_extension()
    result_frame = pd.concat([capital_frame.iloc[:,2], labor_frame, product_frame],
                             axis=1, sort=True).dropna()
    result_frame = result_frame.div(result_frame.iloc[0,:])
    return result_frame


def cobb_douglas_plot(source_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Capital,
    source_frame.iloc[:, 1]: Labor,
    source_frame.iloc[:, 2]: Product
    '''
    def pl(series, k=0.25, b=1.01):
        return b*series**(-k)


    def pc(series, k=0.25, b=1.01):
        return b*series**(1-k)


    function_dict = {'figure_a':'Chart I Progress in Manufacturing %d$-$%d (%d=100)',
                'figure_b':'Chart II Theoretical and Actual Curves of Production %d$-$%d (%d=100)',
                'figure_c':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
                'figure_d':'Chart IV Percentage Deviations of Computed from Actual Product %d$-$%d'}
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])
    from numpy.lib.scimath import log
    X = log(X.astype('float64'))
    Y = log(Y.astype('float64'))
    k, b = np.polyfit(X, Y, 1) ## Original: k = 0.25
    b = np.exp(b)
    source_frame['prod_comp'] = b*(source_frame.iloc[:, 0]**k)*(source_frame.iloc[:, 1]**(1-k))
    source_frame['prod_roll'] = source_frame.iloc[:, 2].rolling(window=3, center=True).mean()
    source_frame['prod_roll_comp'] = source_frame.iloc[:, 3].rolling(window=3, center=True).mean()
    source_frame['sub_prod'] = source_frame.iloc[:, 2].sub(source_frame.iloc[:, 4])
    source_frame['sub_comp'] = source_frame.iloc[:, 3].sub(source_frame.iloc[:, 5])
    source_frame['dev_prod'] = source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])-1
    plt.figure(1)
    plt.semilogy(source_frame.iloc[:, 0], label='Fixed Capital')
    plt.semilogy(source_frame.iloc[:, 1], label='Labor Force')
    plt.semilogy(source_frame.iloc[:, 2], label='Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(function_dict['figure_a'] %(source_frame.index[0],
                                          source_frame.index[len(source_frame)-1],
                                          source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(source_frame.iloc[:, 2], label='Actual Product')
    plt.semilogy(source_frame.iloc[:, 3], label='Computed Product, $P\'=%fL^{%f}C^{%f}$' %(b, 1-k, k))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(function_dict['figure_b'] %(source_frame.index[0],
                                          source_frame.index[len(source_frame)-1],
                                          source_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 6], label='Deviations of $P$')
    plt.plot(source_frame.iloc[:, 7], '--', label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(function_dict['figure_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])-1)
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(function_dict['figure_d'] %(source_frame.index[0],
                                        source_frame.index[len(source_frame)-1]))
    plt.grid(True)
    plt.figure(5, figsize=(5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(source_frame.iloc[:, 1].div(source_frame.iloc[:, 0]),
              source_frame.iloc[:, 2].div(source_frame.iloc[:, 1]))
    plt.scatter(source_frame.iloc[:, 1].div(source_frame.iloc[:, 0]),
              source_frame.iloc[:, 2].div(source_frame.iloc[:, 0]))
    plt.plot(lc, pl(lc, k=k, b=b), label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, pc(lc, k=k, b=b), label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title('Relative Final Productivities of Labor and Capital')
    plt.legend()
    plt.grid(True)
    plt.show()


result_frame = dataset()
cobb_douglas_plot(result_frame)