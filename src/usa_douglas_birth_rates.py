

import os

import matplotlib.pyplot as plt
from core.constants import COUNTRIES
from core.stockpile import stockpile

if __name__ == '__main__':
    SERIES_IDS = {
        # =========================================================================
        # TODO: Apply Wiener Filter to Birth Rates
        # =========================================================================
        'DT25BS01': Dataset.DOUGLAS,
        'DT26BS01': Dataset.DOUGLAS,
        'DT27BS01': Dataset.DOUGLAS,
        'DT28BS01': Dataset.DOUGLAS,
        'DT29BS01': Dataset.DOUGLAS,
        'DT30BAS01': Dataset.DOUGLAS,
        'DT30BBS01': Dataset.DOUGLAS,
        'DT31BS01': Dataset.DOUGLAS,
        'DT32BS01': Dataset.DOUGLAS
    }

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
