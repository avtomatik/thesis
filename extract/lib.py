#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 00:44:36 2022

@author: alexander
"""


import io
import pandas as pd
import requests
from pandas import DataFrame
from zipfile import ZipFile


ARCHIVE_NAMES_UTILISED = (
    'dataset_can_00310004-eng.zip',
    'dataset_douglas.zip',
    'dataset_usa_bea-nipa-2015-05-01.zip',
    'dataset_usa_bea-nipa-selected.zip',
    'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    'dataset_usa_brown.zip',
    'dataset_usa_cobb-douglas.zip',
    'dataset_usa_kendrick.zip',
    'dataset_usa_mc_connell_brue.zip',
)


def extract_can_annual(file_id: int, series_id: str) -> DataFrame:
    '''
    DataFrame Fetching from CANSIM Zip Archives
    '''
    USECOLS = {
        2820012: (5, 7,),
        3800102: (4, 6,),
        3800106: (3, 5,),
        3800518: (4, 6,),
        3800566: (3, 5,),
        3800567: (4, 6,),
    }
    df = pd.read_csv(
        f'dataset_can_{file_id:08n}-eng.zip', usecols=[0, *USECOLS[file_id]]
    )
    df = df[df.iloc[:, 1] == series_id].iloc[:, [0, 2]]
    df.columns = [df.columns[0].upper(), series_id]
    df.set_index(df.columns[0], inplace=True)
    df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0])
    return df


def extract_can_capital_query_archived() -> list[str]:
    '''
    Fetch <SERIES_IDS> from CANSIM Table 031-0004: Flows and stocks of fixed
    non-residential capital, total all industries, by asset, provinces and
    territories, annual (dollars x 1,000,000)
    '''
    # =========================================================================
    # TODO: Consider Using sqlite3
    # =========================================================================
    # =========================================================================
    # https://blog.panoply.io/how-to-read-a-sql-query-into-a-pandas-dataframe
    # =========================================================================
    ARCHIVE_NAME = 'dataset_can_00310004-eng.zip'
    df = pd.read_csv(ARCHIVE_NAME, usecols=[2, 4, 5, 6])
    query = (df.iloc[:, 0].str.contains('2007 constant prices')) & \
            (df.iloc[:, 1] == 'Geometric (infinite) end-year net stock') & \
            (df.iloc[:, 2].str.contains('industrial', flags=re.IGNORECASE))
    df = df[query]
    return sorted(set(df.iloc[:, -1]))


def extract_can_capital_query(df: DataFrame) -> list[str]:
    '''
    Fetch <SERIES_IDS> from Statistics Canada. Table: 36-10-0238-01\
    (formerly CANSIM 031-0004): Flows and stocks of fixed non-residential\
    capital, total all industries, by asset, provinces and territories, annual\
    (dollars x 1,000,000)    
    '''
    # =========================================================================
    # ?: 36100096-eng.zip'
    # =========================================================================
    # =========================================================================
    # usecols = [3, 5, 6, 11]
    # =========================================================================
    query = (df.iloc[:, 0].str.contains('2007 constant prices')) &\
            (df.iloc[:, 1] == 'Straight-line end-year net stock') &\
            (df.iloc[:, 2].str.contains('Industrial'))
    df = df[query]
    return sorted(set(df.iloc[:, -1]))


def extract_can_capital_query() -> list[str]:
    '''
    Fetch <SERIES_IDS> from Statistics Canada. Table: 36-10-0238-01 (formerly
    CANSIM 031-0004): Flows and stocks of fixed non-residential capital, total
    all industries, by asset, provinces and territories, annual
    (dollars x 1,000,000)
    '''
    URL = 'https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip'
    df = extract_can_from_url(URL, usecols=[3, 4, 5, 11])
    query = (df.iloc[:, 0].str.contains('2012 constant prices')) & \
            (df.iloc[:, 1].str.contains('manufacturing', flags=re.IGNORECASE)) & \
            (df.iloc[:, 2] == 'Linear end-year net stock')
    df = df[query]
    return sorted(set(df.iloc[:, -1]))


def extract_can_capital(series_ids: list[str]) -> DataFrame:
    '''
    Fetch <DataFrame> from Statistics Canada. Table: 36-10-0238-01 (formerly
    CANSIM 031-0004): Flows and stocks of fixed non-residential capital, total
    all industries, by asset, provinces and territories, annual
    (dollars x 1,000,000)
    '''
    URL = 'https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip'
    _df = extract_can_from_url(URL, usecols=[0, 11, 13])
    _df = _df[_df.iloc[:, 1].isin(series_ids)]
    df = DataFrame()
    for series_id in series_ids:
        chunk = _df[_df.iloc[:, 1] == series_id].iloc[:, [0, 2]]
        chunk.columns = [chunk.columns[0], series_id]
        chunk.set_index(chunk.columns[0],
                        inplace=True,
                        verify_integrity=True)
        df = pd.concat([df, chunk], axis=1, sort=True)
    df['sum'] = df.sum(axis=1)
    return df.iloc[:, [-1]]


def extract_can(df: DataFrame, series_id: str) -> DataFrame:
    '''
    Data Frame Fetching from CANSIM Zip Archives
    '''
    df = df[df.iloc[:, 10] == series_id].iloc[:, [0, 12]]
    df.iloc[:, 0] = df.iloc[:, 0].astype(int)
    df.iloc[:, 1] = df.iloc[:, 1].astype(float)
    df.columns = [df.columns[0], series_id]
    return df.set_index(df.columns[0])


def extract_can_fixed_assets(series_ids: list[str]) -> DataFrame:
    '''
    Fetch <SERIES_IDS> from CANSIM Table 031-0004: Flows and stocks of fixed
    non-residential capital, total all industries, by asset, provinces and
    territories, annual (dollars x 1,000,000)
    '''
    ARCHIVE_NAME = 'dataset_can_00310004-eng.zip'
    _df = pd.read_csv(ARCHIVE_NAME, usecols=[0, 6, 8])
    _df = _df[_df.iloc[:, 1].isin(series_ids)]
    _df.iloc[:, 2] = pd.to_numeric(
        _df.iloc[:, 2], errors='coerce')
    df = DataFrame()
    for series_id in series_ids:
        chunk = _df[_df.iloc[:, 1] == series_id].iloc[:, [0, 2]]
        chunk.columns = [chunk.columns[0].upper(), series_id]
        chunk.set_index(chunk.columns[0],
                        inplace=True,
                        verify_integrity=True)
        df = pd.concat([df, chunk], axis=1, sort=True)
    df['sum'] = df.sum(axis=1)
    return df.iloc[:, [-1]]


def extract_can_from_url(url: str, usecols: list = None) -> DataFrame:
    '''Downloading zip file from url'''
    name = url.split('/')[-1]
    if os.path.exists(name):
        with ZipFile(name, 'r').open(name.replace('-eng.zip', '.csv')) as f:
            return pd.read_csv(f, usecols=usecols)
    else:
        r = requests.get(url)
        with ZipFile(io.BytesIO(r.content)).open(name.replace('-eng.zip', '.csv')) as f:
            return pd.read_csv(f, usecols=usecols)


def extract_can_group_a(file_id: int, skiprows) -> DataFrame:
    # =========================================================================
    # Not Used Anywhere
    # =========================================================================
    df = pd.read_csv(f'dataset_can_cansim{file_id:n}.csv', skiprows=skiprows)
    if file_id == 7931814471809016759:
        df.columns = [column[:7] for column in df.columns]
        df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1].str.replace(';', ''))
    df = df.set_index(df.columns[0]).transpose()
    df.reset_index(inplace=True)
    df[['quarter', 'period', ]] = df.iloc[:, 0].str.split(expand=True)
    df.set_index(df.columns[0], inplace=True)
    return df.groupby(df.columns[-1]).mean()


def extract_can_group_b(file_id: int, skiprows) -> DataFrame:
    # =========================================================================
    # Not Used Anywhere
    # =========================================================================
    df = pd.read_csv(f'dataset_can_cansim{file_id:n}.csv', skiprows=skiprows)
    df[['month', 'period', ]] = df.iloc[:, 0].str.split('-', expand=True)
    return df.groupby(df.columns[-1]).mean()


def extract_can_quarter(df: DataFrame, series_id: str) -> DataFrame:
    '''
    Data Frame Fetching from Quarterly Data within CANSIM Zip Archives
    '''
    df = df[df.iloc[:, 10] == series_id].iloc[:, [0, 12]]
    df.columns = [df.columns[0], series_id]
    df[['period', 'sub_period', ]] = df.iloc[:, 0].str.split('-', expand=True)
    df.iloc[:, 1] = df.iloc[:, 1].astype(float)
    df.iloc[:, -2] = df.iloc[:, -2].astype(int)
    return df.groupby(df.columns[-2]).sum()


def extract_can_quarter(file_id, series_id: str) -> DataFrame:
    '''
    Data Frame Fetching from Quarterly Data within CANSIM Zip Archives
    Should Be [x 7 columns]
    '''
    RESERVED_FILE_IDS = (2820011, 2820012, 3790031, 3800068,)
    RESERVED_COMBINATIONS = ((3790031, 'v65201809',),
                             (3800084, 'v62306938',),)
    USECOLS = ((4, 6,), (5, 7,),)
    usecols = (USECOLS[0], USECOLS[1])[file_id in RESERVED_FILE_IDS]
    df = pd.read_csv(f'dataset_can_{file_id:08n}-eng.zip',
                     usecols=[0, *usecols])
    df = df[df.iloc[:, 1] == series_id].iloc[:, [0, 2]]
    df.columns = [df.columns[0], series_id]
    df[['period', 'sub_period', ]] = df.iloc[:, 0].str.split('/', expand=True)
    df.iloc[:, 1] = df.iloc[:, 1].astype(float)
    df.iloc[:, -2] = df.iloc[:, -2].astype(int)
    if (file_id, series_id,) in RESERVED_COMBINATIONS:
        return df.groupby(df.columns[-2]).sum()
    else:
        return df.groupby(df.columns[-2]).mean()


def extract_usa_bea(archive_name: str, wb_name: str, sh_name: str, series_id: str) -> DataFrame:
    '''
    Data Frame Fetching from Bureau of Economic Analysis Zip Archives

    Parameters
    ----------
    archive_name : str
        DESCRIPTION.
    wb_name : str
        DESCRIPTION.
    sh_name : str
        DESCRIPTION.
    series_id : str
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    with pd.ExcelFile(ZipFile(archive_name, 'r').open(wb_name)) as xl_file:
        # =====================================================================
        # Load
        # =====================================================================
        df = pd.read_excel(xl_file, sh_name, skiprows=7)
        # =====================================================================
        # Re-Load
        # =====================================================================
        df = pd.read_excel(xl_file,
                           sh_name,
                           usecols=range(2, df.shape[1]),
                           skiprows=7)
    df.dropna(axis=0, inplace=True)
    df.columns = ['period', *df.columns[1:]]
    df = df.set_index(df.columns[0]).transpose()
    return df.loc[:, [series_id]]


def extract_usa_bea_filter(series_id: str) -> DataFrame:
    '''
    Retrieve Yearly Data for BEA Series' Code
    '''
    ARCHIVE_NAME = 'dataset_usa_bea-nipa-2015-05-01.zip'
    _df = pd.read_csv(ARCHIVE_NAME, usecols=[0, *range(14, 18)])
    query = (_df.iloc[:, 1] == series_id) & \
            (_df.iloc[:, 3] == 0)
    _df = _df[query]
    df = DataFrame()
    for source_id in sorted(set(_df.iloc[:, 0])):
        chunk = _df[_df.iloc[:, 0] == source_id].iloc[:, [2, 4]]
        chunk.columns = [chunk.columns[0],
                         '{}{}'.format(source_id.split()[1].replace('.', '_'), series_id)]
        chunk.drop_duplicates(inplace=True)
        chunk.set_index(chunk.columns[0], inplace=True, verify_integrity=True)
        df = pd.concat([df, chunk], axis=1, sort=True)
    return df


def extract_usa_bea_from_loaded(df: DataFrame, series_id: str) -> DataFrame:
    '''`NipaDataA.txt`: U.S. Bureau of Economic Analysis'''
    df = df[df.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    df.columns = [df.columns[0].lower(), series_id]
    return df.set_index(df.columns[0], verify_integrity=True)


def extract_usa_bea_from_url(url: str) -> DataFrame:
    '''Retrieves U.S. Bureau of Economic Analysis DataFrame from URL'''
    return pd.read_csv(io.BytesIO(requests.get(url).content), thousands=',')


def extract_usa_bea_sfat_series() -> DataFrame:
    ARCHIVE_NAME = 'dataset_usa_bea-nipa-selected.zip'
    SERIES_ID = 'k3n31gd1es000'
    _df = pd.read_csv(ARCHIVE_NAME, usecols=[0, *range(8, 11)])
    _df = _df[_df.iloc[:, 1] == SERIES_ID]
    control_frame = DataFrame()
    for source_id in sorted(set(_df.iloc[:, 0])):
        chunk = _df[_df.iloc[:, 0] == source_id].iloc[:, [2, 3]]
        chunk.columns = [chunk.columns[0],
                         '{}{}'.format(source_id.split()[1].replace('.', '_'), SERIES_ID)]
        chunk.set_index(chunk.columns[0], inplace=True, verify_integrity=True)
        control_frame = pd.concat([control_frame, chunk], axis=1, sort=True)

    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAME = 'Section4ALL_xls.xls'
    SH_NAME = '403 Ann'
    # =========================================================================
    # Fixed Assets Series, 1925--2016
    # =========================================================================
    SERIES_IDS = ('k3n31gd1es000', 'k3n31gd1eq000',
                  'k3n31gd1ip000', 'k3n31gd1st000',)
    test_frame = pd.concat(
        [
            extract_usa_bea(ARCHIVE_NAME, WB_NAME, SH_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    return pd.concat([test_frame, control_frame], axis=1, sort=True)


def extract_usa_bls(file_name, series_id: str) -> DataFrame:
    '''
    Bureau of Labor Statistics Data Fetch
    '''
    df = pd.read_csv(file_name,
                     sep='\t',
                     usecols=range(4),
                     low_memory=False)
    query = (df.iloc[:, 0].str.contains(series_id)) & \
            (df.iloc[:, 2] == 'M13')
    df = df[query].iloc[:, [1, 3]]
    df.columns = [df.columns[0], series_id]
    df.iloc[:, 0] = df.iloc[:, 0].astype(int)
    df.iloc[:, 1] = df.iloc[:, 1].astype(float)
    return df.set_index(df.columns[0])


def extract_usa_census(archive_name: str, series_id: str) -> DataFrame:
    '''
    Selected Series by U.S. Bureau of the Census
    U.S. Bureau of the Census, Historical Statistics of the United States,
    1789--1945, Washington, D.C., 1949.
    U.S. Bureau of the Census. Historical Statistics of the United States,
    Colonial Times to 1970, Bicentennial Edition. Washington, D.C., 1975.
    '''
    df = pd.read_csv(archive_name,
                     usecols=range(8, 11),
                     dtype=str)
    df = df[df.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    df.iloc[:, 0] = df.iloc[:, 0].str[:4].astype(int)
    df.iloc[:, 1] = df.iloc[:, 1].astype(float)
    df.columns = [df.columns[0], series_id]
    df.sort_values(df.columns[0], inplace=True)
    return df.groupby(df.columns[0]).mean()


def extract_usa_census_description(archive_name: str, series_id: str) -> str:
    '''Retrieve Series Description U.S. Bureau of the Census'''
    FLAG = 'no_details'
    _df = pd.read_csv(
        archive_name,
        usecols=[0, 1, 3, 4, 5, 6, 8],
        low_memory=False
    )
    _df = _df[_df.iloc[:, 6] == series_id]
    _df.drop_duplicates(inplace=True)
    if _df.iloc[0, 2] == FLAG:
        if _df.iloc[0, 5] == FLAG:
            if _df.iloc[0, 4] == FLAG:
                description = '{}'.format(_df.iloc[0, 3])
            else:
                description = '{} -\n{}'.format(*_df.iloc[0, [3, 4]])
        else:
            description = '{} -\n{} -\n{}'.format(*_df.iloc[0, [3, 4, 5]])
    else:
        if _df.iloc[0, 5] == FLAG:
            if _df.iloc[0, 4] == FLAG:
                description = '{}; {}'.format(*_df.iloc[0, [3, 2]])
            else:
                description = '{} -\n{}; {}'.format(*_df.iloc[0, [3, 4, 2]])
        else:
            description = '{} -\n{} -\n{}; {}'.format(
                *_df.iloc[0, [3, 4, 5, 2]])
    return description


def extract_usa_classic(archive_name: str, series_id: str) -> DataFrame:
    '''
    Data Fetch Procedure for Enumerated Classical Datasets
    '''
    USECOLS = {
        'dataset_douglas.zip': (4, 7,),
        'dataset_usa_brown.zip': (3, 6,),
        'dataset_usa_cobb-douglas.zip': (5, 8,),
        'dataset_usa_kendrick.zip': (4, 7,),
    }
    df = pd.read_csv(
        archive_name,
        skiprows=(None, 4)[archive_name == 'dataset_usa_brown.zip'],
        usecols=range(*USECOLS[archive_name])
    )
    df = df[df.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    df.iloc[:, 0] = df.iloc[:, 0].astype(int)
    df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
    df.columns = [df.columns[0], series_id]
    return df.set_index(df.columns[0])


def extract_usa_mcconnel(series_id: str) -> DataFrame:
    '''Data Frame Fetching from McConnell C.R. & Brue S.L.'''
    ARCHIVE_NAME = 'dataset_usa_mc_connell_brue.zip'
    df = pd.read_csv(ARCHIVE_NAME, index_col=1, usecols=range(1, 4))
    df = df[df.iloc[:, 0] == series_id].iloc[:, [1]]
    return df.sort_index()


def extract_usa_nber(file_name: str, agg: str) -> DataFrame:
    _df = pd.read_csv(file_name)
    _df.drop(_df.columns[0], axis=1, inplace=True)
    if agg == 'mean':
        return _df.groupby(_df.columns[0]).mean()
    elif agg == 'sum':
        return _df.groupby(_df.columns[0]).sum()


def extract_world_bank(df: DataFrame, series_id: str) -> DataFrame:
    chunk = df[df.iloc[:, 1] == series_id].iloc[:, [0, 2]]
    chunk.columns = [chunk.columns[0], series_id]
    return chunk.set_index(df.columns[0])


def extract_series_ids(archive_name: str) -> dict[str]:
    '''Returns Dictionary for Series from Douglas's & Kendrick's Databases'''
    df = pd.read_csv(archive_name, usecols=[3, 4, ])
    return dict(zip(df.iloc[:, 1], df.iloc[:, 0]))
