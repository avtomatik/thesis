# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:17:48 2020

@author: Mastermind
"""


def get_dataset_combined():
    '''Most Up-To-Date Version'''
    file_name = 'dataset_usa_bea_nipadataa.txt'
    semi_frame_a = fetch_bea_usa(file_name, 'A006RC')
    semi_frame_b = fetch_bea_usa(file_name, 'A006RD')
    semi_frame_c = fetch_bea_usa(file_name, 'A008RC')
    semi_frame_d = fetch_bea_usa(file_name, 'A008RD')
    semi_frame_e = fetch_bea_usa(file_name, 'A032RC')
    semi_frame_f = fetch_bea_usa(file_name, 'A191RA')
    semi_frame_g = fetch_bea_usa(file_name, 'A191RC')
    semi_frame_h = fetch_bea_usa(file_name, 'A191RX')
    sub_frame_a = fetch_bea_usa(file_name, 'H4313C')
    sub_frame_b = fetch_bea_usa(file_name, 'J4313C')
    sub_frame_c = fetch_bea_usa(file_name, 'A4313C')
    sub_frame_d = fetch_bea_usa(file_name, 'N4313C')
    semi_frame_i = pd.concat(
        [sub_frame_a, sub_frame_b, sub_frame_c, sub_frame_d], axis=1, sort=True)

    semi_frame_i = semi_frame_i.mean(1)
    semi_frame_i = semi_frame_i.to_frame(name='Labor')
    semi_frame_j = fetch_bea_usa(file_name, 'W170RC')
    semi_frame_k = fetch_bea_usa(file_name, 'W170RX')
# =============================================================================
# Fixed Assets Series: K100701, 1951--1969
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section5ALL_Hist.xls', '51000 Ann', 'K100701')
# =============================================================================
# Fixed Assets Series: K100701, 1969--2013
# =============================================================================
    file_name = 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section5all_xls.xls', '51000 Ann', 'K100701')
    semi_frame_l = sub_frame_a.append(sub_frame_b).drop_duplicates()

# =============================================================================
# US BEA Fixed Assets Series Tests
# =============================================================================
# =============================================================================
# Investment in Fixed Assets, Private, i3ptotl1es000, 1901--2016
# =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_m = fetch_usa_bea(
        file_name, 'Section1ALL_xls.xls', '105 Ann', 'i3ptotl1es000')
# =============================================================================
# Chain-Type Quantity Index for Investment in Fixed Assets, Private, icptotl1es000, 1901--2016
# =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_n = fetch_usa_bea(
        file_name, 'Section1ALL_xls.xls', '106 Ann', 'icptotl1es000')
# =============================================================================
# Current-Cost Net Stock of Fixed Assets, Private, k1ptotl1es000, 1925--2016
# =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_o = fetch_usa_bea(
        file_name, 'Section1ALL_xls.xls', '101 Ann', 'k1ptotl1es000')
# =============================================================================
# Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es000, 1925--2016
# =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_p = fetch_usa_bea(
        file_name, 'Section2ALL_xls.xls', '203 Ann', 'k3ptotl1es000')
# =============================================================================
# Chain-Type Quantity Indexes for Net Stock of Fixed Assets, Private, kcptotl1es000, 1925--2016
# =============================================================================
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_q = fetch_usa_bea(
        file_name, 'Section1ALL_xls.xls', '102 Ann', 'kcptotl1es000')
    semi_frame_r = get_dataset_usa_frb_ms()
    semi_frame_s = get_dataset_usa_frb_ms()
    semi_frame_t = get_dataset_usa_frb_ms()
    file_name = 'dataset_usa_0025_p_r.txt'
    semi_frame_u = pd.read_csv(file_name, index_col=0)
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e,
                              semi_frame_f, semi_frame_g, semi_frame_h, semi_frame_i, semi_frame_j,
                              semi_frame_k, semi_frame_l, semi_frame_m, semi_frame_n, semi_frame_o,
                              semi_frame_p, semi_frame_q, semi_frame_r, semi_frame_s, semi_frame_t,
                              semi_frame_u], axis=1, sort=True)
    return result_frame


def preprocessing_a(source_frame):
    source_frame = source_frame.iloc[:, [0, 4, 6, 7]]
    source_frame = source_frame.dropna()
    source_frame = source_frame.div(source_frame.iloc[0, :])
    source_frame.reset_index(level=0, inplace=True)
    return source_frame


def preprocessing_b(source_frame):
    source_frame = source_frame.iloc[:, [0, 6, 7, 20]]
    source_frame = source_frame.dropna()
    source_frame.reset_index(level=0, inplace=True)
    return source_frame


def preprocessing_c(source_frame):
    source_frame_production = source_frame.iloc[:, [0, 6, 7]]
    source_frame_production = source_frame_production.dropna()
    source_frame_production = source_frame_production.div(
        source_frame_production.iloc[0, :])
    source_frame_money = source_frame.iloc[:, 18:20]
    source_frame_money = source_frame_money.mean(1)
    source_frame_money = pd.DataFrame(source_frame_money, columns=[
                                      'M1'])  # Convert Series to Dataframe
    source_frame_money = source_frame_money.dropna()
    source_frame_money = source_frame_money.div(source_frame_money.iloc[0, :])
    result_frame = pd.concat(
        [source_frame_production, source_frame_money], axis=1)
    result_frame = result_frame.dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    result_frame.reset_index(level=0, inplace=True)
    return result_frame


def preprocessing_d(source_frame):
    source_frame = source_frame.iloc[:, [0, 1, 2, 3, 7]]
    source_frame = source_frame.dropna()
    source_frame.reset_index(level=0, inplace=True)
    return source_frame


def preprocessing_e(source_frame):
    """Works on Result of `get_dataset_combined_archived`"""
    """`Real` Investment"""
    source_frame['inv'] = source_frame.iloc[:, 0].mul(
        source_frame.iloc[:, 7]).div(source_frame.iloc[:, 6])
    """`Real` Capital"""
    source_frame['cap'] = source_frame.iloc[:, 11].mul(
        source_frame.iloc[:, 7]).div(source_frame.iloc[:, 6])
    """Nominal DataSet"""
    nominal_frame = source_frame.iloc[:, [0, 6, 11]].dropna()
    """`Real` DataSet"""
    real_frame = source_frame.iloc[:, [21, 7, 22]].dropna()
    return nominal_frame, real_frame


source_frame_a = get_dataset_combined_archived()
source_frame_b = get_dataset_combined()
# =============================================================================
# Project: Initial Version Dated: 05 October 2012
# =============================================================================
result_frame_a_b = preprocessing_a(source_frame_a)
result_frame_a_c = preprocessing_a(source_frame_b)
plot_a(result_frame_a_b)
plot_a(result_frame_a_c)
# =============================================================================
# Project: Initial Version Dated: 23 November 2012
# =============================================================================
result_frame_b_b = preprocessing_b(source_frame_a)
result_frame_b_c = preprocessing_b(source_frame_b)
plot_b(result_frame_b_b)
plot_b(result_frame_b_c)
# =============================================================================
# Project: Initial Version Dated: 16 June 2013
# =============================================================================
result_frame_c_b = preprocessing_c(source_frame_a)
result_frame_c_c = preprocessing_c(source_frame_b)
plot_c(result_frame_c_b)
plot_c(result_frame_c_c)
# =============================================================================
# Project: Initial Version Dated: 15 June 2015
# =============================================================================
result_frame_d = preprocessing_d(source_frame_b)
plot_d(result_frame_d)
# =============================================================================
# Project: Initial Version Dated: 17 February 2013
# =============================================================================
result_frame_e_a, result_frame_e_b = preprocessing_e(source_frame_a)
plot_e(result_frame_e_a)
plot_e(result_frame_e_b)
# =============================================================================
# Project: BEA Data Compared with Kurenkov Yu.V. Data
# =============================================================================
result_frame_f_a, result_frame_f_b, result_frame_f_c, result_frame_f_d = preprocessing_f(
    source_frame_a)
plot_f(result_frame_f_a, result_frame_f_b, result_frame_f_c, result_frame_f_d)
