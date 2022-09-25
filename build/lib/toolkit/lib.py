#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:25:52 2022

@author: alexander
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.interpolate import UnivariateSpline
from sklearn.metrics import mean_squared_error


def calculate_capital(df: DataFrame, p_i: tuple[float], p_t: tuple[float], ratio: float):
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Investment
    df.iloc[:, 1]      Production
    df.iloc[:, 2]      Capital
    df.iloc[:, 3]      Capital Retirement
    ================== =================================
    p_i[0]: S - Gross Fixed Investment to Gross Domestic Product Ratio - Slope over Period,
    p_i[1]: S - Gross Fixed Investment to Gross Domestic Product Ratio - Absolute Term over Period,
    p_t[0]: Λ - Fixed Assets Turnover Ratio - Slope over Period,
    p_t[1]: Λ - Fixed Assets Turnover Ratio - Absolute Term over Period,
    ratio: Investment to Capital Conversion Ratio
    '''
    return df.index.to_series().shift(1).mul(p_i[0]).add(p_i[1]).mul(df.index.to_series().shift(1).mul(p_t[0]).add(p_t[1])).mul(ratio).add(1).sub(df.iloc[:, 3].shift(1)).mul(df.iloc[:, 2].shift(1))


def calculate_curve_fit_params(df: DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital
    df.iloc[:, 1]      Labor
    df.iloc[:, 2]      Product
    ================== =================================
    '''
    # =========================================================================
    # TODO: Use Feed from transform_cobb_douglas()
    # =========================================================================

    def _curve(regressor: pd.Series, b: float, k: float) -> pd.Series:
        return regressor.pow(k).mul(b)

    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(
        df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(
        df.iloc[:, 1])
    params, matrix = optimization.curve_fit(
        _curve,
        df.iloc[:, -2],
        df.iloc[:, -1],
        np.array([1.0, 0.5])
    )
    print('Factor, b: {:,.4f}; Index, k: {:,.4f}'.format(*params))


def calculate_plot_uspline(df: DataFrame):
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Capital
    df.iloc[:, 1]      Labor
    df.iloc[:, 2]      Product
    ================== =================================
    '''
    # =========================================================================
    # TODO: Increase Cohesion
    # =========================================================================
    # =========================================================================
    # TODO: Use Feed from transform_cobb_douglas()
    # =========================================================================
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    chunk = df.iloc[:, -2:]
    chunk.sort_values(chunk.columns[0], inplace=True)
    spl = UnivariateSpline(chunk.iloc[:, [0]], chunk.iloc[:, [1]])
    # =========================================================================
    # _new_axis = np.linspace(chunk.iloc[:, [0]].min(), chunk.iloc[:, [0]].max(), chunk.shape[0] - 1)
    # =========================================================================
    plt.figure()
    plt.scatter(chunk.iloc[:, [0]], chunk.iloc[:, [1]], label='Original')
    plt.plot(
        chunk.iloc[:, 0],
        spl(chunk.iloc[:, 0]),
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
    plt.grid(True)
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


def calculate_power_function_fit_params_a(df: DataFrame, params: tuple[float]):
    '''
    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Regressor: = Period
    df.iloc[:, 0]      Regressand
    ================== =================================
    params : tuple[float]
        Parameters.

    Returns
    -------
    None.

    '''
    df.reset_index(level=0, inplace=True)
    _t_0 = df.iloc[:, 0].min() - 1
    # =========================================================================
    # {RESULT}(Yhat) = params[0] + params[1]*(T-T_0)**params[2]
    # =========================================================================
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:, 0].sub(_t_0).pow(
        params[2]).mul(params[1]).add(params[0])
    print(f'Model Parameter: T_0 = {_t_0};')
    print(f'Model Parameter: Y_0 = {params[0]};')
    print(f'Model Parameter: A = {params[1]:.4f};')
    print(f'Model Parameter: Alpha = {params[2]:.4f};')
    print(f'Estimator Result: Mean Value: {df.iloc[:, 2].mean():,.4f};')
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f};'.format(
        mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])
    )
    )
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}.'.format(
        np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]))
    )
    )


def calculate_power_function_fit_params_b(df: DataFrame, params: tuple[float]):
    '''
    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Regressor
    df.iloc[:, 1]      Regressand
    ================== =================================
    params : tuple[float]
        Model Parameters.

    Returns
    -------
    None.

    '''
    _param = (params[3]-params[2])/(params[1]-params[0])**params[4]
    # =========================================================================
    # '{RESULT}(Yhat) = U_1 + ((U_2-U_1)/(TAU_2-TAU_1)**Alpha)*({X}-TAU_1)**Alpha'
    # =========================================================================
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:, 0].sub(params[0]).pow(
        params[4]).mul(_param).add(params[2])
    print(f'Model Parameter: TAU_1 = {params[0]};')
    print(f'Model Parameter: TAU_2 = {params[1]};')
    print(f'Model Parameter: U_1 = {params[2]};')
    print(f'Model Parameter: U_2 = {params[3]};')
    print(f'Model Parameter: Alpha = {params[4]:.4f};')
    print(
        f'Model Parameter: A: = (U_2-U_1)/(TAU_2-TAU_1)**Alpha = {_param:,.4f};'
    )
    print(f'Estimator Result: Mean Value: {df.iloc[:, 1].mean():,.4f};')
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f};'.format(
        mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])
    )
    )
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}.'.format(
        np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]))
    )
    )


def calculate_power_function_fit_params_c(df: DataFrame, params: tuple[float]):
    '''
    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Regressor
    df.iloc[:, 1]      Regressand
    ================== =================================
    params : tuple[float]
        Model Parameters.

    Returns
    -------
    None.

    '''
    _alpha = (np.log(params[3])-np.log(params[2])) / \
        (np.log(params[0])-np.log(params[1]))
    # =========================================================================
    # '{RESULT}{Hat}{Y} = Y_1*(X_1/{X})**Alpha'
    # =========================================================================
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:,
                                               0].rdiv(params[0]).pow(_alpha).mul(params[2])
    print(f'Model Parameter: X_1 = {params[0]:.4f};')
    print(f'Model Parameter: X_2 = {params[1]};')
    print(f'Model Parameter: Y_1 = {params[2]:.4f};')
    print(f'Model Parameter: Y_2 = {params[3]};')
    print(f'Model Parameter: Alpha: = LN(Y_2/Y_1)/LN(X_1/X_2) = {_alpha:.4f};')
    print(f'Estimator Result: Mean Value: {df.iloc[:, 1].mean():,.4f};')
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f};'.format(
        mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])
    )
    )
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}.'.format(
        np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]))
    )
    )


def kol_zur_filter(df: DataFrame, k: int = None) -> tuple[DataFrame]:
    '''Kolmogorov--Zurbenko Filter
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    '''
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
    residuals_o = pd.concat(
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
    residuals_e = pd.concat(
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
            df_o.columns = [*df_o.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Odd
            # =================================================================
            residuals_o = pd.concat(
                [
                    residuals_o,
                    df_o.iloc[:, [-2]
                              ].div(df_o.iloc[:, [-2]].shift(1)).sub(1),
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
            df_e.columns = [*df_e.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Kolmogorov--Zurbenko Filter Residuals: Even
            # =================================================================
            residuals_e = pd.concat(
                [
                    residuals_e,
                    df_e.iloc[:, [-1]
                              ].shift(-1).div(df_e.iloc[:, [-1]]).sub(1),
                ],
                axis=1
            )
    df_o.set_index(df_o.columns[0], inplace=True)
    df_e.set_index(df_e.columns[0], inplace=True)
    residuals_o.set_index(residuals_o.columns[0], inplace=True)
    residuals_e.set_index(residuals_e.columns[0], inplace=True)
    df_o.dropna(how='all', inplace=True)
    df_e.dropna(how='all', inplace=True)
    residuals_o.dropna(how='all', inplace=True)
    residuals_e.dropna(how='all', inplace=True)
    return df_o, df_e, residuals_o, residuals_e


def mean_by_year(df: DataFrame) -> DataFrame:
    '''
    Process Non-Indexed Flat DataFrame
    Parameters
    ----------
    df : DataFrame
    Returns
    -------
    DataFrame
    '''
    # =========================================================================
    # Index Width Check
    # =========================================================================
    width = 0
    for item in df.index:
        width = max(len(f'{item}'), width)
    if width > 4:
        df[['YEAR', 'Q']] = df.index.to_series().str.split('-', expand=True)
        df = df.iloc[:, [1, 0]]
        df = df.apply(pd.to_numeric)
        df = df.groupby('YEAR').mean()
        df.index.rename('REF_DATE', inplace=True)
    return df


def m_spline_ea(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    '''Exponential Spline, Type A
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    _params_a, _params_k, _splined = [], [], []
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
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
                DataFrame(_splined, columns=['Splined']),
            ],
            axis=1, sort=True),
        tuple(_params_k)
    )


def m_spline_eb(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    '''Exponential Spline, Type B
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
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
                DataFrame(_splined, columns=['Spline'])
            ],
            axis=1, sort=True),
        tuple(_params_k)
    )


def _m_spline_error_metrics(df: DataFrame) -> None:
    '''Error Metrics Function'''
    print('Criterion, C: {:.6f}'.format(
        df.iloc[:, 2].div(df.iloc[:, 1]).sub(1).abs().mean()))


def m_spline_la(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    '''Linear Spline, Type A
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
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
                DataFrame(_splined, columns=['Spline'])
            ],
            axis=1, sort=True),
        tuple(_params_k)
    )


def m_spline_lb(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    '''Linear Spline, Type B
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
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
                DataFrame(_splined, columns=['Spline'])
            ],
            axis=1, sort=True),
        tuple(_params_k)
    )


def m_spline_lls(df: DataFrame, n_spans: int, knots: tuple[int]) -> tuple[DataFrame, tuple[float]]:
    '''Linear Spline, Linear Regression Kernel
    ================== =================================
    df.iloc[:, 0]      Period
    df.iloc[:, 1]      Target Series
    ================== =================================
    n_spans            Number of Spans
    knots              Interpolation Knots
    ================== =================================
    '''
    _params_a, _params_k, _splined = [], [], []
    # =========================================================================
    # TODO: Rework Algorithm To Make It More Clear Possibly Using `continue` Statement
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
                DataFrame(_splined, columns=['Splined']),
            ],
            axis=1, sort=True),
        tuple(_params_a)
    )


def _m_spline_print_params(n_spans: int, params: tuple[float]) -> None:
    '''
    Results Delivery Function
    ================== =================================
    n_spans            Number of Spans
    params             Coefficients
    ================== =================================
    '''
    if n_spans == len(params):
        for _, _param in enumerate(params, start=1):
            print(f'Model Parameter: K{_:02d} = {_param:.6f}')
    else:
        # =====================================================================
        # n_spans (1 + N): 1 + Number of Spans
        # =====================================================================
        for _, _param in enumerate(params):
            print(f'Model Parameter: A{_:02n} = {_param:.6f}')


def m_spline_manager(df: DataFrame, kernel: callable) -> None:
    '''
    Interactive Shell for Processing Make Shift Spline Functions

    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    kernel : callable
        One Out of m_spline_ea(), m_spline_eb(), m_spline_la(), m_spline_lb(), m_spline_lls().

    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.
    '''
    df.reset_index(level=0, inplace=True)
    df.columns = ['Period', 'Original']
    # =========================================================================
    # Number of Periods
    # =========================================================================
    N = int(input('Define Number of Interpolation Spans (N, N >= 2): '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 2, f'N >= 2 is Required, N = {N} Was Provided'
    # =========================================================================
    # Switch Knots
    # =========================================================================
    _knots = [0, ]
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
        print('Error')
    _knots = tuple(_knots)
    splined_frame, _params = kernel(df, N, _knots)
    _m_spline_print_params(N, _params)
    _m_spline_error_metrics(splined_frame)
    plt.figure()
    plt.scatter(splined_frame.iloc[:, 0], splined_frame.iloc[:, 1])
    plt.plot(
        splined_frame.iloc[:, 0],
        splined_frame.iloc[:, 2],
        color='red',
        label='$s_{}(\\tau)$'.format(0,)
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

        modified.columns = ['Period', 'Corrected']
        splined_frame, _params = kernel(modified, N, _knots)
        _m_spline_print_params(N, _params)
        _m_spline_error_metrics(splined_frame)
        plt.plot(
            splined_frame.iloc[:, 0],
            splined_frame.iloc[:, 2],
            color='g',
            label='$s_{}(\\tau)$'.format(1,)
        )
    plt.grid(True)
    plt.legend()
    plt.show()


def price_direct(df: DataFrame, base: int) -> DataFrame:
    '''
    Returns Cumulative Price Index for Base Year
    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Growth Rate
    ================== =================================
    base : int
        Base Year.

    Returns
    -------
    DataFrame
    '''
    # =========================================================================
    # Cumulative Price Index
    # =========================================================================
    df['p_i'] = df.iloc[:, 0].add(1).cumprod()
    # =========================================================================
    # Cumulative Price Index for the Base Year
    # =========================================================================
    df['cpi'] = df.iloc[:, 1].div(df.iloc[base-df.index[0], 1])
    return df.iloc[:, [-1]]


def price_inverse(df: DataFrame) -> DataFrame:
    '''
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

    '''
    df['gri'] = df.iloc[:, [-1]].div(df.iloc[:, [-1]].shift(1)).sub(1)
    return df.iloc[:, [-1]].dropna(axis=0)


def price_inverse_double(df: DataFrame) -> DataFrame:
    '''
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

    '''
    df['cpi'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['gri'] = df.iloc[:, [-1]].div(df.iloc[:, [-1]].shift(1)).sub(1)
    return df.iloc[:, [-1]].dropna(axis=0)


def price_inverse_single(df: DataFrame) -> DataFrame:
    '''
    Returns Prices Icrement Series from Cumulative Deflator Series

    Parameters
    ----------
    df : DataFrame
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      TODO: Prices
    ================== =================================
    Returns
    -------
    DataFrame
        TODO: DESCRIPTION.

    '''
    return df.div(df.shift(1)).sub(1)


def strip_cumulated_deflator(df: DataFrame):
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return price_inverse_single(df.dropna()).dropna()


def build_load_data_frame(file_name: str, criteria: dict) -> None:
    '''
    Builds DataFrame & Loads It To Excel

    Parameters
    ----------
    file_name : str
        Excel File Name.
    criteria : dict
        DESCRIPTION.

    Returns
    -------
    None
    '''
    df = DataFrame()
    for criterion in criteria:
        _df = extract_can_from_url(string_to_url(criterion['file_name']))
        _df = _df[_df['VECTOR'].isin(criterion['series_ids'])]
        _df = _df[['REF_DATE', 'VECTOR', 'VALUE']]
        for series_id in criterion['series_ids']:
            chunk = _df[_df['VECTOR'] == series_id]
            chunk.set_index(chunk.columns[0], inplace=True)
            chunk = chunk.iloc[:, [1]]
            chunk = mean_by_year(chunk)
            chunk.rename(columns={'VALUE': series_id}, inplace=True)
            df = pd.concat([df, chunk], axis=1, sort=True)
    df.to_excel(file_name)


def rolling_mean_filter(df: DataFrame, k: int = None) -> tuple[DataFrame]:
    '''
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

    '''
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
    residuals_o = pd.concat(
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
    residuals_e = pd.concat(
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
            df_o.columns = [*df_o.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Rolling Mean Filter Residuals: Odd
            # =================================================================
            residuals_o = pd.concat(
                [
                    residuals_o,
                    df_o.iloc[:, [-2]
                              ].div(df_o.iloc[:, [-2]].shift(1)).sub(1),
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
            df_e.columns = [*df_e.columns[:-1],
                            f'{df.columns[1]}_{hex(2 + _)}', ]
            # =================================================================
            # DataFrame for Rolling Mean Filter Residuals: Even
            # =================================================================
            residuals_e = pd.concat(
                [
                    residuals_e,
                    df_e.iloc[:, [-1]
                              ].shift(-1).div(df_e.iloc[:, [-1]]).sub(1),
                ],
                axis=1,
            )
    df_o.set_index(df_o.columns[0], inplace=True)
    df_e.set_index(df_e.columns[0], inplace=True)
    residuals_o.set_index(residuals_o.columns[0], inplace=True)
    residuals_e.set_index(residuals_e.columns[0], inplace=True)
    df_o.dropna(how='all', inplace=True)
    df_e.dropna(how='all', inplace=True)
    residuals_o.dropna(how='all', inplace=True)
    residuals_e.dropna(how='all', inplace=True)
    return df_o, df_e, residuals_o, residuals_e


def simple_linear_regression(df: DataFrame) -> tuple[DataFrame, tuple[float]]:
    '''
    Determine Regression Coefficients

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

    '''
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
    df[f'{df.columns[1]}_estimate'] = df.iloc[:, 0].mul(
        params[0]).add(params[1])
    _r = r2_score(df.iloc[:, 1], df.iloc[:, -1])
    _tss = _ess[0] / (1 - _r)
    # =========================================================================
    # Delivery Block
    # =========================================================================
    print('Period From {} Through {}'.format(*df.index[[0, -1]]))
    print('Model: Yhat = {:,.4f} + {:,.4f}*X'.format(*params[::-1]))
    print('Model Parameter: A_0 = {:,.4f}'.format(params[1]))
    print('Model Parameter: A_1 = {:,.4f}'.format(params[0]))
    print('Model Result: ESS = {:,.4f}; TSS = {:,.4f}; R^2 = {:,.4f}'.format(
        _ess[0],
        _tss,
        _r
    ))
    return df, tuple(params)
