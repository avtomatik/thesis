#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 08:59:10 2022

@author: Alexander Mikhailov
"""


import itertools
from functools import partial
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.plotting import autocorrelation_plot, lag_plot
from scipy import stats
from sklearn.metrics import r2_score

from thesis.src.common import get_fig_map
from thesis.src.lib.combine import combine_data_frames_by_columns
from thesis.src.lib.pull import (pull_by_series_id,
                                 pull_series_ids_description,
                                 pull_uscb_description)
from thesis.src.lib.read import read_usa_hist, read_usa_nber, read_worldbank
from thesis.src.lib.stockpile import stockpile_usa_hist
from thesis.src.lib.tools import (calculate_capital, cap_productivity,
                                  filter_kol_zur, filter_rolling_mean,
                                  get_price_base_nr, lab_productivity,
                                  simple_linear_regression)
from thesis.src.lib.transform import (transform_agg, transform_cobb_douglas,
                                      transform_rebase)


def plot_investment_manufacturing(df: DataFrame) -> None:
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      National Income
        df.iloc[:, 2]      Nominal Gross Domestic Product
        df.iloc[:, 3]      Real Gross Domestic Product
        ================== =================================
    """
    plt.figure()
    plt.title(
        'Gross Private Domestic Investment & National Income, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    new_var = [
        'Gross Private Domestic Investment',
        'National Income',
    ]

    plt.plot(
        df.iloc[:, -4:-2], label=new_var
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    df.index = df.index.to_series().rolling(2).mean()
    plt.plot(
        df.iloc[:, -2], '--',
        df.iloc[:, -1], '--'
    )
    plt.grid()
    plt.legend()
    plt.show()


def plot_investment(df: DataFrame) -> None:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Nominal Gross Domestic Product
        df.iloc[:, 2]      Real Gross Domestic Product
        df.iloc[:, 3]      Prime Rate
        df.iloc[:, 4]      Investment
        ================== =================================.

    Returns
    -------
    None
        DESCRIPTION.

    """
    plt.figure()
    plt.plot(df.iloc[:, 3], df.iloc[:, -1])
    plt.title(
        'Gross Private Domestic Investment, A006RC, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Percentage')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.show()


def plot_manufacturing_money(df: DataFrame) -> None:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Investment
        df.iloc[:, 1]      Nominal Gross Domestic Product
        df.iloc[:, 2]      Real Gross Domestic Product
        df.iloc[:, 3]      M1
        df.iloc[:, 4]      Investment
        ================== =================================.

    Returns
    -------
    None
        DESCRIPTION.

    """
    plt.figure()
    new_var = [
        'Real Gross Domestic Product',
        'Money Supply',
        'Real Gross Domestic Investment',
    ]

    plt.plot(
        df.iloc[:, range(2, 5)], label=new_var
    )
    plt.title('Indexes, {}$-${}'.format(*df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plot_d(df: DataFrame, year_base: np.int64) -> None:
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
        df.iloc[:, 5]      Real Investment
        df.iloc[:, 6]      Real Fixed Investment
        ================== =================================.
    year_base : np.int64
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    plt.figure(1)
    plt.semilogy(
        df.iloc[:, -2],
        label='Real Gross Private Domestic Investment $GPDI$'
    )
    plt.semilogy(
        df.iloc[:, -1],
        color='red',
        label='Real Gross Private Fixed Investment, Nonresidential $GPFI(n)$'
    )
    plt.title('Real Indexes, {}=100, {}$-${}'.format(*
              df.index[[year_base, 0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.grid()
    plt.legend()

    plt.figure(2)
    plt.plot(df.iloc[:, 4])
    plt.title(
        'Real Gross Domestic Product $GDP$, {}=100, {}$-${}'.format(*df.index[[year_base, 0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.grid()

    plt.figure(3)
    plt.plot(df.iloc[:, -2], df.iloc[:, 4])
    plt.title(
        '$GPDI$ & $GPFI(n)$, {}=100, {}$-${}'.format(*df.index[[year_base, 0, -1]]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid()

    plt.figure(4)
    plt.plot(df.iloc[:, -1], df.iloc[:, 4])
    plt.title(
        '$GPFI(n)$ & $GDP$, {}=100, {}$-${}'.format(*df.index[[year_base, 0, -1]]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid()
    plt.show()


def plot_e(df: DataFrame) -> None:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Investment
        df.iloc[:, 1]      Production
        df.iloc[:, 2]      Capital
        df.iloc[:, 3]      Investment to Production
        df.iloc[:, 4]      Fixed Assets Turnover
        df.iloc[:, 5]      Investment to Production: Linear Approximation
        df.iloc[:, 6]      Fixed Assets Turnover: Linear Approximation
        ================== =================================.

    Returns
    -------
    None
        DESCRIPTION.

    """
    plt.figure()
    plt.semilogy(df.iloc[:, 0], df.iloc[:, 1])
    plt.semilogy(df.iloc[:, 0], df.iloc[:, 5])
    plt.title(
        'Investment to Production Ratio, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Investment, Billions of Dollars')
    plt.ylabel('Gross Domestic Product, Billions of Dollars')
    new_var = [
        '$P(I)$',
        'Investment to Production'
    ]

    plt.legend(new_var)
    plt.grid()
    plt.show()


def plot_uscb_manufacturing(df: DataFrame, year_base: int) -> None:
    plt.figure()
    new_var = [
        'Fabricant S., Shiskin J., NBER',
        'E. Frickey',
    ]

    plt.plot(
        df.iloc[:, [0, 2]], label=new_var
    )
    plt.plot(df.iloc[:, 1], color='red', linewidth=4, label='W.M. Persons')
    plt.axvline(x=year_base, linestyle=':')
    plt.title(
        'US Manufacturing Indexes Of Physical Production Of Manufacturing, {}=100, {}$-${}'.format(
            year_base, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plot_uscb_cap(df: DataFrame) -> None:
    """Census Manufacturing Fixed Assets Series"""
    plt.figure()
    new_var = ['Total', 'Structures', 'Equipment']
    plt.semilogy(df, label=new_var)
    plt.title(
        'Census Manufacturing Fixed Assets, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.show()


def plot_uscb_cap_deflator(df: DataFrame) -> None:
    """Census Manufacturing Fixed Assets Deflator Series"""
    plt.figure()
    plt.plot(df)
    plt.title(
        'Census Fused Fixed Assets Deflator, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.show()


def plot_uscb_metals(df: DataFrame, years_base: tuple[int]) -> None:
    _DESCS_RAW = (
        'P262 - Rails Produced, {}=100',
        'P265 - Raw Steel Produced - Total, {}=100',
        'P266 - Raw Steel Produced - Bessemer, {}=100',
        'P267 - Raw Steel Produced - Open Hearth, {}=100',
        'P268 - Raw Steel Produced - Crucible, {}=100',
        'P269 - Raw Steel Produced - Electric and All Other, {}=100',
        'P293 - Locomotives Produced, {}=100',
        'P294 - Railroad Passenger Cars Produced, {}=100',
        'P295 - Railroad Freight Cars Produced, {}=100',
    )
    _DESCS = map(lambda _: _[0].format(_[1]), zip(_DESCS_RAW, years_base))
    _MAPPING = dict(zip(df.columns, _DESCS))
    _COLUMN_LOCS = filter(lambda _: _ not in range(1, 6), range(df.shape[1]))
    plt.figure(1)
    plt.semilogy(
        df.iloc[:, range(1, 6)],
        label=[_MAPPING[_] for _ in df.columns[range(1, 6)]]
    )
    for _ in range(1, 6):
        plt.axvline(x=years_base[_], linestyle=':')
    plt.title('Steel Manufacturing')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.semilogy(
        df.iloc[:, _COLUMN_LOCS],
        label=[_MAPPING[_] for _ in df.columns[_COLUMN_LOCS]]
    )
    for _ in _COLUMN_LOCS:
        plt.axvline(x=years_base[_], linestyle=':')
    plt.title('Rails & Cars Manufacturing')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plot_uscb_commodities(series_ids: dict[str, str]) -> None:
    df = pd.concat(
        map(
            lambda _: read_usa_hist(_[1]).pipe(
                pull_by_series_id, _[0]
            ).sort_index().pipe(transform_rebase),
            series_ids.items()
        ),
        axis=1,
        sort=True
    )
    for series_id in series_ids:
        print(f'<{series_id}> {pull_uscb_description(series_id)}')
    _title = 'Series P 231$-$300. Physical Output of Selected Manufactured Commodities: {}$-${}'.format(
        *df.index[[0, -1]]
    )
    plt.figure()
    plt.semilogy(df)
    plt.title(_title)
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.legend(series_ids)
    plt.grid()
    plt.show()


def plot_uscb_immigration(df: DataFrame) -> None:
    plt.figure()
    plt.plot(df)
    plt.title('Total Immigration, {}$-${}'.format(*df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('People')
    plt.grid()
    plt.show()


def plot_uscb_unemployment_hours_worked(df: DataFrame) -> None:
    plt.figure(1)
    plt.plot(df.iloc[:, 1])
    plt.title('Unemployment, Percent of Civilian Labor Force')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.figure(2)
    plt.plot(df.iloc[:, (2, 3)], label=['Bureau of Labour', 'Wolman'])
    plt.title('All Manufacturing, Average Full-Time Weekly Hours, 1890-1899=100')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.plot(df.iloc[:, 4])
    plt.title('Implicit Number of Workers')
    plt.xlabel('Period')
    plt.ylabel('Persons')
    plt.grid()
    plt.show()


def plot_uscb_employment_conflicts(df: DataFrame) -> None:
    fig, axes_stoppages = plt.subplots()
    color = 'tab:red'
    axes_stoppages.set_xlabel('Period')
    axes_stoppages.set_ylabel('Number', color=color)
    axes_stoppages.plot(df.iloc[:, 0], color=color, label='Stoppages')
    axes_stoppages.set_title('Work Conflicts')
    axes_stoppages.grid()
    axes_stoppages.legend(loc=2)
    axes_stoppages.tick_params(axis='y', labelcolor=color)
    axes_workers = axes_stoppages.twinx()
    color = 'tab:blue'
    axes_workers.set_ylabel('1,000 People', color=color)
    axes_workers.plot(df.iloc[:, 1], color=color, label='Workers Involved')
    axes_workers.legend(loc=1)
    axes_workers.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()
    plt.show()


def plot_uscb_gnp(df: DataFrame) -> None:
    plt.figure()
    new_var = [
        'Gross National Product',
        'Gross National Product Per Capita',
    ]

    plt.plot(df, label=new_var)
    plt.title(
        'Gross National Product, Prices {}=100, {}=100'.format(
            1958, df.index[0]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plot_uscb_farm_lands(df: DataFrame) -> None:
    plt.figure()
    df.plot()
    plt.title('Land in Farms')
    plt.xlabel('Period')
    plt.ylabel('1,000 acres')
    plt.grid()
    plt.show()


def plot_uscb_trade(df: DataFrame) -> None:
    plt.figure()
    new_var = [
        'Exports, U1',
        'Imports, U8',
        'Net Exports, U15',
    ]

    plt.plot(df, label=new_var)
    plt.title(
        'Exports & Imports of Goods and Services, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.show()


def plot_uscb_trade_gold_silver(df: DataFrame) -> None:
    plt.figure()
    new_var = [
        'Exports, U187',
        'Imports, U188',
        'Net Exports, U189',
    ]

    plt.plot(df, label=new_var)
    plt.title(
        'Total Merchandise, Gold and Silver, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.show()


def plot_uscb_trade_by_countries(df: DataFrame) -> None:
    assert df.shape[1] == 58, "Works on DataFrame Produced with combine_uscb_trade_by_countries()"
    _LABELS = (
        'America-Canada',
        'America-Cuba',
        'America-Mexico',
        'America-Brazil',
        'America-Other',
        'Europe-United Kingdom',
        'Europe-France',
        'Europe-Germany',
        'Europe-Other',
        'Asia-Mainland China',
        'Asia-Japan',
        'Asia-Other',
        'Australia and Oceania-All',
        'Africa-All',
    )
    plt.figure(1)
    plt.plot(df.iloc[:, range(28, 42)], label=_LABELS)
    plt.title('Net Exports by Regions')
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.semilogy(df.iloc[:, -len(_LABELS):], label=_LABELS)
    plt.title('Net Exports by Regions to Overall Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plot_uscb_money_stock(df: DataFrame) -> None:
    YEAR_BASE = 1915
    plt.figure()
    new_var = [
        'Currency Held by the Public',
        'M1 Money Supply (Currency Plus Demand Deposits)',
        'M2 Money Supply (M1 Plus Time Deposits)',
    ]

    plt.semilogy(df, label=new_var)
    plt.axvline(x=YEAR_BASE, linestyle=':')
    plt.title('Currency Dynamics, {}=100'.format(YEAR_BASE))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plot_uscb_finance() -> None:
    """Census Financial Markets & Institutions Series"""
    ARCHIVE_NAME = 'dataset_uscb.zip'
    SERIES_IDS = (
        {f'X{_:04n}': ARCHIVE_NAME}
        for _ in itertools.chain(
            range(410, 424),
            range(580, 588),
            range(610, 634),
            range(741, 756),
            range(879, 933),
            range(947, 957),
        )
    )

    for _, series_id in enumerate(SERIES_IDS, start=1):
        df = stockpile_usa_hist(series_id).pipe(transform_rebase)
        descr = pull_uscb_description(series_id)
        plt.figure(_)
        plt.plot(df, label=series_id)
        plt.title('{}, {}$-${}'.format(descr, *df.index[[0, -1]]))
        plt.xlabel('Period')
        plt.ylabel('Percentage')
        plt.grid()
        plt.legend()
        plt.show()


def plot_approx_linear(df: DataFrame, year_base, params) -> None:
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
        df.iloc[:, 4]      Deflator
        df.iloc[:, 5]      Regressor Based
        df.iloc[:, 6]      Regressand Based
        df.iloc[:, 7]      Regressand Estimate
        ================== =================================.
    year_base : TYPE
        DESCRIPTION.
    params : TYPE
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    plt.figure()
    plt.title('$Y(X)$, {}=100, {}$-${}'.format(year_base, *df.index[[0, -1]]))
    plt.xlabel(
        f'Gross Private Domestic Investment, $X(\\tau)$, {year_base}=100, {df.index[0]}=100'
    )
    plt.ylabel(
        f'Gross Domestic Product, $Y(\\tau)$, {year_base}=100, {df.index[0]}=100'
    )
    plt.plot(df.iloc[:, -3], df.iloc[:, -2])
    plt.plot(
        df.iloc[:, -3], df.iloc[:, -1],
        label='$\\hat Y = {:.4f}+{:.4f}X$'.format(*params[::-1])
    )
    plt.grid()
    plt.legend()
    plt.show()


def plot_approx_linear_log(df: DataFrame, year_base: int, params: np.ndarray) -> None:
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
        df.iloc[:, 4]      Deflator
        df.iloc[:, 5]      Regressor Log Based
        df.iloc[:, 6]      Regressand Log Based
        df.iloc[:, 7]      Regressand Estimate
        ================== =================================.
    year_base : int
        DESCRIPTION.
    params : np.ndarray
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    MAP_DESC = {
        'A032RC': 'National Income',
        'A191RC': 'Gross Domestic Product',
    }
    plt.figure()
    plt.title(
        '$Y(X)$, {}=100, {}$-${}'.format(
            year_base, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Logarithm Prime Rate, $X(\\tau)$, {}=100'.format(df.index[0]))
    plt.ylabel(
        'Logarithm {}, $Y(\\tau)$, {}=100, {}=100'.format(
            MAP_DESC[df.columns[3]], year_base, df.index[0]
        )
    )
    plt.plot(df.iloc[:, -3], df.iloc[:, -2])
    plt.plot(
        df.iloc[:, -3], df.iloc[:, -1],
        label='$\\hat Y = {:.4f}+{:.4f}X$'.format(*params[::-1])
    )
    plt.grid()
    plt.legend()
    plt.show()


def plot_lab_cap_inty_lab_prty_closure(df: DataFrame) -> None:
    """
    Plotting

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Labor Capital Intensity
        df.iloc[:, 1]      Labor Productivity
        ================== =================================
    Returns
    -------
    None
    """
    plot_lab_cap_inty_lab_prty(
        *simple_linear_regression(df.iloc[:, -2:]),
        'Original'
    )
    plot_lab_cap_inty_lab_prty(
        *simple_linear_regression(np.log(df.iloc[:, -2:].astype(float))),
        'Logarithm'
    )


def plot_lab_cap_inty(df: DataFrame) -> None:
    """
    Plotting

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Labor Capital Intensity
        ================== =================================
    Returns
    -------
    None
    """
    # =========================================================================
    # Valid Only for _k = 2
    # =========================================================================
    _k = 2
    # =========================================================================
    # Odd DataFrame
    # =========================================================================
    df_o = pd.concat(
        [
            df.iloc[:, [-1]],
            filter_rolling_mean(df.iloc[:, [-1]], _k)[0].iloc[:, [-1]],
            filter_kol_zur(df.iloc[:, [-1]], _k)[0].iloc[:, [-1]],
            df.iloc[:, [-1]].ewm(alpha=0.25, adjust=False).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # Even DataFrame
    # =========================================================================
    df_e = pd.concat(
        [
            filter_rolling_mean(df.iloc[:, [-1]], _k)[1].iloc[:, [-1]],
            filter_kol_zur(df.iloc[:, [-1]], _k)[1].iloc[:, [-1]],
        ],
        axis=1,
    )
    plt.figure()
    plt.plot(
        df_o.iloc[:, 0],
        linewidth=3,
        label='Labor Capital Intensity'
    )
    plt.plot(
        df_o.iloc[:, 1],
        label=f'Rolling Mean, {1+_k}'
    )
    plt.plot(
        df_o.iloc[:, 2],
        label=f'Kolmogorov--Zurbenko Filter, {1+_k}'
    )
    plt.plot(
        df_o.iloc[:, 3],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.25)
    )
    plt.plot(
        df_e,
        label=[
            f'Rolling Mean, {_k}',
            f'Kolmogorov--Zurbenko Filter, {_k}',
        ]
    )
    plt.title(
        'Labor Capital Intensity: Rolling Mean Filter, Kolmogorov--Zurbenko Filter &\n\
        Single Exponential Smoothing'
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plot_lab_prty(df: DataFrame) -> None:
    """
    Plotting

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Labor Productivity
        ================== =================================
    Returns
    -------
    None
    """
    _k = 3
    # =========================================================================
    # Odd DataFrame
    # =========================================================================
    df_o = pd.concat(
        [
            df.iloc[:, [-1]],
            filter_rolling_mean(df.iloc[:, [-1]], _k)[0].iloc[:, [-1]],
            filter_kol_zur(df.iloc[:, [-1]], _k)[0].iloc[:, [1]],
            df.iloc[:, [-1]].ewm(alpha=0.25, adjust=False).mean(),
            df.iloc[:, [-1]].ewm(alpha=0.35, adjust=False).mean(),
            df.iloc[:, [-1]].ewm(alpha=0.45, adjust=False).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # Even DataFrame
    # =========================================================================
    df_e = pd.concat(
        [
            filter_rolling_mean(df.iloc[:, [-1]], _k)[1],
            filter_kol_zur(df.iloc[:, [-1]], _k)[1],
        ],
        axis=1,
    )
    plt.figure()
    plt.plot(
        df_o.iloc[:, 0],
        linewidth=3,
        label='Labor Productivity'
    )
    plt.plot(
        df_o.iloc[:, 1],
        label=f'Rolling Mean, {_k}'
    )
    plt.plot(
        df_o.iloc[:, 2],
        label=f'Kolmogorov--Zurbenko Filter, {_k}'
    )
    plt.plot(
        df_o.iloc[:, 3],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.25)
    )
    plt.plot(
        df_o.iloc[:, 4],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.35)
    )
    plt.plot(
        df_o.iloc[:, 5],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.45)
    )
    plt.plot(
        df_e,
        label=[
            f'Rolling Mean, {_k-1}',
            f'Rolling Mean, {_k+1}',
            f'Kolmogorov--Zurbenko Filter, {_k-1}',
            f'Kolmogorov--Zurbenko Filter, {_k+1}',
        ]
    )
    plt.title(
        'Labor Capital Intensity: Rolling Mean Filter, Kolmogorov--Zurbenko Filter &\n\
        Single Exponential Smoothing'
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plot_built_in() -> None:
    """
    Purpose: Draw:

    Returns
    -------
    None
    """
    FUNCTIONS = (
        # =====================================================================
        # Correlogram, Pandas;
        # =====================================================================
        autocorrelation_plot,
        # =====================================================================
        # Bootstrap Plot, Pandas;
        # =====================================================================
        # bootstrap_plot,
        # =====================================================================
        # Lag Plot, Pandas
        # =====================================================================
        lag_plot,
    )
    SOURCE_ID = 'NY.GDP.MKTP.CD'
    _df = read_worldbank(SOURCE_ID)
    for func in FUNCTIONS:
        for _, country in enumerate(_df.columns, start=1):
            chunk = _df.loc[:, (country,)].dropna(axis=0)
            if not chunk.empty:
                plt.figure(_)
                partial(func, chunk)()
                plt.title(country)
                plt.grid()
        plt.show()


def plot_can_test(df: DataFrame) -> None:
    plt.figure()
    df.plot(logy=True)
    plt.title('Discrepancy')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.show()


def plot_model_capital(df: DataFrame, year_base: int) -> None:
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Investment
        df.iloc[:, 1]      Production
        df.iloc[:, 2]      Capital
        df.iloc[:, 3]      Capital Retirement
        ================== =================================
    """
    _params_i = np.polyfit(
        df.index.to_series().astype(int),
        df.iloc[:, 0].div(df.iloc[:, 1]).astype(float),
        deg=1
    )
    _params_t = np.polyfit(
        df.index.to_series().astype(int),
        df.iloc[:, 1].div(df.iloc[:, 2]).astype(float),
        deg=1
    )
    _df = df.copy()
    # =========================================================================
    # Gross Fixed Investment to Gross Domestic Product Ratio
    # =========================================================================
    _df['inv_to_pro'] = np.poly1d(_params_i)(_df.index.to_series())
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    _df['c_turnover'] = np.poly1d(_params_t)(_df.index.to_series())
    _df['cap_a'] = df.pipe(calculate_capital, _params_i, _params_t, 0.875)
    _df['cap_b'] = df.pipe(calculate_capital, _params_i, _params_t, 1)
    _df['cap_c'] = df.pipe(calculate_capital, _params_i, _params_t, 1.125)
    plt.figure(1)
    plt.title(
        'Fixed Assets Turnover ($\\lambda$) for the US, {}$-${}'.format(
            *_df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(_df.iloc[:, 1].div(_df.iloc[:, 2]), label='$\\lambda$')
    label = '$\\lambda = {1:,.4f}\\ {0:,.4f}\\times t$'.format(
        *_params_t) if _params_t[0] < 0 else '$\\lambda = {1:,.4f} + {0:,.4f} \\times t$'.format(*_params_t)
    plt.plot(_df.iloc[:, -4], label=label)
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.title(
        'Gross Fixed Investment as Percentage of GDP ($S$) for the US, {}$-${}'.format(
            *_df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(_df.iloc[:, 0].div(_df.iloc[:, 1]), label='$S$')
    label = '$S = {1:,.4f}\\ {0:,.4f}\\times t$'.format(
        *_params_i) if _params_i[0] < 0 else '$S = {1:,.4f} + {0:,.4f} \\times t$'.format(*_params_i)
    plt.plot(_df.iloc[:, -5], label=label)
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.title(
        '$\\alpha$ for the US, {}$-${}'.format(
            *_df.index[[0, -2]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(_df.iloc[:, 3], label='$\\alpha$')
    plt.grid()
    plt.legend()
    plt.figure(4)
    plt.title('$K$ for the US, {}$-${}'.format(*_df.index[[0, -2]]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars, {}=100'.format(year_base))
    plt.semilogy(
        _df.iloc[:, -3:],
        label=['$K\\left(\\pi = \\frac{7}{8}\\right)$',
               '$K\\left(\\pi = 1\\right)$',
               '$K\\left(\\pi = \\frac{9}{8}\\right)$', ]
    )
    plt.grid()
    plt.legend()
    plt.show()


def plot_capital_purchases(df: DataFrame) -> None:
    assert df.shape[1] == 27, "Works on DataFrame Produced with 'combine_usa_capital_purchases()"
    plt.figure()
    new_var = [
        '$s^{2;1}_{Cobb-Douglas}$',
        'Total',
        'Structures',
        'Equipment',
    ]

    plt.semilogy(
        df.loc[:, (df.columns[0], *df.columns[-3:])],
        label=new_var
    )
    plt.title('Fixed Assets Purchases, {}$-${}'.format(*df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid()
    plt.legend()
    plt.show()


def plot_uscb_complex(df: DataFrame) -> None:
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    df.copy().pipe(plot_pearson_r_test)
    df.copy().pipe(plot_filter_kol_zur)
    df.copy().pipe(plot_ewm)


def plot_cobb_douglas(df: DataFrame, params: tuple[float], mapping: dict) -> None:
    """
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    """
    assert df.shape[1] == 12

    plt.figure(1)
    plt.semilogy(
        df.iloc[:, range(3)],
        label=[
            'Fixed Capital',
            'Labor Force',
            'Physical Product',
        ]
    )
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_a'].format(*df.index[[0, -1]],
                                     mapping['year_base']))
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.semilogy(
        df.iloc[:, (2, 9)],
        label=[
            'Actual Product',
            'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
                params[1],
                1-params[0],
                params[0],
            ),
        ]
    )
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(mapping['fg_b'].format(*df.index[[0, -1]],
                                     mapping['year_base']))
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.plot(
        df.iloc[:, (8, 11)],
        label=[
            'Deviations of $P$',
            'Deviations of $P\'$',
            # =================================================================
            # TODO: ls=['solid','dashed',]
            # =================================================================
        ]
    )
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_c'])
    plt.grid()
    plt.legend()
    plt.figure(4)
    plt.plot(df.iloc[:, 9].div(df.iloc[:, 2]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_d'].format(*df.index[[0, -1]]))
    plt.grid()
    plt.figure(5, figsize=(5, 8))
    plt.scatter(df.iloc[:, 5], df.iloc[:, 4])
    plt.scatter(df.iloc[:, 5], df.iloc[:, 6])
    lc = np.arange(0.2, 1.0, 0.005)
    plt.plot(
        lc,
        lab_productivity(lc, *params),
        label='$\\frac{3}{4}\\frac{P}{L}$'
    )
    plt.plot(
        lc,
        cap_productivity(lc, *params),
        label='$\\frac{1}{4}\\frac{P}{C}$'
    )
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_e'])
    plt.grid()
    plt.legend()
    plt.show()


def plot_cobb_douglas_3d(df: DataFrame) -> None:
    """
    Cobb--Douglas 3D-Plotting

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
    None
    """
    assert df.shape[1] == 3

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2])
    ax.set_xlabel('Capital')
    ax.set_ylabel('Labor')
    ax.set_zlabel('Production')
    ax.view_init(30, 45)
    plt.show()


def plot_cobb_douglas_alt(df: DataFrame, params: tuple[float], mapping: dict) -> None:
    """
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    """
    assert df.shape[1] == 20

    plt.figure(1)
    plt.semilogy(
        df.iloc[:, range(4)],
        label=[
            'Fixed Capital',
            'Labor Force',
            'Physical Product',
            'Physical Product, Alternative',
        ]
    )
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_a'].format(*df.index[[0, -1]],
                                     mapping['year_base']))
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(
        df.iloc[:, (3, 17)],
        label=[
            'Actual Product',
            'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
                params[1],
                1-params[0],
                params[0],
            ),
        ]
    )
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(mapping['fg_b'].format(*df.index[[0, -1]],
                                     mapping['year_base']))
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.plot(
        df.iloc[:, (15, 18)],
        label=[
            'Deviations of $P$',
            'Deviations of $P\'$',
            # =================================================================
            # TODO: ls=['solid','dashed',]
            # =================================================================
        ]
    )
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_c'])
    plt.grid()
    plt.legend()
    plt.figure(4)
    plt.plot(df.iloc[:, 17].div(df.iloc[:, 3]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_d'].format(*df.index[[0, -1]]))
    plt.grid()
    plt.figure(5, figsize=(5, 8))
    plt.scatter(df.iloc[:, 6], df.iloc[:, 13])
    plt.scatter(df.iloc[:, 6], df.iloc[:, 14])
    lc = np.arange(0.2, 1.0, 0.005)
    plt.plot(
        lc,
        lab_productivity(lc, *params),
        label='$\\frac{3}{4}\\frac{P}{L}$'
    )
    plt.plot(
        lc,
        cap_productivity(lc, *params),
        label='$\\frac{1}{4}\\frac{P}{C}$'
    )
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_e'])
    plt.grid()
    plt.legend()
    plt.show()


def plot_cobb_douglas_complex(df: DataFrame) -> None:
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
    None
    """
    YEAR_BASE = 1899

    _df, _params = df.pipe(transform_cobb_douglas, year_base=YEAR_BASE)
    plot_cobb_douglas(
        _df,
        _params,
        get_fig_map(YEAR_BASE)
    )
    df.iloc[:, range(3)].pipe(plot_cobb_douglas_3d)
    _df.iloc[:, [3, 4]].pipe(plot_lab_prod_polynomial)
    _df.iloc[:, [3, 4]].pipe(plot_lab_cap_inty_lab_prty_closure)
    _df.iloc[:, [3]].pipe(plot_lab_cap_inty)
    _df.iloc[:, [4]].pipe(plot_lab_prty)
    _df.iloc[:, [6]].pipe(plot_turnover)


def plot_cobb_douglas_tight_layout(df: DataFrame, params: tuple[float], mapping: dict) -> None:
    """
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    """
    assert df.shape[1] == 12

    fig, axes = plt.subplots(5, 1)
    axes[0].plot(
        df.iloc[:, range(3)],
        label=[
            'Fixed Capital',
            'Labor Force',
            'Physical Product',
        ]
    )
    axes[0].set_xlabel('Period')
    axes[0].set_ylabel('Indexes')
    axes[0].set_title(mapping['fg_a'].format(*df.index[[0, -1]],
                                             mapping['year_base']))
    axes[0].legend()
    axes[0].grid()
    axes[1].plot(
        df.iloc[:, (2, 5)],
        label=[
            'Actual Product',
            'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
                params[1], 1-params[0], params[0]),
        ]
    )
    axes[1].set_xlabel('Period')
    axes[1].set_ylabel('Production')
    axes[1].set_title(mapping['fg_b'].format(*df.index[[0, -1]],
                                             mapping['year_base']))
    axes[1].legend()
    axes[1].grid()
    axes[2].plot(
        df.iloc[:, (8, 9)],
        label=[
            'Deviations of $P$',
            'Deviations of $P\'$',
        ],
        # =====================================================================
        # TODO: ls=['solid','dashed',]
        # =====================================================================
    )
    axes[2].set_xlabel('Period')
    axes[2].set_ylabel('Percentage Deviation')
    axes[2].set_title(mapping['fg_c'])
    axes[2].legend()
    axes[2].grid()
    axes[3].plot(df.iloc[:, 5].div(df.iloc[:, 2]).sub(1))
    axes[3].set_xlabel('Period')
    axes[3].set_ylabel('Percentage Deviation')
    axes[3].set_title(mapping['fg_d'].format(*df.index[[0, -1]]))
    axes[3].grid()
    axes[4].scatter(df.iloc[:, 10], df.iloc[:, 4])
    axes[4].scatter(df.iloc[:, 10], df.iloc[:, 11])
    lc = np.arange(0.2, 1.0, 0.005)
    axes[4].plot(
        lc,
        lab_productivity(lc, *params),
        label='$\\frac{3}{4}\\frac{P}{L}$'
    )
    axes[4].plot(
        lc,
        cap_productivity(lc, *params),
        label='$\\frac{1}{4}\\frac{P}{C}$'
    )
    axes[4].set_xlabel('$\\frac{L}{C}$')
    axes[4].set_ylabel('Indexes')
    axes[4].set_title(mapping['fg_e'])
    axes[4].legend()
    axes[4].grid()
    plt.tight_layout()
    plt.show()


def plot_douglas(
    archive_name: str,
    group_iters: tuple[int],
    titles: tuple[str],
    measures: tuple[str],
    legends: tuple[str] = None,
    start_at: int = 1,
    skip: int = 1
) -> None:
    """
    Specialised Plotting

    Parameters
    ----------
    archive_name : str
        File Name of Archive for Dataset.
    group_iters : tuple[int]
        Iteration Groups.
    titles : tuple[str]
        Plot Titles.
    measures : tuple[str]
        Series Dimenstion.
    legends : tuple[str], optional
        Additional Sublabels. The default is None.
    start_at : int, optional
        Number of the First Plot. The default is 1.
    skip : int, optional
        Step over Iteration. The default is 1.

    Returns
    -------
    None
    """
    _MAP_SERIES = pull_series_ids_description(archive_name)
    _SERIES_IDS = tuple(_MAP_SERIES.keys())
    if not legends is None:
        for _n, (_lw, _up, _tt, _mr, _lb) in enumerate(
                zip(
                    group_iters[:-1],
                    group_iters[1:],
                    titles,
                    measures,
                    legends
                ),
                start=start_at
        ):
            plt.figure(_n)
            for _ in range(_lw, _up, skip):
                plt.plot(
                    read_usa_hist(archive_name, _SERIES_IDS[_]),
                    # =========================================================
                    # read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
                    # =========================================================
                    label=_MAP_SERIES[_SERIES_IDS[_]]
                )
            plt.title(_tt)
            plt.xlabel('Period')
            plt.ylabel(_mr)
            plt.grid()
            if not _lb is None:
                plt.legend(_lb)
            plt.show()
    else:
        for _n, (_lw, _up, _tt, _mr) in enumerate(
                zip(
                    group_iters[:-1],
                    group_iters[1:],
                    titles,
                    measures,
                ),
                start=start_at
        ):
            plt.figure(_n)
            for _ in range(_lw, _up, skip):
                plt.plot(
                    read_usa_hist(archive_name, _SERIES_IDS[_]),
                    # =========================================================
                    # read_usa_hist(ARCHIVE_NAME).pipe(pull_by_series_id, series_id)
                    # =========================================================
                    label=_MAP_SERIES[_SERIES_IDS[_]]
                )
            plt.title(_tt)
            plt.xlabel('Period')
            plt.ylabel(_mr)
            plt.grid()
            plt.show()


def plot_elasticity(df: DataFrame, plot_title: tuple[str]) -> None:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Real Values for Price Deflator
        df.iloc[:, 1]      Nominal Values for Price Deflator
        df.iloc[:, 2]      Target Series
        df.iloc[:, :]      Etc.
        ================== =================================.
    plot_title : tuple[str]
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    plt.figure(1)
    plt.title('{}, {}, {}=100'.format(*plot_title))
    plt.xlabel('Period')
    plt.ylabel(f'Billions of Dollars, {plot_title[2]}=100')
    plt.plot(df.iloc[:, [3]], label=f'{plot_title[1]}')
    plt.plot(
        df.index.to_series().rolling(2).mean(),
        df.iloc[:, 4],
        label=f'{plot_title[1]}, Rolling Mean, Window = 2'
    )
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.title('Elasticity: {}, {}, {}=100'.format(*plot_title))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(
        df.index.to_series().rolling(2).mean(),
        df.iloc[:, 5],
        label='$\\overline{E}_{T+\\frac{1}{2}}$'
    )
    plt.plot(df.iloc[:, [6]], label='$E_{T+1}$')
    plt.plot(df.iloc[:, [7]], label='$\\overline{E}_{T+1}$')
    plt.plot(
        df.index.to_series().rolling(2).mean(),
        df.iloc[:, 8],
        label='$\\overline{\\epsilon(E_{T+\\frac{1}{2}})}$'
    )
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.title('Elasticity: {}, {}, {}=100'.format(*plot_title))
    plt.xlabel('{}, {}, {}=100'.format(*plot_title))
    plt.ylabel('Elasticity: {}, {}, {}=100'.format(*plot_title))
    plt.plot(df.iloc[:, 3], df.iloc[:, 8], label='$\\frac{\\epsilon(X)}{X}$')
    plt.grid()
    plt.legend()
    plt.show()


def plot_ewm(df: DataFrame, step: float = 0.1) -> None:
    """
    Single Exponential Smoothing
    Robert Goodell Brown, 1956
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    """
    _alpha = 0.25
    # =========================================================================
    # DataFrame for Exponentially Smoothed Series
    # =========================================================================
    _smooth = df.copy()
    while True:
        if _alpha >= 1:
            break
        _smooth = pd.concat(
            [
                _smooth,
                _smooth.iloc[:, [0]].ewm(alpha=_alpha, adjust=False).mean()
            ],
            axis=1
        )
        _smooth.columns = [
            *_smooth.columns[:-1], f'{_smooth.columns[0]}_{_alpha:,.2f}',
        ]
        _alpha += step
    # =========================================================================
    # DataFrame for Deltas of Exponentially Smoothed Series
    # =========================================================================
    _deltas = pd.concat(
        [
            _smooth.iloc[:, [_]].pct_change(-1).mul(-1).dropna(axis=0)
            for _ in range(_smooth.shape[1])
        ],
        axis=1
    )
    _deltas.index = _smooth.index.to_series().rolling(2).mean().dropna(axis=0)
    # =========================================================================
    # Plotting
    # =========================================================================
    _labels = [
        'Original Series',
        *[
            'Smoothing: $\\alpha={:,.2f}$'.format(float(column.split('_')[-1])) for column in _smooth.columns[1:]
        ]
    ]
    plt.figure(1)
    plt.title('Exponentially Smoothed Series')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(_smooth.index, _smooth.iloc[:, 0])
    plt.plot(_smooth.iloc[:, 1:])
    plt.grid()
    plt.legend(_labels)
    plt.figure(2)
    plt.title('Deltas of Exponentially Smoothed Series')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(_deltas.index, _deltas.iloc[:, 0])
    plt.plot(_deltas.iloc[:, 1:])
    plt.grid()
    plt.legend(_labels)
    plt.show()


def plot_fourier_discrete(df: DataFrame, precision: int = 10) -> None:
    """
    Discrete Fourier Transform based on Simpson's Rule
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    """
    _df = df.copy()
    precision += 1
    _p = np.polyfit(
        _df.index.to_series().astype(int),
        _df.iloc[:, 0].astype(float),
        deg=1
    )
    _df['period_calibrated'] = _df.index.to_series().sub(
        _df.index[0]).div(_df.shape[0]).mul(2).mul(np.pi).astype(float)
    _df[f'{_df.columns[0]}_line'] = np.poly1d(_p)(_df.index.to_series())
    _df[f'{_df.columns[0]}_wave'] = _df.iloc[:, 0].sub(_df.iloc[:, 2])
    # =========================================================================
    # DataFrame for Fourier Coefficients
    # =========================================================================
    _fourier = DataFrame(columns=['cos', 'sin'])
    for _ in range(precision):
        _fourier.loc[_] = [
            _df.iloc[:, 3].mul(np.cos(_df.iloc[:, 1].mul(_))).mul(2).mean(),
            _df.iloc[:, 3].mul(np.sin(_df.iloc[:, 1].mul(_))).mul(2).mean()
        ]
    # =========================================================================
    # First Entry Correction
    # =========================================================================
    _fourier.loc[0, 'cos'] /= 2
    plt.figure()
    plt.title(f'$\\alpha$ for the US, {_df.index[0]}$-${_df.index[-1]}')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(_df.index, _df.iloc[:, 0], label='$\\alpha$')
    _df[f'{_df.columns[0]}_fourier_{0}'] = np.cos(_df.iloc[:, 1].mul(0)).mul(
        _fourier.loc[0, 'cos']).add(np.sin(_df.iloc[:, 1].mul(0)).mul(_fourier.loc[0, 'sin']))
    for _ in range(1, precision):
        _df[f'{_df.columns[0]}_fourier_{_}'] = _df.iloc[:, -1].add(np.cos(_df.iloc[:, 1].mul(_)).mul(
            _fourier.loc[_, 'cos'])).add(np.sin(_df.iloc[:, 1].mul(_)).mul(_fourier.loc[_, 'sin']))
        plt.plot(_df.iloc[:, 2].add(_df.iloc[:, -1]),
                 label=f'$FT_{{{_:02}}}(\\alpha)$')
    plt.grid()
    plt.legend()
    plt.show()


def plot_rus_grigoriev(df: DataFrame) -> None:
    for series_id in sorted(set(df.loc[:, "series"])):
        df.pipe(pull_by_series_id, series_id).plot(grid=True)


def plot_growth_elasticity(df: DataFrame) -> None:
    """Growth Elasticity Plotting
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    """
    # =========================================================================
    # TODO: Increase Cohesion of This Code: Send Plotting to Separate Function
    # =========================================================================
    df.reset_index(level=0, inplace=True)
    _df = DataFrame()
    # =========================================================================
    # Period, Centered
    # =========================================================================
    _df[f'{df.columns[0]}'] = df.iloc[:, [0]].rolling(2).mean()
    # =========================================================================
    # df.index.to_series().rolling(2).mean()
    # =========================================================================
    # =========================================================================
    # Series, Centered
    # =========================================================================
    _df[f'{df.columns[1]}_centered'] = df.iloc[:, [1]].rolling(2).mean()
    # =========================================================================
    # Series, Growth Rate
    # =========================================================================
    _df[f'{df.columns[1]}_growth_rate'] = df.iloc[:, [1]].diff(
        2).div(df.iloc[:, [1]].rolling(2).sum().shift(1))
    # =========================================================================
    # Series, Elasticity
    # =========================================================================
    _df[f'{df.columns[1]}_elasticity'] = df.iloc[:, [1]].rolling(2).sum(
    ).shift(-1).mul(2).div(df.iloc[:, [1]].rolling(4).sum().shift(-1)).sub(1)
    _df.set_index(_df.columns[0], inplace=True)
    _df.dropna(inplace=True)
    plt.figure()
    plt.plot(_df.iloc[:, [1]], label='Growth Rate')
    plt.plot(_df.iloc[:, [2]], label='Elasticity Rate')
    plt.title('Growth & Elasticity Rates')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plot_increment(
    df: DataFrame,
    savefig: bool = False,
    path_export: str = '/media/green-machine/KINGSTON',
    file_name: str = 'fig_file_name.pdf'
) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(10, 20))
    axes[0].plot(df.iloc[:, 0], df.iloc[:, 1], label='Curve')
    axes[0].set_xlabel('Labor Capital Intensity')
    axes[0].set_ylabel('Labor Productivity')
    axes[0].set_title('Labor Capital Intensity to Labor Productivity Relation')
    axes[0].legend()
    axes[0].grid()
    axes[1].plot(df.iloc[:, 2], df.iloc[:, 3], label='Curve')
    axes[1].set_xlabel('Labor Capital Intensity Increment')
    axes[1].set_ylabel('Labor Productivity Increment')
    axes[1].set_title(
        'Labor Capital Intensity to Labor Productivity Increments Relation')
    axes[1].grid()
    axes[1].legend()
    for _ in range(3, df.shape[0], 5):
        axes[0].annotate(df.index[_], (df.iloc[_, 0], df.iloc[_, 1]))
        axes[1].annotate(df.index[_], (df.iloc[_, 2], df.iloc[_, 3]))

    fig.tight_layout()
    if savefig:
        fig.savefig(Path(path_export).joinpath(
            file_name), format='pdf', dpi=900)
    else:
        plt.show()


def plot_rus_is_lm(df: DataFrame) -> None:
    """
    Plotting

    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    plt.figure()
    plt.plot(df.iloc[:, 0], df.iloc[:, 1])
    plt.xlabel('Percentage')
    plt.ylabel('RUB, Millions')
    plt.title('M1 Dependency on Prime Rate')
    plt.grid()
    plt.show()


def plot_filter_kol_zur(df: DataFrame) -> None:
    """
    Kolmogorov--Zurbenko Filter

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    Returns
    -------
    None
    """
    df_o, df_e, residuals_o, residuals_e = filter_kol_zur(df)

    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(
        df_o.iloc[:, [0]].index,
        df_o.iloc[:, [0]],
        label='Original Series'
    )
    plt.plot(
        df_o.iloc[:, 1:],
        label=['$filter_kol_zur(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in df_o.columns[1:]]
    )
    plt.plot(
        df_e,
        label=['$filter_kol_zur(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in df_e.columns]
    )
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.title('Kolmogorov$-$Zurbenko Filter Residuals')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(
        residuals_o.iloc[:, [0]].index,
        residuals_o.iloc[:, [0]],
        label='Residuals'
    )
    plt.plot(
        residuals_o.iloc[:, 1:],
        label=['$\\delta filter_kol_zur(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_o.columns[1:]]
    )
    plt.plot(
        residuals_e,
        label=['$\\delta filter_kol_zur(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_e.columns]
    )
    plt.grid()
    plt.legend()
    plt.show()


def plot_usa_kurenkov(*args) -> None:
    """
    Plots Augmented Data for Kurenkov Yu.V. Dataset

    Parameters
    ----------
    *args : TYPE
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    # =========================================================================
    # TODO: Make Use of `year_base` Parameter
    # =========================================================================
    data_frame_gen = combine_data_frames_by_columns(*args)

    fig, axes = plt.subplots(4, 1, figsize=(10, 20))
    axes[0].plot(
        next(data_frame_gen),
        label=['Kurenkov Data', 'BEA Data', 'FRB Data']
    )
    axes[0].set_title(f'Production, {1950}=100')
    axes[0].set_xlabel('Period')
    axes[0].set_ylabel('Percentage')
    axes[0].legend()
    axes[0].grid()
    axes[1].plot(
        next(data_frame_gen),
        label=['Kurenkov Data', 'BEA Data']
    )
    axes[1].set_title('Labor')
    axes[1].set_xlabel('Period')
    axes[1].set_ylabel('Thousands of Persons')
    axes[1].legend()
    axes[1].grid()
    # =========================================================================
    # Revised Capital
    # =========================================================================
    axes[2].plot(
        next(data_frame_gen),
        label=['Kurenkov Data', 'BEA Data']
    )
    axes[2].set_title(f'Capital, {1950}=100')
    axes[2].set_xlabel('Period')
    axes[2].set_ylabel('Percentage')
    axes[2].legend()
    axes[2].grid()
    axes[3].plot(
        next(data_frame_gen),
        label=['Kurenkov Data', 'FRB Data']
    )
    axes[3].set_title('Capacity Utilization')
    axes[3].set_xlabel('Period')
    axes[3].set_ylabel('Percentage')
    axes[3].legend()
    axes[3].grid()


def plot_lab_prod_polynomial(df: DataFrame) -> None:
    """
    Static Labor Productivity Approximation

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Labor Capital Intensity
        df.iloc[:, 1]      Labor Productivity
        ================== =================================
    Returns
    ------
    None
    """

    def _r2_scores():
        for _ in range(5):
            yield r2_score(df.iloc[:, -1], _df.iloc[:, _])

    k, b = np.polyfit(
        np.log(df.iloc[:, -2].astype(float)),
        np.log(df.iloc[:, -1].astype(float)),
        deg=1
    )
    # =========================================================================
    # Polynomials 1, 2, 3 & 4: Labor Productivity
    # =========================================================================
    polyfit_linear = np.polyfit(
        df.iloc[:, -2].astype(float),
        df.iloc[:, -1].astype(float),
        deg=1
    )
    polyfit_quadratic = np.polyfit(
        df.iloc[:, -2].astype(float),
        df.iloc[:, -1].astype(float),
        deg=2
    )
    polyfit_cubic = np.polyfit(
        df.iloc[:, -2].astype(float),
        df.iloc[:, -1].astype(float),
        deg=3
    )
    polyfit_quartic = np.polyfit(
        df.iloc[:, -2].astype(float),
        df.iloc[:, -1].astype(float),
        deg=4
    )
    # =========================================================================
    # DataFrame for Approximation Results
    # =========================================================================
    _df = DataFrame()
    _df['pow'] = df.iloc[:, -2].pow(k).mul(np.exp(b))
    _df['p_1'] = np.poly1d(polyfit_linear)(df.iloc[:, -2])
    _df['p_2'] = np.poly1d(polyfit_quadratic)(df.iloc[:, -2])
    _df['p_3'] = np.poly1d(polyfit_cubic)(df.iloc[:, -2])
    _df['p_4'] = np.poly1d(polyfit_quartic)(df.iloc[:, -2])
    # =========================================================================
    # Deltas
    # =========================================================================
    _df['d_pow'] = _df.iloc[:, 0].div(df.iloc[:, -1]).sub(1).abs()
    _df['d_p_1'] = _df.iloc[:, 1].div(df.iloc[:, -1]).sub(1).abs()
    _df['d_p_2'] = _df.iloc[:, 2].div(df.iloc[:, -1]).sub(1).abs()
    _df['d_p_3'] = _df.iloc[:, 3].div(df.iloc[:, -1]).sub(1).abs()
    _df['d_p_4'] = _df.iloc[:, 4].div(df.iloc[:, -1]).sub(1).abs()
    r = _r2_scores()
    plt.figure(1)
    plt.scatter(
        df.iloc[:, [-1]].index,
        df.iloc[:, [-1]],
        label='Labor Productivity'
    )
    plt.plot(
        _df.iloc[:, 0],
        label='$\\hat Y = {:.2f}X^{{{:.2f}}}, R^2 = {:.4f}$'.format(
            np.exp(b),
            k,
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 1],
        label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X, R^2 = {:.4f}$'.format(
            1,
            *polyfit_linear[::-1],
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 2],
        label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2, R^2 = {:.4f}$'.format(
            2,
            *polyfit_quadratic[::-1],
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 3],
        label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3, R^2 = {:.4f}$'.format(
            3,
            *polyfit_cubic[::-1],
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 4],
        label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3 {:.2f}X^4, R^2 = {:.4f}$'.format(
            4,
            *polyfit_quartic[::-1],
            next(r),
        )
    )
    plt.title('Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
        *df.index[[0, -1]]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(
        _df.iloc[:, 5],
        ':',
        label='$\\|\\frac{{\\hat Y-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            _df.iloc[:, 5].mean()
        )
    )
    plt.plot(
        _df.iloc[:, 6],
        ':',
        label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            1,
            _df.iloc[:, 6].mean()
        )
    )
    plt.plot(
        _df.iloc[:, 7],
        ':',
        label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            2,
            _df.iloc[:, 7].mean()
        )
    )
    plt.plot(
        _df.iloc[:, 8],
        ':',
        label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            3,
            _df.iloc[:, 8].mean()
        )
    )
    plt.plot(
        _df.iloc[:, 9],
        ':',
        label='$\\|\\frac{{\\hat P_{{{}}}(X)-Y}}{{Y}}\\|, \\bar S = {:.4f}$'.format(
            4,
            _df.iloc[:, 9].mean()
        )
    )
    plt.title(
        'Deltas of Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid()
    plt.legend()
    plt.show()


def plot_pearson_r_test(df: DataFrame) -> None:
    """
    Left-Side & Right-Side Rolling Means' Calculation & Plotting
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    """
    _pearson = DataFrame(columns=['right_to_left_ratio'])
    for _ in range(1 + df.shape[0] // 2):
        # =====================================================================
        # Shift Mean Values to Left
        # =====================================================================
        _l_frame = df.iloc[:, 0].rolling(1 + _).mean().shift(-_)
        # =====================================================================
        # Shift Mean Values to Right
        # =====================================================================
        _r_frame = df.iloc[:, 0].rolling(1 + _).mean()
        _pearson.loc[_] = [
            stats.pearsonr(df.iloc[:, 0][_r_frame.notna()], _r_frame.dropna(axis=0))[0] /
            stats.pearsonr(
                df.iloc[:, 0][_l_frame.notna()], _l_frame.dropna(axis=0))[0]
        ]
    # =========================================================================
    # Plot 'Window' to 'Right-Side to Left-Side Pearson R
    # =========================================================================
    plt.figure()
    plt.title('Right-Side to Left-Side Pearson R Ratio')
    plt.xlabel('Window')
    plt.ylabel('Index')
    plt.plot(_pearson, label='Right-Side to Left-Side Pearson R Ratio')
    plt.grid()
    plt.legend()
    plt.show()


def plot_filter_rolling_mean(df: DataFrame) -> None:
    """
    Rolling Mean Filter

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    Returns
    -------
    None
    """
    _df = df.copy()
    df_o, df_e, residuals_o, residuals_e = filter_rolling_mean(_df)
    plt.figure(1)
    plt.title(
        f'Rolling Mean {df_o.index[0]}$-${df_o.index[-1]}'
    )
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.scatter(
        df_o.iloc[:, [0]].index,
        df_o.iloc[:, [0]],
        label='Original Series'
    )
    plt.plot(
        df_o.iloc[:, 1:],
        label=['$\\hat Y_{{m = {}}}$'.format(int(_.split('_')[-1], 16))
               for _ in df_o.columns[1:]]
    )
    plt.plot(
        df_e,
        label=['$\\hat Y_{{m = {}}}$'.format(int(_.split('_')[-1], 16))
               for _ in df_e.columns]
    )
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.title(
        f'Rolling Mean Residuals {df_o.index[0]}$-${df_o.index[-1]}'
    )
    plt.xlabel('Period')
    plt.ylabel('Residuals ($\\delta$), Percent')
    plt.scatter(
        residuals_o.iloc[:, [0]].index,
        residuals_o.iloc[:, [0]],
        label='Residuals'
    )
    plt.plot(
        residuals_o.iloc[:, 1:],
        label=['$\\delta(\\hat Y_{{m = {}}})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_o.columns[1:]]
    )
    plt.plot(
        residuals_e,
        label=['$\\delta(\\hat Y_{{m = {}}})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_e.columns]
    )
    plt.grid()
    plt.legend()
    plt.show()


def plot_lab_cap_inty_lab_prty(df: DataFrame, params: tuple[float], option: str) -> None:
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      [Logarithm] Labor Capital Intensity
        df.iloc[:, 1]      [Logarithm] Labor Productivity
        df.iloc[:, 2]      [Logarithm] Labor Productivity : Estimate
        ================== =================================
    """
    MAP = {
        'Original': {
            1: {
                'title': r'$\mathbf{{Labor\ Capital\ Intensity}}$, $\mathbf{{Labor\ Productivity}}$ Relation, {}$-${}',
                'xlabel': 'Labor Capital Intensity',
                'ylabel': 'Labor Productivity',
            },
            2: {
                'label': r'$\frac{{Y}}{{Y_{{0}}}} = {:,.4f}\frac{{L}}{{L_{{0}}}}+{:,.4f}\frac{{C}}{{C_{{0}}}}$',
                'title': r'Model: $\hat Y = {:.4f}+{:.4f}\times X$, {}$-${}',
                'xlabel': 'Period',
                'ylabel': '$\\hat Y = Labor\ Productivity$, $X = Labor\ Capital\ Intensity$',
            },
            'params': params[::-1],
        },
        'Logarithm': {
            1: {
                'title': '$\\ln(Labor\ Capital\ Intensity), \\ln(Labor\ Productivity)$ Relation, {}$-${}',
                'xlabel': '$\\ln(Labor\ Capital\ Intensity)$',
                'ylabel': '$\\ln(Labor\ Productivity)$',
            },
            2: {
                'label': r'$\ln(\frac{{Y}}{{Y_{{0}}}}) = {:,.4f}+{:,.4f}\ln(\frac{{C}}{{C_{{0}}}})+{:,.4f}\ln(\frac{{L}}{{L_{{0}}}})$',
                'title': 'Model: $\\ln(\\hat Y) = {:.4f}+{:.4f}\\times \\ln(X)$, {}$-${}',
                'xlabel': 'Period',
                'ylabel': '$\\hat Y = \\ln(Labor\ Productivity)$, $X = \\ln(Labor\ Capital\ Intensity)$',
            },
            'params': tuple((*params[::-1], 1 - params[0])),
        }
    }
    plt.figure(1)
    plt.plot(
        df.iloc[:, 0],
        df.iloc[:, 1],
        label=option
    )
    plt.title(MAP[option][1]['title'].format(*df.index[[0, -1]]))
    plt.xlabel(MAP[option][1]['xlabel'])
    plt.ylabel(MAP[option][1]['ylabel'])
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.plot(
        df.iloc[:, 2],
        label=MAP[option][2]['label'].format(*MAP[option]['params'])
    )
    plt.title(MAP[option][2]['title'].format(
        *params[::-1], *df.index[[0, -1]]))
    plt.xlabel(MAP[option][2]['xlabel'])
    plt.ylabel(MAP[option][2]['ylabel'])
    plt.grid()
    plt.legend()
    plt.show()


def plot_turnover(df: DataFrame) -> None:
    """Static Fixed Assets Turnover Approximation
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Fixed Assets Turnover
        ================== =================================
    """
    # =========================================================================
    # Linear: Fixed Assets Turnover
    # =========================================================================
    polyfit_linear = np.polyfit(
        df.index.to_series().astype(float),
        df.iloc[:, -1].astype(float),
        deg=1
    )
    # =========================================================================
    # Exponential: Fixed Assets Turnover
    # =========================================================================
    _exp = np.polyfit(
        df.index.to_series().astype(float),
        np.log(df.iloc[:, -1].astype(float)),
        deg=1
    )
    df['c_turnover_lin'] = np.poly1d(polyfit_linear)(df.index.to_series())
    df['c_turnover_exp'] = np.exp(np.poly1d(_exp)(df.index.to_series().astype(float)))
    # =========================================================================
    # Deltas
    # =========================================================================
    df['d_lin'] = df.iloc[:, -2].div(df.iloc[:, -3]).sub(1).abs()
    df['d_exp'] = df.iloc[:, -2].div(df.iloc[:, -4]).sub(1).abs()
    plt.figure(1)
    plt.plot(df.iloc[:, 2], df.iloc[:, 0])
    plt.title(
        'Fixed Assets Volume to Fixed Assets Turnover, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Fixed Assets Turnover')
    plt.ylabel('Fixed Assets Volume')
    plt.grid()
    plt.figure(2)
    plt.scatter(
        df.index,
        df.iloc[:, -5],
        label='Fixed Assets Turnover'
    )
    plt.plot(
        df.iloc[:, [-4]],
        label='$\\hat K_{{l}} = {:.2f} {:.2f} t, R^2 = {:.4f}$'.format(
            *polyfit_linear[::-1],
            r2_score(df.iloc[:, -5], df.iloc[:, -4])
        )
    )
    plt.plot(
        df.iloc[:, [-3]],
        label='$\\hat K_{{e}} = \\exp ({:.2f} {:.2f} t), R^2 = {:.4f}$'.format(
            *_exp[::-1],
            r2_score(df.iloc[:, -5], df.iloc[:, -3])
        )
    )
    plt.title(
        'Fixed Assets Turnover Approximation, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.figure(3)
    plt.plot(
        df.iloc[:, [-2]],
        ':',
        label='$\\|\\frac{{\\hat K_{{l}}-K}}{{K}}\\|, \\bar S = {:.4%}$'.format(
            df.iloc[:, -2].mean()
        )
    )
    plt.plot(
        df.iloc[:, [-1]],
        ':',
        label='$\\|\\frac{{\\hat K_{{e}}-K}}{{K}}\\|, \\bar S = {:.4%}$'.format(
            df.iloc[:, -1].mean()
        )
    )
    plt.title(
        'Deltas of Fixed Assets Turnover Approximation, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid()
    plt.legend()
    plt.show()


def plot_usa_nber(df_sic: DataFrame, df_naics: DataFrame, agg: str) -> None:
    """Project V: USA NBER Data Plotting"""
    for _, (sic_id, naics_id) in enumerate(zip(df_sic.columns, df_naics.columns)):
        # =====================================================================
        # Ensures Columns in Two DataFrames Are in the Same Ordering
        # =====================================================================
        series_id = tuple(set((sic_id, naics_id)))
        plt.plot(df_sic.iloc[:, _], label='sic_{}'.format(*series_id))
        plt.plot(df_naics.iloc[:, _], label='naics_{}'.format(*series_id))
        plt.title('NBER CES: {} {}'.format(*series_id, agg))
        plt.xlabel('Period')
        plt.ylabel('Dimension')
        plt.grid()
        plt.legend()
        plt.show()


def plot_usa_nber_showcase() -> None:
    FILEPATH_OR_BUFFER = (
        'dataset_usa_nber_ces_mid_sic5811.csv',
        'dataset_usa_nber_ces_mid_naics5811.csv',
    )
    aggs = ('mean', 'sum')
    for agg in aggs:
        sic = read_usa_nber(FILEPATH_OR_BUFFER[0]).pipe(transform_agg, agg=agg)
        naics = read_usa_nber(FILEPATH_OR_BUFFER[1]).pipe(
            transform_agg, agg=agg)
        plot_usa_nber(sic, naics, agg)


def plot_capital_acquisition(df: DataFrame) -> None:
    """
    Interactive Shell for Processing Capital Acquisitions

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal Investment
        df.iloc[:, 1]      Nominal Production
        df.iloc[:, 2]      Real Production
        df.iloc[:, 3]      Maximum Real Production
        df.iloc[:, 4]      Nominal Capital
        df.iloc[:, 5]      Labor
        ================== =================================

    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.

    """
    _df = df.copy()
    _df.reset_index(level=0, inplace=True)
    _df.columns = ('period', *_df.columns[1:])
    # =========================================================================
    # Basic Year
    # =========================================================================
    _b = _df.pipe(get_price_base_nr, columns=(2, 3))
    _df.drop(_df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    _df['c_turnover'] = _df.iloc[:, 3].div(_df.iloc[:, 5])
    # =========================================================================
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I_0/Y_0)
    # =========================================================================
    _df['inv_to_gdp'] = _df.iloc[:, 1].div(_df.iloc[:, 3])
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    _df['lab_cap_int'] = _df.iloc[:, 5].div(_df.iloc[:, 6])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    _df['lab_product'] = _df.iloc[:, 3].div(_df.iloc[:, 6])
    _df.iloc[:, -3:] = _df.iloc[:, -3:].div(_df.iloc[0, -3:])
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    # =========================================================================
    _df[f'{_df.columns[-2]}_log_bas'] = np.log(_df.iloc[:, -2].astype(float))
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    # =========================================================================
    _df[f'{_df.columns[-2]}_log_bas'] = np.log(_df.iloc[:, -2].astype(float))
    # =========================================================================
    # Max: Fixed Assets Turnover Ratio
    # =========================================================================
    _df[f'{_df.columns[-6]}_max'] = _df.iloc[:, 4].div(_df.iloc[:, 5])
    # =========================================================================
    # Max: Investment to Gross Domestic Product Ratio
    # =========================================================================
    _df[f'{_df.columns[-6]}_max'] = _df.iloc[:, 1].div(_df.iloc[:, 4])
    # =========================================================================
    # Max: Labor Productivity
    # =========================================================================
    _df[f'{_df.columns[-5]}_max'] = _df.iloc[:, 4].div(_df.iloc[:, 6])
    _df.iloc[:, -2:] = _df.iloc[:, -2:].div(_df.iloc[0, -2:])
    # =========================================================================
    # Max: Log Labor Productivity
    # =========================================================================
    _df[f'{_df.columns[-1]}_log_bas'] = np.log(_df.iloc[:, -1].astype(float))
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Line Spans for Pi (N, N >= 1): '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 1, f'N >= 1 is Required, N = {N} Was Provided'
    # =========================================================================
    # Pi & Pi Switch Points
    # =========================================================================
    pi, _knots = [], [0, ]
    _ = 0
    if N == 1:
        _knots.append(_df.index[-1])
        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
            _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _] - 1, 0]))))
    elif N >= 2:
        while _ < N:
            if 1 + _ == N:
                _knots.append(_df.index[-1])
                pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _] - 1, 0]))))
            else:
                _knot = int(input('Select Row for Year, Should Be More Than {}: = {}: '.format(
                    0, _df.iloc[0, 0])))
                if _knot > _knots[_]:
                    _knots.append(_knot)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
            _ += 1
    else:
        print("Error")
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    _calculated = [np.nan, ]
    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1 + j]):
            # =================================================================
            # Estimate: GCF[-] or CA[+]
            # =================================================================
            _calculated.append(
                _df.iloc[1 + i, 5] - _df.iloc[i, 5] + pi[j]*_df.iloc[1 + i, 1]
            )
    else:
        for j in range(N):
            if 1 + j == N:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================
                    _calculated.append(
                        _df.iloc[1 + i, 5] - _df.iloc[i, 5] +
                        pi[j]*_df.iloc[1 + i, 1]
                    )
            else:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================
                    _calculated.append(
                        _df.iloc[1 + i, 5] - _df.iloc[i, 5] +
                        pi[j]*_df.iloc[1 + i, 1]
                    )
    _df = pd.concat(
        [
            _df,
            DataFrame(_calculated, columns=['_calculated'])
        ],
        axis=1)
    _df.set_index(_df.columns[0], inplace=True)
    # =========================================================================
    # {
    #     '-': 'Gross Capital Formation',
    #     '+': 'Capital Acquisitions'
    # }
    # =========================================================================
    for _ in range(N):
        if 1 + _ == N:
            print(
                f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _] - 1]}: {pi[_]:.6f}'
            )
            continue
        print(
            f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _]]}: {pi[_]:.6f}'
        )
    plt.figure(1)
    plt.plot(_df.iloc[:, 8], _df.iloc[:, 9])
    plt.plot(_df.iloc[:, 8], _df.iloc[:, 14])
    plt.title(
        'Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel(f'Labor Productivity, {_b}=100')
    plt.grid()
    plt.figure(2)
    plt.plot(_df.iloc[:, 10], _df.iloc[:, 11])
    plt.plot(_df.iloc[:, 10], _df.iloc[:, 15])
    plt.title(
        'Log Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Log Labor Capital Intensity')
    plt.ylabel(f'Log Labor Productivity, {_b}=100')
    plt.grid()
    plt.figure(3)
    plt.plot(_df.iloc[:, 6])
    plt.plot(_df.iloc[:, 12])
    plt.title(
        'Fixed Assets Turnover ($\\lambda$), Observed & Max, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover ($\\lambda$), {_b}=100')
    plt.grid()
    plt.figure(4)
    plt.plot(_df.iloc[:, 7])
    plt.plot(_df.iloc[:, 13])
    plt.title(
        'Investment to Gross Domestic Product Ratio,\nObserved & Max, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(
        f'Investment to Gross Domestic Product Ratio, {_b}=100')
    plt.grid()
    plt.figure(5)
    plt.plot(_df.iloc[:, 16])
    plt.title(
        'Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'GCF or CA, {_b}=100')
    plt.grid()
    plt.show()


def plot_capital_retirement(df: DataFrame) -> None:
    """
    Interactive Shell for Processing Capital Retirement

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal Investment
        df.iloc[:, 1]      Nominal Production
        df.iloc[:, 2]      Real Production
        df.iloc[:, 3]      Nominal Capital
        df.iloc[:, 4]      Labor
        ================== =================================

    Returns
    -------
    None
        Draws matplotlib.pyplot Plots.

    """
    _df = df.copy()
    _df.reset_index(level=0, inplace=True)
    _df.columns = ('period', *_df.columns[1:])
    # =========================================================================
    # Define Basic Year for Deflator
    # =========================================================================
    # =========================================================================
    # Basic Year
    # =========================================================================
    _b = _df.pipe(get_price_base_nr, columns=(2, 3))
    _df.drop(_df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    _df['lab_cap_int_log_bas'] = _df.iloc[:, 4].div(_df.iloc[:, 5])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    _df['lab_product_log_bas'] = _df.iloc[:, 3].div(_df.iloc[:, 5])
    # =========================================================================
    # Investment to Gross Domestic Product Ratio
    # =========================================================================
    _df['inv_to_gdp'] = _df.iloc[:, 1].div(_df.iloc[:, 3])
    # =========================================================================
    # Basing
    # =========================================================================
    _df.iloc[:, -3:] = _df.iloc[:, -3:].div(_df.iloc[0, -3:])
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K_0/L_0))
    # =========================================================================
    _df.iloc[:, -3] = np.log(_df.iloc[:, -3].astype(float))
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y_0/L_0))
    # =========================================================================
    _df.iloc[:, -2] = np.log(_df.iloc[:, -2].astype(float))
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    _df['c_turnover'] = _df.iloc[:, 3].div(_df.iloc[:, 4])
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Line Segments for Pi: '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 1, f'N >= 1 is Required, N = {N} Was Provided'
    # =========================================================================
    # Pi & Pi Switch Points
    # =========================================================================
    pi, _knots = [], [0, ]
    _ = 0
    if N == 1:
        _knots.append(_df.index[-1])
        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
            _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
    elif N >= 2:
        while _ < N:
            if 1 + _ == N:
                _knots.append(_df.index[-1])
                pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                    _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
            else:
                _knot = int(input('Select Row for Year: '))
                if _knot > _knots[_]:
                    _knots.append(_knot)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        _df.iloc[_knots[_], 0], _df.iloc[_knots[1 + _], 0]))))
            _ += 1
    else:
        print("Error")
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    # =========================================================================
    # Fixed Assets Retirement Value
    # =========================================================================
    _value = [np.nan, ]
    # =========================================================================
    # Fixed Assets Retirement Ratio
    # =========================================================================
    _ratio = [np.nan, ]
    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1 + j]):
            # =================================================================
            # Fixed Assets Retirement Value
            # =================================================================
            _value.append(
                _df.iloc[i, 4] - _df.iloc[1 + i, 4] + pi[j]*_df.iloc[i, 1]
            )
            # =================================================================
            # Fixed Assets Retirement Ratio
            # =================================================================
            _ratio.append(
                (_df.iloc[i, 4] - _df.iloc[1 + i, 4] + pi[j]
                 * _df.iloc[i, 1]) / _df.iloc[1 + i, 4]
            )
    else:
        for j in range(N):
            if 1 + j == N:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Fixed Assets Retirement Value
                    # =========================================================
                    _value.append(
                        _df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                        pi[j]*_df.iloc[i, 1]
                    )
                    # =========================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================
                    _ratio.append(
                        (_df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                         pi[j]*_df.iloc[i, 1]) / _df.iloc[1 + i, 4]
                    )
            else:
                for i in range(_knots[j], _knots[1 + j]):
                    # =========================================================
                    # Fixed Assets Retirement Value
                    # =========================================================
                    _value.append(
                        _df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                        pi[j]*_df.iloc[i, 1]
                    )
                    # =========================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================
                    _ratio.append(
                        (_df.iloc[i, 4] - _df.iloc[1 + i, 4] +
                         pi[j]*_df.iloc[i, 1]) / _df.iloc[1 + i, 4]
                    )
    _df = pd.concat(
        [
            _df,
            DataFrame(_value, columns=['_value']),
            DataFrame(_ratio, columns=['_ratio'])
        ],
        axis=1
    )
    _df.set_index(_df.columns[0], inplace=True)
    _df['_ratio_deviation_abs'] = _df.iloc[:, 10].sub(
        _df.iloc[:, 10].mean()).abs()
    _df['_ratio_increment_abs'] = _df.iloc[:, 10].diff().abs()
    for _ in range(N):
        if 1 + _ == N:
            print(
                f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _] - 1]}: {pi[_]:.6f}'
            )
            continue
        print(
            f'Model Parameter: Pi for Period from {_df.index[_knots[_]]} to {_df.index[_knots[1 + _]]}: {pi[_]:.6f}'
        )
    plt.figure(1)
    plt.title('Product, {}=100, {}$-${}'.format(_b, *df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel(f'Product, {_b}=100')
    plt.plot(_df.iloc[:, 2])
    plt.grid()
    plt.figure(2)
    plt.title('Capital, {}=100, {}$-${}'.format(_b, *df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel(f'Capital, {_b}=100')
    plt.plot(_df.iloc[:, 3])
    plt.grid()
    plt.figure(3)
    plt.title(
        'Fixed Assets Turnover ($\\lambda$), {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover ($\\lambda$), {_b}=100')
    plt.plot(_df.iloc[:, 2].div(_df.iloc[:, 3]))
    plt.grid()
    plt.figure(4)
    plt.title(
        'Investment to Gross Domestic Product Ratio, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(
        f'Investment to Gross Domestic Product Ratio, {_b}=100'
    )
    plt.plot(_df.iloc[:, 7])
    plt.grid()
    plt.figure(5)
    plt.title(
        '$\\alpha(t)$, Fixed Assets Retirement Ratio, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel(f'$\\alpha(t)$, {_b}=100')
    plt.plot(_df.iloc[:, 9])
    plt.grid()
    plt.figure(6)
    plt.title(
        'Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {}=100, {}$-${}'.format(
            _b, *df.index[[0, -1]]
        )
    )
    plt.xlabel(f'$\\alpha(t)$, {_b}=100')
    plt.ylabel(f'Fixed Assets Retirement Value, {_b}=100')
    plt.plot(_df.iloc[:, 9], _df.iloc[:, 8])
    plt.grid()
    plt.figure(7)
    plt.title(
        'Labor Capital Intensity, {}=100, {}$-${}'.format(_b, *df.index[[0, -1]]))
    plt.xlabel(f'Labor Capital Intensity, {_b}=100')
    plt.ylabel(f'Labor Productivity, {_b}=100')
    plt.plot(np.exp(_df.iloc[:, 5]), np.exp(_df.iloc[:, 6]))
    plt.grid()
    plt.show()
