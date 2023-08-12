#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 23:56:20 2022

@author: Alexander Mikhailov
"""



import pandas as pd
from core.classes import Dataset


def pull_series_ids_description(filepath_or_buffer: str, key: str = 'description') -> dict[str, str]:
    """Returns Dictionary for Series from Douglas's & Kendrick's Databases"""
    kwargs = {
        'filepath_or_buffer': filepath_or_buffer,
        'index_col': 1,
        'usecols': (3, 4),
    }
    return pd.read_csv(**kwargs).to_dict().get(key)


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
    NAMES = [
        'source', 'table', 'note', 'group1', 'group2', 'group3', 'series_id'
    ]
    USECOLS = [0, 1, 3, 4, 5, 6, 9]

    kwargs = {
        'filepath_or_buffer': Dataset.USCB,
        'header': 0,
        'names': NAMES,
        'usecols': USECOLS,
        'low_memory': False
    }

    df = pd.read_csv(**kwargs)
    lookup_columns = ('group1', 'group2', 'group3', 'note')
    df = df[df.loc[:, 'series_id'] == series_id].loc[:, lookup_columns]
    df.drop_duplicates(inplace=True)
    return '\n'.join(filter(lambda _: isinstance(_, str), df.iloc[0, :].values))
