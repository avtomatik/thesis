#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:24:57 2022

@author: alexander
"""


# =============================================================================
# Stores Unused or Test Codes
# =============================================================================
import os
import pandas as pd
from pandas import DataFrame
from extract.lib import (
    extract_can_quarter,
    extract_usa_bea,
)

# =============================================================================
# Separate Chunk of Code
# =============================================================================


def append_series_ids(df, chunk, series_ids):
    for series_id in series_ids:
        chunk = pd.concat(
            [
                chunk,
                df.loc[:, [series_id]].dropna(axis=0)
            ],
            axis=1, sort=False)
    return chunk


def append_series_ids_sum(df, chunk, series_ids):
    for series_id in series_ids:
        _chunk = pd.concat(
            [
                _chunk,
                df.loc[:, [series_id]].dropna(axis=0)
            ],
            axis=1, sort=False)
    series_ids.extend(['sum'])
    _chunk['_'.join(series_ids)] = _chunk.sum(1)
    return pd.concat(
        [
            chunk,
            _chunk.iloc[:, [-1]]
        ],
        axis=1, sort=False)


def url_to_file_name(_url: str) -> str:
    '''


    Parameters
    ----------
    _url : str
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    '''
    return '/'.join(
        (
            'https://www150.statcan.gc.ca/n1/tbl/csv',
            f"{_url.split('?pid=')[1][:-2]}-eng.zip")
    )


def string_to_url(string):
    return f'https://www150.statcan.gc.ca/n1/tbl/csv/{string}'


# =============================================================================
# Separate Block
# =============================================================================
def test_data_capital_combined_archived():
    '''Data Test'''
    KEYS = (
        'archive_name',
        'wb_name',
        'sh_name',
        'series_id',
    )
    # =============================================================================
    # ONE ARCHIVE NAME
    # =============================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    WB_NAME = 'Section1ALL_Hist.xls'
    # =========================================================================
    # ONE SHEET NAME
    # =========================================================================
    SH_NAME = '10105 Ann'
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1
        # =====================================================================
        'A191RC1',
    )
    KWARGS = [
        {key: value for key, value in zip(
            KEYS,
            (
                ARCHIVE_NAME,
                WB_NAME,
                SH_NAME,
                series_id,
            )
        )
        } for series_id in SERIES_IDS
    ]
    _control = pd.concat(
        [extract_usa_bea(**kwargs) for kwargs in KWARGS],
        axis=1,
        sort=True
    )
    # =========================================================================
    # OTHER SHEET NAME
    # =========================================================================
    SH_NAME = '10505 Ann'
    KWARGS = [
        {key: value for key, value in zip(
            KEYS,
            (
                ARCHIVE_NAME,
                WB_NAME,
                SH_NAME,
                series_id,
            )
        )
        } for series_id in SERIES_IDS
    ]
    _test = pd.concat(
        [extract_usa_bea(**kwargs) for kwargs in KWARGS],
        axis=1,
        sort=True
    )

    if _control.equals(_test):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1929--1969')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')

    # =========================================================================
    # Nominal Investment Series: A006RC1, 1969--2012
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    WB_NAME = 'Section1all_xls.xls'
    # =========================================================================
    # ONE SHEET NAME
    # =========================================================================
    SH_NAME = '10105 Ann'
    KWARGS = [
        {key: value for key, value in zip(
            KEYS,
            (
                ARCHIVE_NAME,
                WB_NAME,
                SH_NAME,
                series_id,
            )
        )
        } for series_id in SERIES_IDS
    ]
    _control = pd.concat(
        [extract_usa_bea(**kwargs) for kwargs in KWARGS],
        axis=1,
        sort=True
    )
    # =========================================================================
    # OTHER SHEET NAME
    # =========================================================================
    SH_NAME = '10505 Ann'
    KWARGS = [
        {key: value for key, value in zip(
            KEYS,
            (
                ARCHIVE_NAME,
                WB_NAME,
                SH_NAME,
                series_id,
            )
        )
        } for series_id in SERIES_IDS
    ]
    _test = pd.concat(
        [extract_usa_bea(**kwargs) for kwargs in KWARGS],
        axis=1,
        sort=True
    )

    if _control.equals(_test):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1969--2012')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')


def collect_usa_bls_cpiu() -> DataFrame:
    '''BLS CPI-U Price Index Fetch'''
    FILE_NAME = 'dataset_usa_bls_cpiai.txt'
    _df = pd.read_csv(
        FILE_NAME,
        sep='\s+',
        index_col=0,
        usecols=range(13),
        skiprows=16
    )
    _df.rename_axis('period', inplace=True)
    _df['mean'] = _df.mean(axis=1)
    _df['sqrt'] = _df.iloc[:, :-1].prod(1).pow(1/12)
    # =========================================================================
    # Tests
    # =========================================================================
    _df['mean_less_sqrt'] = _df.iloc[:, -2].sub(_df.iloc[:, -1])
    _df['dec_on_dec'] = _df.iloc[:, -3].div(_df.iloc[:, -3].shift(1)).sub(1)
    _df['mean_on_mean'] = _df.iloc[:, -4].div(_df.iloc[:, -4].shift(1)).sub(1)
    return _df.iloc[:, [-1]].dropna(axis=0)


def extract_can_group_a(file_id: int, **kwargs) -> DataFrame:
    '''


    Parameters
    ----------
    file_id : int
        DESCRIPTION.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    '''
    # =========================================================================
    # Not Used Anywhere
    # =========================================================================
    _df = pd.read_csv(
        f'dataset_can_cansim{file_id:n}.csv', index_col=0, **kwargs
    )
    if file_id == 7931814471809016759:
        _df.columns = [column[:7] for column in _df.columns]
        _df.iloc[:, -1] = pd.to_numeric(_df.iloc[:, -1].str.replace(';', ''))
    _df = _df.transpose()
    _df['period'] = pd.to_numeric(
        _df.index.astype(str).to_series().str.slice(start=3),
        downcast='integer'
    )
    return _df.groupby(_df.columns[-1]).mean()


def extract_can_group_b(file_id: int, **kwargs) -> DataFrame:
    '''


    Parameters
    ----------
    file_id : int
        DESCRIPTION.
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    '''
    # =========================================================================
    # Not Used Anywhere
    # =========================================================================
    _df = pd.read_csv(
        f'dataset_can_cansim{file_id:n}.csv', index_col=0, **kwargs
    )
    _df['period'] = pd.to_numeric(
        _df.index.astype(str).to_series().str.slice(start=4),
        downcast='integer'
    )
    return _df.groupby(_df.columns[-1]).mean()


def transform_center_by_period(df: DataFrame) -> DataFrame:
    '''
    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    Returns
    -------
    DataFrame
    '''
    # =========================================================================
    # TODO: Any Use?
    # =========================================================================
    # =========================================================================
    # DataFrame for Results
    # =========================================================================
    _df = df.copy()
    _df.reset_index(level=0, inplace=True)
    period = _df.iloc[:, 0]
    series = _df.iloc[:, 1]
    # =========================================================================
    # Loop
    # =========================================================================
    for _ in range(_df.shape[0] // 2):
        period = period.rolling(2).mean()
        series = series.rolling(2).mean()
        period_roll = period.shift(-((1 + _) // 2))
        series_roll = series.shift(-((1 + _) // 2))
        _df = pd.concat(
            [
                _df,
                period_roll,
                series_roll,
                series_roll.div(_df.iloc[:, 1]),
                series_roll.shift(-2).sub(series_roll).div(
                    series_roll.shift(-1)).div(2),
            ],
            axis=1,
            sort=True
        )
    return _df


DIR = '/media/alexander/321B-6A94'

os.chdir(DIR)

# =============================================================================
# Section5ALL_Hist
# =============================================================================
# =============================================================================
# www.bea.gov/histdata/Releases/GDP_and_PI/2012/Q1/Second_May-31-2012/Section5ALL_Hist.xls
# =============================================================================
# =============================================================================
# Metadata: `Section5ALL_Hist.xls`@[`dataset_usa_bea-release-2010-08-05 Section5ALL_Hist.xls` Offsets `dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip`]'''
# =============================================================================
# =============================================================================
# Fixed Assets Series: K160021, 1951--1969
# =============================================================================
kwargs = {
    'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
    'wb_name': 'Section5ALL_Hist.xls',
    'sh_name': '50900 Ann',
    'series_id': 'K160021',
}
_df_sub_a = extract_usa_bea(**kwargs)


# =============================================================================
# Not Clear
# =============================================================================

FILE_NAME = 'dataset_can_cansim-{:08n}-eng-{}.csv'.format(
    310003, 7591839622055840674)
_df = pd.read_csv(FILE_NAME, skiprows=3)

# =============================================================================
# Unallocated
# =============================================================================
# =============================================================================
# Fixed Assets Series: k3n31gd1es000, 1947--2011
# =============================================================================
kwargs = {
    'archive_name': 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip',
    'wb_name': 'Section3ALL_xls.xls',
    'sh_name': '303ES Ann',
    'series_id': 'k3n31gd1es000',
}
_df_semi_c = extract_usa_bea(**kwargs)
KWARGS = (
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1929--1969
    # =========================================================================
    {
        'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'wb_name': 'Section1ALL_Hist.xls',
        'sh_name': '10105 Ann',
        'series_id': 'A191RC1',
    },
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1969--2014
    # =========================================================================
    {
        'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
        'wb_name': 'Section1all_xls.xls',
        'sh_name': '10105 Ann',
        'series_id': 'A191RC1',
    },
)
_df_semi_d = pd.concat(
    [extract_usa_bea(**kwargs) for kwargs in KWARGS],
    sort=True
).drop_duplicates()
# =============================================================================
# Gross fixed capital formation Data Block
# =============================================================================
# =============================================================================
# Not Clear: v62143969 - 380-0068 Gross fixed capital formation; Canada;
# Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial
# machinery and equipment (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
# =============================================================================
# =============================================================================
# Not Clear: v62143990 - 380-0068 Gross fixed capital formation; Canada;
# Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial\
# machinery and equipment (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
# =============================================================================
extract_can_group_a(7931814471809016759, skiprows=241)
extract_can_group_a(8448814858763853126, skiprows=81)
extract_can_group_b(5245628780870031920, skiprows=3)
extract_can_quarter(3800068, 'v62143969')
extract_can_quarter(3800068, 'v62143990')
