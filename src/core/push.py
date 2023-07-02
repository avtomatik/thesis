#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:40:09 2022

@author: Alexander Mikhailov
"""


from pandas import DataFrame


def push_data_frame_listing(
    df: DataFrame,
    file_name: str = 'data_frame_listing.txt'
) -> None:
    """
    Dumps Data Headers & Unique Data Samples

    Parameters
    ----------
    df : DataFrame
    file_name : str, optional
        DESCRIPTION. The default is 'data_frame_listing.txt'.

    Returns
    -------
    None
    """
    with open(file_name, 'w') as f:
        for _, series_id in enumerate(df.columns):
            print(f'{series_id:*^50}', file=f)
            print(sorted(set(df.iloc[:, _])), file=f)
