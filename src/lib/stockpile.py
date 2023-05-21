#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 11:52:01 2022
@author: Alexander Mikhailov
"""


import pandas as pd
from pandas import DataFrame

from thesis.src.lib.pull import pull_by_series_id
from thesis.src.lib.read import read_usa_bea, read_usa_hist


def stockpile_usa_bea(series_ids: dict[str, str]) -> DataFrame:
    """


    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================

    """
    return pd.concat(
        map(
            lambda _: read_usa_bea(_[-1]).pipe(pull_by_series_id, _[0]),
            series_ids.items()
        ),
        axis=1,
        sort=True
    )


def stockpile_usa_hist(series_ids: dict[str, str]) -> DataFrame:
    """


    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================

    """
    return pd.concat(
        map(
            lambda _: read_usa_hist(_[-1]).pipe(pull_by_series_id, _[0]),
            series_ids.items()
        ),
        axis=1,
        sort=True
    )