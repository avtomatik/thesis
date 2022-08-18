# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:45:44 2019

@author: Mastermind
"""


import os
from extract.lib import extract_usa_hist
from plot.lib import plot_rolling_mean_filter
from plot.lib import plot_growth_elasticity


def main():
    DIR = '/media/alexander/321B-6A94'
    ARCHIVE_NAME, SERIES_ID = 'dataset_usa_census1949.zip', 'J0014'

    os.chdir(DIR)
    df = extract_usa_hist(ARCHIVE_NAME, SERIES_ID)
    plot_growth_elasticity(df)
    plot_rolling_mean_filter(df)


if __name__ == '__main__':
    main()
