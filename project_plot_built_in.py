#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 21:45:19 2022

@author: alexander
"""


import io
import os
import pandas as pd
import re
import logging
from zipfile import ZipFile
from pandas.plotting import autocorrelation_plot
import matplotlib.pyplot as plt


# =============================================================================
# Purpose: Draw:
#     Correlogram, Pandas;
#     Bootstrap Plot, Pandas;
#     Lag Plot, Pandas
# =============================================================================
def fetch_world_bank(data_frame: pd.DataFrame, series_id: str) -> pd.DataFrame:
    df = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:, [0, 2]]
    df.columns = [df.columns[0], series_id]
    return df.set_index(df.columns[0])


def plot_built_in(module: callable):
    # =========================================================================
    # TODO: Rework
    # =========================================================================
    FILE_NAMES = (
        'datasetAutocorrelation.txt',
        'CHN_TUR_GDP.zip',
    )
    data = pd.read_csv(FILE_NAMES[0])
    for _, series_id in enumerate(sorted(set(data.iloc[:, 1])), start=1):
        plt.figure(_)
        module(fetch_world_bank(data, series_id))
        plt.grid(True)

    data = pd.read_csv(FILE_NAMES[1])
    for _, series_id in enumerate(sorted(set(data.iloc[:, 1])), start=1):
        plt.figure(_)
        module(fetch_world_bank(data, series_id))
        plt.grid(True)

    plt.show()


os.chdir('/media/alexander/321B-6A94')
ARCHIVE_NAME = 'project_autocorrelation.zip'
FILE_NAMES = (
    'datasetAutocorrelation.txt',
    'CHN_TUR_GDP.zip',
)
# =============================================================================
# TODO: Dig Into Nested Zips
# =============================================================================
# plot_built_in(autocorrelation_plot)
# plot_built_in(bootstrap_plot)
# plot_built_in(lag_plot)
# with ZipFile(ARCHIVE_NAME, 'r').open(dict_template[cfg.template]) as archive_parent:
# with ZipFile(ARCHIVE_NAME, 'r') as archive_parent:
#     data = pd.read_csv(io.BytesIO(archive_parent.open(FILE_NAMES[1], 'r')))
#     print(data)
#     # for file_name in archive_parent.namelist():
#     #     print(file_name)

with ZipFile(ARCHIVE_NAME, 'r') as archive_parent:
    # with ZipFile(io.BytesIO(archive_parent.read(FILE_NAMES[1]))) as archive_target:
    # data = pd.read_csv(io.BytesIO(archive_parent.read(FILE_NAMES[1])))
    data = pd.read_csv(io.BytesIO(archive_parent.read(FILE_NAMES[0])))
    for _, series_id in enumerate(sorted(set(data.iloc[:, 1])), start=1):
        plt.figure(_)
        autocorrelation_plot(fetch_world_bank(data, series_id))
        plt.grid(True)
        print(plt.gcf().number)
