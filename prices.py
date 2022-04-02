# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:47:52 2020

@author: Mastermind
"""


def get_dataset_usa_bls_cpiu():
    '''BLS CPI-U Price Index Fetch'''
    file_name = 'dataset_usa_bls_cpiai.txt'
    data_frame = pd.read_csv(file_name,
                             sep='\s+',
                             index_col=0,
                             usecols=range(13),
                             skiprows=16)
    data_frame.rename_axis('period', inplace=True)
    data_frame['mean'] = data_frame.mean(1)
    data_frame['sqrt'] = data_frame.iloc[:, :-1].prod(1).pow(1/12)
# =============================================================================
# Tests
# =============================================================================
    data_frame['mean_less_sqrt'] = data_frame.iloc[:, -
                                                   2].sub(data_frame.iloc[:, -1])
    data_frame['dec_on_dec'] = data_frame.iloc[:, -
                                               3].div(data_frame.iloc[:, -3].shift(1)).sub(1)
    data_frame['mean_on_mean'] = data_frame.iloc[:, -
                                                 4].div(data_frame.iloc[:, -4].shift(1)).sub(1)
    return data_frame.iloc[:, [-1]].dropna()


def get_dataset_bea_def():
    '''Intent: Returns Cumulative Price Index for Some Base Year from Certain Type BEA Deflator File'''
    file_name = 'dataset_usa_bea-GDPDEF.xls'
    data_frame = pd.read_excel(file_name, skiprows=15, parse_dates=[0])
    data_frame['period'] = data_frame.iloc[:, 0].dt.year
    return data_frame.groupby(data_frame.columns[-1]).prod().pow(1/4)


def get_dataset_bea_gdp():
    '''Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    '''Nominal Nominal Gross Domestic Product Series: A191RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    semi_frame_a = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_b = sub_frame_a.append(sub_frame_b).drop_duplicates()

    result_frame = pd.concat([semi_frame_a, semi_frame_b], axis=1, sort=False)
    return result_frame


def price_direct(data_frame, base):
    '''Intent: Returns Cumulative Price Index for Base Year;
    data_frame.iloc[:, 0]: Growth Rate;
    base: Base Year'''
    '''Cumulative Price Index'''
    data_frame['p_i'] = sp.cumprod(1 + data_frame.iloc[:, 0])
    '''Cumulative Price Index for the Base Year'''
    data_frame['cpi'] = data_frame.iloc[:, 1].div(
        data_frame.iloc[base-data_frame.index[0], 1])
    return data_frame.iloc[:, [2]]


def price_inverse(source_frame):
    '''Intent: Returns Growth Rate from Cumulative Price Index for Some Base Year;
    source_frame.iloc[:, 0]: Cumulative Price Index for Some Base Year'''
    source_frame['gri'] = source_frame.iloc[:, 0].div(
        source_frame.iloc[:, 0].shift(1)).sub(1)
    result_frame = source_frame.iloc[:, [1]].dropna()
    return result_frame


def price_inverse_double(source_frame):
    '''Intent: Returns Growth Rate from Nominal & Real Prices Series;
    source_frame.iloc[:, 0]: Nominal Prices;
    source_frame.iloc[:, 1]: Real Prices'''
    source_frame['cpi'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    source_frame['gri'] = source_frame.iloc[:, 2].div(
        source_frame.iloc[:, 2].shift(1)).sub(1)
    result_frame = source_frame.iloc[:, [3]].dropna()
    return result_frame


def price_base(source_frame):
    '''Returns Base Year'''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 0]-100) > 1/1000:
        # #    while abs(source_frame.iloc[i, 0]-source_frame.iloc[i, 1])>10:
        #    while abs(source_frame.iloc[i, 0]-source_frame.iloc[i, 1])>1:
        i -= 1
        base = i  # Basic Year
    base = source_frame.index[base]
