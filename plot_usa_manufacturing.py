# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:45:44 2019

@author: Mastermind
"""


import os

from plot.lib import plot_growth_elasticity, plot_rolling_mean_filter
from pull.lib import pull_by_series_id
from read.lib import read_usa_hist


def main():
    DIR = '/home/green-machine/321B-6A94'
    SERIES_ID, ARCHIVE_NAME = 'J0014', 'dataset_uscb.zip',

    os.chdir(DIR)
    df = read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, SERIES_ID)
    plot_growth_elasticity(df)
    plot_rolling_mean_filter(df)


if __name__ == '__main__':
    main()
