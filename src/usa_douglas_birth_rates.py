import os

import matplotlib.pyplot as plt

from core.constants import COUNTRIES
from thesis.src.core.backend import stockpile
from thesis.src.core.classes import Dataset

if __name__ == '__main__':
    SERIES_IDS = [
        # =========================================================================
        # TODO: Apply Wiener Filter to Birth Rates
        # =========================================================================
        'DT25BS01',
        'DT26BS01',
        'DT27BS01',
        'DT28BS01',
        'DT29BS01',
        'DT30BAS01',
        'DT30BBS01',
        'DT31BS01',
        'DT32BS01'
    ]

    SERIES_IDS = enlist_series_ids(SERIES_IDS, Dataset.DOUGLAS)

    PATH_SRC = '/home/green-machine/data_science/data/interim'

    os.chdir(PATH_SRC)

    plt.figure(1)
    plt.plot(stockpile(SERIES_IDS), label=COUNTRIES)
    plt.title('Birth Rates by Countries')
    plt.xlabel('Period')
    plt.ylabel('Birth Rate per 1000')
    plt.legend()
    plt.grid()
    plt.show()
