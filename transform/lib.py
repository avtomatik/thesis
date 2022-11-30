#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 17:42:38 2022

@author: Alexander Mikhailov
"""

import numpy as np
import pandas as pd
from collect.lib import collect_usa_hist
from pandas import DataFrame
from pull.lib import pull_by_series_id
from read.lib import (read_temporary, read_usa_frb_g17, read_usa_frb_h6,
                      read_usa_frb_us3)
from sklearn.linear_model import Lasso, LassoCV, LinearRegression, Ridge
from transform.lib import numerify


def transform_a(df: DataFrame) -> DataFrame:
    df = df.iloc[:, [0, 4, 6, 7]].dropna(axis=0)
    df.iloc[:, 1] = df.iloc[:, 1].apply(pd.to_numeric, errors='coerce')
    return df.div(df.iloc[0, :]).dropna(axis=0)


def transform_b(df: DataFrame) -> DataFrame:
    return df.iloc[:, [0, 6, 7, 20]].dropna(axis=0)


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
    #     print(f"R**2: {r2_score(df.iloc[:, 2], df.iloc[:, 3]):,.4f}")
    #     print(df.iloc[:, 3].div(df.iloc[:, 2]).sub(1).abs().mean())
    # =========================================================================
    return df, (k, np.exp(b))


def transform_cobb_douglas_alt(df: DataFrame) -> tuple[DataFrame, tuple[float]]:
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Labor
        df.iloc[:, 2]      Product
        df.iloc[:, 3]      Product Alternative
        ================== =================================
    """
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
    df['_prod_roll'] = df.iloc[:, 3].rolling(window=3, center=True).mean()
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
                                    1].rolling(window=3, center=True).mean()
    df['_prod_comp_roll_sub'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    return df, (k, np.exp(b)), (_k, np.exp(_b))


def transform_cobb_douglas_extension_capital(df: DataFrame) -> DataFrame:
    """


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
    df['nominal_census'] = df.iloc[:, 3].mul(df.iloc[:, 5]).div(df.iloc[:, 4])
    df['nominal_dougls'] = df.iloc[:, 0].mul(
        df.iloc[:, 7]).div(df.iloc[:, 1]).div(1000)
    df['nominal_kndrck'] = df.iloc[:, 3].mul(
        df.iloc[:, 6]).div(df.iloc[:, 4]).div(1000)
    df.iloc[:, -1] = df.iloc[:, -1].mul(
        df.loc[1929, df.columns[4]]).div(df.loc[1929, df.columns[3]])
    # =========================================================================
    # Douglas P.H. -- Kendrick J.W. (Blended) Series
    # =========================================================================
    df['nominal_doug_kndrck'] = df.iloc[:, -2:].mean(axis=1)
    # =========================================================================
    # Cobb C.W., Douglas P.H. -- FRB (Blended) Series
    # =========================================================================
    df['nominal_cbb_dg_frb'] = df.iloc[:, [8, -5]].mean(axis=1)
    # =========================================================================
    # Capital Structure Series: `Cobb C.W., Douglas P.H. -- FRB (Blended) Series` to `Douglas P.H. -- Kendrick J.W. (Blended) Series`
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
    # Patch Series `Douglas P.H. -- Kendrick J.W. (Blended) Series` Multiplied by `Capital Structure Series`
    # =========================================================================
    df['nominal_patch'] = df.iloc[:, -3].mul(df.iloc[:, -1])
    # =========================================================================
    # `Cobb C.W., Douglas P.H. -- FRB (Blended) Series` Patched with `Patch Series`
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


def transform_cobb_douglas_sklearn(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Labor
        df.iloc[:, 2]      Product
        ================== =================================

    Returns
    -------
    None.

    """
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])

    # =========================================================================
    # Original: k=.25, b=1.01
    # =========================================================================
    X = np.column_stack((np.zeros(df.shape[0]), np.log(df.iloc[:, -2])))
    y = np.log(df.iloc[:, -1].to_numpy())
    return X, y
# =============================================================================
#     # =========================================================================
#     # Lasso
#     # =========================================================================
#     las = Lasso(alpha=.01).fit(X, y)
#     k, b = las.coef_[1], las.intercept_
#     # print('Lasso: k = {:.12f}, b = {:.12f}'.format(k, b))
#
#     las = LassoCV(cv=4, random_state=0).fit(X, y)
#     k, b = las.coef_[1], las.intercept_
#     # print('LassoCV: k = {:.12f}, b = {:.12f}'.format(k, b))
#     # =========================================================================
#     #     print(reg.score(X, y))
#     #     print(reg)
#     #     print(reg.predict(X[:1, ]))
#     # =========================================================================
# =============================================================================

    reg = LinearRegression().fit(X, y)
    k, b = reg.coef_[1], reg.intercept_
    # print('Linear Regression: k = {:.12f}, b = {:.12f}'.format(k, b))
    # =========================================================================
    #     reg.score(X, y)
    #     reg.coef_
    #     reg.intercept_
    # =========================================================================

    # =========================================================================
    # tik = Ridge(alpha=.01).fit(X, y)
    # k, b = tik.coef_[1], tik.intercept_
    # print('Ridge Regression: k = {:.12f}, b = {:.12f}'.format(k, b))
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
    return df, (k, np.exp(b))


def transform_d(df: DataFrame) -> DataFrame:
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return df.iloc[:, [0, 1, 2, 3, 7]].dropna(axis=0)


def transform_e(df: DataFrame) -> tuple[DataFrame]:
    assert df.shape[1] == 21, 'Works on DataFrame Produced with "collect_usa_general()"'
    # =========================================================================
    # "Real" Investment
    # =========================================================================
    df['investment'] = df.iloc[:, 0].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    # =========================================================================
    # `Real` Capital
    # =========================================================================
    df['capital'] = df.iloc[:, 11].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    return (
        # =====================================================================
        # DataFrame Nominal
        # =====================================================================
        df.iloc[:, [0, 6, 11]].dropna(axis=0),
        # =====================================================================
        # DataFrame `Real`
        # =====================================================================
        df.iloc[:, [-2, 7, -1]].dropna(axis=0),
    )


def combine_kurenkov(data_testing: DataFrame) -> tuple[DataFrame]:
    """Returns Four DataFrames with Comparison of data_testing: DataFrame and Kurenkov Yu.V. Data"""
    SERIES_ID = 'CAPUTL.B50001.A'
    data_control = read_temporary('dataset_usa_reference_ru_kurenkov_yu_v.csv')
    # =========================================================================
    # Production
    # =========================================================================
    data_a = pd.concat(
        [
            data_control.iloc[:, [0]],
            data_testing.loc[:, ('A191RX',)],
            read_usa_frb_us3().loc[:, ('AIPMA_SA_IX',)],
        ],
        axis=1,
        sort=True
    ).dropna(how='all')
    data_a = data_a.div(data_a.loc[1950, :]).mul(100)
    # =========================================================================
    # Labor
    # =========================================================================
    data_b = pd.concat(
        [
            data_control.iloc[:, [1]],
            data_testing.loc[:, ('bea_labor_mfg',)],
        ],
        axis=1,
        sort=True
    ).dropna(how='all')
    # =========================================================================
    # Capital
    # =========================================================================
    data_c = pd.concat(
        [
            data_control.iloc[:, [2]],
            data_testing.loc[:, ('K10002',)],
        ],
        axis=1,
        sort=True
    ).dropna(how='all')
    data_c = data_c.div(data_c.loc[1951, :]).mul(100)
    # =========================================================================
    # Capacity Utilization
    # =========================================================================
    data_d = pd.concat(
        [
            data_control.iloc[:, [3]],
            read_usa_frb_g17().loc[:, (SERIES_ID,)].dropna(axis=0),
        ],
        axis=1,
        sort=True
    )
    return data_a, data_b, data_c, data_d


def transform_manufacturing_money(df: DataFrame) -> DataFrame:
    SERIES_ID = {'X0414': 'dataset_uscb.zip'}
    df_manufacturing = df.iloc[:, [0, 6, 7]].dropna(axis=0)
    df_manufacturing = df_manufacturing.div(df_manufacturing.iloc[0, :])
    df_money = pd.concat(
        [
            read_usa_frb_h6(),
            collect_usa_hist(SERIES_ID)
        ],
        axis=1
    ).pipe(transform_mean_wide, name="m1_fused").sort_index()
    df = pd.concat(
        [
            df_manufacturing,
            df_money.div(df_money.iloc[0, :])
        ],
        axis=1
    ).dropna(axis=0)
    return df.div(df.iloc[0, :])


def transform_mean_wide(df: DataFrame, name: str) -> DataFrame:
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


def stockpile_by_series_ids(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
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
    series_ids = sorted(set(df.iloc[:, 0]))
    return pd.concat(
        [
            df.pipe(pull_by_series_id, series_id)
            for series_id in series_ids
        ],
        axis=1
    ).apply(pd.to_numeric, errors='coerce')


def transform_sum_wide(df: DataFrame, name: str) -> DataFrame:
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
    df[name] = df.sum(axis=1)
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
