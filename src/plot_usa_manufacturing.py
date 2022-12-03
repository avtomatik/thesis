# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:45:44 2019

@author: Alexander Mikhailov
"""


import os

from lib.collect import stockpile_usa_hist
from lib.plot import plot_growth_elasticity, plot_rolling_mean_filter


def main(
    directory: str = '/media/green-machine/KINGSTON',
    series_id: dict[str, str] = {'J0014': 'dataset_uscb.zip'}
):

    os.chdir(directory)
    df = stockpile_usa_hist(series_id)
    plot_growth_elasticity(df)
    plot_rolling_mean_filter(df)


if __name__ == '__main__':
    main()
