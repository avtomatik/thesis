# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:04:02 2019

@author: Mastermind
"""


import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_is_lm():
    # =========================================================================
    # Read Data
    # =========================================================================
    ARCHIVE_NAME = 'dataset_rus_m1.zip'
    df = pd.read_csv(
        ARCHIVE_NAME,
        names=['period', 'prime_rate', 'm1'],
        index_col=0,
        skiprows=1,
        parse_dates=True
    )
    # =========================================================================
    # Plotting
    # =========================================================================
    plt.figure()
    plt.plot(df.iloc[:, 0], df.iloc[:, 1])
    plt.xlabel('Percentage')
    plt.ylabel('RUB, Millions')
    plt.title('M1 Dependency on Prime Rate')
    plt.grid(True)
    plt.show()


def plot_grigoriev():
    FILE_NAME = 'dataset_rus_grigoriev_v.csv'
    data_frame = pd.read_csv(FILE_NAME, index_col=1, usecols=range(2, 5))
    for series_id in sorted(set(data_frame.iloc[:, 0])):
        chunk = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1]]
        chunk.columns = [series_id]
        chunk.sort_index(inplace=True)
        chunk.plot(grid=True)


def main():
    FOLDER = '/media/alexander/321B-6A94'
    os.chdir(FOLDER)
    plot_is_lm()
    plot_grigoriev()


if __name__ == '__main__':
    main()
