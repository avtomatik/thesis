#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 02:40:19 2023

@author: green-machine

Project I. Approximation
"""

from core.backend import stockpile
from core.classes import URL
from core.combine import enlist_series_ids
from core.plot import plot_approx_linear, plot_approx_linear_log
from core.transform import transform_approx_linear, transform_approx_linear_log


def linear() -> None:
    """
    Project: Linear Approximation
    Returns
    -------
    None.
    """

    SERIES_IDS = ["A191RX", "A191RC", "A006RC", "A191RC"]
    SERIES_IDS = enlist_series_ids(SERIES_IDS, URL.NIPA)
    plot_approx_linear(
        *stockpile(SERIES_IDS).dropna(axis=0).pipe(transform_approx_linear)
    )


def linear_log() -> None:
    """
    Project: Log-Linear Approximation
    Returns
    -------
    None.
    """

    SERIES_IDS = ["A191RX", "A191RC"]

    SERIES_IDS = (
        enlist_series_ids(SERIES_IDS, URL.NIPA)
        + enlist_series_ids(["kcptotl1es00"], URL.FIAS)
        + enlist_series_ids(["A032RC"], URL.NIPA)
    )
    plot_approx_linear_log(
        *stockpile(SERIES_IDS).dropna(axis=0).pipe(transform_approx_linear_log)
    )

    SERIES_IDS = ["A191RX", "A191RC"]

    SERIES_IDS = (
        enlist_series_ids(SERIES_IDS, URL.NIPA)
        + enlist_series_ids(["kcptotl1es00"], URL.FIAS)
        + enlist_series_ids(["A191RC"], URL.NIPA)
    )
    plot_approx_linear_log(
        *stockpile(SERIES_IDS).dropna(axis=0).pipe(transform_approx_linear_log)
    )


if __name__ == "__main__":
    # =========================================================================
    # 'plot_approx_linear': Linear Approximation
    # =========================================================================
    linear()
    # =========================================================================
    # 'plot_approx_linear_log': Log-Linear Approximation
    # =========================================================================
    linear_log()
