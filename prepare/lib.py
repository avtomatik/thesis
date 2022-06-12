#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 11:52:01 2022

@author: alexander
"""

import io
import numpy as np
import pandas as pd
import requests
from functools import partial
from pandas import DataFrame
from extract.lib import extract_usa_classic
from extract.lib import extract_usa_census
from extract.lib import extract_usa_bea
from extract.lib import extract_usa_bea_from_url
from extract.lib import extract_usa_bea_from_loaded
from toolkit.lib import price_inverse_single


def data_select(data, query):
    for column, value in query['filter'].items():
        data = data[data.iloc[:, column] == value]
    return data


def get_data_archived() -> DataFrame:
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # Fixed Assets Series: K160491, 1951--2011
        # `K160491` Replaced with `K10070` in `get_data_combined()`
        # =====================================================================
        'K160491',
    )
    _data_bea = pd.concat(
        [
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(tuple(WB_NAMES[2*(_ // 2)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(tuple(WB_NAMES[1 + 2*(_ // 2)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()
    _df = pd.concat(
        [
            # =====================================================================
            # Do Not Use As It Is CPI-U Not PPI
            # =====================================================================
            get_data_usa_bls_cpiu(),
            _data_bea,
        ],
        axis=1, sort=True).dropna(axis=0)
    # =========================================================================
    # Deflator, 2005=100
    # =========================================================================
    _df['def'] = _df.iloc[:, 0].add(1).cumprod()
    _df.iloc[:, -1] = _df.iloc[:, -
                               1].rdiv(_df.iloc[_df.index.get_loc(2005), -1])
    # =========================================================================
    # Investment, 2005=100
    # =========================================================================
    _df['inv'] = _df.iloc[:, 1].mul(_df.iloc[:, -1])
    # =========================================================================
    # Capital, 2005=100
    # =========================================================================
    _df['cap'] = _df.iloc[:, 3].mul(_df.iloc[:, -1])
    # =========================================================================
    # Capital Retirement Ratio
    # =========================================================================
    _df['ratio_mu'] = _df.iloc[:, -2].mul(1).sub(_df.iloc[:, -1].shift(-1)).div(
        _df.iloc[:, -1]).add(1)
    return (
        _df.loc[:, ['inv', 'A191RX1', 'cap', 'ratio_mu']].dropna(axis=0),
        _df.loc[:, ['ratio_mu']].dropna(axis=0),
        _df.index.get_loc(2005)
    )


def get_data_bea_def() -> DataFrame:
    '''Intent: Returns Cumulative Price Index for Some Base Year from Certain Type BEA Deflator File'''
    FILE_NAME = 'dataset_usa_bea-GDPDEF.xls'
    data_frame = pd.read_excel(
        FILE_NAME,
        names=['period', 'value'],
        index_col=0,
        skiprows=15,
        parse_dates=True
    )
    return data_frame.groupby(data_frame.index.year).prod().pow(1/4)


def get_data_bea_gdp():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10106 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
    )
    return pd.concat(
        [
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[0], WB_NAMES[0], sh, _id)
                    for sh, _id in zip(SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[1], WB_NAMES[1], sh, _id)
                    for sh, _id in zip(SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()


def get_data_brown():
    # =========================================================================
    # Fetch Data from `Reference RU Brown M. 0597_088.pdf`, Page 193
    # Dependent on `extract_usa_classic`
    # Out of Kendrick J.W. Data & Table 2. of `Reference RU Brown M. 0597_088.pdf`
    # =========================================================================
    # =========================================================================
    # FN:Murray Brown
    # ORG:University at Buffalo;Economics
    # TITLE:Professor Emeritus, Retired
    # EMAIL;PREF;INTERNET:mbrown@buffalo.edu
    # =========================================================================
    ARCHIVE_NAMES = ('dataset_usa_brown.zip', 'dataset_usa_kendrick.zip',)
    data_frame = pd.read_csv(ARCHIVE_NAMES[0], skiprows=4, usecols=range(3, 6))
    data_frame.columns = ['series_id', 'period', 'value']
    _b_frame = pd.concat(
        [
            extract_usa_classic(ARCHIVE_NAMES[0], series_id)
            for series_id in sorted(set(data_frame.iloc[:, 0]))
        ],
        axis=1,
        sort=True)
    _b_frame.columns = [
        f'series_{hex(_)}' for _, column in enumerate(_b_frame.columns)
    ]
    # =========================================================================
    # Валовой продукт (в млн. долл., 1929 г.)
    # Чистый основной капитал (в млн. долл., 1929 г.)
    # Используемый основной капитал (в млн. долл., 1929 г.)
    # Отработанные человеко-часы
    # Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
    # Вторая аппроксимация рядов загрузки мощностей, полученная с помощью итеративного процесса
    # =========================================================================
    # =========================================================================
    # Gross Domestic Product, USD 1,000,000, 1929=100
    # Net Fixed Assets, USD 1,000,000, 1929=100
    # Utilized Fixed Assets, USD 1,000,000, 1929=100
    # Actual Man-Hours Worked
    # _
    # _
    # =========================================================================
    SERIES_IDS = ('KTA03S07', 'KTA03S08', 'KTA10S08', 'KTA15S07', 'KTA15S08',)
    _k_frame = pd.concat(
        [
            extract_usa_classic(ARCHIVE_NAMES[1], series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    result_frame = pd.concat(
        [
            _k_frame[_k_frame.index.get_loc(
                1889):2+_k_frame.index.get_loc(1952)],
            # =================================================================
            # Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
            # =================================================================
            _b_frame.iloc[:1+_b_frame.index.get_loc(1953), [4]]
        ],
        axis=1,
        sort=True)
    result_frame = result_frame.assign(
        series_0x0=result_frame.iloc[:, 0].sub(result_frame.iloc[:, 1]),
        series_0x1=result_frame.iloc[:, 3].add(result_frame.iloc[:, 4]),
        series_0x2=result_frame.iloc[:, [3, 4]].sum(axis=1).rolling(
            window=2).mean().mul(result_frame.iloc[:, 5]).div(100),
        series_0x3=result_frame.iloc[:, 2],
    )
    result_frame = result_frame.iloc[:, [6, 7, 8, 9]].dropna(axis=0)
    return pd.concat(
        [
            result_frame,
            # =================================================================
            # Brown M. Numbers Not Found in Kendrick J.W. For Years Starting From 1954 Inclusive
            # =================================================================
            _b_frame.iloc[1+_b_frame.index.get_loc(1953):, [0, 1, 2, 3]]
        ]
    ).round()


def get_data_can():
    # =========================================================================
    # '''A. Fixed Assets Block: `Industrial buildings`, `Industrial machinery`\
    # for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, \
    # `New Brunswick`, `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, \
    # `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    # '''2007 constant prices'''
    # '''Geometric (infinite) end-year net stock'''
    # '''Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, \
    # `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    # `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    # '''Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, \
    # `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    # `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    # '''Table: 36-10-0238-01 (formerly CANSIM 031-0004): Flows and stocks of\
    # fixed non-residential capital, total all industries, by asset, provinces\
    # and territories, annual (dollars x 1,000,000)'''
    # =========================================================================
    URL = 'https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip'
    capital = extract_can_from_url(URL)
    capital = extract_can_capital(extract_can_capital_query())
    # =========================================================================
    # '''B. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly'''
    # '''`v2523012` - Table: 14-10-0027-01 (formerly CANSIM 282-0012): Employment\
    # by class of worker, annual (x 1,000)'''
    # =========================================================================
    URL = 'https://www150.statcan.gc.ca/n1/tbl/csv/14100027-eng.zip'
    labor = extract_can_from_url(URL)
    labor = extract_can(labor, 'v2523012')
    # =========================================================================
    # '''C. Production Block: `v65201809`'''
    # '''`v65201809` - Table: 36-10-0434-01 (formerly CANSIM 379-0031): Gross\
    # domestic product (GDP) at basic prices, by industry, monthly (x 1,000,000)'''
    # =========================================================================
    URL = 'https://www150.statcan.gc.ca/n1/tbl/csv/36100434-eng.zip'
    product = extract_can_from_url(URL)
    product = extract_can_quarter(product, 'v65201809')
    result_frame = pd.concat([capital, labor, product], axis=1, sort=True)
    # result_frame = result_frame.dropna(axis=0)
    result_frame.columns = ['capital', 'labor', 'product']
    # result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def get_data_can():
    data_frame = pd.concat(
        [
            # =============================================================================
            # A. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
            #     `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`
            # 2007 constant prices
            # Geometric (infinite) end-year net stock
            # Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
            #     `v43976019`, `v43976435`, `v43976851`, `v43977267`
            # Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
            #     `v43976010`,  `v43976426`, `v43976842`, `v43977258`
            # =============================================================================
            extract_can_fixed_assets(extract_can_capital_query_archived()),
            # =============================================================================
            # B. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly
            # `v2523012` - 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
            # and sex; Canada; Total employed, all class of workers; Manufacturing; Both sexes (x 1,000) (annual, 1987 to 2017)
            # =============================================================================
            extract_can_annual(2820012, 'v2523012'),
            # =============================================================================
            # C. Production Block: `v65201809`
            # `v65201809` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Trading-day\
            # adjusted; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)
            # =============================================================================
            extract_can_quarter(3790031, 'v65201809'),
        ], axis=1, sort=True
    ).dropna(axis=0)
    data_frame.columns = ['capital', 'labor', 'product']
    return data_frame


def get_data_can():
    '''Number 1. CANSIM Table 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification\
    System (NAICS) and sex'''
    '''Number 2. CANSIM Table 03790031'''
    '''Title: Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS)'''
    '''Measure: monthly (dollars x 1,000,000)'''
    '''Number 3. CANSIM Table 03800068'''
    '''Title: Gross fixed capital formation'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 4. CANSIM Table 031-0004: Flows and stocks of fixed non-residential capital, total all industries, by asset, provinces and territories, \
    annual (dollars x 1,000,000)'''
    '''Number 5. CANSIM Table 03790028'''
    '''Title: Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS), provinces and territories'''
    '''Measure: annual (percentage share)'''
    '''Number 6. CANSIM Table 03800001'''
    '''Title: Gross domestic product (GDP), income-based, *Terminated*'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 7. CANSIM Table 03800002'''
    '''Title: Gross domestic product (GDP), expenditure-based, *Terminated*'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 8. CANSIM Table 03800063'''
    '''Title: Gross domestic product, income-based'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 9. CANSIM Table 03800064'''
    '''Title: Gross domestic product, expenditure-based'''
    '''Measure: quarterly (dollars x 1,000,000)'''
    '''Number 10. CANSIM Table 03800069'''
    '''Title: Investment in inventories'''
    '''Measure: quarterly (dollars unless otherwise noted)'''
    '''---'''
    '''1.0. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly'''
    '''`v2523012` - 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
    and sex; Canada; Total employed, all class of workers; Manufacturing; Both sexes (x 1,000) (annual, 1987 to 2017)'''
    labor = extract_can_annual(2820012, 'v2523012')
    '''1.1. Labor Block, Alternative Option Not Used'''
    '''`v3437501` - 282-0011 Labour Force Survey estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
    and sex, unadjusted for seasonality; Canada; Total employed, all classes of workers; Manufacturing; Both sexes (x 1,000) (monthly, 1987-01-01 to\
    2017-12-01)'''
    # =============================================================================
    # extract_can_quarter(2820011, 'v3437501')
    # =============================================================================
    '''2.i. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
    `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    '''2.0. 2007 constant prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    '''Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    SERIES_IDS = ('v43975603', 'v43977683', 'v43978099', 'v43978515',
                  'v43978931', 'v43979347', 'v43979763', 'v43980179',
                  'v43980595', 'v43976019', 'v43976435', 'v43976851',
                  'v43977267', 'v43975594', 'v43977674', 'v43978090',
                  'v43978506', 'v43978922', 'v43979338', 'v43979754',
                  'v43980170', 'v43980586', 'v43976010', 'v43976426',
                  'v43976842', 'v43977258',)
    '''2.1. Fixed Assets Block, Alternative Option Not Used'''
    '''2.1.1. Chained (2007) dollars'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43980803`, `v43981843`, `v43982051`, `v43982259`, `v43982467`, `v43982675`, `v43982883`, `v43983091`, `v43983299`, \
    `v43981011`, `v43981219`, `v43981427`, `v43981635`'''
    '''Industrial machinery (x 1,000,000): `v43980794`, `v43981834`, `v43982042`, `v43982250`, `v43982458`, `v43982666`, `v43982874`, `v43983082`, `v43983290`, \
    `v43981002`, `v43981210`, `v43981418`, `v43981626`'''
    # SERIES_IDS = ('v43980803', 'v43981843', 'v43982051', 'v43982259',
    #               'v43982467', 'v43982675', 'v43982883', 'v43983091',
    #               'v43983299', 'v43981011', 'v43981219', 'v43981427',
    #               'v43981635', 'v43980794', 'v43981834', 'v43982042',
    #               'v43982250', 'v43982458', 'v43982666', 'v43982874',
    #               'v43983082', 'v43983290', 'v43981002', 'v43981210',
    #               'v43981418', 'v43981626',)
    '''2.1.2. Current prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43975395`, `v43977475`, `v43977891`, `v43978307`, `v43978723`, `v43979139`, `v43979555`, `v43979971`, `v43980387`, \
    `v43975811`, `v43976227`, `v43976643`, `v43977059`'''
    '''Industrial machinery (x 1,000,000): `v43975386`, `v43977466`, `v43977882`, `v43978298`, `v43978714`, `v43979130`, `v43979546`, `v43979962`, `v43980378`, \
    `v43975802`, `v43976218`, `v43976634`, `v43977050`'''
    # SERIES_IDS = ('v43975395', 'v43977475', 'v43977891', 'v43978307',
    #               'v43978723', 'v43979139', 'v43979555', 'v43979971',
    #               'v43980387', 'v43975811', 'v43976227', 'v43976643',
    #               'v43977059', 'v43975386', 'v43977466', 'v43977882',
    #               'v43978298', 'v43978714', 'v43979130', 'v43979546',
    #               'v43979962', 'v43980378', 'v43975802', 'v43976218',
    #               'v43976634', 'v43977050',)
    capital = extract_can_fixed_assets(extract_can_capital_query_archived())
    '''3.i. Production Block: `v65201809`, Preferred Over `v65201536` Which Is Quarterly'''
    '''3.0. Production Block: `v65201809`'''
    '''`v65201809` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Trading-day\
    adjusted; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)'''
    product = extract_can_quarter(3790031, 'v65201809')
    '''3.1. Production Block: `v65201536`, Alternative Option Not Used'''
    '''`v65201536` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Seasonnaly\
    adjusted at annual rates; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)'''
    # =============================================================================
    # extract_can_quarter(3790031, 'v65201536')
    # =============================================================================
    data_frame = pd.concat(
        [
            capital,
            labor,
            product
        ], axis=1, sort=True).dropna(axis=0)
    data_frame.columns = ['capital', 'labor', 'product']
    return data_frame


def get_data_can_price_a():
    FILE_NAME = '/home/alexander/projects/stat_can_cap.xlsx'
    data = pd.read_excel(FILE_NAME)
    data.set_index(data.columns[0], inplace=True)
    groups = [[[i, 5 + i] for i in range(5)],
              # [[i, 10 + i] for i in range(5)],
              [[i, 5 + i] for i in range(35, 39)],
              # [[i, 10 + i] for i in range(35, 40)],
              ]
    combined = DataFrame()
    for pairs in groups:
        for pair in pairs:
            chunk = data.iloc[:, pair].dropna(axis=0)
            chunk['def'] = chunk.iloc[:, 0].div(chunk.iloc[:, 1])
            chunk['prc'] = chunk.iloc[:, 2].div(
                chunk.iloc[:, 2].shift(1)).sub(1)
            chunk.dropna(axis=0, inplace=True)
            combined = pd.concat([combined, chunk.iloc[:, [3]]],
                                 axis=1,
                                 sort=False)
            combined.plot(grid=True)
    # return combined


def get_data_can_price_b():
    FILE_NAME = '/home/alexander/projects/stat_can_cap.xlsx'
    data = pd.read_excel(FILE_NAME)
    data.set_index(data.columns[0], inplace=True)
    combined = DataFrame()
    for i in [i for i in range(21, 24)]:
        chunk = data.iloc[:, [i]].dropna(axis=0)
        chunk[f'{data.columns[i]}_prc'] = chunk.iloc[:, 0].div(
            chunk.iloc[:, 0].shift(1)).sub(1)
        chunk.dropna(axis=0, inplace=True)
        combined = pd.concat([combined, chunk.iloc[:, [1]]],
                             axis=1,
                             sort=False)
    return combined


def get_data_capital_combined_archived():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis;
        # https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
        # http://www.bea.gov/data/economic-accounts/national
        # https://fred.stlouisfed.org/series/K160491A027NBEA
        # https://search.bea.gov/search?affiliate=u.s.bureauofeconomicanalysis&query=k160491
        # =====================================================================
        # =====================================================================
        # Fixed Assets Series: K160021, 1951--2011
        # =====================================================================
        'K160021',
        # =====================================================================
        # Fixed Assets Series: K160491, 1951--2011
        # =====================================================================
        'K160491',
    )
    _data = pd.concat(
        [
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[2*(_ // len(SH_NAMES))]
                              for _ in range(len(SERIES_IDS))),
                        tuple(SH_NAMES[2*(_ // len(SH_NAMES)) + ((_ - 1) % len(SH_NAMES)) *
                                       (2 - ((_ - 1) % len(SH_NAMES)))] for _ in range(len(SERIES_IDS))),
                        SERIES_IDS,
                    )
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id)
                    for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[1 + 2*(_ // len(SH_NAMES))]
                              for _ in range(len(SERIES_IDS))),
                        tuple(SH_NAMES[2*(_ // len(SH_NAMES)) + ((_ - 1) % len(SH_NAMES)) *
                                       (2 - ((_ - 1) % len(SH_NAMES)))] for _ in range(len(SERIES_IDS))),
                        SERIES_IDS,
                    )
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True).drop_duplicates()
    return pd.concat(
        [
            _data,
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            get_data_usa_frb_cu(),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2011
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Labor Series: A4601C0, 1929--2011
            # =================================================================
            get_data_usa_bea_labor()
        ],
        axis=1, sort=True)


def get_data_capital_purchases():
    ARCHIVE_NAMES = (
        # =====================================================================
        # CDT2S1: Nominal; CDT2S3: 1880=100;
        # =====================================================================
        'dataset_usa_cobb-douglas.zip',
        # =====================================================================
        # DT63AS01: 1880=100; DT63AS02: Do Not Use; DT63AS03: Do Not Use;
        # =====================================================================
        'dataset_douglas.zip',)
    SERIES_IDS = ('CDT2S1', 'CDT2S3', 'DT63AS01', 'DT63AS02', 'DT63AS03',)
    _args = [tuple(((ARCHIVE_NAMES[0], ARCHIVE_NAMES[1])[series_id.startswith(
        'DT')], series_id,)) for series_id in SERIES_IDS]
    _data_frame = pd.concat(
        [extract_usa_classic(*arg) for arg in _args],
        axis=1,
        sort=True)

    ARCHIVE_NAMES = (
        # =====================================================================
        # Nominal Series, USD Millions
        # =====================================================================
        'dataset_usa_census1949.zip',
        # =====================================================================
        # P0107, P0108, P0109, P0113, P0114, P0115 -- Nominal Series, USD Billions
        # P0110, P0111, P0112, P0116, P0117, P0118, P0119, P0120, P0121, P0122 -- Real Series, 1958=100, USD Billions
        # =====================================================================
        'dataset_usa_census1975.zip',)
    SERIES_IDS = (
        'J0149', 'J0150', 'J0151', 'P0107', 'P0108', 'P0109', 'P0110',
        'P0111', 'P0112', 'P0113', 'P0114', 'P0115', 'P0116', 'P0117',
        'P0118', 'P0119', 'P0120', 'P0121', 'P0122',
    )
    _args = [(tuple((ARCHIVE_NAMES[0], series_id, 1,)), tuple((ARCHIVE_NAMES[1], series_id, 1000,)))[
        series_id.startswith('P')] for series_id in SERIES_IDS]
    data_frame_ = pd.concat(
        [extract_usa_census(*_[:2]).mul(_[-1]) for _ in _args],
        axis=1,
        sort=True)
    data_frame = pd.concat([_data_frame, data_frame_], axis=1, sort=True)
    data_frame = data_frame[data_frame.index.get_loc(1875):]
    data_frame['total'] = data_frame.loc[:, [
        'CDT2S1', 'J0149', 'P0107']].mean(axis=1)
    data_frame['struc'] = data_frame.loc[:, ['J0150', 'P0108']].mean(axis=1)
    data_frame['equip'] = data_frame.loc[:, ['J0151', 'P0109']].mean(axis=1)
    data_frame.iloc[:, -3] = signal.wiener(data_frame.iloc[:, -3]).round()
    data_frame.iloc[:, -2] = signal.wiener(data_frame.iloc[:, -2]).round()
    data_frame.iloc[:, -1] = signal.wiener(data_frame.iloc[:, -1]).round()
    return data_frame


def get_data_census_a():
    '''Census Manufacturing Indexes, 1899=100'''
    ARCHIVE_NAMES = ('dataset_usa_census1949.zip',
                     'dataset_usa_census1975.zip',)
    SERIES_IDS = (
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014',
        # =====================================================================
        # HSUS 1975 Page 667, P17: Edwin Frickey Series, Indexes of Manufacturing Production
        # =====================================================================
        'P0017',)
    _args = [tuple((ARCHIVE_NAMES[1], series_id,)) if series_id.startswith(
        'P') else tuple((ARCHIVE_NAMES[0], series_id,)) for series_id in SERIES_IDS]
    data_frame = pd.concat([extract_usa_census(*_)
                           for _ in _args], axis=1, sort=True)
    data_frame = data_frame.div(
        data_frame.iloc[data_frame.index.get_loc(1899), :]).mul(100)
    return data_frame, data_frame.index.get_loc(1899)


def get_data_census_b_a():
    '''Returns Nominal Million-Dollar Capital, Including Structures & Equipment, Series'''
    ARCHIVE_NAMES = (
        # =====================================================================
        # Nominal Series, USD Millions
        # =====================================================================
        'dataset_usa_census1949.zip',
        # =====================================================================
        # P0107, P0108, P0109, P0113, P0114, P0115 -- Nominal Series, USD Billions
        # P0110, P0111, P0112, P0116, P0117, P0118, P0119, P0120, P0121, P0122 -- Real Series, 1958=100, USD Billions
        # =====================================================================
        'dataset_usa_census1975.zip',)
    SERIES_IDS = (
        'J0149', 'J0150', 'J0151', 'P0107', 'P0108', 'P0109', 'P0110',
        'P0111', 'P0112', 'P0113', 'P0114', 'P0115', 'P0116', 'P0117',
        'P0118', 'P0119', 'P0120', 'P0121', 'P0122',
    )
    _args = [(tuple((ARCHIVE_NAMES[0], series_id, 1,)), tuple((ARCHIVE_NAMES[1], series_id, 1000,)))[
        series_id.startswith('P')] for series_id in SERIES_IDS]
    data_frame = pd.concat(
        [extract_usa_census(*_[:2]).mul(_[-1]) for _ in _args],
        axis=1,
        sort=True)
    data_frame = data_frame[data_frame.index.get_loc(1875):]
    data_frame['total'] = data_frame.loc[:, ['J0149', 'P0107']].mean(axis=1)
    data_frame['struc'] = data_frame.loc[:, ['J0150', 'P0108']].mean(axis=1)
    data_frame['equip'] = data_frame.loc[:, ['J0151', 'P0109']].mean(axis=1)
    # data_frame.iloc[:, -3] = signal.wiener(data_frame.iloc[:, -3]).round()
    # data_frame.iloc[:, -2] = signal.wiener(data_frame.iloc[:, -2]).round()
    # data_frame.iloc[:, -1] = signal.wiener(data_frame.iloc[:, -1]).round()
    return data_frame.iloc[:, -3:]


def get_data_census_b_b():
    '''Returns Census Fused Capital Deflator'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'P0107',  # Nominal
        'P0108',  # Nominal
        'P0109',  # Nominal
        'P0110',  # 1958=100
        'P0111',  # 1958=100
        'P0112',  # 1958=100
        'P0113',  # Nominal
        'P0114',  # Nominal
        'P0115',  # Nominal
        'P0116',  # 1958=100
        'P0117',  # 1958=100
        'P0118',  # 1958=100
    )
    _data_frame = pd.concat(
        [extract_usa_census(ARCHIVE_NAME, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)
    _data_frame = _data_frame[_data_frame.index.get_loc(1879):]
    _data_frame['purchases_total'] = _data_frame.iloc[:, 0].div(
        _data_frame.iloc[:, 3])
    _data_frame['purchases_struc'] = _data_frame.iloc[:, 1].div(
        _data_frame.iloc[:, 4])
    _data_frame['purchases_equip'] = _data_frame.iloc[:, 2].div(
        _data_frame.iloc[:, 5])
    _data_frame['depreciat_total'] = _data_frame.iloc[:, 6].div(
        _data_frame.iloc[:, 9])
    _data_frame['depreciat_struc'] = _data_frame.iloc[:, 7].div(
        _data_frame.iloc[:, 10])
    _data_frame['depreciat_equip'] = _data_frame.iloc[:, 8].div(
        _data_frame.iloc[:, 11])
    data_frame = pd.concat(
        [
            price_inverse_single(
                _data_frame.iloc[:, [-(1+i)]].dropna()).dropna() for i in range(6)
        ],
        axis=1,
        sort=True)
    data_frame['census_fused'] = data_frame.mean(axis=1)
    return data_frame.iloc[:, [-1]]


def get_data_census_c() -> tuple[DataFrame, tuple[int]]:
    '''Census Primary Metals & Railroad-Related Products Manufacturing Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'P0262', 'P0265', 'P0266', 'P0267', 'P0268', 'P0269', 'P0293', 'P0294', 'P0295',
    )
    # =========================================================================
    # <base_year>=100
    # =========================================================================
    # =========================================================================
    # TODO: Extract Base Years
    # =========================================================================
    BASE_YEARS = (1875, 1875, 1875, 1875, 1875, 1909, 1880, 1875, 1875,)
    data_frame = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    for _ in range(data_frame.shape[1]):
        base_year = data_frame.index.get_loc(BASE_YEARS[_])
        data_frame.iloc[:, _] = data_frame.iloc[:, _].div(
            data_frame.iloc[base_year, _]).mul(100)
    return data_frame, BASE_YEARS


def get_data_census_e() -> DataFrame:
    '''Census Total Immigration Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'C0091', 'C0092', 'C0093', 'C0094', 'C0095', 'C0096', 'C0097', 'C0098',
        'C0099', 'C0100', 'C0101', 'C0103', 'C0104', 'C0105', 'C0106', 'C0107',
        'C0108', 'C0109', 'C0111', 'C0112', 'C0113', 'C0114', 'C0115', 'C0117',
        'C0118', 'C0119',
    )
    data_frame = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)

    data_frame['C89'] = data_frame.sum(1)
    return data_frame.iloc[:, [-1]]


def get_data_census_f() -> DataFrame:
    '''Census Employment Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('D0085', 'D0086', 'D0796', 'D0797', 'D0977', 'D0982',)
    df = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    df['workers'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    df.iloc[:, 4].fillna(
        df.iloc[:df.index.get_loc(1906), 4].mean(), inplace=True)
    df.iloc[:, 5].fillna(
        df.iloc[:df.index.get_loc(1906), 5].mean(), inplace=True)
    return df


def get_data_census_g() -> DataFrame:
    '''Census Gross National Product Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('F0003', 'F0004',)
    data_frame = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    data_frame = data_frame[data_frame.index.get_loc(1889):]
    return data_frame.div(data_frame.iloc[0, :]).mul(100)


def get_data_census_i_a() -> DataFrame:
    '''Census Foreign Trade Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('U0001', 'U0008', 'U0015',)
    return pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)


def get_data_census_i_b() -> DataFrame:
    '''Census Foreign Trade Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('U0187', 'U0188', 'U0189',)
    return pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)


def get_data_census_i_c() -> DataFrame:
    '''Census Foreign Trade Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'U0319', 'U0320', 'U0321', 'U0322', 'U0323', 'U0325', 'U0326', 'U0327',
        'U0328', 'U0330', 'U0331', 'U0332', 'U0333', 'U0334', 'U0337', 'U0338',
        'U0339', 'U0340', 'U0341', 'U0343', 'U0344', 'U0345', 'U0346', 'U0348',
        'U0349', 'U0350', 'U0351', 'U0352',
    )
    df = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)

    for _ in range(len(SERIES_IDS) // 2):
        _title = f'{df.columns[_]}_net_{df.columns[_ + len(SERIES_IDS) // 2]}'
        df[_title] = df.iloc[:, _].sub(df.iloc[:, _ + len(SERIES_IDS) // 2])

    df['exports'] = df.loc[:, SERIES_IDS[:len(SERIES_IDS) // 2]].sum(1)
    df['imports'] = df.loc[:, SERIES_IDS[len(SERIES_IDS) // 2:]].sum(1)

    for _ in range(len(SERIES_IDS) // 2):
        _title = f'{df.columns[_ + len(SERIES_IDS)]}_over_all'
        df[_title] = df.iloc[:, _ +
                             len(SERIES_IDS)].div(df.loc[:, 'exports'].sub(df.loc[:, 'imports']))

    return df


def get_data_census_j() -> DataFrame:
    '''Census Money Supply Aggregates'''
    YEAR_BASE = 1915
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('X0410', 'X0414', 'X0415',)
    df = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    return df.div(df.iloc[df.index.get_loc(YEAR_BASE), :]).mul(100)


def get_data_census_price() -> DataFrame:
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('P0107', 'P0110')
    df = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, series_id) for series_id in SERIES_IDS
        ],
        axis=1)
    df['def'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['prc'] = df.iloc[:, -1].div(df.iloc[:, -1].shift(1)).sub(1)
    return df.iloc[:, [-1]].dropna(axis=0)


def get_data_centered_by_period(data_frame: DataFrame) -> DataFrame:
    '''
    data_frame.index: Period,
    data_frame.iloc[:, 0]: Series
    '''
    # =========================================================================
    # TODO: Any Use?
    # =========================================================================
    # =========================================================================
    # DataFrame for Results
    # =========================================================================
    _data = data_frame.reset_index(level=0).copy()
    period = _data.iloc[:, 0]
    series = _data.iloc[:, 1]
    # =========================================================================
    # Loop
    # =========================================================================
    for _ in range(_data.shape[0] // 2):
        period = period.rolling(2).mean()
        series = series.rolling(2).mean()
        period_roll = period.shift(-((1 + _) // 2))
        series_roll = series.shift(-((1 + _) // 2))
        _data = pd.concat(
            [
                _data,
                period_roll,
                series_roll,
                series_roll.div(_data.iloc[:, 1]),
                series_roll.shift(-2).sub(series_roll).div(
                    series_roll.shift(-1)).div(2),
            ],
            axis=1,
            sort=True
        )
    return _data


def get_data_cobb_douglas_deflator():
    '''Fixed Assets Deflator, 2009=100'''
    # =========================================================================
    # TODO: Change Name; Be Careful with Usage Due to Change in Behavior
    # =========================================================================
    # =========================================================================
    # Combine L2, L15, E7, E23, E40, E68 & P107/P110
    # =========================================================================
    # =========================================================================
    # Bureau of Labor Statistics: Data Not Used As It Covers Only Years of 1998--2017
    # =========================================================================
    # =========================================================================
    # Results:
    # HSUS 1949 - 'L0036' Offset with HSUS 1975 - 'E0183'
    # HSUS 1949 - 'L0038' Offset with HSUS 1975 - 'E0184'
    # HSUS 1949 - 'L0039' Offset with HSUS 1975 - 'E0185'
    # HSUS 1975 - 'E0052' Offset With HSUS 1949 - 'L0002
    # =========================================================================
    # =========================================================================
    # Cost-Of-Living Indexes
    # =========================================================================
    # =========================================================================
    # E0183: Federal Reserve Bank, 1913=100
    # E0184: Burgess, 1913=100
    # E0185: Douglas, 1890-99=100
    # =========================================================================
    # =========================================================================
    # Bureau of the Census
    # =========================================================================
    # =========================================================================
    # Correlation Test:
    # `data_frame.corr(method='kendall')`
    # `data_frame.corr(method='pearson')`
    # `data_frame.corr(method='spearman')`
    # Correlation Test Result: kendall & pearson & spearman: L2, L15, E7, E23, E40, E68
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
    )
    CS_SERIES_IDS = (
        'L0002',
        'L0015',
        'E0007',
        'E0023',
        'E0040',
        'E0068',
        'P0107',
        'P0110',
    )
    # =========================================================================
    # Bureau of Economic Analysis
    # =========================================================================
    URL = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    BE_SERIES_IDS = (
        # =====================================================================
        # Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k1n31gd1es00',
        # =====================================================================
        # Fixed Assets: kcn31gd1es00, 1925--2019, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'kcn31gd1es00',
        # =====================================================================
        # Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # Not Used: Fixed Assets: k3ntotl1si00, 1925--2019, Table 2.3. Historical-Cost Net Stock of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
        # Not Used: mcn31gd1es00, 1925--2019, Table 4.5. Chain-Type Quantity Indexes for Depreciation of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # Not Used: mcntotl1si00, 1925--2019, Table 2.5. Chain-Type Quantity Indexes for Depreciation of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
        # =====================================================================
        'k3n31gd1es00',
        'k3ntotl1si00',
        'mcn31gd1es00',
        'mcntotl1si00',
    )
    data_frame = pd.concat(
        [
            pd.concat(
                [
                    extract_usa_census(**{
                        'archive_name': archive_name,
                        'series_id': series_id,
                    })
                    for archive_name, series_id in zip(ARCHIVE_NAMES[:-2], CS_SERIES_IDS[:-2])
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    extract_usa_census(**{
                        'archive_name': archive_name,
                        'series_id': series_id,
                    })
                    for archive_name, series_id in zip(ARCHIVE_NAMES[-2:], CS_SERIES_IDS[-2:])
                ],
                axis=1,
                sort=True
            ).truncate(before=1885),
        ],
        axis=1,
        sort=True
    )
    # =========================================================================
    # Bureau of Economic Analysis
    # =========================================================================
    web_data = extract_usa_bea_from_url(URL)
    data_frame = pd.concat(
        [
            # =================================================================
            # Bureau of the Census
            # =================================================================
            data_frame,
            # =================================================================
            # Bureau of Economic Analysis
            # =================================================================
            pd.concat(
                [
                    extract_usa_bea_from_loaded(**{
                        'data_frame': web_data,
                        'series_id': series_id,
                    }
                    )
                    for series_id in BE_SERIES_IDS[:2]
                ],
                axis=1,
                sort=True
            ),
            # =================================================================
            # Federal Reserve Board Data
            # =================================================================
            get_data_usa_frb_fa_def(),
        ],
        axis=1,
        sort=True
    ).truncate(before=1794)
    data_frame['fa_def_cs'] = data_frame.loc[:, CS_SERIES_IDS[-2]].div(
        data_frame.loc[:, CS_SERIES_IDS[-1]])
    data_frame['ppi_bea'] = data_frame.loc[:, BE_SERIES_IDS[0]].div(
        data_frame.loc[:, BE_SERIES_IDS[1]]).div(data_frame.loc[2012, BE_SERIES_IDS[0]]).mul(100)
    data_frame.drop(
        [*CS_SERIES_IDS[-2:], *BE_SERIES_IDS[:2]],
        axis=1,
        inplace=True
    )
    # =========================================================================
    # Strip Deflators
    # =========================================================================
    for _ in range(data_frame.shape[1]):
        data_frame.iloc[:, _] = strip_cumulated_deflator(
            data_frame.iloc[:, [_]]
        )
    data_frame['def_mean'] = data_frame.mean(axis=1)
    return data_frame.iloc[:, [-1]].dropna()


def get_data_cobb_douglas_extension_capital() -> DataFrame:
    # =========================================================================
    # Existing Capital Dataset
    # =========================================================================
    df = get_data_usa_capital()
    # =========================================================================
    # Convert Capital Series into Current (Historical) Prices
    # =========================================================================
    df['nominal_cbb_dg'] = df.iloc[:, 0].mul(
        df.iloc[:, 2]).div(df.iloc[:, 1]).div(1000)
    df['nominal_census'] = df.iloc[:, 5].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    df['nominal_dougls'] = df.iloc[:, 0].mul(
        df.iloc[:, 9]).div(df.iloc[:, 1]).div(1000)
    df['nominal_kndrck'] = df.iloc[:, 5].mul(
        df.iloc[:, 8]).div(df.iloc[:, 6]).div(1000)
    df.iloc[:, -1] = df.iloc[:, -1].mul(
        df.loc[1929, df.columns[6]]).div(df.loc[1929, df.columns[5]])
    # =========================================================================
    # Douglas P.H. -- Kendrick J.W. (Blended) Series
    # =========================================================================
    df['nominal_doug_kndrck'] = df.iloc[:, -2:].mean(axis=1)
    # =========================================================================
    # Cobb C.W., Douglas P.H. -- FRB (Blended) Series
    # =========================================================================
    df['nominal_cbb_dg_frb'] = df.iloc[:, [10, 12]].mean(axis=1)
    # =========================================================================
    # Capital Structure Series: `Cobb C.W., Douglas P.H. -- FRB (Blended) Series` to `Douglas P.H. -- Kendrick J.W. (Blended) Series`
    # =========================================================================
    df['struct_ratio'] = df.iloc[:, -1].div(df.iloc[:, -2])
    # =========================================================================
    # Filling the Gaps within Capital Structure Series
    # =========================================================================
    df.loc[1899:, df.columns[-1]].fillna(0.275, inplace=True)
    df.loc[:, df.columns[-1]
           ].fillna(df.loc[1899, df.columns[-1]], inplace=True)
    # =========================================================================
    # Patch Series `Douglas P.H. -- Kendrick J.W. (Blended) Series` Multiplied by `Capital Structure Series`
    # =========================================================================
    df['nominal_patch'] = df.iloc[:, -3].mul(df.iloc[:, -1])
    # =========================================================================
    # `Cobb C.W., Douglas P.H. -- FRB (Blended) Series` Patched with `Patch Series`
    # =========================================================================
    df['nominal_extended'] = df.iloc[:, -3::2].mean(axis=1)
    return df.iloc[:, [-1]].dropna(axis=0)


def get_data_cobb_douglas_extension_labor():
    '''Manufacturing Laborers` Series Comparison'''
    # =========================================================================
    # TODO: Bureau of Labor Statistics
    # TODO: Federal Reserve Board
    # =========================================================================
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'
    ARCHIVE_NAMES = (
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_kendrick.zip',
    )
    SERIES_IDS = (
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1',
        # =====================================================================
        # Census Bureau 1949, D69
        # =====================================================================
        'D0069',
        # =====================================================================
        # Census Bureau 1949, J4
        # =====================================================================
        'J0004',
        # =====================================================================
        # Census Bureau 1975, D130
        # =====================================================================
        'D0130',
        # =====================================================================
        # Census Bureau 1975, P5
        # =====================================================================
        'P0005',
        # =====================================================================
        # Census Bureau 1975, P62
        # =====================================================================
        'P0062',
        # =====================================================================
        # J.W. Kendrick, Productivity Trends in the United States, Table D-II, `Persons Engaged` Column, pp. 465--466
        # =====================================================================
        'KTD02S02',
    )
    FUNCTIONS = (
        extract_usa_classic,
        extract_usa_census,
        extract_usa_census,
        extract_usa_census,
        extract_usa_census,
        extract_usa_census,
        extract_usa_classic,
    )
    data_frame = pd.concat(
        [
            partial(func, **{'archive_name': archive_name,
                             'series_id': series_id})()
            for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS, FUNCTIONS)
        ],
        axis=1,
        sort=True
    )
    # =========================================================================
    # Bureau of Economic Analysis, H4313C & J4313C & A4313C & N4313C
    # =========================================================================
    _data_frame = extract_usa_bea_from_url(URL)
    SERIES_IDS = (
        'H4313C',
        'J4313C',
        'A4313C',
        'N4313C',
    )
    data_nipa = pd.concat(
        [
            extract_usa_bea_from_loaded(_data_frame, series_id) for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    data_nipa['bea_mfg_labor'] = data_nipa.mean(axis=1)
    data_nipa = data_nipa.iloc[:, [-1]]
    data_frame = pd.concat(
        [
            data_frame,
            data_nipa,
            # =================================================================
            # Yu.V. Kurenkov
            # =================================================================
            pd.read_csv(FILE_NAME, index_col=0, usecols=[0, 2]),
        ],
        axis=1, sort=True
    )
    data_frame.drop(data_frame[data_frame.index < 1889].index, inplace=True)
    data_frame.iloc[:, 6] = data_frame.iloc[:, 6].mul(data_frame.iloc[data_frame.index.get_loc(
        1899), 0]).div(data_frame.iloc[data_frame.index.get_loc(1899), 6])
    data_frame['labor'] = data_frame.iloc[:, [0, 1, 3, 6, 7, 8]].mean(axis=1)
    return data_frame.iloc[:, [-1]]


def get_data_cobb_douglas_extension_product():
    ARCHIVE_NAMES = (
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1975.zip',
        'dataset_douglas.zip',
    )
    SERIES_IDS = (
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014',
        # =====================================================================
        # Bureau of the Census, 1975, Page 667, P17: Edwin Frickey Index of Manufacturing Production
        # =====================================================================
        'P0017',
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01',
    )
    FUNCTIONS = (
        extract_usa_census,
        extract_usa_census,
        extract_usa_census,
        extract_usa_classic,
    )
    data_frame = pd.concat(
        [
            partial(func, **{'archive_name': archive_name,
                             'series_id': series_id})()
            for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS, FUNCTIONS)
        ],
        axis=1,
        sort=True
    )
    FILE_NAME = 'dataset_usa_davis-j-h-ip-total.xls'
    data_frame = pd.concat(
        [
            data_frame,
            # =================================================================
            # Joseph H. Davis Production Index
            # =================================================================
            pd.read_excel(FILE_NAME, header=None, names=[
                'period', 'davis_index'], index_col=0, skiprows=5),
            # =================================================================
            # Federal Reserve, AIPMASAIX
            # =================================================================
            get_data_usa_frb_ip(),
        ],
        axis=1,
        sort=True
    )
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].div(
        data_frame.iloc[data_frame.index.get_loc(1899), 1]).mul(100)
    data_frame.iloc[:, 4] = data_frame.iloc[:, 4].div(
        data_frame.iloc[data_frame.index.get_loc(1899), 4]).mul(100)
    data_frame.iloc[:, 5] = data_frame.iloc[:, 5].div(
        data_frame.iloc[data_frame.index.get_loc(1939), 5]).mul(100)
    data_frame['fused_classic'] = data_frame.iloc[:, range(5)].mean(axis=1)
    data_frame.iloc[:, -1] = data_frame.iloc[:, -1].div(
        data_frame.iloc[data_frame.index.get_loc(1939), -1]).mul(100)
    data_frame['fused'] = data_frame.iloc[:, -2:].mean(axis=1)
    return data_frame.iloc[:, [-1]]


def get_data_cobb_douglas_price() -> DataFrame:
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    SERIES_IDS = ('CDT2S1', 'CDT2S3')
    df = pd.concat(
        [
            extract_usa_classic(ARCHIVE_NAME, series_id) for series_id in SERIES_IDS
        ],
        axis=1)
    df['def'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['prc'] = df.iloc[:, -1].div(df.iloc[:, -1].shift(1)).sub(1)
    return df.iloc[:, [-1]].dropna(axis=0)


def get_data_cobb_douglas(series_number: int = 3) -> DataFrame:
    '''Original Cobb--Douglas Data Preprocessing Extension'''
    ARCHIVE_NAMES = (
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_douglas.zip',
    )
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4': 'capital',
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': 'labor',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': 'product',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': 'product_nber',
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': 'product_rev',
    }
    FUNCTIONS = (
        extract_usa_classic,
        extract_usa_classic,
        extract_usa_census,
        extract_usa_census,
        extract_usa_classic,
    )
    data_frame = pd.concat(
        [
            partial(func, **{'archive_name': archive_name,
                             'series_id': series_id})()
            for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS.keys(), FUNCTIONS)
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    data_frame.columns = SERIES_IDS.values()
    return data_frame.div(data_frame.iloc[0, :]).iloc[:, range(series_number)]


def get_data_combined():
    '''Most Up-To-Date Version'''
    # =========================================================================
    # TODO: Refactor It
    # =========================================================================
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    _data = extract_usa_bea_from_url(URL)
    SERIES_IDS = (
        'A006RC',
        'A006RD',
        'A008RC',
        'A008RD',
        'A032RC',
        'A191RA',
        'A191RC',
        'A191RX',
        'W170RC',
        'W170RX',
    )
    _data_nipa = pd.concat(
        [
            extract_usa_bea_from_loaded(_data, _id) for _id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    SERIES_IDS = (
        'H4313C',
        'J4313C',
        'A4313C',
        'N4313C',
    )
    _labor_frame = pd.concat(
        [
            extract_usa_bea_from_loaded(_data, _id) for _id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    _labor_frame['mfg_labor'] = _labor_frame.mean(axis=1)
    _labor_frame = _labor_frame.iloc[:, [-1]]
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    )
    WB_NAMES = (
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAME, SERIES_ID = ('51000 Ann', 'K100701',)
    # =========================================================================
    # Fixed Assets Series: K100701, 1951--2013
    # =========================================================================
    _data_sfat = pd.concat(
        [
            extract_usa_bea(_archive, _wb, SH_NAME, SERIES_ID) for _archive, _wb in zip(ARCHIVE_NAMES, WB_NAMES)
        ],
        sort=True
    ).drop_duplicates()
    # =========================================================================
    # US BEA Fixed Assets Series Tests
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAMES = (
        'Section1ALL_xls.xls',
        'Section2ALL_xls.xls',
    )
    SH_NAMES = (
        '105 Ann',
        '106 Ann',
        '101 Ann',
        '203 Ann',
        '202 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Investment in Fixed Assets, Private, i3ptotl1es000, 1901--2016
        # =====================================================================
        'i3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Index for Investment in Fixed Assets, Private, icptotl1es000, 1901--2016
        # =====================================================================
        'icptotl1es000',
        # =====================================================================
        # Current-Cost Net Stock of Fixed Assets, Private, k1ptotl1es000, 1925--2016
        # =====================================================================
        'k1ptotl1es000',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es000, 1925--2016
        # =====================================================================
        'k3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Indexes for Net Stock of Fixed Assets, Private, kcptotl1es000, 1925--2016
        # =====================================================================
        'kcptotl1es000',
    )
    _data_sfat_ = pd.concat(
        [
            extract_usa_bea(ARCHIVE_NAME, _wb, _sh, _id) for _wb, _sh, _id in zip(
                tuple(WB_NAMES[_ // 3] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    return pd.concat(
        [
            _data_nipa,
            _labor_frame,
            _data_sfat,
            _data_sfat_,
            get_data_usa_frb_ms(),
            get_data_usa_frb_ms(),
            get_data_usa_frb_ms(),
            pd.read_csv(FILE_NAME, index_col=0),
        ],
        axis=1,
        sort=True
    )


def get_data_combined_archived():
    '''Version: 02 December 2013'''
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10103 Ann',
        '10105 Ann',
        '10105 Ann',
        '10105 Ann',
        '10106 Ann',
        '10109 Ann',
        '10109 Ann',
        '10705 Ann',
        '50100 Ann',
        '50206 Ann',
        '50900 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Gross Domestic Product, 2005=100: B191RA3, 1929--2012
        # =====================================================================
        'B191RA3',
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Gross private domestic investment -- Nonresidential: A008RC1, 1929--2012
        # =====================================================================
        'A008RC1',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # Implicit Price Deflator Series: A006RD3, 1929--2012
        # =====================================================================
        'A006RD3',
        # =====================================================================
        # Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD3, 1929--2012
        # =====================================================================
        'A008RD3',
        # =====================================================================
        # Nominal National income Series: A032RC1, 1929--2011
        # =====================================================================
        'A032RC1',
        # =====================================================================
        # Gross Domestic Investment, W170RC1, 1929--2012
        # =====================================================================
        'W170RC1',
        # =====================================================================
        # Gross Domestic Investment, W170RX1, 1967--2011
        # =====================================================================
        'W170RX1',
        # =====================================================================
        # `K160491` Replaced with `K10070` in `get_data_combined()`
        # Fixed Assets Series: K160491, 1951--2011
        # =====================================================================
        'K160491',
    )
    _data_nipa = pd.concat(
        [
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[2*(_ // 8)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[1 + 2*(_ // 8)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
    WB_NAMES = (
        'Section1ALL_xls.xls',
        'Section2ALL_xls.xls',
    )
    SH_NAMES = (
        '105 Ann',
        '106 Ann',
        '101 Ann',
        '203 Ann',
        '202 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Investment in Fixed Assets and Consumer Durable Goods, Private, i3ptotl1es000, 1901--2011
        # =====================================================================
        'i3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Indexes for Investment in Fixed Assets and Consumer Durable Goods, Private, icptotl1es000, 1901--2011
        # =====================================================================
        'icptotl1es000',
        # =====================================================================
        # Current-Cost Net Stock of Fixed Assets and Consumer Durable Goods, Private, k1ptotl1es000, 1925--2011
        # =====================================================================
        'k1ptotl1es000',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Equipment and Software, and Structures by Type, Private fixed assets, k3ptotl1es000, 1925--2011
        # =====================================================================
        'k3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Indexes for Net Stock of Private Fixed Assets, Equipment and Software, and Structures by Type, Private fixed assets, kcptotl1es000, 1925--2011
        # =====================================================================
        'kcptotl1es000',
    )
    _data_sfat = pd.concat(
        [
            extract_usa_bea(ARCHIVE_NAME, _wb, _sh, _id) for _wb, _sh, _id in zip(
                tuple(WB_NAMES[_ // 3] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )
    FILE_NAMES = (
        'dataset_usa_0022_m1.txt',
        'dataset_usa_0025_p_r.txt',
    )
    _data = pd.concat(
        [
            pd.read_csv(file_name, index_col=0) for file_name in FILE_NAMES
        ],
        axis=1,
        sort=True
    )
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_ID = 'X0414'
    data_frame = pd.concat(
        [_data_nipa,
         _data_sfat,
         _data,
         # ====================================================================
         # Labor Series
         # ====================================================================
         get_data_usa_bea_labor_mfg(),
         extract_usa_census(ARCHIVE_NAME, SERIES_ID),
         get_data_usa_frb_ms()],
        axis=1,
        sort=True
    )
    return data_frame.iloc[:, [0, 1, 2, 3, 4, 7, 5, 6, 18, 9, 10, 8, 11, 12, 13, 14, 15, 16, 19, 20, 17, ]]


def get_data_common_archived():
    """Data Fetch"""
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10106 Ann',
        '10109 Ann',
        '11200 Ann',
        '51000 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1, 1929--2014
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX1, 1929--2014, 2009=100
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # Deflator Gross Domestic Product, A191RD3, 1929--2014, 2009=100
        # =====================================================================
        'A191RD3',
        # =====================================================================
        # National Income: A032RC1, 1929--2014
        # =====================================================================
        'A032RC1',
        # =====================================================================
        # Fixed Assets Series: K100021, 1951--2014
        # =====================================================================
        'K100021',
    )
    _data_nipa = pd.concat(
        [
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[2*(_ // 4)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    extract_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id) for _wb, _sh, _id in zip(
                        tuple(WB_NAMES[1 + 2*(_ // 4)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
                ],
                axis=1,
                sort=True
            ),
        ],
        sort=True
    ).drop_duplicates()
    _data_nipa.loc[:, [SERIES_IDS[2]]
                   ] = _data_nipa.loc[:, [SERIES_IDS[2]]].rdiv(100)

    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAMES = (
        'Section2ALL_xls.xls',
        'Section4ALL_xls.xls',
    )
    SH_NAMES = (
        '201 Ann',
        '203 Ann',
        '401 Ann',
        '403 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Fixed Assets Series: k1ntotl1si000, 1925--2016
        # =====================================================================
        'k1ntotl1si000',
        # =====================================================================
        # Fixed Assets Series: k3ntotl1si000, 1925--2016
        # =====================================================================
        'k3ntotl1si000',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es000, 1925--2016
        # =====================================================================
        'k1n31gd1es000',
        # =====================================================================
        # Fixed Assets Series: k3n31gd1es000, 1925--2016
        # =====================================================================
        'k3n31gd1es000',
    )
    _data_sfat = pd.concat(
        [
            extract_usa_bea(ARCHIVE_NAME, _wb, _sh, _id) for _wb, _sh, _id in zip(
                tuple(WB_NAMES[_ // 2] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )

    return pd.concat(
        [
            _data_nipa,
            _data_sfat,
            get_data_usa_bea_labor_mfg(),
            # =====================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =====================================================================
            get_data_usa_frb_cu(),
        ],
        axis=1,
        sort=True)


def get_data_douglas():
    '''Douglas Data Preprocessing'''
    ARCHIVE_NAME = 'dataset_douglas.zip'
    SERIES_IDS = ('DT19AS03', 'DT19AS02', 'DT19AS01',)
    data_frame = pd.concat(
        [
            extract_usa_classic(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True)
    return data_frame.div(data_frame.iloc[data_frame.index.get_loc(1899), :])


def get_data_local():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10105 Ann',
        '10106 Ann',
        '50900 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # `K160491` Replaced with `K10070` in `get_data_combined()`
        # Fixed Assets Series: K160491, 1951--2011
        # =====================================================================
        'K160491',
    )
    _data_nipa = pd.concat(
        [
            pd.concat(
                [extract_usa_bea(ARCHIVE_NAMES[0], _wb, _sh, _id)
                 for _wb, _sh, _id in zip(tuple(WB_NAMES[2*(_ // 3)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True,
            ),
            pd.concat(
                [extract_usa_bea(ARCHIVE_NAMES[1], _wb, _sh, _id)
                 for _wb, _sh, _id in zip(tuple(WB_NAMES[1 + 2*(_ // 3)] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True,
            ),
        ],
        sort=True).drop_duplicates()
    return pd.concat(
        [
            _data_nipa,
            get_data_usa_bea_labor_mfg(),
            get_data_usa_frb_cu(),
        ],
        axis=1,
        sort=True
    )


def get_data() -> DataFrame:
    '''Data Fetch'''
    # =========================================================================
    # TODO: Update Accodring to Change in get_data_cobb_douglas_deflator()
    # =========================================================================
    capital = pd.concat(
        [
            # =================================================================
            # Data Fetch for Capital
            # =================================================================
            get_data_cobb_douglas_extension_capital(),
            # =================================================================
            # Data Fetch for Capital Deflator
            # =================================================================
            get_data_cobb_douglas_deflator(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    capital['capital_real'] = capital.iloc[:, 0].div(capital.iloc[:, 1])
    data_frame = pd.concat(
        [
            capital.iloc[:, [-1]],
            # =================================================================
            # Data Fetch for Labor
            # =================================================================
            get_data_cobb_douglas_extension_labor(),
            # =================================================================
            # Data Fetch for Product
            # =================================================================
            get_data_cobb_douglas_extension_product(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    return data_frame.div(data_frame.iloc[0, :])


def get_data_updated():
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    _data = extract_usa_bea_from_url(URL)
    SERIES_IDS = (
        'A006RC',
        'A006RD',
        'A191RC',
        'A191RX',
    )
    _data_nipa = pd.concat(
        [
            extract_usa_bea_from_loaded(_data, _id) for _id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAME = 'Section4ALL_xls.xls'
    SH_NAMES = (
        '403 Ann',
        '402 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Not Used: Fixed Assets: k3n31gd1es000, 1925--2016, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k3n31gd1es000',
        # =====================================================================
        # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'kcn31gd1es000',
    )
    _data_sfat = pd.concat(
        [
            extract_usa_bea(ARCHIVE_NAME, WB_NAME, _sh, _id) for _sh, _id in zip(SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )
    _data = pd.concat(
        [
            _data_nipa,
            _data_sfat,
        ],
        axis=1,
        sort=True
    )
    # =========================================================================
    # Investment, 2012=100
    # =========================================================================
    _data['_inv'] = _data.loc[:, 'A006RD'].mul(
        _data.loc[2012, 'A006RC']).div(100)
    # =========================================================================
    # Capital, 2012=100
    # =========================================================================
    _data['_cap'] = _data.loc[:, 'kcn31gd1es000'].mul(
        _data.loc[2009, 'k3n31gd1es000']).mul(1000).div(100)
    # =========================================================================
    # Capital Retirement Ratio
    # =========================================================================
    _data['_ratio_mu'] = _data.iloc[:, -
                                    2].mul(1).sub(_data.iloc[:, -1].shift(-1)).div(_data.iloc[:, -1]).add(1)
    return (
        _data.loc[:, ['_inv', 'A191RX', '_cap', '_ratio_mu']].dropna(axis=0),
        _data.loc[:, ['_ratio_mu']].dropna(axis=0),
        _data.index.get_loc(2012)
    )


def get_data_usa_bea_labor():
    # =========================================================================
    # Labor Series: A4601C0, 1929--2011
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section6ALL_Hist.xls',
        'Section6ALL_Hist.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
    )
    SH_NAMES = (
        '60800A Ann',
        '60800B Ann',
        '60800B Ann',
        '60800C Ann',
        '60800D Ann',
    )
    SERIES_ID = 'A4601C0'
    data_frame = pd.concat(
        [
            extract_usa_bea(archive_name, wb, sh, SERIES_ID)
            for archive_name, wb, sh in zip(ARCHIVE_NAMES, WB_NAMES, SH_NAMES)
        ],
        axis=1,
        sort=True)
    data_frame[SERIES_ID] = data_frame.mean(axis=1)
    return data_frame.iloc[:, [-1]].dropna(axis=0)


def get_data_usa_bea_labor_mfg():
    # =========================================================================
    # Manufacturing Labor Series: H4313C0, 1929--1948
    # Manufacturing Labor Series: J4313C0, 1948--1969
    # Manufacturing Labor Series: J4313C0, 1969--1987
    # Manufacturing Labor Series: A4313C0, 1987--2000
    # Manufacturing Labor Series: N4313C0, 1998--2011
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section6ALL_Hist.xls',
        'Section6ALL_Hist.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
        'Section6all_xls.xls',
    )
    SH_NAMES = (
        '60500A Ann',
        '60500B Ann',
        '60500B Ann',
        '60500C Ann',
        '60500D Ann',
    )
    SERIES_IDS = (
        'H4313C0',
        'J4313C0',
        'J4313C0',
        'A4313C0',
        'N4313C0',
    )
    data_frame = pd.concat(
        [
            extract_usa_bea(archive_name, wb, sh, _id)
            for archive_name, wb, sh, _id in zip(ARCHIVE_NAMES, WB_NAMES, SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True)
    data_frame['mfg_labor'] = data_frame.mean(axis=1)
    return data_frame.iloc[:, [-1]].dropna(axis=0)


def get_data_usa_bls_cpiu():
    '''BLS CPI-U Price Index Fetch'''
    FILE_NAME = 'dataset_usa_bls_cpiai.txt'
    data_frame = pd.read_csv(FILE_NAME,
                             sep='\s+',
                             index_col=0,
                             usecols=range(13),
                             skiprows=16)
    data_frame.rename_axis('period', inplace=True)
    data_frame['mean'] = data_frame.mean(axis=1)
    data_frame['sqrt'] = data_frame.iloc[:, :-1].prod(1).pow(1/12)
    # =========================================================================
    # Tests
    # =========================================================================
    data_frame['mean_less_sqrt'] = data_frame.iloc[:, -
                                                   2].sub(data_frame.iloc[:, -1])
    data_frame['dec_on_dec'] = data_frame.iloc[:, -
                                               3].div(data_frame.iloc[:, -3].shift(1)).sub(1)
    data_frame['mean_on_mean'] = data_frame.iloc[:, -
                                                 4].div(data_frame.iloc[:, -4].shift(1)).sub(1)
    return data_frame.iloc[:, [-1]].dropna(axis=0)


def get_data_usa_capital():
    # =========================================================================
    # Series Not Used - `k3ntotl1si00`
    # =========================================================================
    URL = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    SERIES_IDS = (
        # =====================================================================
        # Annual Increase in Terms of Cost Price (1)
        # =====================================================================
        'CDT2S1',
        # =====================================================================
        # Annual Increase in Terms of 1880 dollars (3)
        # =====================================================================
        'CDT2S3',
        # =====================================================================
        # Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4',
    )
    data_frame = pd.concat(
        [
            extract_usa_classic(ARCHIVE_NAME, series_id) for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    _data_frame = extract_usa_bea_from_url(URL)
    SERIES_IDS = (
        # =====================================================================
        # Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k1n31gd1es00',
        # =====================================================================
        # Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k3n31gd1es00',
    )
    data_frame = pd.concat(
        [
            data_frame,
            pd.concat(
                [
                    extract_usa_bea_from_loaded(_data_frame, series_id) for series_id in SERIES_IDS
                ],
                axis=1,
                sort=True
            )
        ],
        axis=1,
        sort=True
    )
    ARCHIVE_NAMES = (
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_census1975.zip',
        'dataset_usa_kendrick.zip',
        'dataset_douglas.zip',
    )
    SERIES_IDS = (
        'P0107',
        'P0110',
        'P0119',
        # =====================================================================
        # Kendrick J.W., Productivity Trends in the United States, Page 320
        # =====================================================================
        'KTA15S08',
        # =====================================================================
        # Douglas P.H., Theory of Wages, Page 332
        # =====================================================================
        'DT63AS01',
    )
    FUNCTIONS = (
        extract_usa_census,
        extract_usa_census,
        extract_usa_census,
        extract_usa_classic,
        extract_usa_classic,
    )
    return pd.concat(
        [
            data_frame,
            pd.concat(
                [
                    partial(func, **{'archive_name': archive_name,
                                     'series_id': series_id})()
                    for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS, FUNCTIONS)
                ],
                axis=1,
                sort=True
            ).truncate(before=1869),
            # =================================================================
            # FRB Data
            # =================================================================
            get_data_usa_frb_fa(),
        ],
        axis=1,
        sort=True
    )


def get_data_usa_frb_cu():
    '''Indexed Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
    CAPUTL.B50001.A Fetching'''
    FILE_NAME = 'dataset_usa_frb_g17_all_annual_2013_06_23.csv'
    SERIES_ID = 'CAPUTLB50001A'
    data_frame = pd.read_csv(FILE_NAME, skiprows=1, usecols=range(5, 100))
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].str.replace(r"[,@\'?\.$%_]",
                                                              '',
                                                              regex=True)
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.index = pd.to_numeric(data_frame.index, downcast='integer')
    return data_frame.loc[:, [SERIES_ID]].dropna(axis=0)


def get_data_usa_frb_fa():
    '''Returns Frame of Manufacturing Fixed Assets Series, Billion USD:
    data_frame.iloc[:,0]: Nominal;
    data_frame.iloc[:,1]: Real
    '''
    FILE_NAME = 'dataset_usa_frb_invest_capital.csv'
    data_frame = pd.read_csv(FILE_NAME,
                             skiprows=4, skipfooter=688, engine='python')
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.index = data_frame.index.astype(int)
    data_frame['frb_nominal'] = ((data_frame.iloc[:, 1].mul(data_frame.iloc[:, 2]).div(data_frame.iloc[:, 0])).add(
        data_frame.iloc[:, 4].mul(data_frame.iloc[:, 5]).div(data_frame.iloc[:, 3]))).div(1000)
    data_frame['frb_real'] = data_frame.iloc[:, [2, 5]].sum(axis=1).div(1000)
    return data_frame.iloc[:, -2:]


def get_data_usa_frb_fa_def():
    '''Returns Frame of Deflator for Manufacturing Fixed Assets Series, Index:
    result_frame.iloc[:,0]: Deflator
    '''
    FILE_NAME = 'dataset_usa_frb_invest_capital.csv'
    data_frame = pd.read_csv(FILE_NAME,
                             skiprows=4, skipfooter=688, engine='python')
    data_frame.columns = ['period', *data_frame.columns[1:]]
    data_frame = data_frame.set_index(data_frame.columns[0]).transpose()
    data_frame.index = data_frame.index.astype(int)
    data_frame['fa_def_frb'] = (data_frame.iloc[:, [1, 4]].sum(axis=1)).div(
        data_frame.iloc[:, [0, 3]].sum(axis=1))
    return data_frame.iloc[:, [-1]]


def get_data_usa_frb_ip():
    '''Indexed Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018'''
    # =========================================================================
    # TODO: https://www.federalreserve.gov/datadownload/Output.aspx?rel=g17&filetype=zip
    # =========================================================================
    # =========================================================================
    # with ZipFile('FRB_g17.zip', 'r').open('G17_data.xml') as f:
    # =========================================================================
    FILE_NAME = 'dataset_usa_frb_us3_ip_2018_09_02.csv'
    SERIES_ID = 'AIPMA_SA_IX'
    data_frame = pd.read_csv(FILE_NAME, skiprows=7, parse_dates=[0])
    data_frame.columns = [column.strip() for column in data_frame.columns]
    data_frame = data_frame.loc[:, [data_frame.columns[0], SERIES_ID]]
    data_frame['period'] = data_frame.iloc[:, 0].dt.year
    return data_frame.groupby(data_frame.columns[-1]).mean()


def get_data_usa_frb_ms() -> DataFrame:
    ''''Indexed Money Stock Measures (H.6) Series'''
    URL = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H6&series=5398d8d1734b19f731aba3105eb36d47&lastobs=&from=01/01/1959&to=12/31/2018&filetype=csv&label=include&layout=seriescolumn'
    data_frame = pd.read_csv(
        io.BytesIO(requests.get(URL).content),
        names=['period', 'm1_m'],
        index_col=0,
        usecols=range(2),
        skiprows=6,
        parse_dates=True,
        thousands=','
    )
    return data_frame.groupby(data_frame.index.year).mean()


def get_data_usa_mcconnel_a():
    SERIES_ID = 'Валовой внутренний продукт, млрд долл. США'
    data_frame = extract_usa_mcconnel(SERIES_ID)
    return data_frame[data_frame.index.get_loc(1980):]


def get_data_usa_mcconnel_b():
    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'prime_rate',
        'Национальный доход, млрд долл. США': 'A032RC1',
    }
    data_frame = pd.concat([extract_usa_mcconnel(series_id)
                           for series_id in SERIES_IDS.keys()],
                           axis=1,
                           sort=True)
    data_frame.columns = SERIES_IDS.values()
    return data_frame[data_frame.index.get_loc(1980):]


def get_data_usa_mcconnel_c():
    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'prime_rate',
        'Валовой объем внутренних частных инвестиций, млрд долл. США': 'A006RC1',
    }
    data_frame = pd.concat([extract_usa_mcconnel(series_id)
                           for series_id in SERIES_IDS.keys()],
                           axis=1,
                           sort=True)
    data_frame.columns = SERIES_IDS.values()
    return data_frame[data_frame.index.get_loc(1980):]


def get_data_usa_sahr_infcf():
    '''Retrieve Yearly Price Rates from `dataset_usa_infcf16652007.zip`'''
    ARCHIVE_NAME = 'dataset_usa_infcf16652007.zip'
    data_frame = pd.read_csv(ARCHIVE_NAME, usecols=range(4, 7))
    result_frame = DataFrame()
    # =========================================================================
    # Retrieve First 14 Series
    # =========================================================================
    for series_id in data_frame.iloc[:, 0].unique()[:14]:
        chunk = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
        chunk.columns = [chunk.columns[0],
                         series_id.replace(' ', '_').lower()]
        chunk.set_index(chunk.columns[0], inplace=True)
        chunk = chunk.rdiv(1)
        chunk = -price_inverse_single(chunk)
        result_frame = pd.concat([result_frame, chunk], axis=1, sort=True)
    result_frame['cpiu_fused'] = result_frame.mean(axis=1)
    return result_frame.iloc[:, [-1]].dropna(axis=0)


def get_data_usa_xlsm():
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAMES = (
        '10105 Ann',
        '10105 Ann',
        '10106 Ann',
        '10705 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC1',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX1',
        # =====================================================================
        # Nominal National income Series: A032RC1, 1929--2011
        # =====================================================================
        'A032RC1',
    )
    _data = pd.concat(
        [
            pd.concat(
                [extract_usa_bea(ARCHIVE_NAMES[0], WB_NAMES[0], _sh, _id)
                 for _sh, _id in zip(SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True
            ),
            pd.concat(
                [extract_usa_bea(ARCHIVE_NAMES[1], WB_NAMES[1], _sh, _id)
                 for _sh, _id in zip(SH_NAMES, SERIES_IDS)],
                axis=1,
                sort=True
            ),
        ],
        sort=True).drop_duplicates()
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    return pd.concat(
        [
            _data,
            pd.read_csv(FILE_NAME, index_col=0)
        ],
        axis=1,
        sort=True
    )


def get_data_version_a():
    '''Data Fetch Archived
    Returns:
        _data_a: Capital, Labor, Product;
        _data_b: Capital, Labor, Product Adjusted to Capacity Utilisation'''
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAME, SERIES_ID = ('10106 Ann', 'A191RX1')
    KWARGS = {
        'archive_name': 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
        'wb_name': 'Section4ALL_xls.xls',
        'sh_name': '402 Ann',
        'series_id': 'kcn31gd1es000',
    }
    _data_a = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            extract_usa_bea(**KWARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
            # =================================================================
            pd.concat(
                [
                    extract_usa_bea(_archive_name, _wb, SH_NAME, SERIES_ID) for _archive_name, _wb in zip(ARCHIVE_NAMES, WB_NAMES)
                ],
                sort=True).drop_duplicates(),
        ],
        axis=1, sort=True).dropna(axis=0)
    _data_b = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            extract_usa_bea(**KWARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
            # =================================================================
            pd.concat(
                [
                    extract_usa_bea(_archive_name, _wb, SH_NAME, SERIES_ID) for _archive_name, _wb in zip(ARCHIVE_NAMES, WB_NAMES)
                ],
                sort=True).drop_duplicates(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            get_data_usa_frb_cu(),
        ],
        axis=1, sort=True).dropna(axis=0)
    _data_b.iloc[:, 2] = _data_b.iloc[:, 2].div(_data_b.iloc[:, 3]).mul(100)
    return _data_a.div(_data_a.iloc[0, :]), _data_b.div(_data_b.iloc[0, :]).iloc[:, range(3)]


def get_data_version_b():
    """
    Returns
        data_frame_a: Capital, Labor, Product;
        data_frame_b: Capital, Labor, Product;
        data_frame_c: Capital, Labor, Product Adjusted to Capacity Utilisation
    """
    '''Data Fetch Revised'''
    KWARGS = {
        'archive_name': 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
        'wb_name': 'Section4ALL_xls.xls',
        'sh_name': '402 Ann',
        'series_id': 'kcn31gd1es000',
    }
    data_frame_a = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            extract_usa_bea(**KWARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
            # =================================================================
            get_data_usa_frb_ip(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    data_frame_b = data_frame_a[data_frame_a.index.get_loc(1967):]
    data_frame_c = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            extract_usa_bea(**KWARGS),
            # =================================================================
            # Labor
            # =================================================================
            get_data_usa_bea_labor_mfg(),
            # =================================================================
            # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
            # =================================================================
            get_data_usa_frb_ip(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            get_data_usa_frb_cu(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    data_frame_c.iloc[:, 2] = data_frame_c.iloc[:, 2].div(
        data_frame_c.iloc[:, 3]).mul(100)
    return (
        data_frame_a.div(data_frame_a.iloc[0, :]),
        data_frame_b.div(data_frame_b.iloc[0, :]),
        data_frame_c.div(data_frame_c.iloc[0, :]).iloc[:, range(3)]
    )


def get_data_version_c():
    """Data Fetch"""
    # =========================================================================
    # Data Fetch for Capital
    # Data Fetch for Capital Deflator
    # =========================================================================
    capital_frame = pd.concat(
        [get_data_cobb_douglas_extension_capital(), get_data_cobb_douglas_deflator()],
        axis=1, sort=True).dropna(axis=0)
    capital_frame['capital_real'] = capital_frame.iloc[:, 0].div(
        capital_frame.iloc[:, 1])
    # =========================================================================
    # Data Fetch for Labor
    # =========================================================================
    labor_frame = get_data_cobb_douglas_extension_labor()
    # =========================================================================
    # Data Fetch for Product
    # =========================================================================
    product_frame = get_data_cobb_douglas_extension_product()
    result_frame = pd.concat(
        [capital_frame.iloc[:, 2], labor_frame, product_frame], axis=1, sort=True).dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def get_mean_for_min_std():
    # =========================================================================
    # Determine Year & Mean Value for Base Vectors for Year with Minimum StandardError
    # =========================================================================
    # =========================================================================
    # Base Vector v123355112
    # Base Vector v1235071986
    # Base Vector v2057609
    # Base Vector v2057818
    # Base Vector v2523013
    # =========================================================================
    result = DataFrame()
    FILE_NAME = '/home/alexander/projects/stat_can_lab.xlsx'
    _ = pd.read_excel(FILE_NAME)
    _.set_index(_.columns[0], inplace=True)
    SERIES_IDS = (
        'v123355112',
        'v1235071986',
        'v2057609',
        'v2057818',
        'v2523013',
    )
    for series_id in SERIES_IDS:
        chunk = _.loc[:, [series_id]]
        chunk.dropna(axis=0, inplace=True)
        result = pd.concat([result, chunk], axis=1, sort=False)
    result.dropna(axis=0, inplace=True)
    result['std'] = result.std(axis=1)
    return (result.iloc[:, [-1]].idxmin()[0],
            result.loc[result.iloc[:, [-1]].idxmin()[0], :][:-1].mean())


def get_price_base(df: DataFrame) -> int:
    '''
    Determine Base Year

    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Deflator
    ================== =================================

    Returns
    -------
    int
        Base Year.

    '''
    df['__deflator'] = df.iloc[:, 0].sub(100).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    return int(df.index[_b])


def transform_a(df: DataFrame) -> DataFrame:
    df = df.iloc[:, [0, 4, 6, 7]]
    df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
    return df.div(df.iloc[0, :]).dropna()


def transform_b(df: DataFrame) -> DataFrame:
    return df.iloc[:, [0, 6, 7, 20]].dropna()


def transform_c(df: DataFrame) -> DataFrame:
    df_production = df.iloc[:, [0, 6, 7]].dropna()
    df_production = df_production.div(df_production.iloc[0, :])
    df_money = df.iloc[:, range(18, 20)].dropna(how='all')
    df_money['m1_fused'] = df_money.mean(axis=1)
    df_money = df_money.iloc[:, -1].div(df_money.iloc[0, -1])
    _df = pd.concat(
        [
            df_production,
            df_money
        ],
        axis=1).dropna()
    return _df.div(_df.iloc[0, :])


def transform_d(df: DataFrame) -> DataFrame:
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return df.iloc[:, [0, 1, 2, 3, 7]].dropna()


def transform_e(df: DataFrame) -> tuple[DataFrame]:
    assert df.shape[1] == 21, 'Works on DataFrame Produced with `get_data_combined_archived()`'
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    df['inv'] = df.iloc[:, 0].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    # =========================================================================
    # `Real` Capital
    # =========================================================================
    df['cap'] = df.iloc[:, 11].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    return (
        # =====================================================================
        # DataFrame Nominal
        # =====================================================================
        df.iloc[:, [0, 6, 11]].dropna(),
        # =====================================================================
        # DataFrame `Real`
        # =====================================================================
        df.iloc[:, [-2, 7, -1]].dropna(),
    )


def transform_cobb_douglas(df: DataFrame) -> tuple[DataFrame, tuple[float]]:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Original: k=0.25
    # =========================================================================
    k, b = np.polyfit(
        np.log(df.iloc[:, -2]),
        np.log(df.iloc[:, -1]),
        deg=1
    )
    # =========================================================================
    # Scipy Signal Median Filter, Non-Linear Low-Pass Filter
    # =========================================================================
    # =========================================================================
    # k, b = np.polyfit(
    #     np.log(signal.medfilt(df.iloc[:, -2])),
    #     np.log(signal.medfilt(df.iloc[:, -1])),
    #     deg=1
    # )
    # =========================================================================
    # =========================================================================
    # Description
    # =========================================================================
    df['cap_to_lab'] = df.iloc[:, 1].div(df.iloc[:, 0])
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 2].div(df.iloc[:, 0])
    # =========================================================================
    # Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_roll'] = df.iloc[:, 2].rolling(window=3, center=True).mean()
    df['prod_roll_sub'] = df.iloc[:, 2].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product
    # =========================================================================
    df['prod_comp'] = df.iloc[:, 0].pow(k).mul(
        df.iloc[:, 1].pow(1-k)).mul(np.exp(b))
    # =========================================================================
    # Computed Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_comp_roll'] = df.iloc[:, -1].rolling(window=3, center=True).mean()
    df['prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    # =========================================================================
    #     print(r2_score(df.iloc[:, 2], df.iloc[:, 3]))
    #     print(df.iloc[:, 3].div(df.iloc[:, 2]).sub(1).abs().mean())
    # =========================================================================
    return df, (k, np.exp(b),)


def transform_cobb_douglas_alt(df: DataFrame) -> tuple[DataFrame, tuple[float]]:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product,
    df.iloc[:, 3]: Product Alternative,
    '''
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Original: k=0.25
    # =========================================================================
    k, b = np.polyfit(
        np.log(df.iloc[:, -2]),
        np.log(df.iloc[:, -1]),
        deg=1
    )
    # =========================================================================
    # Description
    # =========================================================================
    df['cap_to_lab'] = df.iloc[:, 1].div(df.iloc[:, 0])
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 2].div(df.iloc[:, 0])
    # =========================================================================
    # Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_roll'] = df.iloc[:, 2].rolling(window=3, center=True).mean()
    df['prod_roll_sub'] = df.iloc[:, 2].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product
    # =========================================================================
    df['prod_comp'] = df.iloc[:, 0].pow(k).mul(
        df.iloc[:, 1].pow(1-k)).mul(np.exp(b))
    # =========================================================================
    # Computed Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_comp_roll'] = df.iloc[:, -1].rolling(window=3, center=True).mean()
    df['prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    # =========================================================================
    # Labor Productivity Alternative
    # =========================================================================
    df['_lab_product'] = df.iloc[:, 3].div(df.iloc[:, 1])
    # =========================================================================
    # Original: _k=0.25
    # =========================================================================
    _k, _b = np.polyfit(
        np.log(df.iloc[:, 4]),
        np.log(df.iloc[:, -1]),
        deg=1
    )
    # =========================================================================
    # Fixed Assets Turnover Alternative
    # =========================================================================
    df['_c_turnover'] = df.iloc[:, 3].div(df.iloc[:, 0])
    # =========================================================================
    # Product Alternative Trend Line=3 Year Moving Average
    # =========================================================================
    df['_prod_roll'] = df.iloc[:, 3].rolling(window=3, center=True).mean()
    df['_prod_roll_sub'] = df.iloc[:, 3].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product Alternative
    # =========================================================================
    df['_prod_comp'] = df.iloc[:, 0].pow(_k).mul(
        df.iloc[:, 1].pow(1-_k)).mul(np.exp(_b))
    # =========================================================================
    # Computed Product Alternative Trend Line=3 Year Moving Average
    # =========================================================================
    df['_prod_comp_roll'] = df.iloc[:, -
                                    1].rolling(window=3, center=True).mean()
    df['_prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    return df, (k, np.exp(b),), (_k, np.exp(_b),)

# def transform_cobb_douglas(df: DataFrame) -> tuple[DataFrame, tuple[float]]:
# =============================================================================
#     TODO: Implement Additional Features
# =============================================================================
#     '''
#     df.index: Period,
#     df.iloc[:, 0]: Capital,
#     df.iloc[:, 1]: Labor,
#     df.iloc[:, 2]: Product
#     '''
#     from sklearn.linear_model import Lasso
#     from sklearn.linear_model import LassoCV
#     from sklearn.linear_model import LinearRegression
#     from sklearn.linear_model import Ridge
#     # =========================================================================
#     # Labor Capital Intensity
#     # =========================================================================
#     df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
#     # =========================================================================
#     # Labor Productivity
#     # =========================================================================
#     df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
#     # # =========================================================================
#     # # TODO: Refresh
#     # # =========================================================================
#     # df['_lab_cap_int'] = np.vstack(
#     #     (np.zeros((df.shape[0], 1)).T,
#     #      np.log(df.iloc[:, [-2]])))

# # # =============================================================================
# # #     las = Lasso(alpha=0.01).fit(df['_lab_cap_int'], np.log(df.iloc[:, -1]))
# # #     reg = LinearRegression().fit(df['_lab_cap_int'], np.log(df.iloc[:, -1]))
# # # =============================================================================
# #     las = LassoCV(cv=4, random_state=0).fit(
# #         df['_lab_cap_int'], np.log(df.iloc[:, -1]))
# #     print(las)
# # # =============================================================================
# # #     tik = Ridge(alpha=0.01).fit(df['_lab_cap_int'], np.log(df.iloc[:, -1]))
# # #     print('Lasso: a_0 = {0:.12f} & a_1 = {1:.12f}'.format(las.intercept_, las.coef_[1]))
# # #     print('Linear Regression: a_0 = {0:.12f} & a_1 = {1:.12f}'.format(reg.intercept_, reg.coef_[1]))
# # #     print('Ridge Regression: a_0 = {0:.12f} & a_1 = {1:.12f}'.format(tik.intercept_, tik.coef_[1]))
# # # =============================================================================
# #     b = np.exp(las.intercept_)
# # #     # =========================================================================
# # #     # Original: k=0.25
# # #     # =========================================================================
# # #     k, b = np.polyfit(
# # #         np.log(df.iloc[:, -2]),
# # #         np.log(df.iloc[:, -1]),
# # #         deg=1
# # #     )
#     # =========================================================================
#     # Description
#     # =========================================================================
#     df['cap_to_lab'] = df.iloc[:, 1].div(df.iloc[:, 0])
#     # =========================================================================
#     # Fixed Assets Turnover
#     # =========================================================================
#     df['c_turnover'] = df.iloc[:, 2].div(df.iloc[:, 0])
#     # =========================================================================
#     # Product Trend Line=3 Year Moving Average
#     # =========================================================================
#     df['prod_roll'] = df.iloc[:, 2].rolling(window=3, center=True).mean()
#     # df['prod_roll_sub'] = df.iloc[:, 2].sub(df.iloc[:, -1])
#     # =========================================================================
#     # Computed Product
#     # =========================================================================
# #     df['prod_comp'] = df.iloc[:, 0].pow(las.coef_[1]).mul(
# #         df.iloc[:, 1].pow(1-las.coef_[1])).mul(b)
#     # =========================================================================
#     # Computed Product Trend Line=3 Year Moving Average
#     # =========================================================================
#     df['prod_comp_roll'] = df.iloc[:, -1].rolling(window=3, center=True).mean()
#     df['prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
# # #     return df, (k, np.exp(b),)


def transform_kurenkov(data_testing: DataFrame) -> tuple[DataFrame]:
    '''Returns Four DataFrames with Comparison of data_testing: DataFrame and Yu.V. Kurenkov Data'''
    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'
    data_control = pd.read_csv(FILE_NAME, index_col=0)
    # =============================================================================
    # Production
    # =============================================================================
    data_a = pd.concat(
        [
            data_control.iloc[:, [0]],
            data_testing.loc[:, ['A191RX1']],
            get_data_usa_frb_ip(),
        ],
        axis=1, sort=True).dropna(how='all')
    data_a = data_a.div(data_a.loc[1950, :]).mul(100)
    # =============================================================================
    # Labor
    # =============================================================================
    data_b = pd.concat(
        [
            data_control.iloc[:, [1]],
            data_testing.loc[:, ['mfg_labor']],
        ],
        axis=1, sort=True).dropna(how='all')
    # =============================================================================
    # Capital
    # =============================================================================
    data_c = pd.concat(
        [
            data_control.iloc[:, [2]],
            data_testing.loc[:, ['K160491']],
        ],
        axis=1, sort=True).dropna(how='all')
    data_c = data_c.div(data_c.loc[1951, :]).mul(100)
    # =============================================================================
    # Capacity Utilization
    # =============================================================================
    data_d = pd.concat(
        [
            data_control.iloc[:, [3]],
            get_data_usa_frb_cu(),
        ],
        axis=1, sort=True)
    return data_a, data_b, data_c, data_d
