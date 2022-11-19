# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:22:23 2021

@author: Alexander Mikhailov
"""


import os
from pathlib import Path

import pandas as pd
from more_itertools import map_except


def url_to_archive_name(_url: str) -> str:
    """


    Parameters
    ----------
    _url : str
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    """
    return f"{_url.split('?pid=')[1][:-2]}-eng.zip"


def get_archive_names(file_name: str, directory: str = '../stat_can') -> set[str]:
    """


    Parameters
    ----------
    file_name : str
        DESCRIPTION.
    directory : str, optional
        DESCRIPTION. The default is '../stat_can'.

    Returns
    -------
    set[str]
        DESCRIPTION.

    """
    df = pd.read_excel(Path(directory).joinpath(file_name))
    return set(map_except(url_to_archive_name, df.loc[:, "ref"], IndexError))


def main(
    check_option: str,
    directory: str = '../stat_can',
    url_root: str = 'https://www150.statcan.gc.ca/n1/tbl/csv',
):
    """


    Parameters
    ----------
    check_option : str
        `snapshots': Check Two Excel Files;
        `downloaded': Check the Latest Excel File Against Downloaded Collection.
    directory : str, optional
        DESCRIPTION. The default is '../stat_can'.
    url_root : str, optional
        DESCRIPTION. The default is 'https://www150.statcan.gc.ca/n1/tbl/csv'.

    Returns
    -------
    None.

    """
    # =========================================================================
    # Read File Generated with main() @main.py @https://github.com/avtomatik/stat-can
    # =========================================================================

    snapshots_available = tuple(sorted([
        file_name for file_name in os.listdir(Path(directory)) if file_name.endswith(".xlsx")
    ]))
    archive_names_available = get_archive_names(snapshots_available[-1])

    archive_names_seen = get_archive_names(snapshots_available[-2]) \
        if check_option == "snapshots" \
        else {
        f for f in os.listdir(Path(directory).parent.joinpath("data/external")) if f.endswith(('-eng.zip'))
    }

    archive_names_to_check = sorted(
        archive_names_available - archive_names_seen
    )
    if archive_names_to_check:
        print("You Might Want to Check Those New Archives")
        for archive_name in archive_names_to_check:
            print('/'.join((url_root, archive_name)))
    else:
        print("No New Archives Since the Last Snapshot/Download")


if __name__ == '__main__':
    main("snapshots")
