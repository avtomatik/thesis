#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 11:52:01 2022
@author: Alexander Mikhailov
"""


import pandas as pd
from pandas import DataFrame

from .read import read_source
from .transform import transform_rebase


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
