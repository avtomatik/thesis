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
        [
            read_usa_bea(url).pipe(pull_by_series_id, series_id)
            for series_id, url in series_ids.items()
        ],
        axis=1,
        verify_integrity=True,
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
        [
            read_usa_hist(archive_name).sort_index().pipe(
                pull_by_series_id, series_id
            )
            for series_id, archive_name in series_ids.items()
        ],
        axis=1,
        verify_integrity=True,
        sort=True
    )


def stockpile_usa_mcconnel(
    series_ids: tuple[str], archive_name: str = 'dataset_usa_mc_connell_brue.zip'
) -> DataFrame:
    SERIES_IDS = {
        'Ставка прайм-рейт, %': 'prime_rate',
        'Валовой объем внутренних частных инвестиций, млрд долл. США': 'A006RC',
        'Национальный доход, млрд долл. США': 'A032RC',
        'Валовой внутренний продукт, млрд долл. США': 'A191RC',
    }
    return pd.concat(
        [
            read_usa_hist(archive_name).sort_index().pipe(pull_by_series_id, series_id).rename(
                columns={series_id: SERIES_IDS[series_id]})
            for series_id in series_ids
        ],
        axis=1
    ).truncate(before=1980)


def stockpile_usa_sahr_infcf(df: DataFrame) -> DataFrame:
    """
    Retrieves Yearly Price Rates from 'dataset_usa_infcf16652007.zip'

    Returns
    -------
    DataFrame
    """
    # =========================================================================
    # Retrieve First 14 Series
    # =========================================================================
    return pd.concat(
        [
            df.pipe(pull_by_series_id, series_id).rdiv(1).pct_change().mul(-1)
            for series_id in df.iloc[:, 0].unique()[:14]
        ],
        axis=1,
        sort=True
    )


def filter_data_frame(df: DataFrame, query: dict[str]) -> DataFrame:
    for column, criterion in query['filter'].items():
        df = df[df.iloc[:, column] == criterion]
    return df
