# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 18:28:15 2020

@author: Mastermind
"""


import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from functools import partial


def fetch_usa_census(archive_name: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Selected Series by U.S. Bureau of the Census
    # U.S. Bureau of the Census, Historical Statistics of the United States,
    # 1789--1945, Washington, D.C., 1949.
    # U.S. Bureau of the Census. Historical Statistics of the United States,
    # Colonial Times to 1970, Bicentennial Edition. Washington, D.C., 1975.
    # =========================================================================
    data_frame = pd.read_csv(archive_name,
                             usecols=range(8, 11),
                             dtype=str)
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].str[:4].astype(int)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    data_frame.columns = [data_frame.columns[0], series_id]
    data_frame.sort_values(data_frame.columns[0], inplace=True)
    return data_frame.groupby(data_frame.columns[0]).mean()


def fetch_usa_classic(archive_name: str, series_id: str) -> pd.DataFrame:
    # =========================================================================
    # Data Fetch Procedure for Enumerated Classical Datasets
    # =========================================================================
    USECOLS = {
        'dataset_douglas.zip': (4, 7,),
        'dataset_usa_brown.zip': (3, 6,),
        'dataset_usa_cobb-douglas.zip': (5, 8,),
        'dataset_usa_kendrick.zip': (4, 7,),
    }
    data_frame = pd.read_csv(
        archive_name,
        skiprows=(None, 4)[archive_name == 'dataset_usa_brown.zip'],
        usecols=range(*USECOLS[archive_name])
    )
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = pd.to_numeric(
        data_frame.iloc[:, 1], errors='coerce')
    data_frame.columns = [data_frame.columns[0], series_id]
    return data_frame.set_index(data_frame.columns[0])


def get_data_cobb_douglas(series_number: int = 3) -> pd.DataFrame:
    '''Original Cobb--Douglas Data Preprocessing Extension'''
    ARCHIVE_NAMES = (
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_cobb-douglas.zip',
        'dataset_usa_census1949.zip',
        'dataset_usa_census1949.zip',
        'dataset_douglas.zip',
    )
    SERIES_IDS = {
        # =====================================================================
        # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
        # =====================================================================
        'CDT2S4': 'capital',
        # =====================================================================
        # Cobb C.W., Douglas P.H. Labor Series: Average Number Employed (in thousands)
        # =====================================================================
        'CDT3S1': 'labor',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of Physical Production of Manufacturing
        # =====================================================================
        'J0014': 'product',
        # =====================================================================
        # Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic Research Index of Physical Output, All Manufacturing Industries.
        # =====================================================================
        'J0013': 'product_nber',
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01': 'product_rev',
    }
    FUNCTIONS = (
        fetch_usa_classic,
        fetch_usa_classic,
        fetch_usa_census,
        fetch_usa_census,
        fetch_usa_classic,
    )
    data_frame = pd.concat(
        [
            partial(func, **{'archive_name': archive_name,
                             'series_id': series_id})()
            for archive_name, series_id, func in zip(ARCHIVE_NAMES, SERIES_IDS.keys(), FUNCTIONS)
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    data_frame.columns = SERIES_IDS.values()
    return data_frame.div(data_frame.iloc[0, :]).iloc[:, range(series_number)]


def data_preprocessing_cobb_douglas(df: pd.DataFrame) -> tuple[pd.DataFrame, tuple[float]]:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Original: k=0.25
    # =========================================================================
    k, b = np.polyfit(
        np.log(df.iloc[:, -2]),
        np.log(df.iloc[:, -1]),
        1
    )
    # =========================================================================
    # Scipy Signal Median Filter, Non-Linear Low-Pass Filter
    # =========================================================================
    # =========================================================================
    # k, b = np.polyfit(
    #     np.log(signal.medfilt(df.iloc[:, -2])),
    #     np.log(signal.medfilt(df.iloc[:, -1])),
    #     1
    # )
    # =========================================================================
    # =========================================================================
    # Description
    # =========================================================================
    df['cap_to_lab'] = df.iloc[:, 1].div(df.iloc[:, 0])
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 2].div(df.iloc[:, 0])
    # =========================================================================
    # Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_roll'] = df.iloc[:, 2].rolling(window=3, center=True).mean()
    df['prod_roll_sub'] = df.iloc[:, 2].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product
    # =========================================================================
    df['prod_comp'] = df.iloc[:, 0].pow(k).mul(
        df.iloc[:, 1].pow(1-k)).mul(np.exp(b))
    # =========================================================================
    # Computed Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_comp_roll'] = df.iloc[:, -1].rolling(window=3, center=True).mean()
    df['prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    # =========================================================================
    #     print(r2_score(df.iloc[:, 2], df.iloc[:, 3]))
    #     print(np.absolute(df.iloc[:, 3].sub(df.iloc[:, 2]).div(df.iloc[:, 2])).mean())
    # =========================================================================
    return df, (k, np.exp(b),)


def plot_cobb_douglas(data_frame: pd.DataFrame, params: tuple[float], mapping: dict) -> None:
    '''
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    '''
    assert data_frame.shape[1] == 12

    def lab_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, -k), b)

    def cap_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, 1-k), b)

    plt.figure(1)
    plt.semilogy(data_frame.iloc[:, range(3)], label=[
        'Fixed Capital',
        'Labor Force',
        'Physical Product',
    ])
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_a'].format(data_frame.index[0],
                                     data_frame.index[-1],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(data_frame.iloc[:, [2, 9]], label=[
        'Actual Product',
        'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
            params[1],
            1-params[0],
            params[0],
        ),
    ])
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(mapping['fg_b'].format(data_frame.index[0],
                                     data_frame.index[-1],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(data_frame.iloc[:, [8, 11]], label=[
        'Deviations of $P$',
        'Deviations of $P\'$',
        # =========================================================================
        #      TODO: ls=['solid','dashed',]
        # =========================================================================
    ])
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(data_frame.iloc[:, 9].div(data_frame.iloc[:, 2]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_d'].format(data_frame.index[0],
                                     data_frame.index[-1]))
    plt.grid(True)
    plt.figure(5, figsize=(5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(data_frame.iloc[:, 5], data_frame.iloc[:, 4])
    plt.scatter(data_frame.iloc[:, 5], data_frame.iloc[:, 6])
    plt.plot(lc, lab_productivity(lc, *params),
             label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, cap_productivity(lc, *params),
             label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_e'])
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    FIG_MAP = {
        'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_price': 1899,
    }
    os.chdir('/media/alexander/321B-6A94')
    plot_cobb_douglas(
        *data_preprocessing_cobb_douglas(get_data_cobb_douglas()), FIG_MAP)


if __name__ == '__main__':
    main()
