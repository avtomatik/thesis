#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 17:42:38 2022

@author: Alexander Mikhailov
"""

import numpy as np
import pandas as pd
from pandas import DataFrame

from thesis.src.lib.collect import stockpile_usa_hist
from thesis.src.lib.pull import pull_by_series_id
from thesis.src.lib.read import (read_temporary, read_usa_frb_g17,
                                 read_usa_frb_h6, read_usa_frb_us3)


def transform_investment_manufacturing(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      National Income
        df.iloc[:, 2]      Nominal Gross Domestic Product
        df.iloc[:, 3]      Real Gross Domestic Product
        ================== =================================
    """
    df = df.iloc[:, [0, 4, 6, 7]].dropna(axis=0)
    df.iloc[:, 1] = df.iloc[:, 1].apply(pd.to_numeric, errors='coerce')
    return df.div(df.iloc[0, :]).dropna(axis=0)


def transform_investment(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Nominal Gross Domestic Product
        df.iloc[:, 2]      Real Gross Domestic Product
        df.iloc[:, 3]      Prime Rate
        ================== =================================
    """
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
    # Douglas P.H. -- Kendrick J.W. (Blended) Series
    # =========================================================================
    df['nominal_doug_kndrck'] = df.iloc[:, -2:].mean(axis=1)
    # =========================================================================
    # Cobb C.W., Douglas P.H. -- FRB (Blended) Series
    # =========================================================================
    df['nominal_cbb_dg_frb'] = df.iloc[:, (8, -5)].mean(axis=1)
    # =========================================================================
    # Capital Structure Series: "Cobb C.W., Douglas P.H. -- FRB (Blended) Series" to "Douglas P.H. -- Kendrick J.W. (Blended) Series"
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
    # Patch Series "Douglas P.H. -- Kendrick J.W. (Blended) Series" Multiplied by "Capital Structure Series"
    # =========================================================================
    df['nominal_patch'] = df.iloc[:, -3].mul(df.iloc[:, -1])
    # =========================================================================
    # "Cobb C.W., Douglas P.H. -- FRB (Blended) Series" Patched with "Patch Series"
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
    df.iloc[:, -1] = df.iloc[:, (-8, -1)].mean(axis=1)
    return df.iloc[:, [-1]].dropna(axis=0)


def transform_d(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Gross Domestic Investment Price Index
        df.iloc[:, 2]      Fixed Investment
        df.iloc[:, 3]      Fixed Investment Price Index
        df.iloc[:, 4]      Real Gross Domestic Product
        ================== =================================
    """
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return df.iloc[:, (0, 1, 2, 3, 7)].dropna(axis=0)


def transform_e(df: DataFrame) -> tuple[DataFrame]:
    assert df.shape[1] == 21, "Works on DataFrame Produced with combine_usa_general()"
    # =========================================================================
    # "Real" Investment
    # =========================================================================
    df['investment'] = df.iloc[:, 0].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    # =========================================================================
    # "Real" Capital
    # =========================================================================
    df['capital'] = df.iloc[:, 11].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    return (
        # =====================================================================
        # DataFrame Nominal
        # =====================================================================
        df.iloc[:, (0, 6, 11)].dropna(axis=0),
        # =====================================================================
        # DataFrame "Real"
        # =====================================================================
        df.iloc[:, (-2, 7, -1)].dropna(axis=0),
    )


def combine_kurenkov(df: DataFrame) -> tuple[DataFrame]:
    """Returns Four DataFrames with Comparison of df: DataFrame and Kurenkov Yu.V. Data"""
    SERIES_ID = 'CAPUTL.B50001.A'
    FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'
    df_control = read_temporary(FILE_NAME)
    # =========================================================================
    # Manufacturing
    # =========================================================================
    df_a = pd.concat(
        [
            df_control.iloc[:, [0]],
            df.loc[:, ('A191RX',)],
            read_usa_frb_us3().loc[:, ('AIPMA_SA_IX',)],
        ],
        axis=1,
        sort=True
    ).dropna(how='all')
    df_a = df_a.div(df_a.loc[1950, :]).mul(100)
    # =========================================================================
    # Labor
    # =========================================================================
    df_b = pd.concat(
        [
            df_control.iloc[:, [1]],
            df.loc[:, ('bea_labor_mfg',)],
        ],
        axis=1,
        sort=True
    ).dropna(how='all')
    # =========================================================================
    # Capital
    # =========================================================================
    df_c = pd.concat(
        [
            df_control.iloc[:, [2]],
            df.loc[:, ('K10070',)],
        ],
        axis=1,
        sort=True
    ).dropna(how='all')
    df_c = df_c.div(df_c.loc[1951, :]).mul(100)
    # =========================================================================
    # Capacity Utilization
    # =========================================================================
    df_d = pd.concat(
        [
            df_control.iloc[:, [3]],
            read_usa_frb_g17().loc[:, (SERIES_ID,)].dropna(axis=0),
        ],
        axis=1,
        sort=True
    )
    return df_a, df_b, df_c, df_d


def transform_manufacturing_money(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Nominal Gross Domestic Product
        df.iloc[:, 2]      Real Gross Domestic Product
        df.iloc[:, 3]      M1
        ================== =================================
    """
    SERIES_ID = {'X0414': 'dataset_uscb.zip'}
    df_manufacturing = df.iloc[:, (0, 6, 7)].dropna(axis=0)
    df_manufacturing = df_manufacturing.div(df_manufacturing.iloc[0, :])
    df_money = pd.concat(
        [
            read_usa_frb_h6(),
            stockpile_usa_hist(SERIES_ID)
        ],
        axis=1
    ).pipe(transform_mean, name="m1_fused").sort_index()
    df = pd.concat(
        [
            df_manufacturing,
            df_money.div(df_money.iloc[0, :])
        ],
        axis=1
    ).dropna(axis=0)
    return df.div(df.iloc[0, :])


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


def transform_sum(df: DataFrame, name: str) -> DataFrame:
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
    df['frb_real'] = df.iloc[:, (2, 5)].sum(axis=1).div(1000)
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
    df['fa_def_frb'] = (df.iloc[:, (1, 4)].sum(axis=1)).div(
        df.iloc[:, (0, 3)].sum(axis=1))
    return df.iloc[:, [-1]]


def transform_agg(df: DataFrame, agg: str) -> DataFrame:
    if agg == 'mean':
        return df.groupby(df.columns[0]).mean()
    return df.groupby(df.columns[0]).sum()


def transform_agg_sum(df: DataFrame) -> DataFrame:
    return df.groupby(df.index.year).sum()


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
