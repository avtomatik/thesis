

import os

import matplotlib.pyplot as plt
from lib.constants import COUNTRIES

from thesis_work.src.usa_douglas import stockpile_usa_hist

if __name__ == '__main__':
    SERIES_IDS = {
        # =========================================================================
        # TODO: Apply Wiener Filter to Birth Rates
        # =========================================================================
        'DT25BS01': 'dataset_douglas.zip',
        'DT26BS01': 'dataset_douglas.zip',
        'DT27BS01': 'dataset_douglas.zip',
        'DT28BS01': 'dataset_douglas.zip',
        'DT29BS01': 'dataset_douglas.zip',
        'DT30BAS01': 'dataset_douglas.zip',
        'DT30BBS01': 'dataset_douglas.zip',
        'DT31BS01': 'dataset_douglas.zip',
        'DT32BS01': 'dataset_douglas.zip'
    }

    PATH_SRC = '/home/green-machine/data_science/data/interim'

    os.chdir(PATH_SRC)

    plt.figure(1)
    plt.plot(stockpile_usa_hist(SERIES_IDS), label=COUNTRIES)
    plt.title('Birth Rates by Countries')
    plt.xlabel('Period')
    plt.ylabel('Birth Rate per 1000')
    plt.legend()
    plt.grid()
    plt.show()
