#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 11:52:01 2022

@author: Alexander Mikhailov
"""

import itertools
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from pull.lib import (numerify, pull_by_series_id, pull_can_aggregate,
                      pull_can_capital, pull_can_capital_former)
from read.lib import (read_can, read_can_temp, read_usa_bea, read_usa_davis_ip,
                      read_usa_frb, read_usa_frb_g17, read_usa_frb_ms,
                      read_usa_frb_us3, read_usa_fred, read_usa_hist,
                      read_usa_kurenkov, read_usa_prime_rate)
from scipy.signal import wiener
from toolkit.lib import price_inverse_single, strip_cumulated_deflator
from transform.lib import (transform_cobb_douglas_extension_capital,
                           transform_sum, transform_usa_frb_fa,
                           transform_usa_frb_fa_def)

ARCHIVE_NAMES_UTILISED = (
    'dataset_douglas.zip',
    'dataset_usa_brown.zip',
    'dataset_uscb.zip',
    'dataset_usa_cobb-douglas.zip',
    'dataset_usa_infcf16652007.zip',
    'dataset_usa_kendrick.zip',
)
FILE_NAMES_UTILISED = (
    'dataset_usa_0025_p_r.txt',
    'dataset_usa_davis-j-h-ip-total.xls',
    'dataset_usa_frb_g17_all_annual_2013_06_23.csv',
    'dataset_usa_frb_invest_capital.csv',
    'dataset_usa_frb_us3_ip_2018_09_02.csv',
    'dataset_usa_reference_ru_kurenkov_yu_v.csv',
)


def collect_cobb_douglas(series_number: int = 3) -> DataFrame:
    """
    Original Cobb--Douglas Data Preprocessing Extension

    Parameters
    ----------
    series_number : int, optional
        DESCRIPTION. The default is 3.

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital
    df.iloc[:, 1]      Labor
    df.iloc[:, 2]      Product
    ================== =================================
    """
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4': ('dataset_usa_cobb-douglas.zip', 'capital'),
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': ('dataset_usa_cobb-douglas.zip', 'labor'),
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': ('dataset_uscb.zip', 'product'),
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': ('dataset_uscb.zip', 'product_nber'),
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': ('dataset_douglas.zip', 'product_rev'),
    }
    df = pd.concat(
        [
            read_usa_hist(archive_name).pipe(pull_by_series_id, series_id)
            for series_id, (archive_name, _) in SERIES_IDS.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    ).dropna(axis=0)
    df.columns = tuple(column_name for (_, column_name) in SERIES_IDS.values())
    return df.div(df.iloc[0, :]).iloc[:, range(series_number)]


def collect_cobb_douglas_deflator() -> DataFrame:
    """Fixed Assets Deflator, 2009=100"""
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
    # `df.corr(method='kendall')`
    # `df.corr(method='pearson')`
    # `df.corr(method='spearman')`
    # Correlation Test Result: kendall & pearson & spearman: L2, L15, E7, E23, E40, E68
    # =========================================================================
    SERIES_IDS_CB = {
        'L0002': ('dataset_uscb.zip', None),
        'L0015': ('dataset_uscb.zip', None),
        'E0007': ('dataset_uscb.zip', None),
        'E0023': ('dataset_uscb.zip', None),
        'E0040': ('dataset_uscb.zip', None),
        'E0068': ('dataset_uscb.zip', None),
        'P0107': ('dataset_uscb.zip', 1885),
        'P0110': ('dataset_uscb.zip', 1885),
    }
    # =========================================================================
    # Bureau of Economic Analysis
    # =========================================================================
    SERIES_IDS_EA = {
        # =====================================================================
        # Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Fixed Assets: kcn31gd1es00, 1925--2019, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'kcn31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    df = pd.concat(
        [
            # =================================================================
            # Bureau of the Census
            # =================================================================
            pd.concat(
                [
                    read_usa_hist(archive_name).pipe(
                        pull_by_series_id, series_id).sort_index().truncate(before=year)
                    for series_id, (archive_name, year) in SERIES_IDS_CB.items()
                ],
                axis=1,
                verify_integrity=True,
                sort=True
            ),
            # =================================================================
            # Bureau of Economic Analysis
            # =================================================================
            pd.concat(
                [
                    read_usa_bea(url).pipe(pull_by_series_id, series_id)
                    for series_id, url in SERIES_IDS_EA.items()
                ],
                axis=1,
                verify_integrity=True,
                sort=True
            ),
            # =================================================================
            # Federal Reserve Board Data
            # =================================================================
            read_usa_frb().pipe(transform_usa_frb_fa_def),
        ],
        axis=1,
        sort=True
    ).truncate(before=1794)
    SERIES_IDS_CB = tuple(SERIES_IDS_CB)
    SERIES_IDS_EA = tuple(SERIES_IDS_EA)
    df['fa_def_cb'] = df.loc[:, SERIES_IDS_CB[-2]].div(
        df.loc[:, SERIES_IDS_CB[-1]])
    df['ppi_bea'] = df.loc[:, SERIES_IDS_EA[0]].div(
        df.loc[:, SERIES_IDS_EA[1]]).div(df.loc[2012, SERIES_IDS_EA[0]]).mul(100)
    df.drop(
        [*SERIES_IDS_CB[-2:], *SERIES_IDS_EA],
        axis=1,
        inplace=True
    )
    # =========================================================================
    # Strip Deflators
    # =========================================================================
    result = pd.concat(
        [
            strip_cumulated_deflator(df.loc[:, column])
            for column in df.columns
        ],
        axis=1
    )
    result['def_mean'] = result.mean(axis=1)
    return result.iloc[:, [-1]].dropna(axis=0)


def collect_cobb_douglas_extension_labor() -> DataFrame:
    """
    Manufacturing Laborers` Series Comparison

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Labor Series
    ================== =================================
    """
    # =========================================================================
    # TODO: Bureau of Labor Statistics
    # TODO: Federal Reserve Board
    # =========================================================================
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': 'dataset_usa_cobb-douglas.zip',
        # =====================================================================
        # Bureau of the Census 1949, D69
        # =====================================================================
        'D0069': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1949, J4
        # =====================================================================
        'J0004': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1975, D130
        # =====================================================================
        'D0130': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1975, P5
        # =====================================================================
        'P0005': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1975, P62
        # =====================================================================
        'P0062': 'dataset_uscb.zip',
        # =====================================================================
        # Kendrick J.W., Productivity Trends in the United States, Table D-II, `Persons Engaged` Column, pp. 465--466
        # =====================================================================
        'KTD02S02': 'dataset_usa_kendrick.zip',
    }
    df = pd.concat(
        [
            pd.concat(
                [
                    read_usa_hist(archive_name).pipe(
                        pull_by_series_id, series_id)
                    for series_id, archive_name in SERIES_IDS.items()
                ],
                axis=1,
                verify_integrity=True,
                sort=True
            ),
            # =========================================================================
            # Bureau of Economic Analysis, H4313C & J4313C & A4313C & N4313C
            # =========================================================================
            collect_usa_bea_labor_mfg(),
            # =================================================================
            # Kurenkov Yu.V.
            # =================================================================
            read_usa_kurenkov().iloc[:, [1]],
        ],
        axis=1
    ).truncate(before=1889)
    df.iloc[:, 6] = df.iloc[:, 6].mul(
        df.loc[1899, df.columns[0]]
    ).div(df.loc[1899, df.columns[6]])
    df['labor'] = df.iloc[:, [0, 1, 3, 6, 7, 8]].mean(axis=1)
    return df.iloc[:, [-1]]


def collect_cobb_douglas_extension_manufacturing() -> DataFrame:
    SERIES_IDS = {
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census, 1975, Page 667, P17: Edwin Frickey Index of Manufacturing Production
        # =====================================================================
        'P0017': 'dataset_uscb.zip',
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': 'dataset_douglas.zip',
    }
    df = pd.concat(
        [
            pd.concat(
                [
                    read_usa_hist(archive_name).pipe(
                        pull_by_series_id, series_id)
                    for series_id, archive_name in SERIES_IDS.items()
                ],
                axis=1,
                verify_integrity=True,
                sort=True
            ),
            # =================================================================
            # Joseph H. Davis Production Index
            # =================================================================
            read_usa_davis_ip(),
            # =================================================================
            # Federal Reserve, AIPMASAIX
            # =================================================================
            read_usa_frb_us3().loc[:, ['AIPMA_SA_IX']],
        ],
        axis=1
    )
    df.iloc[:, 1] = df.iloc[:, 1].div(
        df.loc[1899, df.columns[1]]).mul(100)
    df.iloc[:, 4] = df.iloc[:, 4].div(df.loc[1899, df.columns[4]]).mul(100)
    df.iloc[:, 5] = df.iloc[:, 5].div(df.loc[1939, df.columns[5]]).mul(100)
    df['fused_classic'] = df.iloc[:, range(5)].mean(axis=1)
    df.iloc[:, -1] = df.iloc[:, -1].div(df.loc[1939, df.columns[-1]]).mul(100)
    df['fused'] = df.iloc[:, -2:].mean(axis=1)
    return df.iloc[:, [-1]]


def collect_douglas() -> DataFrame:
    """Douglas Data Preprocessing"""
    ARCHIVE_NAME = 'dataset_douglas.zip'
    SERIES_IDS = ('DT19AS03', 'DT19AS02', 'DT19AS01',)
    df = pd.concat(
        [
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    return df.div(df.loc[1899, :])


def collect_usa_bea_labor() -> DataFrame:
    """
    Labor Series: A4601C0, 1929--2013
    """
    SERIES_ID, URL = 'A4601C', 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    return read_usa_bea(URL).pipe(pull_by_series_id, SERIES_ID)


def collect_usa_bea_labor_mfg() -> DataFrame:
    """
    Manufacturing Labor Series

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Labor Series
    ================== =================================
    """
    SERIES_IDS = {
        # =====================================================================
        # Manufacturing Labor Series: H4313C, 1929--1948
        # =====================================================================
        'H4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Manufacturing Labor Series: J4313C, 1948--1987
        # =====================================================================
        'J4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Manufacturing Labor Series: A4313C, 1987--2000
        # =====================================================================
        'A4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Manufacturing Labor Series: N4313C, 1998--2020
        # =====================================================================
        'N4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    }
    df = pd.concat(
        [
            read_usa_bea(url).pipe(pull_by_series_id, series_id)
            for series_id, url in SERIES_IDS.items()
        ],
        axis=1,
        sort=True
    )
    df['bea_mfg_labor'] = df.mean(axis=1)
    return df.iloc[:, [-1]].dropna(axis=0)


def collect_usa_brown() -> DataFrame:
    # =========================================================================
    # Fetch Data from <reference_ru_brown_m_0597_088.pdf>, Page 193
    # Out of Kendrick J.W. Data & Table 2. of <reference_ru_brown_m_0597_088.pdf>
    # =========================================================================
    # =========================================================================
    # FN:Murray Brown
    # ORG:University at Buffalo;Economics
    # TITLE:Professor Emeritus, Retired
    # EMAIL;PREF;INTERNET:mbrown@buffalo.edu
    # =========================================================================
    ARCHIVE_NAMES = ('dataset_usa_brown.zip', 'dataset_usa_kendrick.zip',)
    _series_ids = read_usa_hist(ARCHIVE_NAMES[0]).iloc[:, [0]].stack().values
    SERIES_IDS = {
        col: f'series_{hex(_)}' for _, col in enumerate(sorted(set(_series_ids)))
    }
    _b_frame = pd.concat(
        [
            read_usa_hist(ARCHIVE_NAMES[0]).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    _b_frame.columns = SERIES_IDS.values()
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
            read_usa_hist(ARCHIVE_NAMES[1]).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    df = pd.concat(
        [
            # =================================================================
            # Omit Two Last Rows
            # =================================================================
            _k_frame[:-2].truncate(before=1889),
            # =================================================================
            # Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
            # =================================================================
            _b_frame.iloc[:, [-2]].truncate(after=1953)
        ],
        axis=1,
        sort=True
    )
    df = df.assign(
        series_0x0=df.iloc[:, 0].sub(df.iloc[:, 1]),
        series_0x1=df.iloc[:, 3].add(df.iloc[:, 4]),
        series_0x2=df.iloc[:, [3, 4]].sum(axis=1).rolling(
            2).mean().mul(df.iloc[:, 5]).div(100),
        series_0x3=df.iloc[:, 2],
    )
    return pd.concat(
        [
            df.iloc[:, -4:].dropna(axis=0),
            # =================================================================
            # Brown M. Numbers Not Found in Kendrick J.W. For Years Starting From 1954 Inclusive
            # =================================================================
            _b_frame.iloc[:, range(4)].truncate(before=1954)
        ]
    ).round()


def collect_usa_capital() -> DataFrame:
    SERIES_IDS = {
        # =====================================================================
        # Annual Increase in Terms of Cost Price (1)
        # =====================================================================
        'CDT2S1': 'dataset_usa_cobb-douglas.zip',
        # =====================================================================
        # Annual Increase in Terms of 1880 dollars (3)
        # =====================================================================
        'CDT2S3': 'dataset_usa_cobb-douglas.zip',
        # =====================================================================
        # Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4': 'dataset_usa_cobb-douglas.zip',
        'P0107': 'dataset_uscb.zip',
        'P0110': 'dataset_uscb.zip',
        'P0119': 'dataset_uscb.zip',
        # =====================================================================
        # Kendrick J.W., Productivity Trends in the United States, Page 320
        # =====================================================================
        'KTA15S08': 'dataset_usa_kendrick.zip',
        # =====================================================================
        # Douglas P.H., Theory of Wages, Page 332
        # =====================================================================
        'DT63AS01': 'dataset_douglas.zip',
    }
    return pd.concat(
        [
            pd.concat(
                [
                    read_usa_hist(archive_name).pipe(
                        pull_by_series_id, series_id)
                    for series_id, archive_name in SERIES_IDS.items()
                ],
                axis=1,
                verify_integrity=True,
                sort=True
            ).truncate(before=1869),
            # =================================================================
            # FRB Data
            # =================================================================
            read_usa_frb().pipe(transform_usa_frb_fa),
        ],
        axis=1,
        sort=True
    )


def collect_usa_capital_purchases() -> DataFrame:
    SERIES_IDS = {
        'CDT2S1': ('dataset_usa_cobb-douglas.zip', 1, 'nominal, millions'),
        'CDT2S3': ('dataset_usa_cobb-douglas.zip', 1, '1880=100, millions'),
        'DT63AS01': ('dataset_douglas.zip', 1, '1880=100, millions'),
        'DT63AS02': ('dataset_douglas.zip', 1, 'DO_NOT_USE_nominal, millions'),
        'DT63AS03': ('dataset_douglas.zip', 1, 'DO_NOT_USE_nominal, millions'),
        'J0149': ('dataset_uscb.zip', 1, 'nominal, millions'),
        'J0150': ('dataset_uscb.zip', 1, 'nominal, millions'),
        'J0151': ('dataset_uscb.zip', 1, 'nominal, millions'),
        'P0107': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0108': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0109': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0110': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0111': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0112': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0113': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0114': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0115': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0116': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0117': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0118': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0119': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0120': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0121': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0122': ('dataset_uscb.zip', 1000, '1958=100, billions'),
    }
    df = pd.concat(
        [
            read_usa_hist(archive_name).pipe(
                pull_by_series_id, series_id).mul(factor)
            for series_id, (archive_name, factor, _) in SERIES_IDS.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    ).truncate(before=1875)
    df['total'] = wiener(
        df.loc[:, ['CDT2S1', 'J0149', 'P0107']].mean(axis=1)
    ).round()
    df['struc'] = wiener(
        df.loc[:, ['J0150', 'P0108']].mean(axis=1)
    ).round()
    df['equip'] = wiener(
        df.loc[:, ['J0151', 'P0109']].mean(axis=1)
    ).round()
    return df


def collect_usa_general() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    SERIES_ID, ARCHIVE_NAME = 'X0414', 'dataset_uscb.zip'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Implicit Price Deflator Series: A006RD
        # =====================================================================
        'A006RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross private domestic investment -- Nonresidential: A008RC
        # =====================================================================
        'A008RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD
        # =====================================================================
        'A008RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal National income Series: A032RC
        # =====================================================================
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross Domestic Product, 2012=100: A191RA
        # =====================================================================
        'A191RA': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross Domestic Investment, W170RC
        # =====================================================================
        'W170RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross Domestic Investment, W170RX
        # =====================================================================
        'W170RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Investment in Fixed Assets, Private, i3ptotl1es00
        # =====================================================================
        'i3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Chain-Type Quantity Index for Investment in Fixed Assets, Private, icptotl1es00
        # =====================================================================
        'icptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es00
        # =====================================================================
        'k3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    return pd.concat(
        [
            pd.concat(
                [
                    pd.concat(
                        [
                            read_usa_bea(SERIES_IDS[series_id]).pipe(
                                pull_by_series_id, series_id)
                            for series_id in tuple(SERIES_IDS)[:8]
                        ],
                        axis=1
                    ),
                    collect_usa_bea_labor_mfg(),
                    pd.concat(
                        [
                            read_usa_bea(SERIES_IDS[series_id]).pipe(
                                pull_by_series_id, series_id)
                            for series_id in tuple(SERIES_IDS)[8:]
                        ],
                        axis=1
                    ),
                ],
                axis=1,
                sort=True
            ),
            read_usa_frb_ms(),
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, SERIES_ID),
            read_usa_prime_rate(),
        ],
        axis=1
    )


def collect_usa_investment_turnover_bls() -> DataFrame:
    SERIES_ID = 'PPIACO'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC, 1929--2021
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1929--2020
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    df = pd.concat(
        [
            # =================================================================
            # Producer Price Index
            # =================================================================
            read_usa_fred(SERIES_ID),
            pd.concat(
                [
                    read_usa_bea(url).pipe(
                        pull_by_series_id, series_id)
                    for series_id, url in SERIES_IDS.items()
                ],
                axis=1
            ),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    # =========================================================================
    # Deflator, 2012=100
    # =========================================================================
    df['deflator'] = df.iloc[:, 0].add(1).cumprod()
    df.iloc[:, -1] = df.iloc[:, -1].rdiv(df.loc[2012, df.columns[-1]])
    # =========================================================================
    # Investment, 2012=100
    # =========================================================================
    df['investment'] = df.iloc[:, 1].mul(df.iloc[:, -1])
    # =========================================================================
    # Capital, 2012=100
    # =========================================================================
    df['capital'] = df.iloc[:, 3].mul(df.iloc[:, -1])
    # =========================================================================
    # Capital Retirement Ratio
    # =========================================================================
    df['ratio_mu'] = df.iloc[:, -2].mul(1).sub(df.iloc[:, -1].shift(-1)).div(
        df.iloc[:, -1]).add(1)
    return (
        df.loc[:, ['investment', 'A191RX',
                   'capital', 'ratio_mu']].dropna(axis=0),
        df.loc[:, ['ratio_mu']].dropna(axis=0),
    )


def collect_usa_investment_turnover() -> DataFrame:
    SERIES_IDS = {
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A006RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Not Used: Fixed Assets: k3n31gd1es00, 1925--2020, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Fixed Assets: kcn31gd1es00, 1925--2020, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'kcn31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    df = pd.concat(
        [
            read_usa_bea(url).pipe(pull_by_series_id, series_id)
            for series_id, url in SERIES_IDS.items()
        ],
        axis=1,
        sort=True
    )
    # =========================================================================
    # Investment, 2012=100
    # =========================================================================
    df['_investment'] = df.loc[:, 'A006RD'].mul(
        df.loc[2012, 'A006RC']).div(100)
    # =========================================================================
    # Capital, 2012=100
    # =========================================================================
    df['_capital'] = df.loc[:, 'kcn31gd1es00'].mul(
        df.loc[2012, 'k3n31gd1es00']).mul(1000).div(100)
    # =========================================================================
    # Capital Retirement Ratio
    # =========================================================================
    df['_ratio_mu'] = df.iloc[:, -
                              2].mul(1).sub(df.iloc[:, -1].shift(-1)).div(df.iloc[:, -1]).add(1)
    return (
        df.loc[:, ['_investment', 'A191RX',
                   '_capital', '_ratio_mu']].dropna(axis=0),
        df.loc[:, ['_ratio_mu']].dropna(axis=0),
    )


def collect_usa_macroeconomics() -> DataFrame:
    """Data Fetch"""
    SERIES_ID = 'CAPUTL.B50001.A'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX, 1929--2021, 2012=100
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Deflator Gross Domestic Product, A191RD3, 1929--2021, 2012=100
        # =====================================================================
        'A191RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # National Income: A032RC, 1929--2021
        # =====================================================================
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: K10002, 1951--2021
        # =====================================================================
        'K10002': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: k1ntotl1si00, 1925--2020
        # =====================================================================
        'k1ntotl1si00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Fixed Assets Series: k3ntotl1si00, 1925--2020
        # =====================================================================
        'k3ntotl1si00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1925--2020
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Fixed Assets Series: k3n31gd1es00, 1925--2020
        # =====================================================================
        'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    return pd.concat(
        [
            pd.concat(
                [
                    (
                        read_usa_bea(url).pipe(
                            pull_by_series_id, series_id),
                        read_usa_bea(url).pipe(
                            pull_by_series_id, series_id).rdiv(100)
                    )[series_id == 'A191RD']
                    for series_id, url in SERIES_IDS.items()
                ],
                axis=1,
                sort=True
            ),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            collect_usa_bea_labor_mfg(),
            # =====================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =====================================================================
            read_usa_frb_g17().loc[:, [SERIES_ID]].dropna(axis=0),
        ],
        axis=1,
        sort=True
    )


def collect_usa_manufacturing_two_fold() -> tuple[DataFrame]:
    """
    Data Fetch Archived

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital Series
    df.iloc[:, 1]      Labor Series
    df.iloc[:, 2]      Product Series
    ================== =================================
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital Series
    df.iloc[:, 1]      Labor Series
    df.iloc[:, 2]      Product Series Adjusted to Capacity Utilisation
    ================== =================================
    """
    SERIES_ID = 'CAPUTL.B50001.A'
    SERIES_IDS = {
        # =================================================================
        # Fixed Assets: kcn31gd1es00, 1925--2020, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =================================================================
        'kcn31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    }
    df = pd.concat(
        [
            pd.concat(
                [
                    read_usa_bea(url).pipe(
                        pull_by_series_id, series_id)
                    for series_id, url in SERIES_IDS.items()
                ],
                axis=1,
                sort=True
            ),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            collect_usa_bea_labor_mfg(),
        ],
        axis=1
    ).dropna(axis=0)
    # =========================================================================
    # Below Method Is Not So Robust, But Changes the Ordering as Expected
    # =========================================================================
    df = df.reindex(columns=sorted(df.columns)[::-1])
    df_adjusted = pd.concat(
        [
            df.copy(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, [SERIES_ID]].dropna(axis=0),
        ],
        axis=1
    ).dropna(axis=0)
    df_adjusted.iloc[:, -2] = df_adjusted.iloc[:, -2].div(
        df_adjusted.iloc[:, -1]
    ).mul(100)
    return (
        df.div(df.iloc[0, :]),
        df_adjusted.div(df_adjusted.iloc[0, :]).iloc[:, range(3)]
    )


def collect_usa_manufacturing_three_fold() -> tuple[DataFrame]:
    """
    Data Fetch Revised

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital Series
    df.iloc[:, 1]      Labor Series
    df.iloc[:, 2]      Product Series
    ================== =================================
    DataFrame
    ================== =================================
    df.index           Period Truncated
    df.iloc[:, 0]      Capital Series
    df.iloc[:, 1]      Labor Series
    df.iloc[:, 2]      Product Series
    ================== =================================
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital Series
    df.iloc[:, 1]      Labor Series
    df.iloc[:, 2]      Product Series Adjusted to Capacity Utilisation
    ================== =================================
    """
    SERIES_ID, URL = 'kcn31gd1es00', 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    df = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es00, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            read_usa_bea(URL).pipe(pull_by_series_id, SERIES_ID),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            collect_usa_bea_labor_mfg(),
            # =================================================================
            # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
            # =================================================================
            read_usa_frb_us3().loc[:, ['AIPMA_SA_IX']],
        ],
        axis=1
    ).dropna(axis=0)
    SERIES_ID = 'CAPUTL.B50001.A'
    df_adjusted = pd.concat(
        [
            df.copy(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, [SERIES_ID]].dropna(axis=0),
        ],
        axis=1
    ).dropna(axis=0)
    df_adjusted.iloc[:, -2] = df_adjusted.iloc[:, -2].div(
        df_adjusted.iloc[:, -1]
    ).mul(100)
    df_truncated = df.truncate(before=df_adjusted.index[0])
    return (
        df.div(df.iloc[0, :]),
        df_truncated.div(df_truncated.iloc[0, :]),
        df_adjusted.div(df_adjusted.iloc[0, :]).iloc[:, range(3)]
    )


def collect_usa_manufacturing_latest() -> DataFrame:
    """Data Fetch"""
    # =========================================================================
    # TODO: Update Accodring to Change in collect_cobb_douglas_deflator()
    # =========================================================================
    df_capital = pd.concat(
        [
            # =================================================================
            # Data Fetch for Capital
            # =================================================================
            collect_usa_capital().pipe(transform_cobb_douglas_extension_capital),
            # =================================================================
            # Data Fetch for Capital Deflator
            # =================================================================
            collect_cobb_douglas_deflator(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    df_capital['capital_real'] = df_capital.iloc[:, 0].div(
        df_capital.iloc[:, 1])
    df = pd.concat(
        [
            df_capital.iloc[:, [-1]],
            # =================================================================
            # Data Fetch for Labor
            # =================================================================
            collect_cobb_douglas_extension_labor(),
            # =================================================================
            # Data Fetch for Product
            # =================================================================
            collect_cobb_douglas_extension_manufacturing(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    return df.div(df.iloc[0, :])


def collect_usa_mcconnel(series_ids: tuple[str]) -> DataFrame:
    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'prime_rate',
        'Валовой объем внутренних частных инвестиций, млрд долл. США': 'A006RC1',
        'Национальный доход, млрд долл. США': 'A032RC1',
        'Валовой внутренний продукт, млрд долл. США': 'A191RC1',
    }
    return pd.concat(
        [
            read_usa_hist().sort_index().pipe(pull_by_series_id, series_id).rename(
                columns={series_id: SERIES_IDS[series_id]})
            for series_id in series_ids
        ],
        axis=1
    ).truncate(before=1980)


def collect_uscb_cap_deflator() -> DataFrame:
    """Returns Census Fused Capital Deflator"""
    SERIES_IDS = {
        'P0107': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0108': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0109': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0110': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0111': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0112': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0113': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0114': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0115': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0116': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0117': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0118': ('dataset_uscb.zip', 1000, '1958=100, billions'),
    }
    _df = pd.concat(
        [
            read_usa_hist(archive_name).pipe(pull_by_series_id, series_id)
            for series_id, (archive_name, *_) in SERIES_IDS.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    ).truncate(before=1879)
    _df['total_purchases'] = _df.iloc[:, 0].div(_df.iloc[:, 3])
    _df['struc_purchases'] = _df.iloc[:, 1].div(_df.iloc[:, 4])
    _df['equip_purchases'] = _df.iloc[:, 2].div(_df.iloc[:, 5])
    _df['total_depreciat'] = _df.iloc[:, 6].div(_df.iloc[:, 9])
    _df['struc_depreciat'] = _df.iloc[:, 7].div(_df.iloc[:, 10])
    _df['equip_depreciat'] = _df.iloc[:, 8].div(_df.iloc[:, 11])
    df = pd.concat(
        [
            price_inverse_single(
                _df.iloc[:, [-(1+_)]].dropna(axis=0)).dropna(axis=0) for _ in range(6)
        ],
        axis=1
    )
    df['census_fused'] = df.mean(axis=1)
    return df.iloc[:, [-1]]


def collect_uscb_cap(smoothing: bool = False) -> DataFrame:
    """Returns Nominal Million-Dollar Capital, Including Structures & Equipment, Series"""
    SERIES_IDS = {
        'J0149': ('dataset_uscb.zip', 1, 'nominal, millions'),
        'J0150': ('dataset_uscb.zip', 1, 'nominal, millions'),
        'J0151': ('dataset_uscb.zip', 1, 'nominal, millions'),
        'P0107': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0108': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0109': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0110': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0111': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0112': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0113': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0114': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0115': ('dataset_uscb.zip', 1000, 'nominal, billions'),
        'P0116': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0117': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0118': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0119': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0120': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0121': ('dataset_uscb.zip', 1000, '1958=100, billions'),
        'P0122': ('dataset_uscb.zip', 1000, '1958=100, billions'),
    }
    df = pd.concat(
        [
            read_usa_hist(archive_name).pipe(
                pull_by_series_id, series_id).mul(factor)
            for series_id, (archive_name, factor, _) in SERIES_IDS.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    ).truncate(before=1875)
    if smoothing:
        df['total'] = wiener(
            df.loc[:, ['J0149', 'P0107']].mean(axis=1)
        ).round()
        df['struc'] = wiener(
            df.loc[:, ['J0150', 'P0108']].mean(axis=1)
        ).round()
        df['equip'] = wiener(
            df.loc[:, ['J0151', 'P0109']].mean(axis=1)
        ).round()
    else:
        df['total'] = df.loc[:, ['J0149', 'P0107']].mean(axis=1)
        df['struc'] = df.loc[:, ['J0150', 'P0108']].mean(axis=1)
        df['equip'] = df.loc[:, ['J0151', 'P0109']].mean(axis=1)
    return df.iloc[:, -3:]


def collect_uscb_employment_conflicts() -> DataFrame:
    SERIES_IDS = {
        # =====================================================================
        # Stoppages
        # =====================================================================
        'D0977': 'dataset_uscb.zip',
        # =====================================================================
        # Workers Involved
        # =====================================================================
        'D0982': 'dataset_uscb.zip',
    }
    YEAR = 1906
    df = pd.concat(
        [
            read_usa_hist(archive_name).pipe(pull_by_series_id, series_id)
            for series_id, archive_name in SERIES_IDS.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    # =========================================================================
    # Fill the Gaps
    # =========================================================================
    df = df.reindex(range(df.index[0], 1 + df.index[-1]))
    return df.fillna(
        {
            series_id: df.loc[:YEAR, series_id].mean()
            for series_id in SERIES_IDS
        }
    )


def collect_uscb_gnp() -> DataFrame:
    """Census Gross National Product Series"""
    ARCHIVE_NAME = 'dataset_uscb.zip'
    SERIES_IDS = ('F0003', 'F0004',)
    df = pd.concat(
        [
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    ).truncate(before=1889)
    return df.div(df.iloc[0, :]).mul(100)


def collect_uscb_immigration() -> DataFrame:
    """Census Total Immigration Series"""
    ARCHIVE_NAME = 'dataset_uscb.zip'
    ids = itertools.chain(
        range(91, 102),
        range(103, 110),
        range(111, 116),
        range(117, 120),
    )
    SERIES_IDS = tuple(f'C{_id:04n}' for _id in ids)
    df = pd.concat(
        [
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    df['C89'] = df.sum(1)
    return df.iloc[:, [-1]]


def collect_uscb_manufacturing() -> tuple[DataFrame, int]:
    """
    Census Manufacturing Indexes, 1899=100

    Returns
    -------
    tuple[DataFrame, int]
        DESCRIPTION.

    """
    SERIES_IDS = {
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': 'dataset_uscb.zip',
        # =====================================================================
        # HSUS 1975 Page 667, P17: Edwin Frickey Series, Indexes of Manufacturing Production
        # =====================================================================
        'P0017': 'dataset_uscb.zip',
    }
    df = pd.concat(
        [
            read_usa_hist(archive_name).pipe(pull_by_series_id, series_id)
            for series_id, archive_name in SERIES_IDS.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    return df.div(df.loc[1899, :]).mul(100), df.index.get_loc(1899)


def collect_uscb_metals() -> tuple[DataFrame, tuple[int]]:
    """Census Primary Metals & Railroad-Related Products Manufacturing Series"""
    ARCHIVE_NAME = 'dataset_uscb.zip'
    SERIES_IDS = {
        'P0262': 1875,
        'P0265': 1875,
        'P0266': 1875,
        'P0267': 1875,
        'P0268': 1875,
        'P0269': 1909,
        'P0293': 1880,
        'P0294': 1875,
        'P0295': 1875,
    }
    df = pd.concat(
        [
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    for series_id, year in SERIES_IDS.items():
        df.loc[:, series_id] = df.loc[:, [series_id]].div(
            df.loc[year, series_id]
        ).mul(100)
    return df, tuple(SERIES_IDS.values())


def collect_uscb_money_stock() -> DataFrame:
    """Census Money Supply Aggregates"""
    YEAR_BASE = 1915
    ARCHIVE_NAME = 'dataset_uscb.zip'
    SERIES_IDS = ('X0410', 'X0414', 'X0415',)
    df = pd.concat(
        [
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    return df.div(df.loc[YEAR_BASE, :]).mul(100)


def collect_uscb_trade_by_countries() -> DataFrame:
    """Census Foreign Trade Series"""
    ARCHIVE_NAME = 'dataset_uscb.zip'
    ids = itertools.chain(
        range(319, 324),
        range(325, 329),
        range(330, 335),
        range(337, 342),
        range(343, 347),
        range(348, 353),
    )
    SERIES_IDS = tuple(f'U{_id:04n}' for _id in ids)
    df = pd.concat(
        [
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )

    for _ in range(len(SERIES_IDS) // 2):
        _title = f'{df.columns[_]}_net_{df.columns[_ + len(SERIES_IDS) // 2]}'
        df[_title] = df.iloc[:, _].sub(df.iloc[:, _ + len(SERIES_IDS) // 2])

    df['exports'] = df.loc[:, SERIES_IDS[:len(SERIES_IDS) // 2]].sum(1)
    df['imports'] = df.loc[:, SERIES_IDS[len(SERIES_IDS) // 2:]].sum(1)

    for _ in range(len(SERIES_IDS) // 2):
        _title = f'{df.columns[_ + len(SERIES_IDS)]}_over_all'
        df[_title] = df.iloc[:, _ + len(SERIES_IDS)].div(
            df.loc[:, 'exports'].sub(df.loc[:, 'imports'])
        )

    return df


def collect_uscb_trade() -> DataFrame:
    """Census Foreign Trade Series"""
    ARCHIVE_NAME = 'dataset_uscb.zip'
    SERIES_IDS = ('U0001', 'U0008', 'U0015',)
    return pd.concat(
        [
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )


def collect_uscb_trade_gold_silver() -> DataFrame:
    """Census Foreign Trade Series"""
    ARCHIVE_NAME = 'dataset_uscb.zip'
    SERIES_IDS = ('U0187', 'U0188', 'U0189',)
    return pd.concat(
        [
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )


def collect_uscb_unemployment_hours_worked() -> DataFrame:
    """Census Employment Series"""
    SERIES_IDS = {
        # =====================================================================
        # Unemployment
        # =====================================================================
        'D0085': 'dataset_uscb.zip',
        'D0086': 'dataset_uscb.zip',
        # =====================================================================
        # Hours Worked
        # =====================================================================
        'D0796': 'dataset_uscb.zip',
        'D0797': 'dataset_uscb.zip',
    }
    df = pd.concat(
        [
            read_usa_hist(archive_name).pipe(pull_by_series_id, series_id)
            for series_id, archive_name in SERIES_IDS.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    df['workers'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    return df


def collect_can_price_a():
    FILE_NAME = 'stat_can_cap.xlsx'
    _df = read_can_temp(FILE_NAME)
    groups = [
        [[_, 5 + _] for _ in range(5)],
        [[_, 5 + _] for _ in range(35, 39)],
    ]
    # groups = [
    #     [[_, 10 + _] for _ in range(5)],
    #     [[_, 10 + _] for _ in range(35, 40)],
    # ]
    df = DataFrame()
    for pairs in groups:
        for pair in pairs:
            chunk = _df.iloc[:, pair].dropna(axis=0)
            chunk['deflator'] = chunk.iloc[:, 0].div(chunk.iloc[:, 1])
            chunk['prc'] = chunk.iloc[:, -1].div(
                chunk.iloc[:, -1].shift(1)).sub(1)
            df = pd.concat([df, chunk.iloc[:, [-1]].dropna(axis=0)], axis=1)
            df.plot(grid=True)
    # return df


def collect_can_price_b():
    FILE_NAME = 'stat_can_cap.xlsx'
    _df = read_can_temp(FILE_NAME)
    df = DataFrame()
    for _ in range(21, 24):
        chunk = _df.iloc[:, [_]].dropna(axis=0)
        chunk[f'{_df.columns[_]}_prc'] = chunk.iloc[:, 0].div(
            chunk.iloc[:, 0].shift(1)).sub(1)
        df = pd.concat([df, chunk.iloc[:, [1]].dropna(axis=0)], axis=1)
    return df


def construct_can(archive_ids: dict) -> DataFrame:
    """


    Parameters
    ----------
    archive_ids : dict
        DESCRIPTION.

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital
    df.iloc[:, 1]      Labor
    df.iloc[:, 2]      Product
    ================== =================================
    """
    DIR = '/media/green-machine/KINGSTON'
    kwargs = {
        'filepath_or_buffer': Path(DIR).joinpath(f'{tuple(archive_ids)[0]}_preloaded.csv'),
    }
    if Path(DIR).joinpath(f'{tuple(archive_ids)[0]}_preloaded.csv').is_file():
        kwargs['index_col'] = 0
        _df = pd.read_csv(**kwargs)
    else:
        function = (
            # =================================================================
            # WARNING : pull_can_capital() : VERY EXPENSIVE OPERATION !
            # =================================================================
            pull_can_capital,
            pull_can_capital_former
        )[max(archive_ids) < 10 ** 7]
        _df = read_can(tuple(archive_ids)[0]).pipe(
            function, archive_ids.get(tuple(archive_ids)[0]))
        # =====================================================================
        # Kludge
        # =====================================================================
        _df = _df.set_index(_df.iloc[:, 0])
    df = pd.concat(
        [
            _df.loc[:, ('series_id', 'value')].pipe(transform_sum),
            read_can(tuple(archive_ids)[1]).pipe(
                pull_by_series_id, archive_ids.get(tuple(archive_ids)[1])).pipe(numerify),
            read_can(tuple(archive_ids)[-1]).pipe(
                pull_can_aggregate,
                archive_ids.get(tuple(archive_ids)[-1])),
        ],
        axis=1
    ).dropna(axis=0)
    df.columns = ('capital', 'labor', 'product')
    return df.div(df.iloc[0, :])


def construct_cap_deflator(series_ids: dict[str]) -> DataFrame:
    df = pd.concat(
        [
            read_usa_hist(archive_name).pipe(pull_by_series_id, series_id)
            for series_id, archive_name in series_ids.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['prc'] = df.iloc[:, -1].div(df.iloc[:, -1].shift(1)).sub(1)
    return df.iloc[:, [-1]].dropna(axis=0)


def filter_data_frame(df: DataFrame, query: dict[str]) -> DataFrame:
    for column, criterion in query['filter'].items():
        df = df[df.iloc[:, column] == criterion]
    return df


def get_mean_for_min_std():
    """
    Determine Year & Mean Value for Base Vectors for Year with Minimum StandardError
    """
    FILE_NAME = 'stat_can_lab.xlsx'
    # =========================================================================
    # Base Vectors
    # =========================================================================
    SERIES_IDS = (
        'v123355112',
        'v1235071986',
        'v2057609',
        'v2057818',
        'v2523013',
    )
    _df = read_can_temp(FILE_NAME)
    df = pd.concat(
        [
            _df.loc[:, [series_id]].dropna(axis=0) for series_id in SERIES_IDS
        ],
        axis=1
    ).dropna(axis=0)
    df['std'] = df.std(axis=1)
    return (
        df.iloc[:, [-1]].idxmin()[0],
        df.loc[df.iloc[:, [-1]].idxmin()[0], :][:-1].mean()
    )


def get_price_base(df: DataFrame) -> int:
    """
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

    """
    df['__deflator'] = df.iloc[:, 0].sub(100).abs()
    return int(df.index[df.iloc[:, -1].astype(float).argmin()])
