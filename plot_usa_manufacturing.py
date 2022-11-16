# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:45:44 2019

@author: Mastermind
"""


import os

from plot.lib import plot_growth_elasticity, plot_rolling_mean_filter
from pull.lib import pull_by_series_id
from read.lib import read_usa_hist


def main(
    directory: str = '/media/green-machine/KINGSTON',
    series_id: str = 'J0014',
    archive_name: str = 'dataset_uscb.zip',
):

    os.chdir(directory)
    df = read_usa_hist(archive_name).pipe(pull_by_series_id, series_id)
    plot_growth_elasticity(df)
    plot_rolling_mean_filter(df)


if __name__ == '__main__':
    main()
