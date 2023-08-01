#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 02:40:19 2023

@author: green-machine

Project I. Approximation
"""


from core.plot import plot_approx_linear, plot_approx_linear_log
from core.stockpile import stockpile_usa_bea
from core.transform import transform_approx_linear, transform_approx_linear_log


def linear() -> None:
    """
    Project: Linear Approximation
    Returns
    -------
    None.
    """
    URL_NIPA_DATA_A = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    SERIES_IDS = {
        'A191RX': URL_NIPA_DATA_A,
        'A191RC': URL_NIPA_DATA_A,
        'A006RC': URL_NIPA_DATA_A,
        'A191RC': URL_NIPA_DATA_A
    }
    plot_approx_linear(
        *stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(transform_approx_linear)
    )


def linear_log() -> None:
    """
    Project: Log-Linear Approximation
    Returns
    -------
    None.
    """
    URL_FIXED_ASSETS = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    URL_NIPA_DATA_A = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    SERIES_IDS = {
        'A191RX': URL_NIPA_DATA_A,
        'A191RC': URL_NIPA_DATA_A,
        'kcptotl1es00': URL_FIXED_ASSETS,
        'A032RC': URL_NIPA_DATA_A
    }
    plot_approx_linear_log(
        *stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(transform_approx_linear_log)
    )

    SERIES_IDS = {
        'A191RX': URL_NIPA_DATA_A,
        'A191RC': URL_NIPA_DATA_A,
        'kcptotl1es00': URL_FIXED_ASSETS,
        'A191RC': URL_NIPA_DATA_A
    }
    plot_approx_linear_log(
        *stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(transform_approx_linear_log)
    )


if __name__ == '__main__':
    # =========================================================================
    # 'plot_approx_linear': Linear Approximation
    # =========================================================================
    linear()
    # =========================================================================
    # 'plot_approx_linear_log': Log-Linear Approximation
    # =========================================================================
    linear_log()
