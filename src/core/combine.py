#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 21:55:10 2023

@author: green-machine
"""


import itertools

import pandas as pd
from pandas import DataFrame
from scipy.signal import wiener
from sklearn.impute import SimpleImputer

from thesis.src.core.classes import Dataset, SeriesID
from thesis.src.core.common import get_kwargs_usa_davis_ip, get_pre_kwargs

from .backend import stockpile
from .constants import SERIES_IDS_LAB
from .read import (read_usa_frb, read_usa_frb_g17, read_usa_frb_h6,
                   read_usa_frb_us3, read_usa_fred)
from .tools import construct_usa_hist_deflator
from .transform import (transform_cobb_douglas_extension_capital,
                        transform_mean, transform_usa_frb_fa,
                        transform_usa_frb_fa_def, transform_usa_manufacturing)


def combine_cobb_douglas(series_number: int = 3) -> DataFrame:
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
    MAP = {
        'CDT2S4': 'capital',
        'CDT3S1': 'labor',
        'J0014': 'product',
        'J0013': 'product_nber',
        'DT24AS01': 'product_rev',
    }
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4': Dataset.USA_COBB_DOUGLAS,
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': Dataset.USA_COBB_DOUGLAS,
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': Dataset.USCB,
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': Dataset.USCB,
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': Dataset.DOUGLAS,
    }
    return stockpile(SERIES_IDS).rename(columns=MAP).iloc[:, range(series_number)].dropna(axis=0)


def combine_deflator_hist(SERIES_IDS_CB, SERIES_IDS_PRCH) -> DataFrame:
    """Fixed Assets Deflator, 2009=100"""
    # =========================================================================
    # TODO: Be Careful with Usage Due to Change in Behavior
    # =========================================================================
    # =========================================================================
    # Combine E0007, E0023, E0040, E0068, L0002, L0015 & P107/P110
    # =========================================================================
    # =========================================================================
    # TODO: Bureau of Labor Statistics: PPIACO
    # =========================================================================

    return pd.concat(
        [
            # =================================================================
            # Bureau of the Census
            # =================================================================
            stockpile(SERIES_IDS_CB).pct_change().truncate(
                before=1795
            ).pipe(transform_mean, name='df_uscb'),
            construct_usa_hist_deflator(SERIES_IDS_PRCH).truncate(before=1885),
            # =================================================================
            # Federal Reserve Board Data
            # =================================================================
            read_usa_frb().pipe(transform_usa_frb_fa_def).pct_change(),
        ],
        axis=1,
        sort=True
    )


def combine_cobb_douglas_extension_labor() -> DataFrame:
    """
    Manufacturing Laborers' Series Comparison
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

    YEAR_BASE = 1929
    COL_NAME = 'historical'

    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'
    # =========================================================================
    # Kendrick J.W., Productivity Trends in the United States, Table D-II, 'Persons Engaged' Column, pp. 465--466
    # =========================================================================
    SERIES_ID = [SeriesID('KTD02S02', Dataset.USA_KENDRICK)]

    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': Dataset.USA_COBB_DOUGLAS,
        # =====================================================================
        # Bureau of the Census 1949, D0069
        # =====================================================================
        'D0069': Dataset.USCB,
        # =====================================================================
        # Bureau of the Census 1975, D0130
        # =====================================================================
        'D0130': Dataset.USCB,
    } or {
        # =====================================================================
        # Bureau of the Census 1949, J0004
        # =====================================================================
        'J0004': Dataset.USCB,
        # =====================================================================
        # Bureau of the Census 1975, P0005
        # =====================================================================
        'P0005': Dataset.USCB,
        # =====================================================================
        # Bureau of the Census 1975, P0062
        # =====================================================================
        'P0062': Dataset.USCB,
    }

    df = pd.concat(
        [
            stockpile(SERIES_IDS),
            stockpile(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            pd.read_csv(**get_pre_kwargs(FILE_NAME)).iloc[:, [1]]
        ],
        axis=1
    ).pipe(transform_mean, name=COL_NAME)

    return pd.concat(
        [
            stockpile(SERIES_ID).mul(
                df.at[YEAR_BASE, COL_NAME]
            ).div(100),
            df
        ],
        axis=1
    ).pipe(transform_mean, name='labor_combined')


def combine_cobb_douglas_extension_manufacturing() -> DataFrame:
    SERIES_IDS = {
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': Dataset.USCB,
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': Dataset.USCB,
        # =====================================================================
        # Bureau of the Census, 1975, Page 667, P17: Edwin Frickey Index of Manufacturing Production
        # =====================================================================
        'P0017': Dataset.USCB,
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': Dataset.DOUGLAS,
    }
    df = pd.concat(
        [
            stockpile(SERIES_IDS),
            # =================================================================
            # Joseph H. Davis Production Index
            # =================================================================
            pd.read_excel(**get_kwargs_usa_davis_ip()),
            # =================================================================
            # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
            # =================================================================
            read_usa_frb_us3().loc[:, ['AIPMA_SA_IX']],
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


def combine_usa_capital() -> DataFrame:
    SERIES_IDS = {
        # =====================================================================
        # Annual Increase in Terms of Cost Price (1)
        # =====================================================================
        'CDT2S1': Dataset.USA_COBB_DOUGLAS,
        # =====================================================================
        # Annual Increase in Terms of 1880 dollars (3)
        # =====================================================================
        'CDT2S3': Dataset.USA_COBB_DOUGLAS,
        # =====================================================================
        # Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4': Dataset.USA_COBB_DOUGLAS,
        'P0107': Dataset.USCB,
        'P0110': Dataset.USCB,
        'P0119': Dataset.USCB,
        # =====================================================================
        # Kendrick J.W., Productivity Trends in the United States, Page 320
        # =====================================================================
        'KTA15S08': Dataset.USA_KENDRICK,
        # =====================================================================
        # Douglas P.H., Theory of Wages, Page 332
        # =====================================================================
        'DT63AS01': Dataset.DOUGLAS,
        # =====================================================================
        # 'Чистый основной капитал (в млн. долл., 1929 г.)'
        # =====================================================================
        # =====================================================================
        # 'brown_0x1': Dataset.USA_BROWN
        # =====================================================================
    }
    return pd.concat(
        [
            stockpile(SERIES_IDS),
            # =================================================================
            # FRB Data
            # =================================================================
            read_usa_frb().pipe(transform_usa_frb_fa),
        ],
        axis=1,
        sort=True
    )


def combine_usa_capital_purchases() -> DataFrame:

    SERIES_IDS = [
        'CDT2S1',
        'CDT2S3',
        'DT63AS01',
        'DT63AS02',
        'DT63AS03',
        'J0149',
        'J0150',
        'J0151',
        'P0107',
        'P0108',
        'P0109',
        'P0110',
        'P0111',
        'P0112',
        'P0113',
        'P0114',
        'P0115',
        'P0116',
        'P0117',
        'P0118',
        'P0119',
        'P0120',
        'P0121',
        'P0122'
    ]

    UNIT_A = 'nominal, millions'
    UNIT_B = '1880=100, millions'
    UNIT_C = 'nominal, billions'
    UNIT_D = '1958=100, billions'

    YEAR_BASE = 1875

    ACCESSORY = dict.fromkeys(
        SERIES_IDS[:1] + SERIES_IDS[3:8], UNIT_A
    ) | dict.fromkeys(
        SERIES_IDS[1:3], UNIT_B
    ) | dict.fromkeys(
        SERIES_IDS[8:11] + SERIES_IDS[14:17], UNIT_C
    ) | dict.fromkeys(
        SERIES_IDS[11:14] + SERIES_IDS[17:], UNIT_D
    )

    df = stockpile(
        dict.fromkeys(
            SERIES_IDS[:2], Dataset.USA_COBB_DOUGLAS
        ) | dict.fromkeys(
            SERIES_IDS[2:5], Dataset.DOUGLAS
        ) | dict.fromkeys(
            SERIES_IDS[5:], Dataset.USCB
        )
    ).mul(
        dict.fromkeys(SERIES_IDS[:8], 1) | dict.fromkeys(SERIES_IDS[8:], 1000)
    ).truncate(before=YEAR_BASE)

    df['total'] = df.loc[:, ['CDT2S1', 'J0149', 'P0107']].mean(
        axis=1).pipe(wiener).round()
    df['struc'] = df.loc[:, ['J0150', 'P0108']].mean(
        axis=1).pipe(wiener).round()
    df['equip'] = df.loc[:, ['J0151', 'P0109']].mean(
        axis=1).pipe(wiener).round()
    return df


def combine_usa_investment_turnover_bls() -> DataFrame:
    SERIES_ID = 'PPIACO'

    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC, 1929--2021
        # =====================================================================
        'A006RC': URL.NIPA,
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =====================================================================
        'A191RX': URL.NIPA,
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1929--2020
        # =====================================================================
        'k1n31gd1es00': URL.FIAS,
    }
    df = pd.concat(
        [
            # =================================================================
            # Producer Price Index
            # =================================================================
            read_usa_fred(SERIES_ID),
            stockpile(SERIES_IDS),
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


def combine_usa_investment_turnover() -> DataFrame:

    SERIES_IDS = {
        'A006RC': URL.NIPA,
        'A006RD': URL.NIPA,
        'A191RC': URL.NIPA,
        'A191RX': URL.NIPA,
        # =====================================================================
        # Not Used: Fixed Assets: k3n31gd1es00, 1925--2020, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k3n31gd1es00': URL.FIAS,
        # =====================================================================
        # Fixed Assets: kcn31gd1es00, 1925--2020, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'kcn31gd1es00': URL.FIAS,
    }
    df = stockpile(SERIES_IDS)
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


def combine_usa_manufacturing_two_fold() -> tuple[DataFrame]:
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
        'kcn31gd1es00': URL.FIAS,
        # =================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =================================================================
        'A191RX': URL.NIPA,
    }
    df = pd.concat(
        [
            stockpile(SERIES_IDS),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
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


def combine_usa_manufacturing_three_fold() -> tuple[DataFrame]:
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
        'kcn31gd1es00': URL.FIAS
    }
    df = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es00, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            stockpile(SERIES_IDS),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            # =================================================================
            # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
            # =================================================================
            read_usa_frb_us3().loc[:, ['AIPMA_SA_IX']],
        ],
        axis=1
    ).dropna(axis=0)
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


def combine_usa_manufacturing_latest() -> DataFrame:
    """Data Fetch"""
    # =========================================================================
    # TODO: Update Accodring to Change in combine_deflator_hist()
    # =========================================================================
    df_capital = pd.concat(
        [
            # =================================================================
            # Data Fetch for Capital
            # =================================================================
            combine_usa_capital().truncate(before=1869).pipe(
                transform_cobb_douglas_extension_capital
            ),
            # =================================================================
            # Data Fetch for Capital Deflator
            # =================================================================
            combine_deflator_hist().pipe(
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
            combine_cobb_douglas_extension_labor(),
            # =================================================================
            # Data Fetch for Product
            # =================================================================
            combine_cobb_douglas_extension_manufacturing(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    return df.div(df.iloc[0, :])


def combine_uscb_cap_deflator() -> DataFrame:
    """Returns Census Fused Capital Deflator"""

    SERIES_IDS_NOM = ['P0107', 'P0108', 'P0109', 'P0113', 'P0114', 'P0115']

    SERIES_IDS_REA = ['P0110', 'P0111', 'P0112', 'P0116', 'P0117', 'P0118']

    COLUMNS = [
        'total_purchases',
        'struc_purchases',
        'equip_purchases',
        'total_depreciat',
        'struc_depreciat',
        'equip_depreciat',
    ]

    YEAR_BASE = 1879

    df_num = stockpile(
        enlist_series_ids(SERIES_IDS_NOM, Dataset.USCB)
    ).set_axis(COLUMNS, axis=1)

    df_den = stockpile(
        enlist_series_ids(SERIES_IDS_REA, Dataset.USCB)
    ).set_axis(COLUMNS, axis=1)

    # =========================================================================
    # Strip Deflators
    # =========================================================================
    return df_num.div(df_den).truncate(before=YEAR_BASE).pct_change().dropna(axis=0, how='all')


def combine_uscb_cap(smoothing: bool = False) -> DataFrame:
    """Returns Nominal Million-Dollar Capital, Including Structures & Equipment, Series"""

    SERIES_IDS = [
        'J0149',
        'J0150',
        'J0151',
        'P0107',
        'P0108',
        'P0109',
        'P0110',
        'P0111',
        'P0112',
        'P0113',
        'P0114',
        'P0115',
        'P0116',
        'P0117',
        'P0118',
        'P0119',
        'P0120',
        'P0121',
        'P0122'
    ]

    UNIT_A = 'nominal, millions'
    UNIT_B = 'nominal, billions'
    UNIT_C = '1958=100, billions'

    YEAR_BASE = 1875

    ACCESSORY = dict.fromkeys(
        SERIES_IDS[:3], UNIT_A
    ) | dict.fromkeys(
        SERIES_IDS[3:6] + SERIES_IDS[9:12], UNIT_B
    ) | dict.fromkeys(
        SERIES_IDS[6:9] + SERIES_IDS[12:], UNIT_C
    )

    df = stockpile(enlist_series_ids(SERIES_IDS, Dataset.USCB)).mul(
        (
            enlist_series_ids(SERIES_IDS[:3], 1) |
            enlist_series_ids(SERIES_IDS[3:], 1000)
        ).values()
    ).truncate(before=YEAR_BASE)
    if smoothing:
        df['total'] = df.loc[:, ['J0149', 'P0107']].mean(
            axis=1).pipe(wiener).round()
        df['struc'] = df.loc[:, ['J0150', 'P0108']].mean(
            axis=1).pipe(wiener).round()
        df['equip'] = df.loc[:, ['J0151', 'P0109']].mean(
            axis=1).pipe(wiener).round()

    else:
        df['total'] = df.loc[:, ['J0149', 'P0107']].mean(axis=1)
        df['struc'] = df.loc[:, ['J0150', 'P0108']].mean(axis=1)
        df['equip'] = df.loc[:, ['J0151', 'P0109']].mean(axis=1)
    return df.iloc[:, -3:]


def combine_uscb_employment_conflicts() -> DataFrame:
    SERIES_IDS = {
        # =====================================================================
        # Stoppages
        # =====================================================================
        'D0977': Dataset.USCB,
        # =====================================================================
        # Workers Involved
        # =====================================================================
        'D0982': Dataset.USCB,
    }
    df = stockpile(SERIES_IDS)
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


def combine_uscb_metals() -> tuple[DataFrame, list[int]]:
    """Census Primary Metals & Railroad-Related Products Manufacturing Series"""

    SERIES_IDS = [
        'P0262',
        'P0265',
        'P0266',
        'P0267',
        'P0268',
        'P0269',
        'P0293',
        'P0294',
        'P0295'
    ]

    df = stockpile(enlist_series_ids(SERIES_IDS, Dataset.USCB))

    YEARS_BASE = [1875, 1875, 1875, 1875, 1875, 1909, 1880, 1875, 1875]

    for series_id, year in zip(SERIES_IDS, YEARS_BASE):
        df.loc[:, series_id] = df.loc[:, [series_id]].div(
            df.loc[year, series_id]
        )
    return df.mul(100), YEARS_BASE


def combine_uscb_trade_by_countries() -> DataFrame:
    """Census Foreign Trade Series"""

    SERIES_IDS = dict.fromkeys(
        map(
            lambda _: f'U{_:04n}', itertools.chain(
                range(319, 324),
                range(325, 329),
                range(330, 335),
                range(337, 342),
                range(343, 347),
                range(348, 353),
            )
        ),
        Dataset.USCB
    )
    df = stockpile(SERIES_IDS)

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


def combine_uscb_unemployment_hours_worked() -> DataFrame:
    """Census Employment Series"""
    SERIES_IDS = [
        # =====================================================================
        # Unemployment
        # =====================================================================
        'D0085',
        'D0086',
        # =====================================================================
        # Hours Worked
        # =====================================================================
        'D0796',
        'D0797',
    ]
    df = stockpile(enlist_series_ids(SERIES_IDS, Dataset.USCB))
    df['workers'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    return df


def combine_usa_investment_manufacturing() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Nominal National Income
        df.iloc[:, 2]      Nominal Gross Domestic Product
        df.iloc[:, 3]      Real Gross Domestic Product
        ================== =================================.

    """

    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC
        # =====================================================================
        'A006RC': URL.NIPA,
        # =====================================================================
        # Nominal National income Series: A032RC
        # =====================================================================
        'A032RC': URL.NIPA,
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        'A191RC': URL.NIPA,
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': URL.NIPA,
    }
    return stockpile(SERIES_IDS)


def combine_usa_investment() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Nominal Gross Domestic Product
        df.iloc[:, 2]      Real Gross Domestic Product
        df.iloc[:, 3]      Prime Rate
        ================== =================================.

    """
    FILE_NAME = 'dataset_usa_0025_p_r.txt'

    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC
        # =====================================================================
        'A006RC': URL.NIPA,
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        'A191RC': URL.NIPA,
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': URL.NIPA,
    }
    return pd.concat(
        [
            stockpile(SERIES_IDS),
            pd.read_csv(**get_pre_kwargs(FILE_NAME))
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)


def combine_usa_manufacturing() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Nominal Gross Domestic Product
        df.iloc[:, 2]      Real Gross Domestic Product
        ================== =================================.

    """

    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC
        # =====================================================================
        'A006RC': URL.NIPA,
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        'A191RC': URL.NIPA,
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': URL.NIPA,
    }
    return stockpile(SERIES_IDS).dropna(axis=0)


def combine_usa_money() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      M1
        ================== =================================.

    """
    SERIES_ID = [SeriesID('X0414', Dataset.USCB)]
    df = pd.concat(
        [
            read_usa_frb_h6(),
            stockpile(SERIES_ID)
        ],
        axis=1
    ).pipe(transform_mean, name="m1_fused").sort_index()
    return df.div(df.iloc[0, :])


def combine_usa_manufacturing_money() -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Nominal Gross Domestic Product
        df.iloc[:, 2]      Real Gross Domestic Product
        df.iloc[:, 3]      M1
        ================== =================================
    """
    df = pd.concat(
        [
            combine_usa_manufacturing().pipe(transform_usa_manufacturing),
            combine_usa_money()
        ],
        axis=1
    ).dropna(axis=0)
    return df.div(df.iloc[0, :])


def combine_usa_d() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Gross Domestic Investment Price Index
        df.iloc[:, 2]      Fixed Investment
        df.iloc[:, 3]      Fixed Investment Price Index
        df.iloc[:, 4]      Real Gross Domestic Product
        ================== =================================.

    """

    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC
        # =====================================================================
        'A006RC': URL.NIPA,
        # =====================================================================
        # Implicit Price Deflator Series: A006RD
        # =====================================================================
        'A006RD': URL.NIPA,
        # =====================================================================
        # Gross private domestic investment -- Nonresidential: A008RC
        # =====================================================================
        'A008RC': URL.NIPA,
        # =====================================================================
        # Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD
        # =====================================================================
        'A008RD': URL.NIPA,
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': URL.NIPA,
    }
    return stockpile(SERIES_IDS)


def combine_usa_e() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Investment
        df.iloc[:, 1]      Production
        df.iloc[:, 2]      Capital
        ================== =================================.

    """

    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC
        # =====================================================================
        'A006RC': URL.NIPA,
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        'A191RC': URL.NIPA,
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': URL.NIPA,
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00
        # =====================================================================
        'k1n31gd1es00': URL.FIAS,
    }
    return stockpile(SERIES_IDS).dropna(axis=0)


def combine_data_frames_by_columns(
    df_c: DataFrame,
    df_t: DataFrame,
    columns_to_test: list[str],
    columns_to_base: set[str] = {'Y', 'K'},
    year_base: int = 1950,
) -> DataFrame:
    """


    Parameters
    ----------
    df_c : DataFrame
        DESCRIPTION.
    df_t : DataFrame
        DESCRIPTION.
    columns_to_test : list[str]
        DESCRIPTION.
    columns_to_base : set[str], optional
        DESCRIPTION. The default is {'Y', 'K'}.
    year_base : int, optional
        DESCRIPTION. The default is 1950.

    Yields
    ------
    DataFrame
        DESCRIPTION.

    """
    for col_control, cols_test in zip(df_c.columns, columns_to_test):
        df = pd.concat(
            [
                df_c.loc[:, [col_control]],
                df_t.loc[:, cols_test],
            ],
            axis=1,
            sort=True
        ).dropna(axis=0, how='all')
        if col_control in columns_to_base:
            yield df.div(df.loc[year_base, :]).mul(100)
        else:
            yield df


def combine_usa_kurenkov() -> DataFrame:

    SERIES_IDS = {
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': URL.NIPA,
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00
        # =====================================================================
        'k1n31gd1es00': URL.FIAS,
    }
    return pd.concat(
        [
            stockpile(SERIES_IDS),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            read_usa_frb_us3().loc[:, ['AIPMA_SA_IX']],
            read_usa_frb_g17().loc[:, ['CAPUTL.B50001.A']],
        ],
        axis=1,
        sort=True
    )
