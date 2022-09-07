# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:22:23 2021

@author: Mastermind
"""


import os
import pandas as pd
from read.lib import read_can


def url_to_file_name(_url: str) -> str:
    '''


    Parameters
    ----------
    _url : str
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    '''
    return '/'.join(
        (
            'https://www150.statcan.gc.ca/n1/tbl/csv',
            f"{_url.split('?pid=')[1][:-2]}-eng.zip")
    )


def main():
    DIR = '/home/alexander/science'
    FILE_NAME = 'stat_can_all.xlsx'

    # =============================================================================
    # TODO: Modify
    # =============================================================================
    # =============================================================================
    # Read File Generated with main() @ stat_can_web_scraper.py @ https://github.com/avtomatik/stat-can
    # =============================================================================
    df = pd.read_excel(os.path.join(DIR, FILE_NAME))

    urls_available = set()
    for _ in range(df.shape[0]):
        try:
            urls_available.add(url_to_file_name(df.iloc[_, 8]))
        except IndexError:
            pass

    MAP_FILES = {url.split('/')[-1]: url for url in urls_available}

    file_names_downloaded = {
        f for f in os.listdir(os.path.join(DIR, 'data')) if f.endswith(('_eng.zip'))
    }

    file_names_to_check = set(MAP_FILES) - file_names_downloaded

    urls_to_check = tuple(
        MAP_FILES[file_name] for file_name in file_names_to_check
    )

    with open(os.path.join(DIR, 'stat_can_dump.txt'), 'w') as f:
        for url in sorted(urls_to_check):
            # =================================================================
            # TODO: UPDATE ACCORDING TO NEW SIGNATURE
            # =================================================================
            _df = read_can(url)
            print(url, file=f)
            print(f"Periods Length: {len(set(_df['REF_DATE'])):3};", file=f)
            print(_df['REF_DATE'].unique(), file=f)

    # =============================================================================
    # df.dropna(how='all').to_excel(os.path.join(DIR, FILE_NAME), index=False)
    # =============================================================================


if __name__ == '__main__':
    main()
