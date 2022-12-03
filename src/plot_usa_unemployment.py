# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 23:12:03 2019

@author: Alexander Mikhailov
"""


import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import autocorrelation_plot

from lib.collect import stockpile_usa_hist
from lib.pull import pull_by_series_id
from lib.read import read_usa_bls
from lib.transform import transform_mean


def main(
    savefig: bool = False,
    directory: str = '/media/green-machine/KINGSTON'
) -> None:
    SERIES_ID_CB = {'D0086': 'dataset_uscb.zip'}
    SERIES_ID_LS = {
        'LNU04000000': 'dataset_usa_bls-2017-07-06-ln.data.1.AllData'
    }
    DIR = '/home/green-machine/Downloads'
    FILE_NAME = 'plot_usa_unemployment_autocorrelation.pdf'

    os.chdir(directory)

    df = pd.concat(
        [
            stockpile_usa_hist(SERIES_ID_CB),
            pd.concat(
                [
                    read_usa_bls(file_name).pipe(pull_by_series_id, series_id)
                    for series_id, file_name in SERIES_ID_LS.items()
                ],
                axis=1
            ).apply(pd.to_numeric, errors='coerce'),
        ],
        axis=1
    )
    df.plot(title='US Unemployment, {}$-${}'.format(*df.index[[0, -1]]))
    df.pipe(transform_mean, name="fused").pipe(autocorrelation_plot)

    if savefig:
        plt.savefig(Path(DIR).joinpath(FILE_NAME), format='pdf', dpi=900)


if __name__ == '__main__':
    main()
