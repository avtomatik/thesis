# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 23:12:03 2019

@author: Alexander Mikhailov
"""


import os

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import autocorrelation_plot
from pull.lib import pull_by_series_id
from read.lib import read_usa_bls, read_usa_hist


def main():
    FLAG = True
    DIR = '/media/green-machine/KINGSTON'
    _DIR = '/home/green-machine/Downloads'
    ARCHIVE_NAME = 'dataset_uscb.zip'
    FILE_NAME = 'dataset_usa_bls-2017-07-06-ln.data.1.AllData'
    _FILE_NAME = 'plot_usa_unemployment_autocorrelation.pdf'

    os.chdir(DIR)
    df = pd.concat(
        [
            read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, 'D0086'),
            read_usa_bls(FILE_NAME).pipe(pull_by_series_id, 'LNU04000000'),
        ],
        axis=1
    )
    df.plot(
        title='US Unemployment, {}$-${}'.format(*df.index[[0, -1]]),
        grid=True
    )
    df['fused'] = df.mean(1)
    autocorrelation_plot(df.iloc[:, -1])
    plt.grid(True)
    if FLAG:
        plt.savefig(os.path.join(_DIR, _FILE_NAME), format='pdf', dpi=900)


if __name__ == '__main__':
    main()