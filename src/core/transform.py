#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 17:42:38 2022

@author: Alexander Mikhailov
"""

import numpy as np
from pandas import DataFrame

from .tools import calculate_capital, get_price_base_nr


def transform_investment_manufacturing(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      National Income
        df.iloc[:, 2]      Nominal Gross Domestic Product
        df.iloc[:, 3]      Real Gross Domestic Product
        ================== =================================.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    df = df.div(df.iloc[0, :]).dropna(axis=0)
    # =========================================================================
    # "Real" Investment
    # =========================================================================
    df['investment'] = df.iloc[:, 0].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
    # =========================================================================
    # "Real" Manufacturing
    # =========================================================================
    df['manufacturing'] = df.iloc[:, 1].mul(
        df.iloc[:, 3]).div(df.iloc[:, 2])
    df['inv_roll_mean'] = df.iloc[:, -2].rolling(2).mean()
    df['prd_roll_mean'] = df.iloc[:, -2].rolling(2).mean()
    return df


def transform_investment(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Nominal Gross Domestic Product
        df.iloc[:, 2]      Real Gross Domestic Product
        df.iloc[:, 3]      <M1> OR <Prime Rate>
        ================== =================================.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    # =========================================================================
    # "Real" Investment
    # =========================================================================
    df['investment'] = df.iloc[:, 0].mul(df.iloc[:, 2]).div(df.iloc[:, 1])
    return df


def transform_cobb_douglas(df: DataFrame, year_base: int) -> tuple[DataFrame, tuple[float]]:
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Labor
        df.iloc[:, 2]      Product
        ================== =================================
    """
    df = df.div(df.loc[year_base, :])
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Original: k=0.25, b=1.01
    # =========================================================================
    k, b = np.polyfit(
        np.log(df.iloc[:, -2].astype(float)),
        np.log(df.iloc[:, -1].astype(float)),
        deg=1
    )
    # =========================================================================
    # Scipy Signal Median Filter, Non-Linear Low-Pass Filter
    # =========================================================================
    # =========================================================================
    # k, b = np.polyfit(
    #     np.log(signal.medfilt(df.iloc[:, -2])),
    #     np.log(signal.medfilt(df.iloc[:, -1])),
    #     deg=1
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
    df['prod_roll'] = df.iloc[:, 2].rolling(3, center=True).mean()
    df['prod_roll_sub'] = df.iloc[:, 2].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product
    # =========================================================================
    df['prod_comp'] = df.iloc[:, 0].pow(k).mul(
        df.iloc[:, 1].pow(1-k)).mul(np.exp(b))
    # =========================================================================
    # Computed Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_comp_roll'] = df.iloc[:, -1].rolling(3, center=True).mean()
    df['prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    # =========================================================================
    #     print(f"R**2: {r2_score(df.iloc[:, 2], df.iloc[:, 3]):,.4f}")
    #     print(df.iloc[:, 3].div(df.iloc[:, 2]).sub(1).abs().mean())
    # =========================================================================
    return df, (k, np.exp(b))


def transform_cobb_douglas_alt(df: DataFrame, year_base: int) -> tuple[DataFrame, tuple[float]]:
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Labor
        df.iloc[:, 2]      Product
        df.iloc[:, 3]      Product Alternative
        ================== =================================
    """
    df = df.div(df.loc[year_base, :])
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Original: k=0.25, b=1.01
    # =========================================================================
    k, b = np.polyfit(
        np.log(df.iloc[:, -2]),
        np.log(df.iloc[:, -1]),
        deg=1
    )
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
    df['prod_roll'] = df.iloc[:, 2].rolling(3, center=True).mean()
    df['prod_roll_sub'] = df.iloc[:, 2].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product
    # =========================================================================
    df['prod_comp'] = df.iloc[:, 0].pow(k).mul(
        df.iloc[:, 1].pow(1-k)).mul(np.exp(b))
    # =========================================================================
    # Computed Product Trend Line=3 Year Moving Average
    # =========================================================================
    df['prod_comp_roll'] = df.iloc[:, -1].rolling(3, center=True).mean()
    df['prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    # =========================================================================
    # Labor Productivity Alternative
    # =========================================================================
    df['_lab_product'] = df.iloc[:, 3].div(df.iloc[:, 1])
    # =========================================================================
    # Original: _k=0.25, _b=1.01
    # =========================================================================
    _k, _b = np.polyfit(
        np.log(df.iloc[:, 4]),
        np.log(df.iloc[:, -1]),
        deg=1
    )
    # =========================================================================
    # Fixed Assets Turnover Alternative
    # =========================================================================
    df['_c_turnover'] = df.iloc[:, 3].div(df.iloc[:, 0])
    # =========================================================================
    # Product Alternative Trend Line=3 Year Moving Average
    # =========================================================================
    df['_prod_roll'] = df.iloc[:, 3].rolling(3, center=True).mean()
    df['_prod_roll_sub'] = df.iloc[:, 3].sub(df.iloc[:, -1])
    # =========================================================================
    # Computed Product Alternative
    # =========================================================================
    df['_prod_comp'] = df.iloc[:, 0].pow(_k).mul(
        df.iloc[:, 1].pow(1-_k)).mul(np.exp(_b))
    # =========================================================================
    # Computed Product Alternative Trend Line=3 Year Moving Average
    # =========================================================================
    df['_prod_comp_roll'] = df.iloc[:, -
                                    1].rolling(3, center=True).mean()
    df['_prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    return df, ((k, np.exp(b)), (_k, np.exp(_b)))


def transform_cobb_douglas_extension_capital(df: DataFrame) -> DataFrame:
    """
    Manufacturing Fixed Assets Series Comparison

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      CDT2S1
        df.iloc[:, 1]      CDT2S3
        df.iloc[:, 2]      CDT2S4
        df.iloc[:, 3]      P0107
        df.iloc[:, 4]      P0110
        df.iloc[:, 5]      P0119
        df.iloc[:, 6]      KTA15S08
        df.iloc[:, 7]      DT63AS01
        df.iloc[:, 8]      frb_nominal
        df.iloc[:, 9]      frb_real
        ================== =================================

    Returns
    -------
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal Extended
        ================== =================================
    """
    # =========================================================================
    # Convert Capital Series into Current (Historical) Prices
    # =========================================================================
    df['nominal_cbb_dg'] = df.iloc[:, 0].mul(
        df.iloc[:, 2]).div(df.iloc[:, 1]).div(1000)
    df['nominal_uscb'] = df.iloc[:, 3].mul(df.iloc[:, 5]).div(df.iloc[:, 4])
    df['nominal_dougls'] = df.iloc[:, 0].mul(
        df.iloc[:, 7]).div(df.iloc[:, 1]).div(1000)
    df['nominal_kndrck'] = df.iloc[:, 3].mul(
        df.iloc[:, 6]).div(df.iloc[:, 4]).div(1000)
    df.iloc[:, -1] = df.iloc[:, -1].mul(
        df.loc[1929, df.columns[4]]).div(df.loc[1929, df.columns[3]])
    # =========================================================================
    # P.H. Douglas -- J.W. Kendrick (Blended) Series
    # =========================================================================
    df['nominal_doug_kndrck'] = df.iloc[:, -2:].mean(axis=1)
    # =========================================================================
    # C.W. Cobb, P.H. Douglas -- FRB (Blended) Series
    # =========================================================================
    df['nominal_cbb_dg_frb'] = df.iloc[:, [8, -5]].mean(axis=1)
    # =========================================================================
    # Capital Structure Series: "C.W. Cobb, P.H. Douglas -- FRB (Blended) Series" to "P.H. Douglas -- J.W. Kendrick (Blended) Series"
    # =========================================================================
    df['struct_ratio'] = df.iloc[:, -1].div(df.iloc[:, -2])
    # =========================================================================
    # Filling the Gaps within Capital Structure Series
    # =========================================================================
    df.loc[1899:, df.columns[-1]].fillna(0.275, inplace=True)
    df.loc[:, df.columns[-1]].fillna(
        df.loc[1899, df.columns[-1]], inplace=True
    )
    # =========================================================================
    # Patch Series "P.H. Douglas -- J.W. Kendrick (Blended) Series" Multiplied by "Capital Structure Series"
    # =========================================================================
    df['nominal_patch'] = df.iloc[:, -3].mul(df.iloc[:, -1])
    # =========================================================================
    # "C.W. Cobb, P.H. Douglas -- FRB (Blended) Series" Patched with "Patch Series"
    # =========================================================================
    df['nominal_extended'] = df.iloc[:, -3::2].mean(axis=1)
    # =========================================================================
    # Adjustment of Nominalized Census P119 to Retrieved Results
    # =========================================================================
    df.iloc[:, -8] = df.iloc[:, -8].mul(
        df.loc[1925, df.columns[-1]]
    ).div(df.loc[1925, df.columns[-8]])
    # =========================================================================
    # Blending Previous Series with 'nominal_extended'
    # =========================================================================
    df.iloc[:, -1] = df.iloc[:, [-8, -1]].mean(axis=1)
    return df.iloc[:, [-1]].dropna(axis=0)


def transform_d(df: DataFrame) -> tuple[DataFrame, np.int64]:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Gross Domestic Investment Price Index
        df.iloc[:, 2]      Fixed Investment
        df.iloc[:, 3]      Fixed Investment Price Index
        df.iloc[:, 4]      Real Gross Domestic Product
        ================== =================================.

    Returns
    -------
    df : TYPE
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Gross Domestic Investment Price Index
        df.iloc[:, 2]      Fixed Investment
        df.iloc[:, 3]      Fixed Investment Price Index
        df.iloc[:, 4]      Real Gross Domestic Product
        df.iloc[:, 5]      Real Investment
        df.iloc[:, 6]      Real Fixed Investment
        ================== =================================.
    year_base : TYPE
        DESCRIPTION.

    """
    # =========================================================================
    # Basic Year
    # =========================================================================
    df['__deflator'] = df.iloc[:, 1].sub(100).abs()
    year_base = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Convert to Billions
    # =========================================================================
    df.iloc[:, -1] = df.iloc[:, -1].div(1000)
    # =========================================================================
    # Real Investment, Billions
    # =========================================================================
    df['investment'] = df.iloc[:, 1].mul(
        df.iloc[year_base, 0]).div(1000).div(100)
    # =========================================================================
    # Real Fixed Investment, Billions
    # =========================================================================
    df['investment_f'] = df.iloc[:, 3].mul(
        df.iloc[year_base, 2]).div(1000).div(100)
    return df, year_base


def transform_e(df: DataFrame) -> tuple[DataFrame]:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Investment
        df.iloc[:, 1]      Nominal Gross Domestic Product
        df.iloc[:, 2]      Real Gross Domestic Product
        df.iloc[:, 3]      Capital
        ================== =================================.

    Returns
    -------
    tuple[DataFrame]
        DESCRIPTION.

    """
    # =========================================================================
    # "Real" Investment
    # =========================================================================
    df['investment'] = df.iloc[:, 0].mul(df.iloc[:, 2]).div(df.iloc[:, 1])
    # =========================================================================
    # "Real" Capital
    # =========================================================================
    df['capital'] = df.iloc[:, 3].mul(df.iloc[:, 2]).div(df.iloc[:, 1])
    return (
        # =====================================================================
        # DataFrame Nominal
        # =====================================================================
        df.copy().iloc[:, [0, 1, 3]].pipe(transform_e_post),
        # =====================================================================
        # DataFrame "Real"
        # =====================================================================
        df.copy().iloc[:, [-2, 2, -1]].pipe(transform_e_post),
    )


def transform_e_post(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Investment
        df.iloc[:, 1]      Production
        df.iloc[:, 2]      Capital
        ================== =================================.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    # =========================================================================
    # Investment to Production Ratio
    # =========================================================================
    df['inv_to_pro'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 1].div(df.iloc[:, 2])
    _params_i = np.polyfit(
        df.iloc[:, 0].astype(float),
        df.iloc[:, 1].astype(float),
        deg=1
    )
    _params_t = np.polyfit(
        df.iloc[:, 1].astype(float),
        df.iloc[:, 2].astype(float),
        deg=1
    )
    df['inv_to_pro_lin'] = np.poly1d(_params_i)(df.iloc[:, 0])
    df['c_turnover_lin'] = np.poly1d(_params_t)(df.iloc[:, 2])
    print('Investment to Production: Linear Approximation')
    print(df.iloc[:, 3].describe())
    print('{:,.6f}+{:,.6f} X'.format(*_params_i[::-1]))
    print('Fixed Assets Turnover: Linear Approximation')
    print(df.iloc[:, 4].describe())
    print('{:,.6f}+{:,.6f} X'.format(*_params_t[::-1]))
    print(df.info())
    return df


def transform_mean(df: DataFrame, name: str) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    name : str
        New Column Name.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Sum of <series_ids>
        ================== =================================
    """
    df[name] = df.mean(axis=1)
    return df.iloc[:, [-1]]


def transform_usa_frb_fa(df: DataFrame) -> DataFrame:
    """
    Retrieves DataFrame for Manufacturing Fixed Assets Series, Billion USD

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================
    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal
        df.iloc[:, 1]      Real
        ================== =================================
    """
    df['frb_nominal'] = ((df.iloc[:, 1].mul(df.iloc[:, 2]).div(df.iloc[:, 0])).add(
        df.iloc[:, 4].mul(df.iloc[:, 5]).div(df.iloc[:, 3]))).div(1000)
    df['frb_real'] = df.iloc[:, [2, 5]].sum(axis=1).div(1000)
    return df.iloc[:, -2:]


def transform_usa_frb_fa_def(df: DataFrame) -> DataFrame:
    """
    Retrieves DataFrame for Deflator for Manufacturing Fixed Assets Series

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator
        ================== =================================

    """
    df['fa_def_frb'] = (df.iloc[:, [1, 4]].sum(axis=1)).div(
        df.iloc[:, [0, 3]].sum(axis=1))
    return df.iloc[:, [-1]]


def transform_pct_change(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    df[f'{df.columns[0]}_prc'] = df.iloc[:, 0].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)


def transform_deflator(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal
        df.iloc[:, 1]      Real
        ================== =================================

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator PRC
        ================== =================================
    """
    assert df.shape[1] == 2
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['prc'] = df.iloc[:, -1].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)


def transform_rebase(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    assert df.shape[1] == 1
    return df.div(df.iloc[0, :]).mul(100)


def transform_usa_manufacturing(df: DataFrame) -> DataFrame:
    return df.div(df.iloc[0, :])


def transform_approx_linear(df: DataFrame) -> tuple[DataFrame, int, np.ndarray]:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Real Values for Price Deflator
        df.iloc[:, 1]      Nominal Values for Price Deflator
        df.iloc[:, 2]      Regressor
        df.iloc[:, 3]      Regressand
        ================== =================================.

    Returns
    -------
    df : TYPE
        DESCRIPTION.
    year_base : TYPE
        DESCRIPTION.
    polyfit_linear : TYPE
        DESCRIPTION.

    """
    # =========================================================================
    # Basic Year
    # =========================================================================
    year_base = df.pipe(get_price_base_nr)
    df.drop(df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Deflator
    # =========================================================================
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df[f'{df.columns[2]}_bas'] = df.iloc[:, 2].mul(df.iloc[:, 4]).div(
        df.iloc[0, 2]).div(df.iloc[0, 4])
    df[f'{df.columns[3]}_bas'] = df.iloc[:, 3].mul(df.iloc[:, 4]).div(
        df.iloc[0, 3]).div(df.iloc[0, 4])
    polyfit_linear = np.polyfit(
        df.iloc[:, -2].astype(float),
        df.iloc[:, -1].astype(float),
        deg=1
    )
    # =========================================================================
    # Yhat
    # =========================================================================
    df[f'{df.columns[3]}_estimate'] = np.poly1d(polyfit_linear)(df.iloc[:, -2])
    # =========================================================================
    # Delivery Block
    # =========================================================================
    print('Period From: {} Through: {}'.format(*df.index[[0, -1]]))
    print(f'Prices: {year_base}=100')
    print('Model: Yhat = {:.4f} + {:.4f}*X'.format(*polyfit_linear[::-1]))
    for _, param in enumerate(polyfit_linear[::-1]):
        print(f'Model Parameter: A_{_} = {param:,.4f}')
    return df, year_base, polyfit_linear


def transform_approx_linear_log(df: DataFrame) -> tuple[DataFrame, int, np.ndarray]:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Real Values for Price Deflator
        df.iloc[:, 1]      Nominal Values for Price Deflator
        df.iloc[:, 2]      Regressor
        df.iloc[:, 3]      Regressand
        ================== =================================.

    Returns
    -------
    df : TYPE
        DESCRIPTION.
    year_base : TYPE
        DESCRIPTION.
    polyfit_linear : TYPE
        DESCRIPTION.

    """
    # =========================================================================
    # Basic Year
    # =========================================================================
    year_base = df.pipe(get_price_base_nr)
    df.drop(df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Deflator
    # =========================================================================
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df[f'{df.columns[2]}_log_bas'] = np.log(df.iloc[:, 2].div(df.iloc[0, 2]))
    df[f'{df.columns[3]}_log_bas'] = np.log(df.iloc[:, 3].mul(df.iloc[:, 4]).div(
        df.iloc[0, 3]).div(df.iloc[0, 4]))
    polyfit_linear = np.polyfit(
        df.iloc[:, -2].astype(float),
        df.iloc[:, -1].astype(float),
        deg=1
    )
    # =========================================================================
    # Yhat
    # =========================================================================
    df[f'{df.columns[3]}_estimate'] = np.poly1d(polyfit_linear)(df.iloc[:, -2])
    # =========================================================================
    # Delivery Block
    # =========================================================================
    print('Period From: {} Through: {}'.format(*df.index[[0, -1]]))
    print(f'Prices: {year_base}=100')
    print('Model: Yhat = {:.4f} + {:.4f}*Ln(X)'.format(*polyfit_linear[::-1]))
    for _, param in enumerate(polyfit_linear[::-1]):
        print(f'Model Parameter: A_{_} = {param:,.4f}')
    return df, year_base, polyfit_linear


def transform_elasticity(df: DataFrame) -> tuple[DataFrame, tuple[str]]:
    """


    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    tuple[DataFrame, tuple[str]]
        DESCRIPTION.

    """
    # =========================================================================
    # Basic Year
    # =========================================================================
    year_base = df.pipe(get_price_base_nr)
    df.drop(df.columns[-1], axis=1, inplace=True)
    plot_title = (
        'National Income' if df.columns[2] == 'A032RC' else 'Series',
        df.columns[2],
        year_base,
    )
    df[f'{df.columns[2]}_real'] = df.iloc[:, 0].mul(
        df.iloc[:, 2]).div(df.iloc[:, 1])
    df[f'{df.columns[2]}_centered'] = df.iloc[:, 3].rolling(2).mean()
    # =========================================================================
    # \dfrac{x_{k} - x_{k-1}}{\dfrac{x_{k} + x_{k-1}}{2}}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_a'] = df.iloc[:,
                                                  3].diff().div(df.iloc[:, -1])
    # =========================================================================
    # \frac{x_{k+1} - x_{k-1}}{2 x_{k}}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_b'] = df.iloc[:, 3].diff(
        2).shift(-1).div(df.iloc[:, 3]).div(2)
    # =========================================================================
    # 2 \times \frac{x_{k+1} - x_{k-1}}{x_{k-1} + 2 x_{k} + x_{k+1}}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_c'] = df.iloc[:, 3].diff(2).shift(-1).div(
        df.iloc[:, 3].mul(2).add(df.iloc[:, 3].shift(-1)).add(df.iloc[:, 3].shift(1))).mul(2)
    # =========================================================================
    # \frac{-x_{k-1} - x_{k} + x_{k+1} + x_{k+2}}{2 \times (x_{k} + x_{k+1})}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_d'] = df.iloc[:, 3].shift(-1).add(df.iloc[:, 3].shift(-2)).sub(
        df.iloc[:, 3].shift(1)).sub(df.iloc[:, 3]).div(df.iloc[:, 3].add(df.iloc[:, 3].shift(-1)).mul(2))
    return df, plot_title


def transform_model_capital(df: DataFrame) -> tuple[DataFrame, np.ndarray]:
    params_i = np.polyfit(
        df.index.to_series().astype(int),
        df.iloc[:, 0].div(df.iloc[:, 1]).astype(float),
        deg=1
    )
    params_t = np.polyfit(
        df.index.to_series().astype(int),
        df.iloc[:, 1].div(df.iloc[:, 2]).astype(float),
        deg=1
    )
    # =========================================================================
    # Gross Fixed Investment to Gross Domestic Product Ratio
    # =========================================================================
    df['inv_to_pro'] = np.poly1d(params_i)(df.index.to_series())
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df['c_turnover'] = np.poly1d(params_t)(df.index.to_series())
    df['cap_a'] = df.pipe(calculate_capital, params_i, params_t, 0.875)
    df['cap_b'] = df.pipe(calculate_capital, params_i, params_t, 1)
    df['cap_c'] = df.pipe(calculate_capital, params_i, params_t, 1.125)
    return df, params_i, params_t


def transform_fourier_discrete(df: DataFrame, precision: int):
    _p = np.polyfit(
        df.index.to_series().astype(int),
        df.iloc[:, 0].astype(float),
        deg=1
    )
    df['period_calibrated'] = df.index.to_series().sub(
        df.index[0]).div(df.shape[0]).mul(2).mul(np.pi).astype(float)
    df[f'{df.columns[0]}_line'] = np.poly1d(_p)(df.index.to_series())
    df[f'{df.columns[0]}_wave'] = df.iloc[:, 0].sub(df.iloc[:, 2])
    # =========================================================================
    # DataFrame for Fourier Coefficients
    # =========================================================================
    df_fourier = DataFrame(columns=['cos', 'sin'])
    for _ in range(1, precision):
        df_fourier.loc[_] = [
            df.iloc[:, 3].mul(np.cos(df.iloc[:, 1].mul(_))).mul(2).mean(),
            df.iloc[:, 3].mul(np.sin(df.iloc[:, 1].mul(_))).mul(2).mean()
        ]
    # =========================================================================
    # First Entry Correction
    # =========================================================================
    df_fourier.loc[0, 'cos'] /= 2
    return df, df_fourier
