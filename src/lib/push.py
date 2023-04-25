#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:40:09 2022

@author: Alexander Mikhailov
"""

import os
import zipfile
from pathlib import Path
from zipfile import ZipFile

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


def push_data_frame_to_csv_zip(
    df: DataFrame,
    file_name: str,
    path_export: str = '/media/green-machine/KINGSTON'
) -> None:
    kwargs = {
        'path_or_buf': Path(path_export).joinpath(file_name),
        'index': True,
        'encoding': 'utf-8-sig'
    }
    df.to_csv(**kwargs)
    # =========================================================================
    # TODO: Rename .csv to .zip
    # =========================================================================
    with ZipFile(Path(path_export).joinpath(f'{file_name}.zip'), 'w') as archive:
        archive.write(
            Path(path_export).joinpath(file_name),
            compress_type=zipfile.ZIP_DEFLATED
        )
        os.unlink(Path(path_export).joinpath(file_name))


def push_files_to_zip(archive_name: str, file_names: tuple[str]) -> None:
    with ZipFile(f'{archive_name}.zip', 'w') as archive:
        for file_name in file_names:
            archive.write(file_name, compress_type=zipfile.ZIP_DEFLATED)
            os.unlink(file_name)
