#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:40:09 2022

@author: alexander
"""

import os
import zipfile
from zipfile import ZipFile
from pandas import DataFrame


def push_data_frame_listing(df: DataFrame, file_name: str = 'data_frame_listing.txt') -> None:
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


def push_data_frame_to_csv_zip(df: DataFrame, file_name: str) -> None:
    df.to_csv(f'{file_name}.csv', index=True, encoding='utf-8-sig')
    with ZipFile(f'{file_name}.zip', 'w') as archive:
        archive.write(f'{file_name}.csv', compress_type=zipfile.ZIP_DEFLATED)
        os.unlink(f'{file_name}.csv')


def push_files_to_zip(archive_name: str, file_names: tuple[str]) -> None:
    with ZipFile(f'{archive_name}.zip', 'w') as archive:
        for file_name in file_names:
            archive.write(file_name, compress_type=zipfile.ZIP_DEFLATED)
            os.unlink(file_name)
