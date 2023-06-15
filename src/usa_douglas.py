#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 23:30:39 2023

@author: green-machine
"""

import os

import pandas as pd
from matplotlib import pyplot as plt

from thesis.src.lib.constants import (TITLES_DEU, TITLES_DOUGLAS,
                                      YLABELS_DOUGLAS)
from thesis.src.lib.stockpile import stockpile_usa_hist


def group_series_ids(series_ids: list[str], upper_bound: int = 4) -> dict[str, list[str]]:
    series_id_group = ''
    series_id_groups = {}
    for series_id in series_ids:
        if series_id[:upper_bound] != series_id_group:
            series_id_groups[series_id[:upper_bound]] = [series_id]
        else:
            series_id_groups[series_id[:upper_bound]].append(series_id)
        series_id_group = series_id[:upper_bound]
    return series_id_groups


def pull_series_ids_description(filepath_or_buffer: str) -> dict[str, str]:
    """Returns Dictionary for Series from Douglas's & Kendrick's Databases"""
    kwargs = {
        'filepath_or_buffer': filepath_or_buffer,
        'index_col': 1,
        'usecols': (3, 4),
    }
    return pd.read_csv(**kwargs).to_dict().get('series')


def plot_douglas(
    archive_name: str,
    titles: tuple[str],
    ylabels: tuple[str],
    ylabels_plus: tuple[str]
) -> None:
    """


    Parameters
    ----------
    archive_name : str
        DESCRIPTION.
    titles : tuple[str]
        DESCRIPTION.
    ylabels : tuple[str]
        DESCRIPTION.
    ylabels_plus : tuple[str]
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    map_series_ids = pull_series_ids_description(archive_name)

    series_ids_struct = {}
    for series_id_group, series_ids in group_series_ids(sorted(map_series_ids)).items():
        series_ids_struct[series_id_group] = dict(
            zip(series_ids, [archive_name] * len(series_ids))
        )

    for _, ((series_id_group, series_ids), title, ylabel) in enumerate(
            zip(series_ids_struct.items(), titles, ylabels)
    ):
        plt.figure(_)
        plt.plot(
            stockpile_usa_hist(series_ids),
            label=list(map(map_series_ids.get, series_ids.keys()))
        )
        plt.title(title)
        plt.xlabel('Period')
        plt.ylabel(ylabel)
        plt.grid()
    # =============================================================================
    #     if series_id_group == 'DT30':
    #         plt.legend(ylabels_plus)
    # =============================================================================
        plt.legend()
        plt.show()


if __name__ == '__main__':
    # =========================================================================
    # Douglas European Demographics & Growth of US Capital
    # =========================================================================
    PATH_SRC = '/home/green-machine/data_science/data/interim'

    ARCHIVE_NAME = 'dataset_douglas.zip'

    os.chdir(PATH_SRC)
    plot_douglas(ARCHIVE_NAME, TITLES_DOUGLAS, YLABELS_DOUGLAS, TITLES_DEU)
