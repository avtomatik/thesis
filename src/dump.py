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
from pathlib import Path

import pandas as pd
from lib.collect import stockpile_usa_bea
from lib.pull import pull_by_series_id
from lib.read import read_temporary, read_usa_bea_excel, read_usa_frb_g17
from lib.transform import transform_mean
from pandas import DataFrame

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
# =============================================================================
# Separate Chunk of Code
# =============================================================================





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
    # =========================================================================
    # ONE ARCHIVE NAME
    # =========================================================================
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
        print("Series 'A006RC1' & 'A191RC1' @ Worksheet '10105 Ann' Equals Series 'A006RC1' & 'A191RC1' @ Worksheet '10505 Ann' for Period 1929--1969")
    else:
        print("Data Varies from Worksheet '10105 Ann' to Worksheet '10505 Ann'")

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
        print("Series 'A006RC1' & 'A191RC1' @ Worksheet '10105 Ann' Equals Series 'A006RC1' & 'A191RC1' @ Worksheet '10505 Ann' for Period 1969--2012")
    else:
        print("Data Varies from Worksheet '10105 Ann' to Worksheet '10505 Ann'")


def test_data_capital_combined_archived():
    """Data Test"""
    # =========================================================================
    # Nominal Investment Series: A006RC1, 1929--1969
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAME_CONTROL, SH_NAME_TEST = '10105 Ann', '10505 Ann'
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1
        # =====================================================================
        'A191RC1'
    )
    df_control = pd.concat(
        [
            read_usa_bea_excel(
                archive_name, wb_name, SH_NAME_CONTROL
            ).loc[:, SERIES_IDS]
            for archive_name, wb_name in zip(ARCHIVE_NAMES, WB_NAMES)
        ]
    ).drop_duplicates()
    df_test = pd.concat(
        [
            read_usa_bea_excel(
                archive_name, wb_name, SH_NAME_TEST
            ).loc[:, SERIES_IDS]
            for archive_name, wb_name in zip(ARCHIVE_NAMES, WB_NAMES)
        ]
    ).drop_duplicates()
    if df_control.equals(df_test):
        print(
            """
            Series "A006RC1" & "A191RC1" @ Worksheet "10105 Ann" Equals Series "A006RC1" & "A191RC1" @ Worksheet "10505 Ann"
            """
        )
    else:
        print(
            """
            Data Varies from Worksheet "10105 Ann" to Worksheet "10505 Ann"
            """
        )


def collect_usa_bls_cpiu() -> DataFrame:
    """BLS CPI-U Price Index Fetch"""
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_bls_cpiai.txt',
        'sep': '\s+',
        'index_col': 0,
        'usecols': range(13),
        'skiprows': 16,
    }
    df = pd.read_csv(**kwargs)
    df.rename_axis('period', inplace=True)
    df['mean'] = df.mean(axis=1)
    df['sqrt'] = df.iloc[:, :-1].prod(1).pow(1/12)
    # =========================================================================
    # Tests
    # =========================================================================
    df['mean_less_sqrt'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    df['dec_on_dec'] = df.iloc[:, -3].pct_change()
    df['mean_on_mean'] = df.iloc[:, -4].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)


def read_can_group_a(file_id: int, **kwargs) -> DataFrame:
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
    df = pd.read_csv(**kwargs)
    if file_id == 7931814471809016759:
        df.columns = (column[:7] for column in df.columns)
        df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1].str.replace(';', ''))
    df = df.transpose()
    df['period'] = pd.to_numeric(
        df.index.astype(str).to_series().str.slice(start=3),
        downcast='integer'
    )
    return df.groupby(df.columns[-1]).mean()


def read_can_group_b(file_id: int, **kwargs) -> DataFrame:
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
    df = pd.read_csv(**kwargs)
    df['period'] = pd.to_numeric(
        df.index.astype(str).to_series().str.slice(start=4),
        downcast='integer'
    )
    return df.groupby(df.columns[-1]).mean()


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


def read_usa_bea_pull_by_series_id(series_id: str) -> DataFrame:
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
            series_id = '{series_id}'
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


def read_usa_bea_pull_by_series_id(df: DataFrame, series_id: str) -> DataFrame:
    """
    Retrieve Yearly Data for BEA Series ID
    """
    df = df[df.loc[:, "series_id"] == series_id]
    source_ids = sorted(set(df.loc[:, "source_id"]))
    chunk = pd.concat(
        [
            df[df.loc[:, "source_id"] == source_id].iloc[:, [-1]].drop_duplicates()
            for source_id in source_ids
        ],
        axis=1,
        sort=True
    )
    chunk.columns = [
        ''.join((source_id.split()[1].replace('.', '_'), series_id))
        for source_id in source_ids
    ]
    return chunk


def collect_usa_xlsm() -> DataFrame:
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC, 1929--2021
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal National income Series: A032RC, 1929--2021
        # =====================================================================
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    }
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            read_temporary(FILE_NAME),
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
    df = collect_usa_bea_gdp()
    df['deflator_gdp'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    return df.iloc[:, [-1]]


def collect_usa_bea_gdp() -> DataFrame:
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
    return stockpile_usa_bea(SERIES_IDS)


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
            stockpile_usa_bea(SERIES_IDS),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, (SERIES_ID,)].dropna(axis=0),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name="bea_labor_mfg"),
            # =================================================================
            # For Overall Labor Series, See: A4601C0, 1929--2020
            # =================================================================
            collect_usa_bea_labor()
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)


def collect_usa_bea_labor() -> DataFrame:
    """
    Labor Series: A4601C0, 1929--2013
    """
    SERIES_IDS = {
        'A4601C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    return stockpile_usa_bea(SERIES_IDS)


DIR = '/media/green-machine/KINGSTON'

os.chdir(DIR)

# =============================================================================
# www.bea.gov/histdata/Releases/GDP_and_PI/2012/Q1/Second_May-31-2012/Section5ALL_Hist.xls
# =============================================================================
# =============================================================================
# Metadata: 'Section5ALL_Hist.xls'@['dataset_usa_bea-release-2010-08-05 Section5ALL_Hist.xls' Offsets 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip']"""
# =============================================================================
kwargs = {
    'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
    'wb_name': 'Section5ALL_Hist.xls',
    'sh_name': '50900 Ann',
}
# =============================================================================
# Fixed Assets Series: K160021, 1951--1969
# =============================================================================
SERIES_ID = 'K160021'
df = read_usa_bea_excel(**kwargs).loc[:, (SERIES_ID, )]

# =============================================================================
# Not Clear
# =============================================================================
kwargs = {
    'filepath_or_buffer': 'dataset_read_can-{:08n}-eng-{}.csv'.format(
        310003, 7591839622055840674
    ),
    'skiprows': 3,
}
df = pd.read_csv(**kwargs)

# =============================================================================
# Unallocated
# =============================================================================
# =============================================================================
# Fixed Assets Series
# =============================================================================
SERIES_ID = {'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'}
df = stockpile_usa_bea(SERIES_ID)

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
df_semi_d = pd.concat(
    [read_usa_bea_excel(**kwargs).loc[:, (SERIES_ID,)] for kwargs in KWARGS],
    sort=True
).drop_duplicates()
# =============================================================================
# Gross fixed capital formation Data Block
# =============================================================================
# =============================================================================
# Not Clear:
{
    "table": 3800068,
    "title": "Gross fixed capital formation",
    "geo": "Canada",
    "prices": "Chained (2007) dollars",
    "seas": "Seasonally adjusted at annual rates",
    "estimates": "Industrial machinery and equipment (x 1,000,000)",
    "frequency_start_end": "(quarterly, 1961-03-01 to 2017-09-01)",
    "series_id": "v62143969"
}
# =============================================================================
# =============================================================================
# Not Clear:
{
    "table": 3800068,
    "title": "Gross fixed capital formation",
    "geo": "Canada",
    "prices": "Chained (2007) dollars",
    "seas": "Seasonally adjusted at annual rates",
    "estimates": "Industrial machinery and equipment (x 1,000,000)",
    "frequency_start_end": "(quarterly, 1961-03-01 to 2017-09-01)",
    "series_id": "v62143990"
}
# =============================================================================

read_can_group_a(7931814471809016759, skiprows=241)
read_can_group_a(8448814858763853126, skiprows=81)
read_can_group_b(5245628780870031920, skiprows=3)
stockpile_can({'v62143969': 36100108}).pipe(transform_agg_sum)
stockpile_can({'v62143990': 36100108}).pipe(transform_agg_sum)


def read_usa_bea_sfat_pull_by_series_id(series_id: str) -> DataFrame:
    """
    Retrieve Historical Manufacturing Series from BEA SFAT CSV File
    """
    MAP = {
        'source_id': 0, 'group1': 6, 'series_id': 8, 'period': 9, 'value': 10
    }
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_bea-nipa-2017-08-23-sfat.zip',
        'header': 0,
        'names': tuple(MAP.keys()),
        'index_col': 3,
        'usecols': tuple(MAP.values()),
    }
    df = pd.read_csv(**kwargs)

    _filter = (
        (df.loc[:, "source_id"].str.contains('Historical')) &
        (df.loc[:, "group1"].str.contains('Manufacturing')) &
        (df.loc[:, "series_id"] == series_id)
    )
    df.drop(["group1", "series_id"], axis=1, inplace=True)

    source_ids = sorted(set(df.loc[:, "source_id"]))

    chunk = pd.concat(
        [
            df[df.loc[:, "source_id"] == source_id].iloc[:, [-1]].drop_duplicates()
            for source_id in source_ids
        ],
        axis=1,
        sort=True
    )
    chunk.columns = [
        ''.join((source_id.split()[1].replace('.', '_'), series_id))
        for source_id in source_ids
    ]
    return chunk


def read_pull_for_autocorrelation(filepath_or_buffer: str, series_id: str) -> DataFrame:
    """


    Parameters
    ----------
    filepath_or_buffer : str
        'datasetAutocorrelation.txt' | 'CHN_TUR_GDP.zip'.
    series_id : str
        DESCRIPTION.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    kwargs = {
        'filepath_or_buffer': filepath_or_buffer,
        'names': ('period', 'series_id', 'value'),
        'index_col': 0,
        'skiprows': 1
    }
    return pd.read_csv(**kwargs).pipe(pull_by_series_id, series_id)


def plot_usa_un_former() -> None:
    """
    https://unstats.un.org/unsd/snaama/Index

    Returns
    -------
    None
        DESCRIPTION.

    """
    kwargs = {
        "io": "dataset_world_united-nations-Download-GDPcurrent-USD-countries.xls",
        "index_col": 0,
        "skiprows": 2,
    }
    _df = pd.read_excel(**kwargs)
    _df = _df[_df.iloc[:, 0] == 'Gross Domestic Product (GDP)']
    _df = _df.select_dtypes(exclude=['object']).transpose()
    df = pd.DataFrame()
    df['us_to_world'] = _df.loc[:, 'United States'].div(_df.sum(axis=1))
    df.plot(grid=True)


def collect_bea_def() -> DataFrame:
    """


    Returns Cumulative Price Index for Some Base Year from Certain Type BEA Deflator File
    -------
    DataFrame
        DESCRIPTION.

    """
    kwargs = {
        "io": "dataset_usa_bea-GDPDEF.xls",
        "names": ('period', 'deflator_gdp'),
        "index_col": 0,
        "skiprows": 15,
        "parse_dates": True
    }
    df = pd.read_excel(**kwargs)
    return df.groupby(df.index.year).prod().pow(1/4)
