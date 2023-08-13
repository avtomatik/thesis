#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:25:52 2022

@author: Alexander Mikhailov
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.interpolate import UnivariateSpline
from sklearn.metrics import r2_score

from .backend import stockpile
from .transform import transform_deflator


def calculate_capital(df: DataFrame, p_i: tuple[float], p_t: tuple[float], ratio: float) -> pd.Series:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Investment
        df.iloc[:, 1]      Production
        df.iloc[:, 2]      Capital
        df.iloc[:, 3]      Capital Retirement
        ================== =================================
    p_i : tuple[float]
        p_i[0]: S - Gross Fixed Investment to Gross Domestic Product Ratio - Slope over Period,
        p_i[1]: S - Gross Fixed Investment to Gross Domestic Product Ratio - Absolute Term over Period.
    p_t : tuple[float]
        p_t[0]: Λ - Fixed Assets Turnover Ratio - Slope over Period,
        p_t[1]: Λ - Fixed Assets Turnover Ratio - Absolute Term over Period.
    ratio : float
        ratio: Investment to Capital Conversion Ratio.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return np.multiply(
        np.subtract(
            np.add(
                np.multiply(
                    np.multiply(
                        np.poly1d(p_i)(df.index.to_series().shift(1)),
                        np.poly1d(p_t)(df.index.to_series().shift(1)),
                    ),
                    ratio
                ),
                1
            ),
            df.iloc[:, 3].shift(1)
        ),
        df.iloc[:, 2].shift(1)
    )


def calculate_plot_uspline(df: DataFrame):
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Labor Capital Intensity
        df.iloc[:, 1]      Labor Productivity
        ================== =================================
    """
    df.sort_values(df.columns[0], inplace=True)
    # =========================================================================
    # _new_axis = np.linspace(df.iloc[:, [0]].min(), df.iloc[:, [0]].max(), df.shape[0] - 1)
    # =========================================================================
    spl = UnivariateSpline(df.iloc[:, [0]], df.iloc[:, [1]])
    plt.figure()
    plt.scatter(df.iloc[:, [0]], df.iloc[:, [1]], label='Original')
    plt.plot(
        df.iloc[:, 0],
        spl(df.iloc[:, 0]),
        'g',
        lw=3,
        label='Spline'
    )
    plt.title(
        'Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid()
    plt.legend()
    # =========================================================================
    # TODO: Figure Out How It Works
    # =========================================================================
    print(spl.antiderivative())
    # =========================================================================
    # TODO: Figure Out How It Works
    # =========================================================================
    print(spl.derivative())
    print(spl.derivatives(1))
    print(spl.ext)
    print(spl.get_coeffs())
    print(spl.get_knots())
    print(spl.get_residual())
    print(spl.integral(1., 1.75))
    print(spl.roots())
    print(spl.set_smoothing_factor(0.25))
    plt.show()


def filter_kol_zur(df: DataFrame, k: int = None) -> tuple[DataFrame]:
    """
    Kolmogorov--Zurbenko Filter
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    """
    if k is None:
        k = df.shape[0] // 2
    df.reset_index(level=0, inplace=True)
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Results: Odd
    # =========================================================================
    df_o = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            df,
        ],
        axis=1
    )
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Results: Even
    # =========================================================================
    df_e = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            df.iloc[:, [0]].rolling(2).mean(),
        ],
        axis=1
    )
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Odd
    # =========================================================================
    df_residuals_o = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            df.iloc[:, [0]].rolling(2).mean(),
        ],
        axis=1
    )
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Even
    # =========================================================================
    df_residuals_e = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            df.iloc[:, [0]],
        ],
        axis=1
    )
    chunk = df.iloc[:, [1]]
    for _ in range(k):
        chunk = chunk.rolling(2).mean()
        if _ % 2 == 1:
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Results: Odd
            # =================================================================
            df_o = pd.concat(
                [
                    df_o,
                    chunk.shift(-((1 + _) // 2)),
                ],
                axis=1
            )
            df_o.columns = (*df_o.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', )
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Odd
            # =================================================================
            df_residuals_o = pd.concat(
                [
                    df_residuals_o,
                    df_o.iloc[:, [-2]].pct_change(),
                ],
                axis=1
            )
        else:
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Results: Even
            # =================================================================
            df_e = pd.concat(
                [
                    df_e,
                    chunk.shift(-((1 + _) // 2)),
                ],
                axis=1
            )
            df_e.columns = (*df_e.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', )
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Even
            # =================================================================
            df_residuals_e = pd.concat(
                [
                    df_residuals_e,
                    df_e.iloc[:, [-1]].pct_change(-1).mul(-1),
                ],
                axis=1
            )
    return (
        df_o.set_index(df_o.columns[0]).dropna(how='all'),
        df_e.set_index(df_e.columns[0]).dropna(how='all'),
        df_residuals_o.set_index(df_residuals_o.columns[0]).dropna(how='all'),
        df_residuals_e.set_index(df_residuals_e.columns[0]).dropna(how='all')
    )


def lash_up_spline_ea(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    """
    Exponential Spline, Type A

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.iloc[:, 0]      Period
        df.iloc[:, 1]      Target Series
        ================== =================================
    n_spans : int
        Number of Spans.
    knots : tuple[int]
        Interpolation Knots.

    Returns
    -------
    tuple[DataFrame, tuple[float]]
        DESCRIPTION.

    """
    _params_a, _params_k, _splined = [], [], []
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using "continue" Statement
    # =========================================================================
    # =========================================================================
    # Coefficient Section
    # =========================================================================
    for j in range(n_spans):
        _params_a.append(
            ((df.iloc[knots[1 + j], 0] - df.iloc[knots[0], 0])*np.log(df.iloc[knots[j], 1]) - (df.iloc[knots[j], 0] -
                                                                                               df.iloc[knots[0], 0])*np.log(df.iloc[knots[1 + j], 1])) / (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
        )
        if j == 0:
            _params_k.append(
                (np.log(df.iloc[knots[1 + j], 1]) - np.log(df.iloc[knots[j], 1])) /
                (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
            )
        else:
            _params_k.append(
                _params_k[j - 1] + np.log(df.iloc[knots[1 + j], 1]) / (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0]) -
                (df.iloc[knots[1 + j], 0] - df.iloc[knots[j - 1], 0])*np.log(df.iloc[knots[j], 1]) / ((df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])*(df.iloc[knots[j], 0] - df.iloc[knots[j - 1], 0])) +
                np.log(df.iloc[knots[j - 1], 1]) /
                (df.iloc[knots[j], 0] - df.iloc[knots[j - 1], 0])
            )
        # =====================================================================
        # Splined Section
        # =====================================================================
        if 1 + j == n_spans:
            for i in range(knots[j], 1 + knots[1 + j]):
                _splined.append(
                    np.exp(_params_a[j] + _params_k[j] *
                           (df.iloc[i, 0] - df.iloc[0, 0]))
                )
        else:
            for i in range(knots[j], knots[1 + j]):
                _splined.append(
                    np.exp(_params_a[j] + _params_k[j] *
                           (df.iloc[i, 0] - df.iloc[0, 0]))
                )
    return (
        pd.concat(
            [
                df,
                DataFrame(_splined, columns=('Splined')),
            ],
            axis=1,
            sort=True
        ),
        tuple(_params_k)
    )


def lash_up_spline_eb(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    """
    Exponential Spline, Type B

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.iloc[:, 0]      Period
        df.iloc[:, 1]      Target Series
        ================== =================================
    n_spans : int
        Number of Spans.
    knots : tuple[int]
        Interpolation Knots.

    Returns
    -------
    tuple[DataFrame, tuple[float]]
        DESCRIPTION.

    """
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using "continue" Statement
    # =========================================================================
    _params_k, _splined = [], []
    # =========================================================================
    # Coefficient Section
    # =========================================================================
    for j in range(n_spans):
        _params_k.append(
            (np.log(df.iloc[knots[1 + j], 1]) - np.log(df.iloc[knots[j], 1]))/(
                df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
        )
        # =====================================================================
        # Spline Section
        # =====================================================================
        if 1 + j == n_spans:
            for i in range(knots[j], 1 + knots[1 + j]):
                _splined.append(
                    df.iloc[knots[j], 1]*np.exp(_params_k[j] *
                                                (df.iloc[i, 0] - df.iloc[knots[j], 0]))
                )
        else:
            for i in range(knots[j], knots[1 + j]):
                _splined.append(
                    df.iloc[knots[j], 1]*np.exp(_params_k[j] *
                                                (df.iloc[i, 0] - df.iloc[knots[j], 0]))
                )
    return (
        pd.concat(
            [
                df,
                DataFrame(_splined, columns=('Spline'))
            ],
            axis=1,
            sort=True
        ),
        tuple(_params_k)
    )


def _lash_up_spline_error_metrics(df: DataFrame) -> None:
    """Error Metrics Function"""
    print('Criterion, C: {:.6f}'.format(
        df.iloc[:, 2].div(df.iloc[:, 1]).sub(1).abs().mean()))


def lash_up_spline_la(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    """
    Linear Spline, Type A
        ================== =================================
        df.iloc[:, 0]      Period
        df.iloc[:, 1]      Target Series
        ================== =================================
        n_spans            Number of Spans
        knots              Interpolation Knots
        ================== =================================
    """
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using "continue" Statement
    # =========================================================================
    _params_a, _params_k, _splined = [], [], []
    for j in range(n_spans):
        _params_a.append(
            ((df.iloc[knots[1 + j], 0] - df.iloc[knots[0], 0])*df.iloc[knots[j], 1] - (df.iloc[knots[j], 0] -
                                                                                       df.iloc[knots[0], 0])*df.iloc[knots[1 + j], 1])/(df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
        )
        if j == 0:
            _params_k.append(
                (df.iloc[knots[1 + j], 1] - df.iloc[knots[j], 1]) /
                (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
            )
        else:
            _params_k.append(
                _params_k[j - 1] + df.iloc[knots[1 + j], 1]/(df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0]) -
                (df.iloc[knots[1 + j], 0] - df.iloc[knots[j - 1], 0])*df.iloc[knots[j], 1]/((df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])*(df.iloc[knots[j], 0] - df.iloc[knots[j - 1], 0])) +
                df.iloc[knots[j - 1], 1] /
                (df.iloc[knots[j], 0] - df.iloc[knots[j - 1], 0])
            )
        if 1 + j == n_spans:
            for i in range(knots[j], 1 + knots[1 + j]):
                _splined.append(
                    _params_a[j] + _params_k[j]*(df.iloc[i, 0] - df.iloc[0, 0])
                )
        else:
            for i in range(knots[j], knots[1 + j]):
                _splined.append(
                    _params_a[j] + _params_k[j]*(df.iloc[i, 0] - df.iloc[0, 0])
                )
    return (
        pd.concat(
            [
                df,
                DataFrame(_splined, columns=('Spline'))
            ],
            axis=1,
            sort=True
        ),
        tuple(_params_k)
    )


def lash_up_spline_lb(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    """
    Linear Spline, Type B
        ================== =================================
        df.iloc[:, 0]      Period
        df.iloc[:, 1]      Target Series
        ================== =================================
        n_spans            Number of Spans
        knots              Interpolation Knots
        ================== =================================
    """
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using "continue" Statement
    # =========================================================================
    _params_k, _splined = [], []
    for j in range(n_spans):
        _params_k.append(
            (df.iloc[knots[1 + j], 1] - df.iloc[knots[j], 1]) /
            (df.iloc[knots[1 + j], 0] - df.iloc[knots[j], 0])
        )
        if 1 + j == n_spans:
            for i in range(knots[j], 1 + knots[1 + j]):
                _splined.append(
                    df.iloc[knots[j], 1] + _params_k[j] *
                    (df.iloc[i, 0] - df.iloc[knots[j], 0])
                )
        else:
            for i in range(knots[j], knots[1 + j]):
                _splined.append(
                    df.iloc[knots[j], 1] + _params_k[j] *
                    (df.iloc[i, 0] - df.iloc[knots[j], 0])
                )
    return (
        pd.concat(
            [
                df,
                DataFrame(_splined, columns=('Spline'))
            ],
            axis=1,
            sort=True
        ),
        tuple(_params_k)
    )


def lash_up_spline_lls(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    """
    Linear Spline, Linear Regression Kernel
        ================== =================================
        df.iloc[:, 0]      Period
        df.iloc[:, 1]      Target Series
        ================== =================================
        n_spans            Number of Spans
        knots              Interpolation Knots
        ================== =================================
    """
    _params_a, _params_k, _splined = [], [], []
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using "continue" Statement
    # =========================================================================
    for _ in range(n_spans):
        if 1 + _ == n_spans:
            _s__x = df.iloc[knots[_]:, 0].sum()
            _s__y = df.iloc[knots[_]:, 1].sum()
            _s_x2 = df.iloc[knots[_]:, 0].pow(2).sum()
            _s_xy = df.iloc[knots[_]:, 0].mul(df.iloc[knots[_]:, 1]).sum()
            _params_a.append(
                ((1 + knots[1 + _] - knots[_])*_s_xy - _s__x*_s__y) /
                ((1 + knots[1 + _] - knots[_])*_s_x2 - _s__x**2)
            )
        else:
            _s__x = df.iloc[knots[_]:knots[1 + _], 0].sum()
            _s__y = df.iloc[knots[_]:knots[1 + _], 1].sum()
            _s_x2 = df.iloc[knots[_]:knots[1 + _], 0].pow(2).sum()
            _s_xy = df.iloc[knots[_]:knots[1 + _],
                            0].mul(df.iloc[knots[_]:knots[1 + _], 1]).sum()
            if _ == 0:
                _params_a.append(
                    (_s__y*_s_x2 - _s__x*_s_xy) /
                    ((knots[1 + _] - knots[_])*_s_x2 - _s__x**2)
                )
            _params_a.append(
                ((knots[1 + _] - knots[_])*_s_xy - _s__x*_s__y) /
                ((knots[1 + _] - knots[_])*_s_x2 - _s__x**2)
            )

    for _ in range(n_spans):
        if _ == 0:
            _params_k.append(_params_a[_])
        else:
            _params_k.append(
                _params_k[_ - 1] + (_params_a[_] - _params_a[1 + _])*df.iloc[knots[_], 0])

        if 1 + _ == n_spans:
            for _i in range(knots[_], 1 + knots[1 + _]):
                _splined.append(_params_k[_] + _params_a[1 + _]*df.iloc[_i, 0])
        else:
            for _i in range(knots[_], knots[1 + _]):
                _splined.append(_params_k[_] + _params_a[1 + _]*df.iloc[_i, 0])
    return (
        pd.concat(
            [
                df,
                DataFrame(_splined, columns=('Splined')),
            ],
            axis=1,
            sort=True
        ),
        tuple(_params_a)
    )


def _lash_up_spline_print_params(n_spans: int, params: tuple[float]) -> None:
    """
    Results Delivery Function
    ================== =================================
    n_spans            Number of Spans
    params             Coefficients
    ================== =================================
    """
    if n_spans == len(params):
        for _, param in enumerate(params, start=1):
            print(f'Model Parameter: K{_:02d} = {param:.6f}')
    else:
        # =====================================================================
        # n_spans (1 + N): 1 + Number of Spans
        # =====================================================================
        for _, param in enumerate(params):
            print(f'Model Parameter: A{_:02n} = {param:.6f}')


def run_lash_up_spline(df: DataFrame, kernel: callable) -> None:
    """
    Interactive Shell for Processing Make Shift Spline Functions

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    kernel : callable
        One Out of lash_up_spline_ea(), lash_up_spline_eb(), lash_up_spline_la(), lash_up_spline_lb(), lash_up_spline_lls().

    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.
    """
    df.reset_index(level=0, inplace=True)
    df.columns = ('Period', 'Original')
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Interpolation Spans (N, N >= 2): '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 2, f'N >= 2 is Required, N = {N} Was Provided'
    # =========================================================================
    # Switch Knots
    # =========================================================================
    _knots = [0]
    _ = 0
    # =========================================================================
    # Although N >=2, Left for Consistency Purpose Only
    # =========================================================================
    if N == 1:
        _knots.append(df.index[-1])
    elif N >= 2:
        while _ < N:
            if 1 + _ == N:
                _knots.append(df.index[-1])
            else:
                _knot = int(input('Select Row for Year: ')) - 1
                # =============================================================
                # Ensure Knots Are In Ascending Order
                # =============================================================
                if _knot > _knots[_]:
                    _knots.append(_knot)
            _ += 1
    else:
        # =====================================================================
        # Should Never Happen
        # =====================================================================
        print("Error")
    _knots = tuple(_knots)
    df_splined, _params = kernel(df, N, _knots)
    _lash_up_spline_print_params(N, _params)
    _lash_up_spline_error_metrics(df_splined)
    plt.figure()
    plt.scatter(df_splined.iloc[:, 0], df_splined.iloc[:, 1])
    plt.plot(
        df_splined.iloc[:, 0],
        df_splined.iloc[:, 2],
        color='red',
        label=f'$s_{0}(\\tau)$'
    )
    _go_no_go = input('Does the Resulting Series Need an Improvement?, Y: ')
    if _go_no_go.lower() == 'y':
        assert len(_knots) == 1 + N
        _correction_factors = [
            float(
                input(f'Correction Factor of Knot {1 + _:02d} out of {len(_knots):02d}: '))
            for _, _knot in enumerate(_knots)
        ]
        # =====================================================================
        # Series Modification
        # =====================================================================
        modified = df.copy()
        for _knot, _factor in zip(_knots, _correction_factors):
            modified.iloc[_knot, 1] = modified.iloc[_knot, 1]*_factor

        modified.columns = ('Period', 'Corrected')
        df_splined, _params = kernel(modified, N, _knots)
        _lash_up_spline_print_params(N, _params)
        _lash_up_spline_error_metrics(df_splined)
        plt.plot(
            df_splined.iloc[:, 0],
            df_splined.iloc[:, 2],
            color='g',
            label=f'$s_{1}(\\tau)$'
        )
    plt.grid()
    plt.legend()
    plt.show()


def price_direct(df: DataFrame, year_base: int) -> DataFrame:
    """
    Returns Cumulative Price Index for Base Year
    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Growth Rate
        ================== =================================
    year_base : int
        Base Year.

    Returns
    -------
    DataFrame
    """
    # =========================================================================
    # Cumulative Price Index
    # =========================================================================
    df['p_i'] = df.iloc[:, 0].add(1).cumprod()
    # =========================================================================
    # Cumulative Price Index for the Base Year
    # =========================================================================
    df['cpi'] = df.iloc[:, 1].div(df.iloc[year_base-df.index[0], 1])
    return df.iloc[:, [-1]]


def price_inverse(df: DataFrame) -> DataFrame:
    """
    Returns Growth Rate from Cumulative Price Index for Some Base Year

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Cumulative Price Index for Some Base Year
        ================== =================================
    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    df['gri'] = df.iloc[:, [-1]].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)


def price_inverse_double(df: DataFrame) -> DataFrame:
    """
    Returns Growth Rate from Nominal & Real Prices Series

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal Prices
        df.iloc[:, 1]      Real Prices
        ================== =================================
    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    df['cpi'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['gri'] = df.iloc[:, [-1]].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)


def filter_rolling_mean(df: DataFrame, k: int = None) -> tuple[DataFrame]:
    """
    Rolling Mean Filter

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    k : int, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    tuple[DataFrame]
        DESCRIPTION.

    """
    if k is None:
        k = df.shape[0] // 2
    df.reset_index(level=0, inplace=True)
    # =========================================================================
    # DataFrame for Rolling Mean Filter Results: Odd
    # =========================================================================
    df_o = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            df,
        ],
        axis=1,
    )
    # =========================================================================
    # DataFrame for Rolling Mean Filter Results: Even
    # =========================================================================
    df_e = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            df.iloc[:, [0]].rolling(2, center=True).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # DataFrame for Rolling Mean Filter Residuals: Odd
    # =========================================================================
    df_residuals_o = pd.concat(
        [
            # =================================================================
            # Period Shift
            # =================================================================
            df.iloc[:, [0]].rolling(2).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # DataFrame for Rolling Mean Filter Residuals: Even
    # =========================================================================
    df_residuals_e = pd.concat(
        [
            # =================================================================
            # No Period Shift
            # =================================================================
            df.iloc[:, [0]],
        ],
        axis=1,
    )
    for _ in range(k):
        if _ % 2 == 1:
            # =================================================================
            # DataFrame for Rolling Mean Filter Results: Odd
            # =================================================================
            df_o = pd.concat(
                [
                    df_o,
                    df.iloc[:, [1]].rolling(2 + _, center=True).mean(),
                ],
                axis=1,
            )
            df_o.columns = (*df_o.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', )
            # =================================================================
            # DataFrame for Rolling Mean Filter Residuals: Odd
            # =================================================================
            df_residuals_o = pd.concat(
                [
                    df_residuals_o,
                    df_o.iloc[:, [-2]].pct_change(),
                ],
                axis=1,
            )
        else:
            # =================================================================
            # DataFrame for Rolling Mean Filter Results: Even
            # =================================================================
            df_e = pd.concat(
                [
                    df_e,
                    df.iloc[:, [1]].rolling(2 + _, center=True).mean(),
                ],
                axis=1,
            )
            df_e.columns = (*df_e.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', )
            # =================================================================
            # DataFrame for Rolling Mean Filter Residuals: Even
            # =================================================================
            df_residuals_e = pd.concat(
                [
                    df_residuals_e,
                    df_e.iloc[:, [-1]].pct_change(-1).mul(-1),
                ],
                axis=1,
            )
    return (
        df_o.set_index(df_o.columns[0]).dropna(how='all'),
        df_e.set_index(df_e.columns[0]).dropna(how='all'),
        df_residuals_o.set_index(df_residuals_o.columns[0]).dropna(how='all'),
        df_residuals_e.set_index(df_residuals_e.columns[0]).dropna(how='all')
    )


def simple_linear_regression(df: DataFrame) -> tuple[DataFrame, tuple[float]]:
    """
    Determining of Coefficients of Regression

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Regressor
        df.iloc[:, 1]      Regressand
        ================== =================================
    Returns
    -------
    tuple[DataFrame, tuple[float]]
        DESCRIPTION.

    """
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    params, _ess, *_ = np.polyfit(
        df.iloc[:, 0],
        df.iloc[:, 1],
        deg=1,
        full=True
    )
    # =========================================================================
    # Approximation
    # =========================================================================
    df[f'{df.columns[1]}_estimate'] = np.poly1d(params)(df.iloc[:, 0])
    _r = r2_score(df.iloc[:, 1], df.iloc[:, -1])
    _tss = _ess[0] / (1 - _r)
    # =========================================================================
    # Delivery Block
    # =========================================================================
    print('Period From {} Through {}'.format(*df.index[[0, -1]]))
    print('Model: Yhat = {:,.4f} + {:,.4f}*X'.format(*params[::-1]))
    for _, param in enumerate(params[::-1]):
        print(f'Model Parameter: A_{_} = {param:,.4f}')

    print(
        'Model Result: ESS = {:,.4f}; TSS = {:,.4f}; R^2 = {:,.4f}'.format(
            _ess[0],
            _tss,
            _r
        )
    )
    return df, tuple(params)


def get_price_base(df: DataFrame) -> int:
    """
    Determine Base Year
    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator
        ================== =================================
    Returns
    -------
    int
        Base Year.
    """
    df['__deflator'] = df.iloc[:, 0].sub(100).abs()
    return int(df.index[df.iloc[:, -1].astype(float).argmin()])


def get_price_base_nr(df: DataFrame, columns: tuple[int] = (0, 1)) -> int:
    """
    Determine Base Year

    Parameters
    ----------
    df : DataFrame
        ======================== ===========================
        df.index                 Period
        ...                      ...
        df.iloc[:, columns[0]]   Nominal
        df.iloc[:, columns[-1]]  Real
        ======================== ===========================
    columns : tuple[int], optional
        Column Nominal, Column Real. The default is (0, 1).

    Returns
    -------
    int
        Base Year.

    """
    df['__deflator'] = df.iloc[:, columns[0]].div(
        df.iloc[:, columns[-1]]
    ).sub(1).abs()
    # =========================================================================
    # Basic Year
    # =========================================================================
    return int(df.index[df.iloc[:, -1].astype(float).argmin()])


def construct_usa_hist_deflator(series_ids: dict[str, str]) -> DataFrame:
    """


    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator PRC
        ================== =================================
    """
    return stockpile(series_ids).pipe(transform_deflator)


def lab_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
    return np.multiply(np.power(array, -k), b)


def cap_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
    return np.multiply(np.power(array, 1-k), b)
