# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:45:44 2019

@author: Alexander Mikhailov
"""


import os

from lib.collect import stockpile_usa_hist
from lib.plot import plot_filter_rolling_mean, plot_growth_elasticity


def main(
    path_src: str = '/media/green-machine/KINGSTON',
    series_id: dict[str, str] = {'J0014': 'dataset_uscb.zip'}
):

    os.chdir(path_src)
    df = stockpile_usa_hist(series_id)
    df.pipe(plot_growth_elasticity)
    df.pipe(plot_filter_rolling_mean)


if __name__ == '__main__':
    main()
