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

from thesis.src.lib.pull import pull_by_series_id
from thesis.src.lib.read import read_usa_bls
from thesis.src.lib.stockpile import stockpile_usa_hist
from thesis.src.lib.transform import transform_mean


def main(
    savefig: bool = False,
    path_src: str = '/media/green-machine/KINGSTON',
    path_export: str = '/home/green-machine/Downloads',
    file_name: str = 'plot_usa_unemployment_autocorrelation.pdf'
) -> None:
    SERIES_ID_CB = {'D0086': 'dataset_uscb.zip'}
    SERIES_ID_LS = {
        'LNU04000000': 'dataset_usa_bls-2017-07-06-ln.data.1.AllData'
    }

    os.chdir(path_src)

    df = pd.concat(
        [
            stockpile_usa_hist(SERIES_ID_CB),
            pd.concat(
                map(
                    lambda _: read_usa_bls(_[-1]).pipe(
                        pull_by_series_id, _[0]
                    ),
                    SERIES_ID_LS.items()
                ),
                axis=1,
                sort=True
            ).apply(pd.to_numeric, errors='coerce'),
        ],
        axis=1
    )
    df.plot(title='US Unemployment, {}$-${}'.format(*df.index[[0, -1]]))
    df.pipe(transform_mean, name="fused").pipe(autocorrelation_plot)

    if savefig:
        plt.savefig(
            Path(path_export).joinpath(file_name), format='pdf', dpi=900
        )


if __name__ == '__main__':
    main()
