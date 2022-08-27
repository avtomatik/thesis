#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 11:52:01 2022

@author: alexander
"""

import itertools
import numpy as np
import pandas as pd
from patlib import Path
from pandas import DataFrame
from scipy import signal
# from sklearn.linear_model import Lasso
# from sklearn.linear_model import LassoCV
from sklearn.linear_model import LinearRegression
# from sklearn.linear_model import Ridge
from extract.lib import numerify
from extract.lib import pull_can_capital
from extract.lib import pull_can_capital_former
from extract.lib import pull_can_quarter
from extract.lib import pull_can_quarter_former
from extract.lib import pull_by_series_id
from extract.lib import read_from_url_usa_bea
from extract.lib import read_manager_can
from extract.lib import read_manager_can_former
from extract.lib import read_pull_usa_frb_cu
from extract.lib import read_pull_usa_frb_ms
from extract.lib import read_pull_usa_fred
from extract.lib import read_pull_usa_hist
from extract.lib import read_pull_usa_mcconnel
from toolkit.lib import price_inverse_single
from toolkit.lib import strip_cumulated_deflator


ARCHIVE_NAMES_UTILISED = (
    'dataset_douglas.zip',
    'dataset_usa_brown.zip',
    'dataset_usa_census1949.zip',
    'dataset_usa_census1975.zip',
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
URLS_UTILISED = (
    'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    'https://www.federalreserve.gov/datadownload/Output.aspx?rel=g17&filetype=zip',
)


def construct_can():
    DIR = '/home/alexander/science'
    ARCHIVE_IDS = {
        # =====================================================================
        # Capital
        # =====================================================================
        36100096: (
            2012,
            "Manufacturing",
            "Linear end-year net stock",
            (
                "Non-residential buildings",
                "Engineering construction",
                "Machinery and equipment"
            )
        ),
        # =====================================================================
        # Labor : "v2523012", Preferred Over "v3437501" Which Is Quarterly
        # =====================================================================
        14100027: 'v2523012',
        # =====================================================================
        # Production
        # =====================================================================
        36100434: 'v65201809',
    }
    if Path(DIR).joinpath(f'{tuple(ARCHIVE_IDS)[0]}_preloaded.csv').is_file():
        _df = pd.read_csv(
            Path(DIR).joinpath(f'{tuple(ARCHIVE_IDS)[0]}_preloaded.csv'),
            index_col=0
        )
    else:
        _df = read_manager_can(tuple(ARCHIVE_IDS)[0])
        # =====================================================================
        # WARNING : VERY EXPENSIVE OPERATION !
        # =====================================================================
        _df = pull_can_capital(_df, ARCHIVE_IDS.get(tuple(ARCHIVE_IDS)[0]))
        # =====================================================================
        # Kludge
        # =====================================================================
        _df = _df.set_index(_df.iloc[:, 0]).loc[:, _df.columns[1:]]
    df = pd.concat(
        [
            transform_sum(_df.loc[:, ('series_id', 'value')]),
            numerify(
                pull_by_series_id(
                    read_manager_can(
                        tuple(ARCHIVE_IDS)[1]),
                    ARCHIVE_IDS.get(tuple(ARCHIVE_IDS)[1])
                )
            ),
            pull_can_quarter(
                read_manager_can(tuple(ARCHIVE_IDS)[-1]),
                ARCHIVE_IDS.get(tuple(ARCHIVE_IDS)[-1])
            )
        ],
        axis=1
    ).dropna(axis=0)
    df.columns = ('capital', 'labor', 'product')
    return df.div(df.iloc[0, :])


def construct_can_former():
    ARCHIVE_IDS = {
        # =====================================================================
        # Capital
        # =====================================================================
        310004: (2007, "Geometric (infinite) end-year net stock", "industrial"),
        # =====================================================================
        # Labor : "v2523012", Preferred Over "v3437501" Which Is Quarterly
        # =====================================================================
        2820012: 'v2523012',
        # =====================================================================
        # Production
        # =====================================================================
        3790031: 'v65201809',
    }
    _df = read_manager_can_former(tuple(ARCHIVE_IDS)[0])
    _df = pull_can_capital_former(_df, ARCHIVE_IDS.get(tuple(ARCHIVE_IDS)[0]))
    # =========================================================================
    # Kludge
    # =========================================================================
    _df = _df.set_index(_df.iloc[:, 0]).loc[:, _df.columns[1:]]
    df = pd.concat(
        [
            transform_sum(_df.loc[:, ('series_id', 'value')]),
            numerify(
                pull_by_series_id(
                    read_manager_can_former(
                        tuple(ARCHIVE_IDS)[1]),
                    ARCHIVE_IDS.get(tuple(ARCHIVE_IDS)[1])
                )
            ),
            pull_can_quarter_former(
                read_manager_can_former(tuple(ARCHIVE_IDS)[-1]),
                ARCHIVE_IDS.get(tuple(ARCHIVE_IDS)[-1])
            ),
        ],
        axis=1
    ).dropna(axis=0)
    df.columns = ('capital', 'labor', 'product')
    return df.div(df.iloc[0, :])


def collect_can_price_a():
    DIR = '/home/alexander/science'
    FILE_NAME = 'stat_can_cap.xlsx'
    _df = pd.read_excel(Path(DIR).joinpath(FILE_NAME), index_col=0)
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
            chunk['prc'] = chunk.iloc[:, 2].div(
                chunk.iloc[:, 2].shift(1)).sub(1)
            df = pd.concat([df, chunk.iloc[:, [3]].dropna(axis=0)], axis=1)
            df.plot(grid=True)
    # return df


def collect_can_price_b():
    DIR = '/home/alexander/science'
    FILE_NAME = 'stat_can_cap.xlsx'
    _df = pd.read_excel(Path(DIR).joinpath(FILE_NAME), index_col=0)
    df = DataFrame()
    for _ in range(21, 24):
        chunk = _df.iloc[:, [_]].dropna(axis=0)
        chunk[f'{_df.columns[_]}_prc'] = chunk.iloc[:, 0].div(
            chunk.iloc[:, 0].shift(1)).sub(1)
        df = pd.concat([df, chunk.iloc[:, [1]].dropna(axis=0)], axis=1)
    return df


def collect_archived() -> DataFrame:
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
    _df = pd.concat(
        [
            # =================================================================
            # Producer Price Index
            # =================================================================
            read_pull_usa_fred(SERIES_ID),
            pd.concat(
                [
                    pull_by_series_id(read_from_url_usa_bea(url), series_id)
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
    _df['deflator'] = _df.iloc[:, 0].add(1).cumprod()
    _df.iloc[:, -1] = _df.iloc[:, -1].rdiv(_df.loc[2012, _df.columns[-1]])
    # =========================================================================
    # Investment, 2012=100
    # =========================================================================
    _df['investment'] = _df.iloc[:, 1].mul(_df.iloc[:, -1])
    # =========================================================================
    # Capital, 2012=100
    # =========================================================================
    _df['capital'] = _df.iloc[:, 3].mul(_df.iloc[:, -1])
    # =========================================================================
    # Capital Retirement Ratio
    # =========================================================================
    _df['ratio_mu'] = _df.iloc[:, -2].mul(1).sub(_df.iloc[:, -1].shift(-1)).div(
        _df.iloc[:, -1]).add(1)
    return (
        _df.loc[:, ['investment', 'A191RX',
                    'capital', 'ratio_mu']].dropna(axis=0),
        _df.loc[:, ['ratio_mu']].dropna(axis=0),
    )


def collect_bea_def() -> DataFrame:
    '''
    USA BEA Gross Domestic Product Deflator: Cumulative Price Index

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Gross Domestic Product Deflator
    ================== =================================

    '''
    _df = collect_bea_gdp()
    _df['deflator_gdp'] = _df.iloc[:, 0].div(_df.iloc[:, 1]).mul(100)
    return _df.iloc[:, [-1]]


def collect_bea_gdp() -> DataFrame:
    '''
    USA BEA Gross Domestic Product

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Nominal
    df.iloc[:, 1]      Real
    ================== =================================
    '''
    SERIES_IDS = {
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX1
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    }
    return pd.concat(
        [
            pull_by_series_id(read_from_url_usa_bea(url), series_id)
            for series_id, url in SERIES_IDS.items()
        ],
        axis=1
    )


def collect_brown() -> DataFrame:
    # =========================================================================
    # Fetch Data from `Reference RU Brown M. 0597_088.pdf`, Page 193
    # Dependent on `read_pull_usa_hist`
    # Out of Kendrick J.W. Data & Table 2. of `Reference RU Brown M. 0597_088.pdf`
    # =========================================================================
    # =========================================================================
    # FN:Murray Brown
    # ORG:University at Buffalo;Economics
    # TITLE:Professor Emeritus, Retired
    # EMAIL;PREF;INTERNET:mbrown@buffalo.edu
    # =========================================================================
    ARCHIVE_NAMES = ('dataset_usa_brown.zip', 'dataset_usa_kendrick.zip',)
    kwargs = {
        'filepath_or_buffer': ARCHIVE_NAMES[0],
        'skiprows': 4,
        'usecols': (3,)
    }
    _series_ids = pd.read_csv(**kwargs).stack().values
    SERIES_IDS = {
        col: f'series_{hex(_)}' for _, col in enumerate(sorted(set(_series_ids)))
    }
    _b_frame = pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAMES[0], series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
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
            read_pull_usa_hist(ARCHIVE_NAMES[1], series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
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


def collect_capital_combined_archived() -> DataFrame:
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC, 1929--2021
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX, 1929--2021
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1925--2020
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    return pd.concat(
        [
            pd.concat(
                [
                    pull_by_series_id(read_from_url_usa_bea(url), series_id)
                    for series_id, url in SERIES_IDS.items()
                ],
                axis=1,
                sort=True
            ),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_pull_usa_frb_cu(),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            collect_usa_bea_labor_mfg(),
            # =================================================================
            # For Overall Labor Series, See: A4601C0, 1929--2020
            # =================================================================
            collect_usa_bea_labor_mfg()
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)


def collect_capital_purchases() -> DataFrame:
    SERIES_IDS = {
        'CDT2S1': ('dataset_usa_cobb-douglas.zip', 1, 'nominal, millions'),
        'CDT2S3': ('dataset_usa_cobb-douglas.zip', 1, '1880=100, millions'),
        'DT63AS01': ('dataset_douglas.zip', 1, '1880=100, millions'),
        'DT63AS02': ('dataset_douglas.zip', 1, 'DO_NOT_USE_nominal, millions'),
        'DT63AS03': ('dataset_douglas.zip', 1, 'DO_NOT_USE_nominal, millions'),
        'J0149': ('dataset_usa_census1949.zip', 1, 'nominal, millions',),
        'J0150': ('dataset_usa_census1949.zip', 1, 'nominal, millions',),
        'J0151': ('dataset_usa_census1949.zip', 1, 'nominal, millions',),
        'P0107': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0108': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0109': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0110': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0111': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0112': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0113': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0114': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0115': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0116': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0117': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0118': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0119': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0120': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0121': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0122': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
    }
    df = pd.concat(
        [
            read_pull_usa_hist(archive_name, series_id).mul(factor)
            for series_id, (archive_name, factor, _) in SERIES_IDS.items()
        ],
        axis=1,
        sort=True
    ).truncate(before=1875)
    df['total'] = signal.wiener(
        df.loc[:, ['CDT2S1', 'J0149', 'P0107']].mean(axis=1)
    ).round()
    df['struc'] = signal.wiener(
        df.loc[:, ['J0150', 'P0108']].mean(axis=1)
    ).round()
    df['equip'] = signal.wiener(
        df.loc[:, ['J0151', 'P0109']].mean(axis=1)
    ).round()
    return df


def collect_uscb_production() -> tuple[DataFrame, int]:
    '''
    Census Manufacturing Indexes, 1899=100

    Returns
    -------
    tuple[DataFrame, int]
        DESCRIPTION.

    '''
    SERIES_IDS = {
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': 'dataset_usa_census1949.zip',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': 'dataset_usa_census1949.zip',
        # =====================================================================
        # HSUS 1975 Page 667, P17: Edwin Frickey Series, Indexes of Manufacturing Production
        # =====================================================================
        'P0017': 'dataset_usa_census1975.zip',
    }
    df = pd.concat(
        [
            read_pull_usa_hist(archive_name, series_id)
            for series_id, archive_name in SERIES_IDS.items()
        ],
        axis=1
    )
    return df.div(df.loc[1899, :]).mul(100), df.index.get_loc(1899)


def collect_uscb_cap(smoothing: bool = False) -> DataFrame:
    '''Returns Nominal Million-Dollar Capital, Including Structures & Equipment, Series'''
    SERIES_IDS = {
        'J0149': ('dataset_usa_census1949.zip', 1, 'nominal, millions',),
        'J0150': ('dataset_usa_census1949.zip', 1, 'nominal, millions',),
        'J0151': ('dataset_usa_census1949.zip', 1, 'nominal, millions',),
        'P0107': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0108': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0109': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0110': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0111': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0112': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0113': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0114': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0115': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0116': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0117': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0118': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0119': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0120': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0121': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0122': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
    }
    df = pd.concat(
        [
            read_pull_usa_hist(archive_name, series_id).mul(factor)
            for series_id, (archive_name, factor, _) in SERIES_IDS.items()
        ],
        axis=1,
        sort=True
    ).truncate(before=1875)
    if smoothing:
        df['total'] = signal.wiener(
            df.loc[:, ['J0149', 'P0107']].mean(axis=1)
        ).round()
        df['struc'] = signal.wiener(
            df.loc[:, ['J0150', 'P0108']].mean(axis=1)
        ).round()
        df['equip'] = signal.wiener(
            df.loc[:, ['J0151', 'P0109']].mean(axis=1)
        ).round()
    else:
        df['total'] = df.loc[:, ['J0149', 'P0107']].mean(axis=1)
        df['struc'] = df.loc[:, ['J0150', 'P0108']].mean(axis=1)
        df['equip'] = df.loc[:, ['J0151', 'P0109']].mean(axis=1)
    return df.iloc[:, -3:]


def collect_uscb_cap_deflator() -> DataFrame:
    '''Returns Census Fused Capital Deflator'''
    SERIES_IDS = {
        'P0107': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0108': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0109': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0110': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0111': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0112': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0113': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0114': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0115': ('dataset_usa_census1975.zip', 1000, 'nominal, billions',),
        'P0116': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0117': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
        'P0118': ('dataset_usa_census1975.zip', 1000, '1958=100, billions',),
    }
    _df = pd.concat(
        [
            read_pull_usa_hist(archive_name, series_id)
            for series_id, (archive_name, *_) in SERIES_IDS.items()
        ],
        axis=1,
        sort=True
    ).truncate(before=1879)
    _df['purchases_total'] = _df.iloc[:, 0].div(_df.iloc[:, 3])
    _df['purchases_struc'] = _df.iloc[:, 1].div(_df.iloc[:, 4])
    _df['purchases_equip'] = _df.iloc[:, 2].div(_df.iloc[:, 5])
    _df['depreciat_total'] = _df.iloc[:, 6].div(_df.iloc[:, 9])
    _df['depreciat_struc'] = _df.iloc[:, 7].div(_df.iloc[:, 10])
    _df['depreciat_equip'] = _df.iloc[:, 8].div(_df.iloc[:, 11])
    df = pd.concat(
        [
            price_inverse_single(
                _df.iloc[:, [-(1+_)]].dropna(axis=0)).dropna(axis=0) for _ in range(6)
        ],
        axis=1
    )
    df['census_fused'] = df.mean(axis=1)
    return df.iloc[:, [-1]]


def collect_uscb_metals() -> tuple[DataFrame, tuple[int]]:
    '''Census Primary Metals & Railroad-Related Products Manufacturing Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
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
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1
    )
    for series_id, year in SERIES_IDS.items():
        df.loc[:, series_id] = df.loc[:, [series_id]].div(
            df.loc[year, series_id]
        ).mul(100)
    return df, tuple(SERIES_IDS.values())


def collect_uscb_immigration() -> DataFrame:
    '''Census Total Immigration Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    ids = itertools.chain(
        range(91, 102),
        range(103, 110),
        range(111, 116),
        range(117, 120),
    )
    SERIES_IDS = tuple(f'C{_id:04n}' for _id in ids)
    df = pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    df['C89'] = df.sum(1)
    return df.iloc[:, [-1]]


def collect_uscb_employment() -> DataFrame:
    '''Census Employment Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        # =====================================================================
        # Unemployment
        # =====================================================================
        'D0085', 'D0086',
        # =====================================================================
        # Hours Worked
        # =====================================================================
        'D0796', 'D0797',
        # =====================================================================
        # Stoppages & Workers Involved
        # =====================================================================
        'D0977', 'D0982',
    )
    df = pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    df['workers'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    df.loc[:, SERIES_IDS[-2:]] = df.loc[:, SERIES_IDS[-2:]].fillna(
        {
            series_id: df.loc[:1906, series_id].mean()
            for series_id in SERIES_IDS[-2:]
        }
    )
    return df


def collect_uscb_gnp() -> DataFrame:
    '''Census Gross National Product Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('F0003', 'F0004',)
    df = pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    ).truncate(before=1889)
    return df.div(df.iloc[0, :]).mul(100)


def collect_uscb_trade() -> DataFrame:
    '''Census Foreign Trade Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('U0001', 'U0008', 'U0015',)
    return pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )


def collect_uscb_trade_gold_silver() -> DataFrame:
    '''Census Foreign Trade Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('U0187', 'U0188', 'U0189',)
    return pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )


def collect_uscb_trade_by_countries() -> DataFrame:
    '''Census Foreign Trade Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
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
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
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


def collect_uscb_money_stock() -> DataFrame:
    '''Census Money Supply Aggregates'''
    YEAR_BASE = 1915
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('X0410', 'X0414', 'X0415',)
    df = pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    return df.div(df.loc[YEAR_BASE, :]).mul(100)


def collect_uscb_cap_prices() -> DataFrame:
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = ('P0107', 'P0110')
    df = pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1
    )
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['prc'] = df.iloc[:, -1].div(df.iloc[:, -1].shift(1)).sub(1)
    return df.iloc[:, [-1]].dropna(axis=0)


def collect_cobb_douglas_deflator() -> DataFrame:
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
    # `df.corr(method='kendall')`
    # `df.corr(method='pearson')`
    # `df.corr(method='spearman')`
    # Correlation Test Result: kendall & pearson & spearman: L2, L15, E7, E23, E40, E68
    # =========================================================================
    SERIES_IDS_CS = {
        'L0002': ('dataset_usa_census1949.zip', None),
        'L0015': ('dataset_usa_census1949.zip', None),
        'E0007': ('dataset_usa_census1975.zip', None),
        'E0023': ('dataset_usa_census1975.zip', None),
        'E0040': ('dataset_usa_census1975.zip', None),
        'E0068': ('dataset_usa_census1975.zip', None),
        'P0107': ('dataset_usa_census1975.zip', 1885),
        'P0110': ('dataset_usa_census1975.zip', 1885),
    }
    # =========================================================================
    # Bureau of Economic Analysis
    # =========================================================================
    URL = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    SERIES_IDS_BE = (
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
    # =========================================================================
    # Bureau of Economic Analysis
    # =========================================================================
    _df_sfat = read_from_url_usa_bea(URL)
    df = pd.concat(
        [
            # =================================================================
            # Bureau of the Census
            # =================================================================
            pd.concat(
                [
                    read_pull_usa_hist(
                        archive_name, series_id).truncate(before=year)
                    for series_id, (archive_name, year) in SERIES_IDS_CS.items()
                ],
                axis=1,
                sort=True
            ),
            # =================================================================
            # Bureau of Economic Analysis
            # =================================================================
            pd.concat(
                [
                    pull_by_series_id(_df_sfat, series_id)
                    for series_id in SERIES_IDS_BE[:2]
                ],
                axis=1,
                sort=True
            ),
            # =================================================================
            # Federal Reserve Board Data
            # =================================================================
            collect_usa_frb_fa_def(),
        ],
        axis=1,
        sort=True
    ).truncate(before=1794)
    SERIES_IDS_CS = tuple(SERIES_IDS_CS)
    df['fa_def_cs'] = df.loc[:, SERIES_IDS_CS[-2]].div(
        df.loc[:, SERIES_IDS_CS[-1]])
    df['ppi_bea'] = df.loc[:, SERIES_IDS_BE[0]].div(
        df.loc[:, SERIES_IDS_BE[1]]).div(df.loc[2012, SERIES_IDS_BE[0]]).mul(100)
    df.drop(
        [*SERIES_IDS_CS[-2:], *SERIES_IDS_BE[:2]],
        axis=1,
        inplace=True
    )
    # =========================================================================
    # Strip Deflators
    # =========================================================================
    result = pd.concat(
        [
            strip_cumulated_deflator(df.iloc[:, [_]])
            for _ in range(df.shape[1])
        ],
        axis=1
    )
    result['def_mean'] = result.mean(axis=1)
    return result.iloc[:, [-1]].dropna(axis=0)


def collect_cobb_douglas_extension_capital() -> DataFrame:
    # =========================================================================
    # Existing Capital Dataset
    # =========================================================================
    df = collect_usa_capital()
    # =========================================================================
    # Convert Capital Series into Current (Historical) Prices
    # =========================================================================
    df['nominal_cbb_dg'] = df.iloc[:, 0].mul(
        df.iloc[:, 2]).div(df.iloc[:, 1]).div(1000)
    df['nominal_census'] = df.iloc[:, 3].mul(df.iloc[:, 5]).div(df.iloc[:, 4])
    df['nominal_dougls'] = df.iloc[:, 0].mul(
        df.iloc[:, 7]).div(df.iloc[:, 1]).div(1000)
    df['nominal_kndrck'] = df.iloc[:, 3].mul(
        df.iloc[:, 6]).div(df.iloc[:, 4]).div(1000)
    df.iloc[:, -1] = df.iloc[:, -1].mul(
        df.loc[1929, df.columns[4]]).div(df.loc[1929, df.columns[3]])
    # =========================================================================
    # Douglas P.H. -- Kendrick J.W. (Blended) Series
    # =========================================================================
    df['nominal_doug_kndrck'] = df.iloc[:, -2:].mean(axis=1)
    # =========================================================================
    # Cobb C.W., Douglas P.H. -- FRB (Blended) Series
    # =========================================================================
    df['nominal_cbb_dg_frb'] = df.iloc[:, [8, -5]].mean(axis=1)
    # =========================================================================
    # Capital Structure Series: `Cobb C.W., Douglas P.H. -- FRB (Blended) Series` to `Douglas P.H. -- Kendrick J.W. (Blended) Series`
    # =========================================================================
    df['struct_ratio'] = df.iloc[:, -1].div(df.iloc[:, -2])
    # =========================================================================
    # Filling the Gaps within Capital Structure Series
    # =========================================================================
    df.loc[1899:, df.columns[-1]].fillna(0.275, inplace=True)
    df.loc[:, df.columns[-1]].fillna(
        df.loc[1899, df.columns[-1]], inplace=True
    )
    # =========================================================================
    # Patch Series `Douglas P.H. -- Kendrick J.W. (Blended) Series` Multiplied by `Capital Structure Series`
    # =========================================================================
    df['nominal_patch'] = df.iloc[:, -3].mul(df.iloc[:, -1])
    # =========================================================================
    # `Cobb C.W., Douglas P.H. -- FRB (Blended) Series` Patched with `Patch Series`
    # =========================================================================
    df['nominal_extended'] = df.iloc[:, -3::2].mean(axis=1)
    # =========================================================================
    # Adjustment of Nominalized Census P119 to Retrieved Results
    # =========================================================================
    df.iloc[:, -8] = df.iloc[:, -8].mul(
        df.loc[1925, df.columns[-1]]
    ).div(df.loc[1925, df.columns[-8]])
    # =========================================================================
    # Blending Previous Series with 'nominal_extended'
    # =========================================================================
    df.iloc[:, -1] = df.iloc[:, [-8, -1]].mean(axis=1)
    return df.iloc[:, [-1]].dropna(axis=0)


def collect_cobb_douglas_extension_labor() -> DataFrame:
    '''
    Manufacturing Laborers` Series Comparison

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Labor Series
    ================== =================================
    '''
    # =========================================================================
    # TODO: Bureau of Labor Statistics
    # TODO: Federal Reserve Board
    # =========================================================================
    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': 'dataset_usa_cobb-douglas.zip',
        # =====================================================================
        # Census Bureau 1949, D69
        # =====================================================================
        'D0069': 'dataset_usa_census1949.zip',
        # =====================================================================
        # Census Bureau 1949, J4
        # =====================================================================
        'J0004': 'dataset_usa_census1949.zip',
        # =====================================================================
        # Census Bureau 1975, D130
        # =====================================================================
        'D0130': 'dataset_usa_census1975.zip',
        # =====================================================================
        # Census Bureau 1975, P5
        # =====================================================================
        'P0005': 'dataset_usa_census1975.zip',
        # =====================================================================
        # Census Bureau 1975, P62
        # =====================================================================
        'P0062': 'dataset_usa_census1975.zip',
        # =====================================================================
        # J.W. Kendrick, Productivity Trends in the United States, Table D-II, `Persons Engaged` Column, pp. 465--466
        # =====================================================================
        'KTD02S02': 'dataset_usa_kendrick.zip',
    }
    _df = pd.concat(
        [
            pd.concat(
                [
                    read_pull_usa_hist(archive_name, series_id)
                    for series_id, archive_name in SERIES_IDS.items()
                ],
                axis=1
            ),
            # =========================================================================
            # Bureau of Economic Analysis, H4313C & J4313C & A4313C & N4313C
            # =========================================================================
            collect_usa_bea_labor_mfg(),
            # =================================================================
            # Yu.V. Kurenkov
            # =================================================================
            pd.read_csv(FILE_NAME, index_col=0, usecols=[0, 2]),
        ],
        axis=1
    ).truncate(before=1889)
    _df.iloc[:, 6] = _df.iloc[:, 6].mul(
        _df.loc[1899, _df.columns[0]]
    ).div(_df.loc[1899, _df.columns[6]])
    _df['labor'] = _df.iloc[:, [0, 1, 3, 6, 7, 8]].mean(axis=1)
    return _df.iloc[:, [-1]]


def collect_cobb_douglas_extension_product() -> DataFrame:
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_davis-j-h-ip-total.xls',
        'header': None,
        'names': ('period', 'davis_index'),
        'index_col': 0,
        'skiprows': 5
    }
    SERIES_IDS = {
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': 'dataset_usa_census1949.zip',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': 'dataset_usa_census1949.zip',
        # =====================================================================
        # Bureau of the Census, 1975, Page 667, P17: Edwin Frickey Index of Manufacturing Production
        # =====================================================================
        'P0017': 'dataset_usa_census1975.zip',
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': 'dataset_douglas.zip',
    }
    df = pd.concat(
        [
            pd.concat(
                [
                    read_pull_usa_hist(archive_name, series_id)
                    for series_id, archive_name in SERIES_IDS.items()
                ],
                axis=1
            ),
            # =================================================================
            # Joseph H. Davis Production Index
            # =================================================================
            pd.read_excel(**kwargs),
            # =================================================================
            # Federal Reserve, AIPMASAIX
            # =================================================================
            collect_usa_frb_ip(),
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


def collect_cobb_douglas_price() -> DataFrame:
    ARCHIVE_NAME = 'dataset_usa_cobb-douglas.zip'
    SERIES_IDS = ('CDT2S1', 'CDT2S3')
    df = pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1
    )
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['prc'] = df.iloc[:, -1].div(df.iloc[:, -1].shift(1)).sub(1)
    return df.iloc[:, [-1]].dropna(axis=0)


def collect_cobb_douglas(series_number: int = 3) -> DataFrame:
    '''
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
    '''
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4': ('dataset_usa_cobb-douglas.zip', 'capital', ),
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': ('dataset_usa_cobb-douglas.zip', 'labor',),
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': ('dataset_usa_census1949.zip', 'product', ),
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': ('dataset_usa_census1949.zip', 'product_nber', ),
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': ('dataset_douglas.zip', 'product_rev',),
    }
    df = pd.concat(
        [
            read_pull_usa_hist(archive_name, series_id)
            for series_id, (archive_name, _) in SERIES_IDS.items()
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    df.columns = tuple(column_name for (_, column_name) in SERIES_IDS.values())
    return df.div(df.iloc[0, :]).iloc[:, range(series_number)]


def collect_combined() -> DataFrame:
    '''


    Returns
    -------
    DataFrame
        DESCRIPTION.

    '''
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    ARCHIVE_NAME, SERIES_ID = 'dataset_usa_census1975.zip', 'X0414'
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
        # Current-Cost Net Stock of Fixed Assets, Private, k1ptotl1es00
        # =====================================================================
        'k1ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es00
        # =====================================================================
        'k3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Chain-Type Quantity Indexes for Net Stock of Fixed Assets, Private, kcptotl1es00
        # =====================================================================
        'kcptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    return pd.concat(
        [
            pd.concat(
                [
                    pd.concat(
                        [
                            pull_by_series_id(
                                read_from_url_usa_bea(
                                    SERIES_IDS[series_id]), series_id
                            )
                            for series_id in tuple(SERIES_IDS)[:8]
                        ],
                        axis=1
                    ),
                    collect_usa_bea_labor_mfg(),
                    pd.concat(
                        [
                            pull_by_series_id(
                                read_from_url_usa_bea(
                                    SERIES_IDS[series_id]), series_id
                            )
                            for series_id in tuple(SERIES_IDS)[8:]
                        ],
                        axis=1
                    ),
                ],
                axis=1,
                sort=True
            ),
            read_pull_usa_frb_ms(),
            read_pull_usa_hist(ARCHIVE_NAME, SERIES_ID),
            pd.read_csv(FILE_NAME, index_col=0),
        ],
        axis=1
    )


def collect_common_archived() -> DataFrame:
    '''Data Fetch'''
    URLS = (
        'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    )
    SERIES_IDS_NIPA = (
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX, 1929--2021, 2012=100
        # =====================================================================
        'A191RX',
        # =====================================================================
        # Deflator Gross Domestic Product, A191RD3, 1929--2021, 2012=100
        # =====================================================================
        'A191RD',
        # =====================================================================
        # National Income: A032RC, 1929--2021
        # =====================================================================
        'A032RC',
        # =====================================================================
        # Fixed Assets Series: K10002, 1951--2021
        # =====================================================================
        'K10002',
    )
    SERIES_IDS_SFAT = (
        # =====================================================================
        # Fixed Assets Series: k1ntotl1si00, 1925--2020
        # =====================================================================
        'k1ntotl1si00',
        # =====================================================================
        # Fixed Assets Series: k3ntotl1si00, 1925--2020
        # =====================================================================
        'k3ntotl1si00',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1925--2020
        # =====================================================================
        'k1n31gd1es00',
        # =====================================================================
        # Fixed Assets Series: k3n31gd1es00, 1925--2020
        # =====================================================================
        'k3n31gd1es00',
    )
    _df_nipa = read_from_url_usa_bea(URLS[0])
    _df_sfat = read_from_url_usa_bea(URLS[-1])
    return pd.concat(
        [
            pd.concat(
                [
                    (
                        pull_by_series_id(_df_nipa, series_id),
                        pull_by_series_id(
                            _df_nipa, series_id).rdiv(100)
                    )[series_id == 'A191RD']
                    for series_id in SERIES_IDS_NIPA
                ],
                axis=1
            ),
            pd.concat(
                [
                    pull_by_series_id(_df_sfat, series_id)
                    for series_id in SERIES_IDS_SFAT
                ],
                axis=1
            ),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            collect_usa_bea_labor_mfg(),
            # =====================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =====================================================================
            read_pull_usa_frb_cu(),
        ],
        axis=1,
        sort=True
    )


def collect_douglas() -> DataFrame:
    '''Douglas Data Preprocessing'''
    ARCHIVE_NAME = 'dataset_douglas.zip'
    SERIES_IDS = ('DT19AS03', 'DT19AS02', 'DT19AS01',)
    df = pd.concat(
        [
            read_pull_usa_hist(ARCHIVE_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    return df.div(df.loc[1899, :])


def collect_updated() -> DataFrame:
    URLS = (
        'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    )
    SERIES_IDS_NIPA = (
        'A006RC',
        'A006RD',
        'A191RC',
        'A191RX',
    )
    SERIES_IDS_SFAT = (
        # =====================================================================
        # Not Used: Fixed Assets: k3n31gd1es00, 1925--2016, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'k3n31gd1es00',
        # =====================================================================
        # Fixed Assets: kcn31gd1es00, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =====================================================================
        'kcn31gd1es00',
    )
    _df_nipa = read_from_url_usa_bea(URLS[0])
    _df_sfat = read_from_url_usa_bea(URLS[-1])
    df = pd.concat(
        [
            pd.concat(
                [
                    pull_by_series_id(_df_nipa, series_id)
                    for series_id in SERIES_IDS_NIPA
                ],
                axis=1
            ),
            pd.concat(
                [
                    pull_by_series_id(_df_sfat, series_id)
                    for series_id in SERIES_IDS_SFAT
                ],
                axis=1
            ),
        ],
        axis=1
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


def collect_usa_bea_labor() -> DataFrame:
    '''
    Labor Series: A4601C0, 1929--2013
    '''
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    SERIES_ID = 'A4601C'
    _df_nipa = read_from_url_usa_bea(URL)
    return pull_by_series_id(_df_nipa, SERIES_ID)


def collect_usa_bea_labor_mfg() -> DataFrame:
    '''
    Manufacturing Labor Series

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Labor Series
    ================== =================================
    '''
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
            pull_by_series_id(read_from_url_usa_bea(url), series_id)
            for series_id, url in SERIES_IDS.items()
        ],
        axis=1,
        sort=True
    )
    df['bea_mfg_labor'] = df.mean(axis=1)
    return df.iloc[:, [-1]].dropna(axis=0)


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
        'P0107': 'dataset_usa_census1975.zip',
        'P0110': 'dataset_usa_census1975.zip',
        'P0119': 'dataset_usa_census1975.zip',
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
                    read_pull_usa_hist(archive_name, series_id)
                    for series_id, archive_name in SERIES_IDS.items()
                ],
                axis=1,
                sort=True
            ).truncate(before=1869),
            # =================================================================
            # FRB Data
            # =================================================================
            collect_usa_frb_fa(),
        ],
        axis=1,
        sort=True
    )


def collect_usa_frb_fa() -> DataFrame:
    '''
    Retrieves DataFrame for Manufacturing Fixed Assets Series, Billion USD

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Nominal
    df.iloc[:, 1]      Real
    ================== =================================
    '''
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_frb_invest_capital.csv',
        'index_col': 0,
        'skiprows': 4,
    }
    df = pd.read_csv(**kwargs).transpose()
    df.index = df.index.astype(int)
    df['frb_nominal'] = ((df.iloc[:, 1].mul(df.iloc[:, 2]).div(df.iloc[:, 0])).add(
        df.iloc[:, 4].mul(df.iloc[:, 5]).div(df.iloc[:, 3]))).div(1000)
    df['frb_real'] = df.iloc[:, [2, 5]].sum(axis=1).div(1000)
    return df.iloc[:, -2:]


def collect_usa_frb_fa_def() -> DataFrame:
    '''
    Retrieves DataFrame for Deflator for Manufacturing Fixed Assets Series

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Deflator
    ================== =================================
    '''
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_frb_invest_capital.csv',
        'index_col': 0,
        'skiprows': 4,
    }
    df = pd.read_csv(**kwargs).transpose()
    df.index = df.index.astype(int)
    df['fa_def_frb'] = (df.iloc[:, [1, 4]].sum(axis=1)).div(
        df.iloc[:, [0, 3]].sum(axis=1))
    return df.iloc[:, [-1]]


def collect_usa_frb_ip() -> DataFrame:
    '''
    Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      AIPMA_SA_IX
    ================== =================================
    '''
    # =========================================================================
    # TODO: https://www.federalreserve.gov/datadownload/Output.aspx?rel=g17&filetype=zip
    # =========================================================================
    # =========================================================================
    # with ZipFile('FRB_g17.zip', 'r').open('G17_data.xml') as f:
    # =========================================================================
    SERIES_ID = 'AIPMA_SA_IX'
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_frb_us3_ip_2018_09_02.csv',
        'index_col': 0,
        'skiprows': 7,
        'parse_dates': True
    }
    _df = pd.read_csv(**kwargs)
    _df.rename_axis('period', inplace=True)
    _df.columns = tuple(column_name.strip() for column_name in _df.columns)
    return _df.groupby(_df.index.year).mean().loc[:, [SERIES_ID]]


def collect_usa_mcconnel(series_ids: tuple[str]) -> DataFrame:
    return pd.concat(
        [read_pull_usa_mcconnel(series_id) for series_id in series_ids],
        axis=1
    ).truncate(before=1980)


def collect_usa_sahr_infcf() -> DataFrame:
    '''
    Retrieve Yearly Price Rates from `dataset_usa_infcf16652007.zip`

    Returns
    -------
    DataFrame
    '''
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_infcf16652007.zip',
        'index_col': 1,
        'usecols': range(4, 7)
    }
    _df = pd.read_csv(**kwargs)
    # =========================================================================
    # Retrieve First 14 Series
    # =========================================================================
    df = pd.concat(
        [
            -price_inverse_single(
                _df[_df.iloc[:, 0] == series_id].iloc[:, [1]].rdiv(1)
            )
            for series_id in _df.iloc[:, 0].unique()[:14]
        ],
        axis=1,
        sort=True
    )
    df['cpiu_fused'] = df.mean(axis=1)
    return df.iloc[:, [-1]].dropna(axis=0)


def collect_version_a() -> tuple[DataFrame]:
    '''
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
    '''
    URLS = (
        'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    )
    SERIES_IDS = (
        # =================================================================
        # Fixed Assets: kcn31gd1es00, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
        # =================================================================
        'kcn31gd1es00',
        # =================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2012
        # =================================================================
        'A191RX',
    )
    _df = pd.concat(
        [
            pd.concat(
                [
                    pull_by_series_id(
                        read_from_url_usa_bea(url), series_id)
                    for url, series_id in zip(URLS[::-1], SERIES_IDS)
                ],
                axis=1
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
    _df = _df.reindex(columns=sorted(_df.columns)[::-1])
    _df_adjusted = pd.concat(
        [
            _df.copy(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_pull_usa_frb_cu(),
        ],
        axis=1
    ).dropna(axis=0)
    _df_adjusted.iloc[:, -2] = _df_adjusted.iloc[:, -2].div(
        _df_adjusted.iloc[:, -1]
    ).mul(100)
    return (
        _df.div(_df.iloc[0, :]),
        _df_adjusted.div(_df_adjusted.iloc[0, :]).iloc[:, range(3)]
    )


def collect_version_b() -> tuple[DataFrame]:
    '''
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
    '''
    URL = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    SERIES_ID = 'kcn31gd1es00'
    _df_sfat = read_from_url_usa_bea(URL)
    _df = pd.concat(
        [
            # =================================================================
            # Fixed Assets: kcn31gd1es00, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization
            # =================================================================
            pull_by_series_id(_df_sfat, SERIES_ID),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            collect_usa_bea_labor_mfg(),
            # =================================================================
            # Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018
            # =================================================================
            collect_usa_frb_ip(),
        ],
        axis=1
    ).dropna(axis=0)
    _df_adjusted = pd.concat(
        [
            _df.copy(),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_pull_usa_frb_cu(),
        ],
        axis=1
    ).dropna(axis=0)
    _df_adjusted.iloc[:, -2] = _df_adjusted.iloc[:, -2].div(
        _df_adjusted.iloc[:, -1]
    ).mul(100)
    _df_truncated = _df.truncate(before=_df_adjusted.index[0])
    return (
        _df.div(_df.iloc[0, :]),
        _df_truncated.div(_df_truncated.iloc[0, :]),
        _df_adjusted.div(_df_adjusted.iloc[0, :]).iloc[:, range(3)]
    )


def collect_version_c() -> DataFrame:
    '''Data Fetch'''
    # =========================================================================
    # TODO: Update Accodring to Change in collect_cobb_douglas_deflator()
    # =========================================================================
    df_capital = pd.concat(
        [
            # =================================================================
            # Data Fetch for Capital
            # =================================================================
            collect_cobb_douglas_extension_capital(),
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
            collect_cobb_douglas_extension_product(),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    return df.div(df.iloc[0, :])


def get_mean_for_min_std():
    '''
    Determine Year & Mean Value for Base Vectors for Year with Minimum StandardError
    '''
    DIR = '/home/alexander/science'
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
    _df = pd.read_excel(Path(DIR).joinpath(FILE_NAME), index_col=0)
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
    df = df.iloc[:, [0, 4, 6, 7]].dropna(axis=0)
    df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
    return df.div(df.iloc[0, :]).dropna(axis=0)


def transform_b(df: DataFrame) -> DataFrame:
    return df.iloc[:, [0, 6, 7, 20]].dropna(axis=0)


def transform_c(df: DataFrame) -> DataFrame:
    df_production = df.iloc[:, [0, 6, 7]].dropna(axis=0)
    df_production = df_production.div(df_production.iloc[0, :])
    df_money = df.iloc[:, range(18, 20)].dropna(how='all')
    df_money['m1_fused'] = df_money.mean(axis=1)
    df_money = df_money.iloc[:, -1].div(df_money.iloc[0, -1])
    _df = pd.concat(
        [
            df_production,
            df_money
        ],
        axis=1
    ).dropna(axis=0)
    return _df.div(_df.iloc[0, :])


def transform_d(df: DataFrame) -> DataFrame:
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return df.iloc[:, [0, 1, 2, 3, 7]].dropna(axis=0)


def transform_e(df: DataFrame) -> tuple[DataFrame]:
    assert df.shape[1] == 21, 'Works on DataFrame Produced with `collect_combined()`'
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    df['investment'] = df.iloc[:, 0].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    # =========================================================================
    # `Real` Capital
    # =========================================================================
    df['capital'] = df.iloc[:, 11].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    return (
        # =====================================================================
        # DataFrame Nominal
        # =====================================================================
        df.iloc[:, [0, 6, 11]].dropna(axis=0),
        # =====================================================================
        # DataFrame `Real`
        # =====================================================================
        df.iloc[:, [-2, 7, -1]].dropna(axis=0),
    )


def transform_cobb_douglas(df: DataFrame) -> tuple[DataFrame, tuple[float]]:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital
    df.iloc[:, 1]      Labor
    df.iloc[:, 2]      Product
    ================== =================================
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
    # Original: k=0.25, b=1.01
    # =========================================================================
    k, b = np.polyfit(
        np.log(df.iloc[:, -2].astype(float)),
        np.log(df.iloc[:, -1].astype(float)),
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
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital
    df.iloc[:, 1]      Labor
    df.iloc[:, 2]      Product
    df.iloc[:, 3]      Product Alternative
    ================== =================================
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
    # Original: k=0.25, b=1.01
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
    # Original: _k=0.25, _b=1.01
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


def transform_cobb_douglas_sklearn(df: DataFrame) -> DataFrame:
    '''


    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital
    df.iloc[:, 1]      Labor
    df.iloc[:, 2]      Product
    ================== =================================

    Returns
    -------
    None.

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
    # Original: k=.25, b=1.01
    # =========================================================================
    X = np.column_stack((np.zeros(df.shape[0]), np.log(df.iloc[:, -2])))
    y = np.log(df.iloc[:, -1].to_numpy())
    return X, y
# =============================================================================
#     # =========================================================================
#     # Lasso
#     # =========================================================================
#     las = Lasso(alpha=.01).fit(X, y)
#     k, b = las.coef_[1], las.intercept_
#     # print('Lasso: k = {:.12f}, b = {:.12f}'.format(k, b))
#
#     las = LassoCV(cv=4, random_state=0).fit(X, y)
#     k, b = las.coef_[1], las.intercept_
#     # print('LassoCV: k = {:.12f}, b = {:.12f}'.format(k, b))
#     # =========================================================================
#     #     print(reg.score(X, y))
#     #     print(reg)
#     #     print(reg.predict(X[:1, ]))
#     # =========================================================================
# =============================================================================

    reg = LinearRegression().fit(X, y)
    k, b = reg.coef_[1], reg.intercept_
    # print('Linear Regression: k = {:.12f}, b = {:.12f}'.format(k, b))
    # =========================================================================
    #     reg.score(X, y)
    #     reg.coef_
    #     reg.intercept_
    # =========================================================================

    # =========================================================================
    # tik = Ridge(alpha=.01).fit(X, y)
    # k, b = tik.coef_[1], tik.intercept_
    # print('Ridge Regression: k = {:.12f}, b = {:.12f}'.format(k, b))
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
    return df, (k, np.exp(b),)


def transform_kurenkov(data_testing: DataFrame) -> tuple[DataFrame]:
    '''Returns Four DataFrames with Comparison of data_testing: DataFrame and Yu.V. Kurenkov Data'''
    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'
    data_control = pd.read_csv(FILE_NAME, index_col=0)
    # =========================================================================
    # Production
    # =========================================================================
    data_a = pd.concat(
        [
            data_control.iloc[:, [0]],
            data_testing.loc[:, ['A191RX1']],
            collect_usa_frb_ip(),
        ],
        axis=1,
        sort=True
    ).dropna(how='all')
    data_a = data_a.div(data_a.loc[1950, :]).mul(100)
    # =========================================================================
    # Labor
    # =========================================================================
    data_b = pd.concat(
        [
            data_control.iloc[:, [1]],
            data_testing.loc[:, ['bea_mfg_labor']],
        ],
        axis=1,
        sort=True
    ).dropna(how='all')
    # =========================================================================
    # Capital
    # =========================================================================
    data_c = pd.concat(
        [
            data_control.iloc[:, [2]],
            data_testing.loc[:, ['K100701']],
        ],
        axis=1,
        sort=True
    ).dropna(how='all')
    data_c = data_c.div(data_c.loc[1951, :]).mul(100)
    # =========================================================================
    # Capacity Utilization
    # =========================================================================
    data_d = pd.concat(
        [
            data_control.iloc[:, [3]],
            read_pull_usa_frb_cu(),
        ],
        axis=1,
        sort=True
    )
    return data_a, data_b, data_c, data_d


def transform_sum(df: DataFrame) -> DataFrame:
    '''


    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series IDs
    df.iloc[:, 1]      Values
    ================== =================================
    series_ids : Iterable[str]
        DESCRIPTION.

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Sum of <series_ids>
    ================== =================================
    '''
    series_ids = sorted(set(df.iloc[:, 0]))
    df = pd.concat(
        [
            numerify(pull_by_series_id(df, series_id))
            for series_id in series_ids
        ],
        axis=1
    )
    df.columns = series_ids
    df['sum'] = df.sum(axis=1)
    return df.iloc[:, [-1]]


def filter_data_frame(df: DataFrame, query: dict[str]) -> DataFrame:
    for column, criterion in query['filter'].items():
        df = df[df.iloc[:, column] == criterion]
    return df
