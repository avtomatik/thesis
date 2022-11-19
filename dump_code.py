#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:24:57 2022

@author: Alexander Mikhailov
"""


# =============================================================================
# Stores Unused or Test Codes
# =============================================================================
import os
import sqlite3

import pandas as pd
from pandas import DataFrame
from pull.lib import pull_by_series_id, pull_can_quarter_former
from read.lib import read_usa_bea, read_usa_bea_excel

# =============================================================================
# Separate Chunk of Code
# =============================================================================


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


def string_to_url(string):
    return f'https://www150.statcan.gc.ca/n1/tbl/csv/{string}'


# =============================================================================
# Separate Block
# =============================================================================
def test_data_capital_combined_archived():
    """Data Test"""
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
        # =====================================================================
        # TODO: UPDATE ACCORDING TO NEW SIGNATURE
        # =====================================================================
        [read_usa_bea_excel(**kwargs) for kwargs in KWARGS],
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
        # =====================================================================
        # TODO: UPDATE ACCORDING TO NEW SIGNATURE
        # =====================================================================
        [read_usa_bea_excel(**kwargs) for kwargs in KWARGS],
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
        # =====================================================================
        # TODO: UPDATE ACCORDING TO NEW SIGNATURE
        # =====================================================================
        [read_usa_bea_excel(**kwargs) for kwargs in KWARGS],
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
        # =====================================================================
        # TODO: UPDATE ACCORDING TO NEW SIGNATURE
        # =====================================================================
        [read_usa_bea_excel(**kwargs) for kwargs in KWARGS],
        axis=1,
        sort=True
    )

    if _control.equals(_test):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1969--2012')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')


def collect_usa_bls_cpiu() -> DataFrame:
    """BLS CPI-U Price Index Fetch"""
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_bls_cpiai.txt',
        'sep': '\s+',
        'index_col': 0,
        'usecols': range(13),
        'skiprows': 16,
    }
    _df = pd.read_csv(**kwargs)
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
    """


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

    """
    # =========================================================================
    # Not Used Anywhere
    # =========================================================================
    kwargs['filepath_or_buffer'] = f'dataset_read_can{file_id:n}.csv'
    kwargs['index_col'] = 0
    _df = pd.read_csv(**kwargs)
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
    """


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

    """
    # =========================================================================
    # Not Used Anywhere
    # =========================================================================
    kwargs['filepath_or_buffer'] = f'dataset_read_can{file_id:n}.csv'
    kwargs['index_col'] = 0
    _df = pd.read_csv(**kwargs)
    _df['period'] = pd.to_numeric(
        _df.index.astype(str).to_series().str.slice(start=4),
        downcast='integer'
    )
    return _df.groupby(_df.columns[-1]).mean()


def transform_center_by_period(df: DataFrame) -> DataFrame:
    """
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
    """
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


def extract_read_usa_bea_pull_by_series_id(series_id: str) -> DataFrame:
    """
    Retrieves Yearly Data for BEA Series' series_id
    Parameters
    ----------
    series_id : str
        DESCRIPTION.
    Returns
    -------
    DataFrame
        DESCRIPTION.
    """
    DIR = "/home/green-machine/data_science"
    DBNAME = "temporary"
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_bea-nipa-2015-05-01.zip',
        'usecols': [0, *range(14, 18)],
    }
    _df = pd.read_csv(**kwargs)
    with sqlite3.connect(Path(DIR).joinpath(f"{DBNAME}.db")) as conn:
        cursor = conn.cursor()
        _df.to_sql("temporary", conn, if_exists="replace", index=False)
        stmt = f"""
        SELECT * FROM temporary
        WHERE
            vector = '{series_id}'
            AND subperiod = 0
            ;
        """
        cursor = conn.execute(stmt)
    _df = DataFrame(
        cursor.fetchall(),
        columns=['source_id', 'series_id', 'period', 'sub_period', 'value'],
    )
    _df.set_index('period', inplace=True)
    _df.drop('sub_period', axis=1, inplace=True)
    df = pd.concat(
        [
            _df[_df.iloc[:, 0] == source_id].iloc[:, [2]].drop_duplicates()
            for source_id in sorted(set(_df.iloc[:, 0]))
        ],
        axis=1
    )
    df.columns = [
        ''.join((source_id.split()[1].replace('.', '_'), series_id))
        for source_id in sorted(set(_df.iloc[:, 0]))
    ]
    return df


def collect_usa_xlsm() -> DataFrame:
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC, 1929--2021
        # =====================================================================
        'A006RC',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =====================================================================
        'A191RX',
        # =====================================================================
        # Nominal National income Series: A032RC, 1929--2021
        # =====================================================================
        'A032RC',
    )
    return pd.concat(
        [
            pd.concat(
                [
                    read_usa_bea(URL).pipe(pull_by_series_id, series_id)
                    for series_id in SERIES_IDS
                ],
                axis=1
            ),
            read_usa_prime_rate(),
        ],
        axis=1
    )


def collect_bea_def() -> DataFrame:
    """
    USA BEA Gross Domestic Product Deflator: Cumulative Price Index

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Gross Domestic Product Deflator
    ================== =================================

    """
    _df = collect_bea_gdp()
    _df['deflator_gdp'] = _df.iloc[:, 0].div(_df.iloc[:, 1]).mul(100)
    return _df.iloc[:, [-1]]


def collect_bea_gdp() -> DataFrame:
    """
    USA BEA Gross Domestic Product

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Nominal
    df.iloc[:, 1]      Real
    ================== =================================
    """
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
            pull_by_series_id(read_usa_bea(url), series_id)
            for series_id, url in SERIES_IDS.items()
        ],
        axis=1
    )


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
                    pull_by_series_id(read_usa_bea(url), series_id)
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


DIR = '/media/green-machine/KINGSTON'

os.chdir(DIR)

# =============================================================================
# Section5ALL_Hist
# =============================================================================
# =============================================================================
# www.bea.gov/histdata/Releases/GDP_and_PI/2012/Q1/Second_May-31-2012/Section5ALL_Hist.xls
# =============================================================================
# =============================================================================
# Metadata: `Section5ALL_Hist.xls`@[`dataset_usa_bea-release-2010-08-05 Section5ALL_Hist.xls` Offsets `dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip`]"""
# =============================================================================
# =============================================================================
# Fixed Assets Series: K160021, 1951--1969
# =============================================================================
kwargs = {
    'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
    'wb_name': 'Section5ALL_Hist.xls',
    'sh_name': '50900 Ann',
}
SERIES_ID = 'K160021'
_df_sub_a = read_usa_bea_excel(**kwargs).loc[:, [SERIES_ID]]

# =============================================================================
# Not Clear
# =============================================================================

kwargs = {
    'filepath_or_buffer': 'dataset_read_can-{:08n}-eng-{}.csv'.format(
        310003, 7591839622055840674
    ),
    'skiprows': 3,
}
_df = pd.read_csv(**kwargs)

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
}
SERIES_ID = 'k3n31gd1es000'
_df_semi_c = read_usa_bea_excel(**kwargs).loc[:, [SERIES_ID]]
KWARGS = (
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1929--1969
    # =========================================================================
    {
        'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'wb_name': 'Section1ALL_Hist.xls',
        'sh_name': '10105 Ann',
    },
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1969--2014
    # =========================================================================
    {
        'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
        'wb_name': 'Section1all_xls.xls',
        'sh_name': '10105 Ann',
    },
)
SERIES_ID = 'A191RC1'
_df_semi_d = pd.concat(
    [read_usa_bea_excel(**kwargs).loc[:, [SERIES_ID]] for kwargs in KWARGS],
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
pull_can_quarter_former(read_can(3800068), 'v62143969')
pull_can_quarter_former(read_can(3800068), 'v62143990')
