#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:40:09 2022

@author: alexander
"""

from pandas import DataFrame


def load_data_frame_listing(df: DataFrame) -> None:
    # =========================================================================
    # TODO: Re-Write to Text File
    # =========================================================================
    for _, series_id in enumerate(df.columns):
        series = sorted(set(df.iloc[:, _]))
        print(f'{series_id:*^50}')
        print(series)


def load_data_frame_to_csv_zip(df: DataFrame, file_name: str) -> None:
    df.to_csv(f'{file_name}.csv', index=True, encoding='utf-8-sig')
    with ZipFile(f'{file_name}.zip', 'w') as archive:
        archive.write(f'{file_name}.csv', compress_type=zipfile.ZIP_DEFLATED)
        os.unlink(f'{file_name}.csv')


def load_files_to_zip(archive_name: str, file_names: tuple[str]) -> None:
    with ZipFile(f'{archive_name}.zip', 'w') as z:
        for file_name in file_names:
            z.write(file_name, compress_type=zipfile.ZIP_DEFLATED)
            os.unlink(file_name)
