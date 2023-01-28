#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 11:52:01 2022
@author: Alexander Mikhailov
"""

import itertools
from operator import itemgetter
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from scipy.signal import wiener
from sklearn.impute import SimpleImputer

from .pull import (pull_by_series_id, pull_can_aggregate, pull_can_capital,
                   pull_can_capital_former)
from .read import (read_can, read_temporary, read_usa_bea, read_usa_davis_ip,
                   read_usa_frb, read_usa_frb_g17, read_usa_frb_h6,
                   read_usa_frb_us3, read_usa_fred, read_usa_hist)
from .tools import price_inverse_single
from .transform import (stockpile_by_series_ids,
                        transform_cobb_douglas_extension_capital,
                        transform_mean, transform_sum, transform_usa_frb_fa,
                        transform_usa_frb_fa_def)

ARCHIVE_NAMES_UTILISED = (
    'dataset_douglas.zip',
    'dataset_usa_brown.zip',
    'dataset_uscb.zip',
    'dataset_usa_cobb-douglas.zip',
    'dataset_usa_kendrick.zip',
)
FILE_NAMES_UTILISED = (
    'dataset_usa_0025_p_r.txt',
    'dataset_usa_reference_ru_kurenkov_yu_v.csv',
)
# =============================================================================
# U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
# =============================================================================
SERIES_IDS_LAB = {
    # =========================================================================
    # 1929--1948
    # =========================================================================
    'H4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =========================================================================
    # 1948--1987
    # =========================================================================
    'J4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =========================================================================
    # 1987--2000
    # =========================================================================
    'A4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =========================================================================
    # 1998--2020
    # =========================================================================
    'N4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
}


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
    # {'L0036': 'dataset_uscb.zip'} Offset With {'E0183': 'dataset_uscb.zip'}
    # {'L0038': 'dataset_uscb.zip'} Offset With {'E0184': 'dataset_uscb.zip'}
    # {'L0039': 'dataset_uscb.zip'} Offset With {'E0185': 'dataset_uscb.zip'}
    # {'E0052': 'dataset_uscb.zip'} Offset With {'L0002': 'dataset_uscb.zip'}
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
    # 'df.corr(method='kendall')'
    # 'df.corr(method='pearson')'
    # 'df.corr(method='spearman')'
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
            stockpile_usa_bea(SERIES_IDS_EA),
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
    df['fa_def_cb'] = df.loc[:, SERIES_IDS_CB[-2]
                             ].div(df.loc[:, SERIES_IDS_CB[-1]])
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
    return pd.concat(
        [
            df.loc[:, (column,)].pipe(price_inverse_single)
            for column in df.columns
        ],
        axis=1
    )


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
    FILE_NAME = "dataset_usa_reference_ru_kurenkov_yu_v.csv"
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': 'dataset_usa_cobb-douglas.zip',
        # =====================================================================
        # Bureau of the Census 1949, D0069
        # =====================================================================
        'D0069': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1949, J0004
        # =====================================================================
        'J0004': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1975, D0130
        # =====================================================================
        'D0130': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1975, P0005
        # =====================================================================
        'P0005': 'dataset_uscb.zip',
        # =====================================================================
        # Bureau of the Census 1975, P0062
        # =====================================================================
        'P0062': 'dataset_uscb.zip',
        # =====================================================================
        # Kendrick J.W., Productivity Trends in the United States, Table D-II, 'Persons Engaged' Column, pp. 465--466
        # =====================================================================
        'KTD02S02': 'dataset_usa_kendrick.zip',
    }
    df = pd.concat(
        [
            stockpile_usa_hist(SERIES_IDS),
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name="bea_labor_mfg"),
            # =================================================================
            # Kurenkov Yu.V.
            # =================================================================
            read_temporary(FILE_NAME).iloc[:, [1]],
        ],
        axis=1
    ).truncate(before=1889)
    df.iloc[:, 6] = df.iloc[:, 6].mul(
        df.loc[1899, df.columns[0]]
    ).div(df.loc[1899, df.columns[6]])
    df['labor'] = df.iloc[:, (0, 1, 3, 6, 7, 8)].mean(axis=1)
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
            stockpile_usa_hist(SERIES_IDS),
            # =================================================================
            # Joseph H. Davis Production Index
            # =================================================================
            read_usa_davis_ip(),
            # =================================================================
            # Federal Reserve, AIPMASAIX
            # =================================================================
            read_usa_frb_us3().loc[:, ('AIPMA_SA_IX',)],
        ],
        axis=1
    )
    df.iloc[:, 1] = df.iloc[:, 1].div(df.loc[1899, df.columns[1]]).mul(100)
    df.iloc[:, 4] = df.iloc[:, 4].div(df.loc[1899, df.columns[4]]).mul(100)
    df.iloc[:, 5] = df.iloc[:, 5].div(df.loc[1939, df.columns[5]]).mul(100)
    df['fused_classic'] = df.iloc[:, range(5)].mean(axis=1)
    df.iloc[:, -1] = df.iloc[:, -1].div(df.loc[1939, df.columns[-1]]).mul(100)
    df['fused'] = df.iloc[:, -2:].mean(axis=1)
    return df.iloc[:, [-1]]


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
        # =====================================================================
        # 'brown_0x1': 'dataset_usa_brown.zip'
        # =====================================================================
    }
    return pd.concat(
        [
            stockpile_usa_hist(SERIES_IDS).truncate(before=1869),
            # =================================================================
            # FRB Data
            # =================================================================
            read_usa_frb().pipe(transform_usa_frb_fa),
        ],
        axis=1,
        sort=True
    )


def collect_usa_capital_purchases() -> DataFrame:
    SERIES_IDS_EXT = {
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
    SERIES_IDS = dict(zip(
        SERIES_IDS_EXT, map(itemgetter(0), SERIES_IDS_EXT.values())
    ))
    df = stockpile_usa_hist(SERIES_IDS).mul(
        tuple(map(itemgetter(1), SERIES_IDS_EXT.values()))
    ).truncate(before=1875)
    df['total'] = wiener(
        df.loc[:, ('CDT2S1', 'J0149', 'P0107')].mean(axis=1)
    ).round()
    df['struc'] = wiener(
        df.loc[:, ('J0150', 'P0108')].mean(axis=1)
    ).round()
    df['equip'] = wiener(
        df.loc[:, ('J0151', 'P0109')].mean(axis=1)
    ).round()
    return df


def collect_usa_general() -> DataFrame:
    """
    Returns
    -------
    DataFrame
        DESCRIPTION.
    """
    FILE_NAME = "dataset_usa_0025_p_r.txt"
    SERIES_ID = {'X0414': 'dataset_uscb.zip'}
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
        # Investment in Fixed Assets and Consumer Durable Goods, Private
        # =====================================================================
        'i3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Chain-Type Quantity Indexes for Investment in Fixed Assets and Consumer Durable Goods, Private
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
                    stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                        transform_mean, name="bea_labor_mfg"),
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
            read_usa_frb_h6(),
            stockpile_usa_hist(SERIES_ID),
            read_temporary(FILE_NAME),
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
            stockpile_usa_bea(SERIES_IDS),
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
        df.loc[:, ('ratio_mu',)].dropna(axis=0),
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
    df = stockpile_usa_bea(SERIES_IDS)
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
        df.loc[:, ('_ratio_mu',)].dropna(axis=0),
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
        # Fixed Assets Series: K10070, 1951--2021
        # =====================================================================
        'K10070': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
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
                        read_usa_bea(url).pipe(pull_by_series_id, series_id),
                        read_usa_bea(url).pipe(
                            pull_by_series_id, series_id).rdiv(100)
                    )[series_id == 'A191RD']
                    for series_id, url in SERIES_IDS.items()
                ],
                axis=1,
                sort=True
            ),
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name="bea_labor_mfg"),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, (SERIES_ID,)].dropna(axis=0),
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
            stockpile_usa_bea(SERIES_IDS),
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name="bea_labor_mfg"),
        ],
        axis=1
    ).dropna(axis=0)
    # =========================================================================
    # Below Method Is Not So Robust, But Changes the Ordering as Expected: ('kcn31gd1es00', 'bea_labor_mfg', 'A191RX')
    # =========================================================================
    df = df.reindex(columns=sorted(df.columns)[::-1])
    df_adjusted = pd.concat(
        [
            df.copy(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, (SERIES_ID,)].dropna(axis=0),
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
    SERIES_ID = 'CAPUTL.B50001.A'
    SERIES_IDS = {
        'kcn31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    }
    df = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es00, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            stockpile_usa_bea(SERIES_IDS),
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name="bea_labor_mfg"),
            # =================================================================
            # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
            # =================================================================
            read_usa_frb_us3().loc[:, ('AIPMA_SA_IX',)],
        ],
        axis=1
    ).dropna(axis=0)
    df_adjusted = pd.concat(
        [
            df.copy(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, (SERIES_ID,)].dropna(axis=0),
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
            collect_cobb_douglas_deflator().pipe(
                transform_mean, name="def_mean").dropna(axis=0),
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


def collect_uscb_cap_deflator() -> DataFrame:
    """Returns Census Fused Capital Deflator"""
    SERIES_IDS_EXT = {
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
    SERIES_IDS = dict(zip(
        SERIES_IDS_EXT, map(itemgetter(0), SERIES_IDS_EXT.values())
    ))
    df = stockpile_usa_hist(SERIES_IDS).mul(
        tuple(map(itemgetter(1), SERIES_IDS_EXT.values()))
    ).truncate(before=1879)
    df['total_purchases'] = df.iloc[:, 0].div(df.iloc[:, 3])
    df['struc_purchases'] = df.iloc[:, 1].div(df.iloc[:, 4])
    df['equip_purchases'] = df.iloc[:, 2].div(df.iloc[:, 5])
    df['total_depreciat'] = df.iloc[:, 6].div(df.iloc[:, 9])
    df['struc_depreciat'] = df.iloc[:, 7].div(df.iloc[:, 10])
    df['equip_depreciat'] = df.iloc[:, 8].div(df.iloc[:, 11])
    # =========================================================================
    # Strip Deflators
    # =========================================================================
    return pd.concat(
        [
            df.iloc[:, [-(1+_)]].pipe(price_inverse_single).dropna(axis=0) for _ in range(6)
        ],
        axis=1
    )


def collect_uscb_cap(smoothing: bool = False) -> DataFrame:
    """Returns Nominal Million-Dollar Capital, Including Structures & Equipment, Series"""
    SERIES_IDS_EXT = {
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
    SERIES_IDS = dict(zip(
        SERIES_IDS_EXT, map(itemgetter(0), SERIES_IDS_EXT.values())
    ))
    df = stockpile_usa_hist(SERIES_IDS).mul(
        tuple(map(itemgetter(1), SERIES_IDS_EXT.values()))
    ).truncate(before=1875)
    if smoothing:
        df['total'] = wiener(
            df.loc[:, ('J0149', 'P0107')].mean(axis=1)
        ).round()
        df['struc'] = wiener(
            df.loc[:, ('J0150', 'P0108')].mean(axis=1)
        ).round()
        df['equip'] = wiener(
            df.loc[:, ('J0151', 'P0109')].mean(axis=1)
        ).round()
    else:
        df['total'] = df.loc[:, ('J0149', 'P0107')].mean(axis=1)
        df['struc'] = df.loc[:, ('J0150', 'P0108')].mean(axis=1)
        df['equip'] = df.loc[:, ('J0151', 'P0109')].mean(axis=1)
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
    df = stockpile_usa_hist(SERIES_IDS)
    # =========================================================================
    # Extend Period Index
    # =========================================================================
    df = df.reindex(range(df.index[0], 1 + df.index[-1]))
    # =========================================================================
    # Inpute Values
    # =========================================================================
    return DataFrame(
        data=SimpleImputer(strategy="median").fit_transform(df),
        index=df.index,
        columns=df.columns
    )


def collect_uscb_metals() -> tuple[DataFrame, tuple[int]]:
    """Census Primary Metals & Railroad-Related Products Manufacturing Series"""
    SERIES_IDS_EXT = {
        'P0262': ('dataset_uscb.zip', 1875),
        'P0265': ('dataset_uscb.zip', 1875),
        'P0266': ('dataset_uscb.zip', 1875),
        'P0267': ('dataset_uscb.zip', 1875),
        'P0268': ('dataset_uscb.zip', 1875),
        'P0269': ('dataset_uscb.zip', 1909),
        'P0293': ('dataset_uscb.zip', 1880),
        'P0294': ('dataset_uscb.zip', 1875),
        'P0295': ('dataset_uscb.zip', 1875)
    }
    SERIES_IDS = dict(zip(
        SERIES_IDS_EXT, map(itemgetter(0), SERIES_IDS_EXT.values())
    ))
    df = stockpile_usa_hist(SERIES_IDS)
    SERIES_IDS = dict(zip(
        SERIES_IDS_EXT, map(itemgetter(1), SERIES_IDS_EXT.values())
    ))
    for series_id, year in SERIES_IDS.items():
        df.loc[:, series_id] = df.loc[:, (series_id,)].div(
            df.loc[year, series_id]
        )
    return df.mul(100), tuple(map(itemgetter(1), SERIES_IDS_EXT.values()))


def collect_uscb_trade_by_countries() -> DataFrame:
    """Census Foreign Trade Series"""
    ARCHIVE_NAME = 'dataset_uscb.zip'
    SERIES_IDS = {
        f'U{_:04n}': ARCHIVE_NAME
        for _ in itertools.chain(
            range(319, 324),
            range(325, 329),
            range(330, 335),
            range(337, 342),
            range(343, 347),
            range(348, 353),
        )
    }
    df = stockpile_usa_hist(SERIES_IDS)

    for _ in range(len(SERIES_IDS) // 2):
        _title = f'{df.columns[_]}_net_{df.columns[_ + len(SERIES_IDS) // 2]}'
        df[_title] = df.iloc[:, _].sub(df.iloc[:, _ + len(SERIES_IDS) // 2])

    df['exports'] = df.loc[:, SERIES_IDS[:len(SERIES_IDS) // 2]].sum(axis=1)
    df['imports'] = df.loc[:, SERIES_IDS[len(SERIES_IDS) // 2:]].sum(axis=1)

    for _ in range(len(SERIES_IDS) // 2):
        _title = f'{df.columns[_ + len(SERIES_IDS)]}_over_all'
        df[_title] = df.iloc[:, _ + len(SERIES_IDS)].div(
            df.loc[:, 'exports'].sub(df.loc[:, 'imports'])
        )

    return df


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
    df = stockpile_usa_hist(SERIES_IDS)
    df['workers'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    return df


def collect_can_price_a():
    FILE_NAME = 'stat_can_cap.csv'
    _df = read_temporary(FILE_NAME)
    groups = [
        # =====================================================================
        # Nominal
        # =====================================================================
        [[_, 5 + _] for _ in range(5)],
        # =====================================================================
        # Real
        # =====================================================================
        [[_, 5 + _] for _ in range(35, 39)],
    ]
    # groups = [
    #     [[_, 10 + _] for _ in range(5)],
    #     [[_, 10 + _] for _ in range(35, 40)],
    # ]
    return pd.concat(
        [
            construct_deflator(_df.iloc[:, pair]) for pairs in groups for pair in pairs
        ],
        axis=1
    )


def collect_can_price_b():
    FILE_NAME = 'stat_can_cap.csv'
    _df = read_temporary(FILE_NAME)
    df = DataFrame()
    for _ in range(21, 24):
        chunk = _df.iloc[:, [_]].dropna(axis=0)
        chunk[f'{_df.columns[_]}_prc'] = chunk.iloc[:, 0].pct_change()
        df = pd.concat([df, chunk.iloc[:, [1]].dropna(axis=0)], axis=1)
    return df


def stockpile_cobb_douglas(series_number: int = 3) -> DataFrame:
    """
    Original Cobb--Douglas Data Collection Extension
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
    SERIES_IDS_EXT = {
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
    SERIES_IDS = dict(zip(
        SERIES_IDS_EXT, map(itemgetter(0), SERIES_IDS_EXT.values())
    ))
    df = stockpile_usa_hist(SERIES_IDS)
    df.columns = map(itemgetter(1), SERIES_IDS_EXT.values())
    return df.iloc[:, range(series_number)].dropna(axis=0)


def stockpile_usa_bea(series_ids: dict[str, str]) -> DataFrame:
    """


    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================

    """
    return pd.concat(
        [
            read_usa_bea(url).pipe(pull_by_series_id, series_id)
            for series_id, url in series_ids.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )


def stockpile_usa_hist(series_ids: dict[str, str]) -> DataFrame:
    """


    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================

    """
    return pd.concat(
        [
            read_usa_hist(archive_name).sort_index().pipe(
                pull_by_series_id, series_id
            )
            for series_id, archive_name in series_ids.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )


def stockpile_usa_mcconnel(
    series_ids: tuple[str], archive_name: str = 'dataset_usa_mc_connell_brue.zip'
) -> DataFrame:
    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'prime_rate',
        'Валовой объем внутренних частных инвестиций, млрд долл. США': 'A006RC1',
        'Национальный доход, млрд долл. США': 'A032RC1',
        'Валовой внутренний продукт, млрд долл. США': 'A191RC1',
    }
    return pd.concat(
        [
            read_usa_hist(archive_name).sort_index().pipe(pull_by_series_id, series_id).rename(
                columns={series_id: SERIES_IDS[series_id]})
            for series_id in series_ids
        ],
        axis=1
    ).truncate(before=1980)


def stockpile_usa_sahr_infcf(df: DataFrame) -> DataFrame:
    """
    Retrieves Yearly Price Rates from 'dataset_usa_infcf16652007.zip'

    Returns
    -------
    DataFrame
    """
    # =========================================================================
    # Retrieve First 14 Series
    # =========================================================================
    return pd.concat(
        [
            df.pipe(pull_by_series_id, series_id).rdiv(
                1).pipe(price_inverse_single).mul(-1)
            for series_id in df.iloc[:, 0].unique()[:14]
        ],
        axis=1,
        sort=True
    )


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
            _df.loc[:, ('series_id', 'value')].pipe(
                stockpile_by_series_ids).pipe(transform_sum, name="capital"),
            read_can(tuple(archive_ids)[1]).pipe(
                pull_by_series_id, archive_ids.get(tuple(archive_ids)[1])).apply(pd.to_numeric, errors='coerce'),
            read_can(tuple(archive_ids)[-1]).pipe(
                pull_can_aggregate,
                archive_ids.get(tuple(archive_ids)[-1])),
        ],
        axis=1
    ).dropna(axis=0)
    df.columns = ('capital', 'labor', 'product')
    return df.div(df.iloc[0, :])


def construct_deflator(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal
        df.iloc[:, 1]      Real
        ================== =================================

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator PRC
        ================== =================================
    """
    assert df.shape[1] == 2
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['prc'] = df.iloc[:, -1].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)


def filter_datdf_a(df: DataFrame, query: dict[str]) -> DataFrame:
    for column, criterion in query['filter'].items():
        df = df[df.iloc[:, column] == criterion]
    return df


def get_mean_for_min_std():
    """
    Determine Year & Mean Value for Base Vectors for Year with Minimum StandardError
    """
    FILE_NAME = 'stat_can_lab.csv'
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
    _df = read_temporary(FILE_NAME)
    df = pd.concat(
        [
            _df.loc[:, (series_id,)].dropna(axis=0) for series_id in SERIES_IDS
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


def get_price_base_nr(df: DataFrame, columns: tuple[int] = (0, 1)) -> int:
    """
    Determine Base Year

    Parameters
    ----------
    df : DataFrame
        ======================== ===========================
        df.index                 Period
        ...                      ...
        df.iloc[:, columns[0]]   Nominal
        df.iloc[:, columns[-1]]  Real
        ======================== ===========================
    columns : tuple[int], optional
        Column Nominal, Column Real. The default is (0, 1).

    Returns
    -------
    int
        Base Year.

    """
    df['__deflator'] = df.iloc[:, columns[0]].div(
        df.iloc[:, columns[-1]]
    ).sub(1).abs()
    # =========================================================================
    # Basic Year
    # =========================================================================
    return int(df.index[df.iloc[:, -1].astype(float).argmin()])
