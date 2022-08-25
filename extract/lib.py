#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 00:44:36 2022
@author: alexander
"""


import io
import os
import sqlite3
from zipfile import ZipFile
from functools import cache
from pathlib import Path
import pandas as pd
import requests
from pandas import DataFrame


ARCHIVE_NAMES_UTILISED = (
    'dataset_douglas.zip',
    'dataset_usa_brown.zip',
    'dataset_usa_cobb-douglas.zip',
    'dataset_usa_kendrick.zip',
    'dataset_usa_mc_connell_brue.zip',
)


@cache
def read_manager_can(archive_id: int) -> DataFrame:
    MAP = {
        14100027: {'ref_date': 0, 'series_id': 10, 'value': 12},
        36100096:
            {
                'ref_date': 0,
                'geo': 1,
                'prices': 3,
                'industry': 4,
                'category': 5,
                'component': 6,
                'series_id': 11,
                'value': 13
        },
        36100434: {'ref_date': 0, 'series_id': 10, 'value': 12},
    }
    url = f'https://www150.statcan.gc.ca/n1/tbl/csv/{archive_id}-eng.zip'
    kwargs = {
        'header': 0,
        'names': tuple(MAP.get(archive_id).keys()),
        'index_col': 0,
        'usecols': tuple(MAP.get(archive_id).values()),
        'parse_dates': archive_id == 36100434
    }
    return read_from_url_can(url, **kwargs)


def read_manager_can_annual(archive_id: int) -> DataFrame:
    '''
    Collects Summarized Data from CANSIM Table 031-0004: Flows and stocks of
    fixed non-residential capital, total all industries, by asset, provinces
    and territories, annual (dollars x 1,000,000) by <SERIES_IDS>
    Parameters
    ----------
    series_ids : list[str]
        DESCRIPTION.
    Returns
    -------
    DataFrame
    '''
    '''
    Fetch <SERIES_IDS> from CANSIM Table 031-0004: Flows and stocks of fixed
    non-residential capital, total all industries, by asset, provinces and
    territories, annual (dollars x 1,000,000)
    '''
    '''
    Retrieves DataFrame from CANSIM Zip Archives
    '''
    MAP = {
        310004: {
            'ref_date': 0,
            'prices': 2,
            'category': 4,
            'component': 5,
            'series_id': 6,
            'value': 8,
        },
        2820012: {'ref_date': 0, 'series_id': 5, 'value': 7},
        3800102: {'ref_date': 0, 'series_id': 4, 'value': 6},
        3800106: {'ref_date': 0, 'series_id': 3, 'value': 5},
        3800518: {'ref_date': 0, 'series_id': 4, 'value': 6},
        3800566: {'ref_date': 0, 'series_id': 3, 'value': 5},
        3800567: {'ref_date': 0, 'series_id': 4, 'value': 6},
    }
    return pd.read_csv(
        f'dataset_can_{archive_id:08n}-eng.zip',
        header=0,
        names=tuple(MAP.get(archive_id).keys()),
        index_col=0,
        usecols=tuple(MAP.get(archive_id).values()),
    )


def pull_can_annual(df: DataFrame, series_id: str) -> DataFrame:
    '''
    Retrieves DataFrame from CANSIM Zip Archives
    '''
    df = df[df.iloc[:, 0] == series_id].iloc[:, [1]]
    df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    return df


@cache
def read_from_url_can(url: str, **kwargs) -> DataFrame:
    '''
    Downloading zip file from url
    Parameters
    ----------
    url : str
        DESCRIPTION.
    **kwargs : TYPE
        DESCRIPTION.
    Returns
    -------
    DataFrame
        DESCRIPTION.
    '''
    name = url.split('/')[-1]
    if os.path.exists(name):
        with ZipFile(name, 'r').open(name.replace('-eng.zip', '.csv')) as f:
            return pd.read_csv(f, **kwargs)
    else:
        r = requests.get(url)
        with ZipFile(io.BytesIO(r.content)).open(name.replace('-eng.zip', '.csv')) as f:
            return pd.read_csv(f, **kwargs)


def read_pull_can_quarter(file_id: int, series_id: str) -> DataFrame:
    '''
    Retrieves DataFrame from Quarterly Data within CANSIM Zip Archives
    Should Be [x 7 columns]
    '''
    RESERVED_FILE_IDS = (2820011, 2820012, 3790031, 3800068,)
    RESERVED_COMBINATIONS = (
        (3790031, 'v65201809',),
        (3800084, 'v62306938',),
    )
    USECOLS = ((4, 6,), (5, 7,),)
    usecols = (USECOLS[0], USECOLS[1])[file_id in RESERVED_FILE_IDS]
    _df = pd.read_csv(
        f'dataset_can_{file_id:08n}-eng.zip',
        header=0,
        names=('REF_DATE', 'series_id', series_id),
        index_col=0,
        usecols=tuple(0, *usecols),
    )
    # =========================================================================
    # TODO: Extract to __call__
    # =========================================================================
    _df = _df[_df.iloc[:, 0] == series_id].iloc[:, [1]]
    _df.index = pd.to_numeric(
        _df.index.astype(str).to_series().str.slice(stop=4),
        downcast='integer'
    )
    _df.iloc[:, 0] = pd.to_numeric(_df.iloc[:, 0], errors='coerce')
    if (file_id, series_id,) in RESERVED_COMBINATIONS:
        return _df.groupby(_df.index).sum()
    return _df.groupby(_df.index).mean()


def extract_usa_bea(archive_name: str, wb_name: str, sh_name: str, series_id: str) -> DataFrame:
    '''
    Retrieves DataFrame from Bureau of Economic Analysis Zip Archives
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
        df = pd.read_excel(
            xl_file,
            sh_name,
            index_col=0,
            usecols=range(2, df.shape[1]),
            skiprows=7
        ).dropna(axis=0).transpose()
    return df.loc[:, [series_id]]


@cache
def extract_usa_bea_from_url(url: str) -> DataFrame:
    '''Retrieves U.S. Bureau of Economic Analysis DataFrame from URL'''
    try:
        return pd.read_csv(
            io.BytesIO(requests.get(url).content),
            header=0,
            names=('series_ids', 'period', 'value'),
            index_col=1,
            thousands=',',
        )
    except requests.ConnectionError:
        return pd.read_csv(
            url.split('/')[-1],
            header=0,
            names=('series_ids', 'period', 'value'),
            index_col=1,
            thousands=',',
        )


def extract_usa_bls(file_name: str, series_id: str) -> DataFrame:
    '''
    Bureau of Labor Statistics Data Fetch

    Parameters
    ----------
    file_name : str
        DESCRIPTION.
    series_id : str
        DESCRIPTION.

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    _df = pd.read_csv(
        file_name,
        sep='\t',
        header=0,
        names=('series_id', 'period', 'sub_period', series_id),
        index_col=1,
        usecols=range(4),
        low_memory=False
    )
    _q = (_df.iloc[:, 0].str.contains(series_id)) & (_df.iloc[:, 1] == 'M13')
    _df.index = pd.to_numeric(
        _df.index.astype(str).to_series().str.slice(stop=4),
        downcast='integer'
    )
    _df.iloc[:, -1] = pd.to_numeric(_df.iloc[:, -1], errors='coerce')
    return _df[_q].iloc[:, [-1]]


def extract_usa_frb_ms() -> DataFrame:
    '''
    Money Stock Measures (H.6) Series
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      M1
    ================== =================================
    '''
    URL = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H6&series=5398d8d1734b19f731aba3105eb36d47&lastobs=&from=01/01/1959&to=12/31/2018&filetype=csv&label=include&layout=seriescolumn'
    _df = pd.read_csv(
        io.BytesIO(requests.get(URL).content),
        header=0,
        names=('period', 'm1_m'),
        index_col=0,
        usecols=range(2),
        skiprows=5,
        parse_dates=True,
    )
    return _df.groupby(_df.index.year).mean()


def extract_usa_fred(series_id: str) -> DataFrame:
    '''
    ('PPIACO', 'PRIME',)
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    URL = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
    _df = pd.read_csv(
        io.BytesIO(requests.get(URL).content),
        header=0,
        names=('period', series_id.lower()),
        index_col=0,
        parse_dates=True,
    )
    return _df.groupby(_df.index.year).mean()


def extract_usa_hist(archive_name: str, series_id: str) -> DataFrame:
    '''
    Extract Data from Enumerated Historical Datasets
    Parameters
    ----------
    archive_name : str
        DESCRIPTION.
    series_id : str
        DESCRIPTION.
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    USECOLS = {
        'dataset_douglas.zip': (4, 7,),
        'dataset_usa_brown.zip': (3, 6,),
        'dataset_usa_census1949.zip': (8, 11,),
        'dataset_usa_census1975.zip': (8, 11,),
        'dataset_usa_cobb-douglas.zip': (5, 8,),
        'dataset_usa_kendrick.zip': (4, 7,),
    }
    df = pd.read_csv(
        archive_name,
        header=0,
        names=('series_id', 'period', series_id),
        index_col=1,
        skiprows=(0, 4)[archive_name == 'dataset_usa_brown.zip'],
        usecols=range(*USECOLS[archive_name]),
        dtype=str,
    )
    # =========================================================================
    # TODO: Extract to __call__
    # =========================================================================
    df = df[df.iloc[:, 0] == series_id].iloc[:, [1]]
    df.index = pd.to_numeric(
        df.index.astype(str).to_series().str.slice(stop=4),
        downcast='integer'
    )
    df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    if 'census' in archive_name:
        return df.groupby(df.index).mean()
    return df.sort_index()


def extract_usa_mcconnel(series_id: str) -> DataFrame:
    '''
    Retrieves DataFrame from McConnell C.R. & Brue S.L.

    Parameters
    ----------
    series_id : str
        DESCRIPTION.

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    ARCHIVE_NAME = 'dataset_usa_mc_connell_brue.zip'
    MAP = {
        'prime_rate': 'Ставка прайм-рейт, %',
        'A006RC1': 'Валовой объем внутренних частных инвестиций, млрд долл. США',
        'A032RC1': 'Национальный доход, млрд долл. США',
        'A191RC1': 'Валовой внутренний продукт, млрд долл. США',
    }
    df = pd.read_csv(
        ARCHIVE_NAME,
        header=0,
        names=('series_id', 'period', series_id),
        index_col=1,
        usecols=range(1, 4)
    )
    return df[df.iloc[:, 0] == MAP[series_id]].iloc[:, [1]].sort_index()


def extract_usa_nber(file_name: str, agg: str) -> DataFrame:
    _df = pd.read_csv(file_name)
    _df.drop(_df.columns[0], axis=1, inplace=True)
    if agg == 'mean':
        return _df.groupby(_df.columns[0]).mean()
    return _df.groupby(_df.columns[0]).sum()


def extract_worldbank() -> DataFrame:
    URL = 'https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv'
    with ZipFile(io.BytesIO(requests.get(URL).content)) as archive:
        _map = {_.file_size: _.filename for _ in archive.filelist}
        # =====================================================================
        # Select Largest File
        # =====================================================================
        with archive.open(_map[max(_map)]) as f:
            df = pd.read_csv(
                f,
                index_col=0,
                skiprows=4
            ).dropna(axis=1, how='all').transpose()
            df.drop(df.index[:3], inplace=True)
            return df.rename_axis('period')


def pull_can_capital(df: DataFrame, params: tuple[int, str]) -> DataFrame:
    '''
    WARNING: VERY EXPENSIVE OPERATION !
    Retrieves Series IDs from Statistics Canada -- Fixed Assets Tables

    Parameters
    ----------
    df : DataFrame
    params : tuple[int, str]
        param : BASE_YEAR : Basic Price Year.
        param : CATEGORY : Estimate Basis.
        param : COMPONENT : Search Key Word

    Returns
    -------
    list[str]
        SERIES_IDS.
    '''
    DIR = Path("/home/alexander/science")
    DBNAME = "capital"
    stmt = f"""
    SELECT * FROM {DBNAME}
    WHERE
        geo = 'Canada'
        AND prices LIKE '%{params[0]} constant prices%'
        AND industry = '{params[1]}'
        AND category = '{params[2]}'
        AND component IN {params[-1]}
    ;
    """
    with sqlite3.connect(DIR.joinpath(f"{DBNAME}.db")) as conn:
        cursor = conn.cursor()
        df.to_sql(DBNAME, conn, if_exists="replace", index=True)
        cursor = conn.execute(stmt)
        return pd.DataFrame(
            cursor.fetchall(),
            columns=("ref_date", "geo", "prices", "industry", "category",
                     "component", "series_id", "value")
        )


def pull_can_capital_former(df: DataFrame, params: tuple[int, str]) -> DataFrame:
    '''
    Retrieves Series IDs from Statistics Canada -- Fixed Assets Tables

    Parameters
    ----------
    df : DataFrame
    params : tuple[int, str]
        param : BASE_YEAR : Basic Price Year.
        param : CATEGORY : Estimate Basis.
        param : COMPONENT : Search Key Word

    Returns
    -------
    list[str]
        SERIES_IDS.
    '''
    DIR = Path("/home/alexander/science")
    DBNAME = "capital"
    stmt = f"""
    SELECT * FROM {DBNAME}
    WHERE
        prices LIKE '%{params[0]} constant prices%'
        AND category = '{params[1]}'
        AND lower(component) LIKE '%{params[-1]}%'
    ;
    """
    with sqlite3.connect(DIR.joinpath(f"{DBNAME}.db")) as conn:
        cursor = conn.cursor()
        df.to_sql(DBNAME, conn, if_exists="replace", index=True)
        cursor = conn.execute(stmt)
        return pd.DataFrame(
            cursor.fetchall(),
            columns=("ref_date", "prices", "category", "component",
                     "series_id", "value")
        )


def pull_can(df: DataFrame, series_id: str) -> DataFrame:
    '''
    Retrieves DataFrame from CANSIM Zip Archives
    Parameters
    ----------
    df : DataFrame
        Retrieved with read_from_url_can().
    series_id : str
        DESCRIPTION.
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    assert df.shape[1] == 2
    df = df[df.iloc[:, 0] == series_id].iloc[:, [1]]
    # =========================================================================
    # TODO: Extract to __call__
    # =========================================================================
    df.index = pd.to_numeric(
        df.index.astype(str).to_series().str.slice(stop=4),
        downcast='integer'
    )
    df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    return df.rename(columns={"value": series_id})


def pull_can_quarter(df: DataFrame, series_id: str) -> DataFrame:
    '''
    DataFrame Fetching from Quarterly Data within CANSIM Zip Archives
    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.
    series_id : str
        DESCRIPTION.
    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    assert df.shape[1] == 2
    df = df[df.iloc[:, 0] == series_id].iloc[:, [1]]
    df.rename(columns={"value": series_id}, inplace=True)
    return df.groupby(df.index.year).sum()


def retrieve_series_ids(archive_name: str) -> dict[str]:
    '''Returns Dictionary for Series from Douglas's & Kendrick's Databases'''
    df = pd.read_csv(archive_name, usecols=(3, 4, ))
    return dict(zip(df.iloc[:, 1], df.iloc[:, 0]))


def retrieve_usa_bea_from_cached(df: DataFrame, series_id: str) -> DataFrame:
    '''`NipaDataA.txt`: U.S. Bureau of Economic Analysis'''
    _df = df[df.iloc[:, 0] == series_id].iloc[:, [1]]
    return _df.rename(columns={"value": series_id})


def retrieve_uscb_description(
        series_id: str,
        archive_name: str = 'dataset_usa_census1975.zip'
) -> str:
    '''
    Retrieves Series Description U.S. Bureau of the Census

    Parameters
    ----------
    series_id : str
        DESCRIPTION.
    archive_name : ('dataset_usa_census1949.zip' | 'dataset_usa_census1975.zip'), optional
        DESCRIPTION. The default is 'dataset_usa_census1975.zip': str.

    Returns
    -------
    str
        Series Description.

    '''
    FLAG = 'no_details'
    _df = pd.read_csv(
        archive_name,
        usecols=tuple(_ for _ in range(9) if _ not in range(2, 9, 5)),
        low_memory=False
    )
    _df = _df[_df.iloc[:, -1] == series_id]
    _df.drop_duplicates(inplace=True)
    if _df.iloc[0, 2] == FLAG:
        if _df.iloc[0, 5] == FLAG:
            if _df.iloc[0, 4] == FLAG:
                _desc = '{}'.format(_df.iloc[0, 3])
            else:
                _desc = '{} -\n{}'.format(*_df.iloc[0, [3, 4]])
        else:
            _desc = '{} -\n{} -\n{}'.format(*_df.iloc[0, [3, 4, 5]])
    else:
        if _df.iloc[0, 5] == FLAG:
            if _df.iloc[0, 4] == FLAG:
                _desc = '{}; {}'.format(*_df.iloc[0, [3, 2]])
            else:
                _desc = '{} -\n{}; {}'.format(*_df.iloc[0, [3, 4, 2]])
        else:
            _desc = '{} -\n{} -\n{}; {}'.format(*_df.iloc[0, [3, 4, 5, 2]])
    return _desc
