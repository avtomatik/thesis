#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 00:44:36 2022

@author: Alexander Mikhailov
"""


import io
from functools import cache

import pandas as pd
import requests
from pandas import DataFrame


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
        'names': ['series_id', 'period', 'sub_period', 'value'],
        'index_col': 1,
        'usecols': range(4),
        'low_memory': False
    }
    df = pd.read_csv(**kwargs)
    df.loc[:, 'series_id'] = df.loc[:, 'series_id'].str.strip()
    return df[df.loc[:, 'sub_period'] == 'M13'].loc[:, ('series_id', 'value')]


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
        'period', *map(int, map(float, df.columns[1 + _start:]))
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
        'names': ['period', 'm1_m'],
        'index_col': 0,
        'usecols': range(2),
        'skiprows': 5,
        'parse_dates': True
    }
    df = pd.read_csv(**kwargs)
    return df.groupby(df.index.year).agg('mean')


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
    return df.groupby(df.index.year).agg('mean')


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
        'names': ['period', series_id.lower()],
        'index_col': 0,
        'parse_dates': True
    }
    df = pd.read_csv(**kwargs)
    return df.groupby(df.index.year).agg('mean')
