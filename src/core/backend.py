#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 14:54:44 2023

@author: green-machine
"""


from functools import cache

import pandas as pd
from core.classes import DatasetDesc, SeriesID
from core.read import read_source
from core.transform import transform_rebase
from pandas import DataFrame


def stockpile(series_ids: list[SeriesID]) -> DataFrame:
    """


    Parameters
    ----------
    series_ids : list[SeriesID]
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================.

    """
    return pd.concat(
        map(
            lambda _: read_source(_).pipe(pull_by_series_id, _),
            series_ids
        ),
        axis=1,
        sort=True
    )


def stockpile_rebased(series_ids: list[SeriesID]) -> DataFrame:
    return pd.concat(
        map(
            lambda _: read_source(_).pipe(
                pull_by_series_id, _
            ).sort_index().pipe(transform_rebase),
            series_ids
        ),
        axis=1,
        sort=True
    )


def pull_by_series_id(df: DataFrame, series_id: SeriesID) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================.
    series_id : SeriesID
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================.

    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id.series_id].iloc[:, [1]].rename(
        columns={"value": series_id.series_id}
    )


def read_get_desc(token: DatasetDesc, key: str = 'description') -> dict[str, str]:
    """Returns Dictionary for Series from Douglas's & Kendrick's Databases"""
    return pd.read_csv(**token.get_kwargs()).to_dict().get(key)


@cache
def read_uscb_get_desc(token: DatasetDesc = DatasetDesc.USCB) -> DataFrame:
    return pd.read_csv(**token.get_kwargs()).drop_duplicates()


def lookup_uscb_desc(df: DataFrame, series_id: SeriesID) -> str:
    """
    Retrieves Series Description U.S. Bureau of the Census

    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.
    series_id : SeriesID
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    """
    LOOKUP_COLUMNS = ['group1', 'group2', 'group3', 'note']
    df = df[
        df.loc[:, 'series_id'] == series_id.series_id
    ].loc[:, LOOKUP_COLUMNS]
    return '\n'.join(filter(lambda _: isinstance(_, str), df.iloc[0, :].values))
