# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 23:12:03 2019

@author: Mastermind
"""


import matplotlib.pyplot as plt
import os
import pandas as pd
from pandas.plotting import autocorrelation_plot
from extract.lib import extract_usa_bls
from extract.lib import extract_usa_census


def main():
    FLAG = True
    FOLDER = '/media/alexander/321B-6A94'
    _FOLDER = '/home/alexander/Downloads'
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    FILE_NAME = 'dataset_usa_bls-2017-07-06-ln.data.1.AllData'
    _FILE_NAME = 'plot_usa_unemployment_autocorrelation.pdf'
    os.chdir(FOLDER)
    df = pd.concat(
        [
            extract_usa_census(ARCHIVE_NAME, 'D0086'),
            extract_usa_bls(FILE_NAME, 'LNU04000000'),
        ],
        axis=1, sort=True)
    df.plot(
        title='US Unemployment, {}$-${}'.format(*df.index[[0, -1]]),
        grid=True
    )
    df['fused'] = df.mean(1)
    autocorrelation_plot(df.iloc[:, -1])
    plt.grid(True)
    if FLAG:
        plt.savefig(os.path.join(_FOLDER, _FILE_NAME), format='pdf', dpi=900)


if __name__ == '__main__':
    main()
