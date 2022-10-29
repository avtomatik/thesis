#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 00:44:36 2022

@author: alexander
"""


import io
from functools import cache
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import requests
from pandas import DataFrame


@cache
def read_can(archive_id: int) -> DataFrame:
    """


    Parameters
    ----------
    archive_id : int

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    ...                ...
    df.iloc[:, -1]     Values
    ================== =================================
    """
    MAP = {
        310004: {
            'period': 0,
            'prices': 2,
            'category': 4,
            'component': 5,
            'series_id': 6,
            'value': 8
        },
        2820011: {
            'period': 0,
            'geo': 1,
            'classofworker': 2,
            'industry': 3,
            'sex': 4,
            'series_id': 5,
            'value': 7
        },
        2820012: {'period': 0, 'series_id': 5, 'value': 7},
        3790031: {
            'period': 0,
            'geo': 1,
            'seas': 2,
            'prices': 3,
            'naics': 4,
            'series_id': 5,
            'value': 7
        },
        3800084: {
            'period': 0,
            'geo': 1,
            'seas': 2,
            'est': 3,
            'series_id': 4,
            'value': 6
        },
        3800102: {'period': 0, 'series_id': 4, 'value': 6},
        3800106: {'period': 0, 'series_id': 3, 'value': 5},
        3800518: {'period': 0, 'series_id': 4, 'value': 6},
        3800566: {'period': 0, 'series_id': 3, 'value': 5},
        3800567: {'period': 0, 'series_id': 4, 'value': 6},
        14100027: {'period': 0, 'series_id': 10, 'value': 12},
        36100096: {
            'period': 0,
            'geo': 1,
            'prices': 3,
            'industry': 4,
            'category': 5,
            'component': 6,
            'series_id': 11,
            'value': 13
        },
        36100434: {'period': 0, 'series_id': 10, 'value': 12}
    }
    _url = f'https://www150.statcan.gc.ca/n1/tbl/csv/{archive_id:08n}-eng.zip'
    kwargs = {
        'header': 0,
        'names': tuple(MAP.get(archive_id).keys()),
        'index_col': 0,
        'usecols': tuple(MAP.get(archive_id).values()),
        'parse_dates': archive_id in (2820011, 3790031, 3800084, 36100434)
    }
    if archive_id < 10 ** 7:
        return pd.read_csv(f'dataset_can_{archive_id:08n}-eng.zip', **kwargs)
    if Path(f'{archive_id:08n}-eng.zip').is_file():
        with ZipFile(f'{archive_id:08n}-eng.zip', 'r').open(f'{archive_id:08n}.csv') as f:
            return pd.read_csv(f, **kwargs)
    with ZipFile(io.BytesIO(requests.get(_url).content)).open(f'{archive_id:08n}.csv') as f:
        return pd.read_csv(f, **kwargs)


@cache
def read_usa_bea(url: str) -> DataFrame:
    """
    Retrieves U.S. Bureau of Economic Analysis DataFrame from URL

    Parameters
    ----------
    url : str

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series IDs
    df.iloc[:, 1]      Values
    ================== =================================
    """
    kwargs = {
        'header': 0,
        'names': ('series_ids', 'period', 'value'),
        'index_col': 1,
        'thousands': ','
    }
    if requests.head(url).status_code == 200:
        kwargs['filepath_or_buffer'] = io.BytesIO(requests.get(url).content)
    else:
        kwargs['filepath_or_buffer'] = url.split('/')[-1]
    return pd.read_csv(**kwargs)


@cache
def read_usa_bea_excel(archive_name: str, wb_name: str, sh_name: str) -> DataFrame:
    """
    Retrieves DataFrame from Bureau of Economic Analysis Zip Archives

    Parameters
    ----------
    archive_name : str
    wb_name : str
    sh_name : str

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, ...]    Series
    ================== =================================
    """
    kwargs = {
        'sheet_name': sh_name,
        'skiprows': 7
    }
    with pd.ExcelFile(ZipFile(archive_name, 'r').open(wb_name)) as xl_file:
        # =====================================================================
        # Load
        # =====================================================================
        kwargs['io'] = xl_file
        _df = pd.read_excel(**kwargs)
        # =====================================================================
        # Re-Load
        # =====================================================================
        kwargs['index_col'] = 0
        kwargs['usecols'] = range(2, _df.shape[1])
        return pd.read_excel(**kwargs).dropna(axis=0).transpose()


def read_usa_bls(file_name: str) -> DataFrame:
    """
    Bureau of Labor Statistics Data Fetch

    Parameters
    ----------
    file_name : str

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series IDs
    df.iloc[:, 1]      Values
    ================== =================================
    """
    kwargs = {
        'filepath_or_buffer': file_name,
        'sep': '\t',
        'header': 0,
        'names': ('series_id', 'period', 'sub_period', 'value'),
        'index_col': 1,
        'usecols': range(4),
        'low_memory': False
    }
    _df = pd.read_csv(**kwargs)
    _df.loc[:, 'series_id'] = _df.loc[:, 'series_id'].str.strip()
    return _df[_df.loc[:, 'sub_period'] == 'M13'].loc[:, ('series_id', 'value')]


def read_usa_frb() -> DataFrame:
    """


    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, ...]    Series
    ================== =================================
    """
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_frb_invest_capital.csv',
        'skiprows': 4,
    }
    # =========================================================================
    # Load
    # =========================================================================
    _df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = ['period', *[int(_) for _ in _df.columns[1:]]]
    kwargs['index_col'] = 0
    # =========================================================================
    # Re-Load
    # =========================================================================
    return pd.read_csv(**kwargs).transpose()


def read_usa_frb_g17() -> DataFrame:
    """


    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, ...]    Series
    ================== =================================
    """
    _start = 5
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_frb_g17_all_annual_2013_06_23.csv',
        'skiprows': 1,
    }
    # =========================================================================
    # Load
    # =========================================================================
    _df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = [
        'period',
        *[int(float(_)) for _ in _df.columns[1 + _start:_df.shape[1]]]
    ]
    kwargs['index_col'] = 0
    kwargs['usecols'] = range(_start, _df.shape[1])
    # =========================================================================
    # Re-Load
    # =========================================================================
    return pd.read_csv(**kwargs).transpose()


def read_usa_frb_ms() -> DataFrame:
    """
    Money Stock Measures (H.6) Series

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      M1
    ================== =================================
    """
    # =========================================================================
    # hex(3**3 * 23 * 197 * 2039 * 445466883143470280668577791313)
    # =========================================================================
    _url = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H6&series=5398d8d1734b19f731aba3105eb36d47&lastobs=&from=01/01/1959&to=12/31/2018&filetype=csv&label=include&layout=seriescolumn'
    kwargs = {
        'filepath_or_buffer': io.BytesIO(requests.get(_url).content),
        'header': 0,
        'names': ('period', 'm1_m'),
        'index_col': 0,
        'usecols': range(2),
        'skiprows': 5,
        'parse_dates': True
    }
    _df = pd.read_csv(**kwargs)
    return _df.groupby(_df.index.year).mean()


def read_usa_frb_us3() -> DataFrame:
    """


    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, ...]    Series
    ================== =================================
    """
    # =========================================================================
    # TODO: https://www.federalreserve.gov/datadownload/Output.aspx?rel=g17&filetype=zip
    # =========================================================================
    # =========================================================================
    # with ZipFile('FRB_g17.zip', 'r').open('G17_data.xml') as f:
    # =========================================================================
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_frb_us3_ip_2018_09_02.csv',
        'skiprows': 7,
        'parse_dates': True
    }
    # =========================================================================
    # Load
    # =========================================================================
    _df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = ['period', *[_.strip() for _ in _df.columns[1:]]]
    kwargs['index_col'] = 0
    # =========================================================================
    # Re-Load
    # =========================================================================
    _df = pd.read_csv(**kwargs)
    return _df.groupby(_df.index.year).mean()


def read_usa_fred(series_id: str) -> DataFrame:
    """
    ('PPIACO', 'PRIME',)

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    """
    _url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
    kwargs = {
        'filepath_or_buffer': io.BytesIO(requests.get(_url).content),
        'header': 0,
        'names': ('period', series_id.lower()),
        'index_col': 0,
        'parse_dates': True
    }
    _df = pd.read_csv(**kwargs)
    return _df.groupby(_df.index.year).mean()


@cache
def read_usa_hist(archive_name: str) -> DataFrame:
    """
    Extract Data from Enumerated Historical Datasets
    Parameters
    ----------
    archive_name : str

    Returns
    -------
    DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series IDs
    df.iloc[:, 1]      Values
    ================== =================================
    """
    MAP = {
        'dataset_douglas.zip': {'series_id': 4, 'period': 5, 'value': 6},
        'dataset_usa_brown.zip': {'series_id': 3, 'period': 4, 'value': 5},
        'dataset_usa_cobb-douglas.zip': {'series_id': 5, 'period': 6, 'value': 7},
        'dataset_usa_kendrick.zip': {'series_id': 4, 'period': 5, 'value': 6},
        'dataset_usa_mc_connell_brue.zip': {'series_id': 1, 'period': 2, 'value': 3},
        'dataset_uscb.zip': {'series_id': 9, 'period': 10, 'value': 11},
    }
    kwargs = {
        'filepath_or_buffer': archive_name,
        'header': 0,
        'names': tuple(MAP.get(archive_name).keys()),
        'index_col': 1,
        'skiprows': (0, 4)[archive_name == 'dataset_usa_brown.zip'],
        'usecols': tuple(MAP.get(archive_name).values()),
    }
    return pd.read_csv(**kwargs)


def read_usa_nber(file_name: str, agg: str) -> DataFrame:
    _df = pd.read_csv(file_name)
    _df.drop(_df.columns[0], axis=1, inplace=True)
    if agg == 'mean':
        return _df.groupby(_df.columns[0]).mean()
    return _df.groupby(_df.columns[0]).sum()


def read_worldbank(source_id: str) -> DataFrame:
    _url = f'https://api.worldbank.org/v2/en/indicator/{source_id}?downloadformat=csv'
    with ZipFile(io.BytesIO(requests.get(_url).content)) as archive:
        _map = {_.file_size: _.filename for _ in archive.filelist}
        # =====================================================================
        # Select Largest File
        # =====================================================================
        with archive.open(_map[max(_map)]) as f:
            kwargs = {
                'filepath_or_buffer': f,
                'index_col': 0,
                'skiprows': 4
            }
            _df = pd.read_csv(**kwargs).dropna(axis=1, how='all').transpose()
            return _df.drop(_df.index[:3]).rename_axis('period')
