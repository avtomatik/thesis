#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 00:44:36 2022

@author: Alexander Mikhailov
"""


import io
from functools import cache
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import requests
from pandas import DataFrame

from .constants import MAP_READ_CAN, MAP_READ_USA_HIST


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
    MAP_DEFAULT = {'period': 0, 'series_id': 10, 'value': 12}
    url = f'https://www150.statcan.gc.ca/n1/tbl/csv/{archive_id:08n}-eng.zip'
    TO_PARSE_DATES = (
        2820011, 3790031, 3800084, 10100094, 14100221, 14100235, 14100238, 14100355, 16100109, 16100111, 36100108, 36100207, 36100434
    )
    kwargs = {
        'header': 0,
        'names': list(MAP_READ_CAN.get(archive_id, MAP_DEFAULT).keys()),
        'index_col': 0,
        'usecols': list(MAP_READ_CAN.get(archive_id, MAP_DEFAULT).values()),
        'parse_dates': archive_id in TO_PARSE_DATES
    }
    if archive_id < 10 ** 7:
        kwargs['filepath_or_buffer'] = f'dataset_can_{archive_id:08n}-eng.zip'
    else:
        if Path(f'{archive_id:08n}-eng.zip').is_file():
            kwargs['filepath_or_buffer'] = ZipFile(
                f'{archive_id:08n}-eng.zip'
            ).open(f'{archive_id:08n}.csv')
        else:
            kwargs['filepath_or_buffer'] = ZipFile(
                io.BytesIO(requests.get(url).content)
            ).open(f'{archive_id:08n}.csv')
    return pd.read_csv(**kwargs)


def read_temporary(
    file_name: str, path_src: str = '/home/green-machine/data_science/data/interim'
) -> DataFrame:
    """


    Parameters
    ----------
    file_name : str
        DESCRIPTION.
    path_src : str, optional
        DESCRIPTION. The default is '/home/green-machine/data_science/data/interim'.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    kwargs = {
        'filepath_or_buffer': Path(path_src).joinpath(file_name),
        'index_col': 0,
    }
    return pd.read_csv(**kwargs)


def read_unstats(url: str = 'https://unstats.un.org/unsd/amaapi/api/file/2') -> DataFrame:
    """


    Parameters
    ----------
    url : str, optional
        DESCRIPTION. The default is 'https://unstats.un.org/unsd/amaapi/api/file/2'.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    kwargs = {
        'io': io.BytesIO(requests.get(url).content),
        'index_col': 1,
        'skiprows': 2,
    }
    return pd.read_excel(**kwargs)


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


def read_usa_bls(filepath_or_buffer: str) -> DataFrame:
    """
    Bureau of Labor Statistics Data Fetch

    Parameters
    ----------
    filepath_or_buffer : str

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
        'filepath_or_buffer': filepath_or_buffer,
        'sep': '\t',
        'header': 0,
        'names': ('series_id', 'period', 'sub_period', 'value'),
        'index_col': 1,
        'usecols': range(4),
        'low_memory': False
    }
    df = pd.read_csv(**kwargs)
    df.loc[:, 'series_id'] = df.loc[:, 'series_id'].str.strip()
    return df[df.loc[:, 'sub_period'] == 'M13'].loc[:, ('series_id', 'value')]


def read_usa_davis_ip() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    kwargs = {
        'io': 'dataset_usa_davis-j-h-ip-total.xls',
        'header': None,
        'names': ('period', 'davis_index'),
        'index_col': 0,
        'skiprows': 5
    }
    return pd.read_excel(**kwargs)


@cache
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
    df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = ('period', *map(int, df.columns[1:]))
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
    df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = (
        'period', *map(int, map(float, df.columns[1 + _start:df.shape[1]]))
    )
    kwargs['index_col'] = 0
    kwargs['usecols'] = range(_start, df.shape[1])
    # =========================================================================
    # Re-Load
    # =========================================================================
    return pd.read_csv(**kwargs).transpose()


def read_usa_frb_h6() -> DataFrame:
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
    url = 'https://www.federalreserve.gov/datadownload/Output.aspx?rel=H6&series=798e2796917702a5f8423426ba7e6b42&lastobs=&from=&to=&filetype=csv&label=include&layout=seriescolumn&type=package'
    kwargs = {
        'filepath_or_buffer': io.BytesIO(requests.get(url).content),
        'header': 0,
        'names': ('period', 'm1_m'),
        'index_col': 0,
        'usecols': range(2),
        'skiprows': 5,
        'parse_dates': True
    }
    df = pd.read_csv(**kwargs)
    return df.groupby(df.index.year).mean()


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
    # with ZipFile('FRB_g17.zip').open('G17_data.xml') as f:
    # =========================================================================
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_frb_us3_ip_2018_09_02.csv',
        'skiprows': 7,
        'parse_dates': True
    }
    # =========================================================================
    # Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = ('period', *map(str.strip, df.columns[1:]))
    kwargs['index_col'] = 0
    # =========================================================================
    # Re-Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    return df.groupby(df.index.year).mean()


def read_usa_fred(series_id: str) -> DataFrame:
    """
    ('PCUOMFGOMFG', 'PPIACO', 'PRIME')

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
    kwargs = {
        'filepath_or_buffer': io.BytesIO(requests.get(url).content),
        'header': 0,
        'names': ('period', series_id.lower()),
        'index_col': 0,
        'parse_dates': True
    }
    df = pd.read_csv(**kwargs)
    return df.groupby(df.index.year).mean()


@cache
def read_usa_hist(filepath_or_buffer: str) -> DataFrame:
    """
    Retrieves Data from Enumerated Historical Datasets
    Parameters
    ----------
    filepath_or_buffer : str

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
        'filepath_or_buffer': filepath_or_buffer,
        'header': 0,
        'names': tuple(MAP_READ_USA_HIST.get(filepath_or_buffer).keys()),
        'index_col': 1,
        'skiprows': (0, 4)[filepath_or_buffer == 'dataset_usa_brown.zip'],
        'usecols': tuple(MAP_READ_USA_HIST.get(filepath_or_buffer).values()),
    }
    return pd.read_csv(**kwargs)


def read_usa_nber(filepath_or_buffer: str) -> DataFrame:
    """


    Parameters
    ----------
    filepath_or_buffer : str
        DESCRIPTION.
    agg : str
        ("mean" | "sum").

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    """
    kwargs = {"filepath_or_buffer": filepath_or_buffer}
    # =========================================================================
    # Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = ('period', *map(str.strip, df.columns[2:]))
    kwargs['index_col'] = 0
    # =========================================================================
    # Re-Load
    # =========================================================================
    return pd.read_csv(**kwargs)
