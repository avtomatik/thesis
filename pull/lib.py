#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 23:56:20 2022

@author: Alexander Mikhailov
"""


import sqlite3
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from transform.lib import numerify


def pull_by_series_id(df: DataFrame, series_id: str) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    series_id : str

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id].iloc[:, [1]].rename(
        columns={"value": series_id}
    )


def pull_can_aggregate(df: DataFrame, series_id: str) -> DataFrame:
    """
    Retrieves DataFrame from Quarterly Data within CANSIM Zip Archives
    Parameters
    ----------
    df : DataFrame
    series_id : str

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    _df = df.loc[:, ('series_id', 'value')].pipe(
        pull_by_series_id, series_id).pipe(numerify)
    if 'seas' in df.columns:
        return _df.groupby(_df.index.year).sum()
    return _df.groupby(_df.index.year).mean()


def pull_can_capital(df: DataFrame, params: tuple[int, str]) -> DataFrame:
    """
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
    DataFrame

    """
    DIR = "/home/green-machine/data_science"
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
    with sqlite3.connect(Path(DIR).joinpath(f"{DBNAME}.db")) as conn:
        cursor = conn.cursor()
        df.to_sql(DBNAME, conn, if_exists="replace", index=True)
        cursor = conn.execute(stmt)
        return pd.DataFrame(
            cursor.fetchall(),
            columns=("period", "geo", "prices", "industry", "category",
                     "component", "series_id", "value")
        )


def pull_can_capital_former(df: DataFrame, params: tuple[int, str]) -> DataFrame:
    """
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
    DataFrame

    """
    DIR = "/home/green-machine/data_science"
    DBNAME = "capital"
    stmt = f"""
    SELECT * FROM {DBNAME}
    WHERE
        prices LIKE '%{params[0]} constant prices%'
        AND category = '{params[1]}'
        AND lower(component) LIKE '%{params[-1]}%'
    ;
    """
    with sqlite3.connect(Path(DIR).joinpath(f"{DBNAME}.db")) as conn:
        cursor = conn.cursor()
        df.to_sql(DBNAME, conn, if_exists="replace", index=True)
        cursor = conn.execute(stmt)
        return pd.DataFrame(
            cursor.fetchall(),
            columns=("period", "prices", "category", "component",
                     "series_id", "value")
        )


def pull_series_ids_description(archive_name: str) -> dict[str, str]:
    """Returns Dictionary for Series from Douglas's & Kendrick's Databases"""
    kwargs = {
        'filepath_or_buffer': archive_name,
        'index_col': 1,
        'usecols': (3, 4),
    }
    return pd.read_csv(**kwargs).to_dict().get('description')


def pull_uscb_description(series_id: str) -> str:
    """
    Retrieves Series Description U.S. Bureau of the Census

    Parameters
    ----------
    series_id : str

    Returns
    -------
    str
        Series Description.

    """
    MAP = {
        'source': 0,
        'table': 1,
        'note': 3,
        'group1': 4,
        'group2': 5,
        'group3': 6,
        'series_id': 9
    }
    kwargs = {
        'filepath_or_buffer': 'dataset_uscb.zip',
        'header': 0,
        'names': tuple(MAP.keys()),
        'usecols': tuple(MAP.values()),
        'low_memory': False
    }
    df = pd.read_csv(**kwargs)
    lookup_columns = ('group1', 'group2', 'group3', 'note')
    df = df[df.loc[:, 'series_id'] == series_id].loc[:, lookup_columns]
    df.drop_duplicates(inplace=True)
    return '\n'.join(_ for _ in dict(df.iloc[0, :]).values() if isinstance(_, str))
