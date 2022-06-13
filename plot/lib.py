#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 08:59:10 2022

@author: alexander
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from toolkit.lib import rolling_mean_filter
from extract.lib import extract_usa_census_description
from extract.lib import extract_usa_census


ARCHIVE_NAMES_UTILISED = (
    'CHN_TUR_GDP.zip',
    'dataset_rus_m1.zip',
    'dataset_usa_census1975.zip',
)
FILE_NAMES_UTILISED = (
    'datasetAutocorrelation.txt',
    'dataset_rus_grigoriev_v.csv',
    'dataset_usa_nber_ces_mid_naics5811.csv',
    'dataset_usa_nber_ces_mid_sic5811.csv',
)


def plot_a(df: DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Gross Domestic Investment
    df.iloc[:, 1]      National Income
    df.iloc[:, 2]      Nominal Gross Domestic Product
    df.iloc[:, 3]      Real Gross Domestic Product
    ================== =================================
    '''
    _df = df.copy()
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    _df['inv'] = _df.iloc[:, 0].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    # =========================================================================
    # `Real` Production
    # =========================================================================
    _df['prd'] = _df.iloc[:, 1].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    _df['inv_roll_mean'] = _df.iloc[:, -2].rolling(2).mean()
    _df['prd_roll_mean'] = _df.iloc[:, -2].rolling(2).mean()
    plt.figure()
    plt.title(
        'Gross Private Domestic Investment & National Income, {}$-${}'.format(
            *_df.index[[0, -1]]
        )
    )
    plt.plot(_df.iloc[:, -4:-2], label=[
        'Gross Private Domestic Investment',
        'National Income',
    ])
    plt.xlabel('Period')
    plt.ylabel('Index')
    _df.index = _df.index.to_series().rolling(2).mean()
    plt.plot(
        _df.index, _df.iloc[:, -2], '--',
        _df.index, _df.iloc[:, -1], '--'
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_b(df: DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Gross Domestic Investment
    df.iloc[:, 1]      Nominal Gross Domestic Product
    df.iloc[:, 2]      Real Gross Domestic Product
    df.iloc[:, 3]      Prime Rate
    ================== =================================
    '''
    _df = df.copy()
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    _df['inv'] = _df.iloc[:, 0].mul(_df.iloc[:, 2]).div(_df.iloc[:, 1])
    plt.figure()
    plt.plot(_df.iloc[:, 3], _df.iloc[:, -1])
    plt.title(
        'Gross Private Domestic Investment, A006RC, {}$-${}'.format(
            *_df.index[[0, -1]]
        )
    )
    plt.xlabel('Percentage')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.show()


def plot_c(df: DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Gross Domestic Investment
    df.iloc[:, 1]      Nominal Gross Domestic Product
    df.iloc[:, 2]      Real Gross Domestic Product
    df.iloc[:, 3]      M1
    ================== =================================
    '''
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    df['inv'] = df.iloc[:, 0].mul(df.iloc[:, 2]).div(df.iloc[:, 1])
    plt.figure()
    plt.plot(df.iloc[:, range(2, 5)], label=[
        'Real Gross Domestic Product',
        'Money Supply',
        '`Real` Gross Domestic Investment',
    ])
    plt.title('Indexes, {}$-${}'.format(*df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_d(df: DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Gross Domestic Investment
    df.iloc[:, 1]      Gross Domestic Investment Price Index
    df.iloc[:, 2]      Fixed Investment
    df.iloc[:, 3]      Fixed Investment Price Index
    df.iloc[:, 4]      Real Gross Domestic Product
    ================== =================================
    '''
    # =========================================================================
    # Basic Year
    # =========================================================================
    df['__deflator'] = df.iloc[:, 1].sub(100).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Convert to Billions
    # =========================================================================
    df.iloc[:, -1] = df.iloc[:, -1].div(1000)
    # =========================================================================
    # Real Investment, Billions
    # =========================================================================
    df['invmnt'] = df.iloc[:, 1].mul(df.iloc[_b, 0]).div(100).div(1000)
    # =========================================================================
    # Real Fixed Investment, Billions
    # =========================================================================
    df['fxd_invmnt'] = df.iloc[:, 3].mul(df.iloc[_b, 2]).div(100).div(1000)
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
    plt.title('Real Indexes, {}=100, {}$-${}'.format(*df.index[[_b, 0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(df.iloc[:, 4])
    plt.title(
        'Real Gross Domestic Product $GDP$, {}=100, {}$-${}'.format(*df.index[[_b, 0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(3)
    plt.plot(df.iloc[:, -2], df.iloc[:, 4])
    plt.title(
        '$GPDI$ & $GPFI(n)$, {}=100, {}$-${}'.format(*df.index[[_b, 0, -1]]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(4)
    plt.plot(df.iloc[:, -1], df.iloc[:, 4])
    plt.title(
        '$GPFI(n)$ & $GDP$, {}=100, {}$-${}'.format(*df.index[[_b, 0, -1]]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.show()


def plot_e(df: DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Investment
    df.iloc[:, 1]      Production
    df.iloc[:, 2]      Capital
    ================== =================================
    '''
    # =========================================================================
    # Investment to Production Ratio
    # =========================================================================
    df['inv_to_pro'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 1].div(df.iloc[:, 2])
    _params_i = np.polyfit(
        df.iloc[:, 0],
        df.iloc[:, 1],
        deg=1
    )
    _params_t = np.polyfit(
        df.iloc[:, 1].astype(float),
        df.iloc[:, 2].astype(float),
        deg=1
    )
    df['inv_to_pro_lin'] = df.iloc[:, 0].mul(_params_i[0]).add(_params_i[1])
    df['c_turnover_lin'] = df.iloc[:, 2].mul(_params_t[0]).add(_params_t[1])
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
    plt.grid(True)
    plt.legend(
        [
            '$P(I)$',
            '$\\hat{{P(I)}} = {:.4f}+{:.4f} I$'.format(*_params_i[::-1])
        ]
    )
    print(df.iloc[:, 3].describe())
    print(_params_i)
    print(df.iloc[:, 4].describe())
    print(_params_t)
    plt.show()


def plot_census_a(df: DataFrame, base: int) -> None:
    plt.figure()
    plt.plot(df.iloc[:, [0, 2]], label=[
        'Fabricant S., Shiskin J., NBER',
        'E. Frickey',
    ])
    plt.plot(df.iloc[:, 1], color='red', linewidth=4, label='W.M. Persons')
    plt.axvline(x=df.index[base], linestyle=':')
    plt.title(
        'US Manufacturing Indexes Of Physical Production Of Manufacturing, {}=100, {}$-${}'.format(
            df.index[base], *df.index[[0, -1]])
    )
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_b_capital(df: DataFrame) -> None:
    '''Census Manufacturing Fixed Assets Series'''
    plt.figure()
    plt.semilogy(df, label=['Total', 'Structures', 'Equipment'])
    plt.title('Census Manufacturing Fixed Assets, {}$-${}'.format(
        *df.index[[0, -1]]
    ))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_b_deflator(df: DataFrame) -> None:
    '''Census Manufacturing Fixed Assets Deflator Series'''
    plt.figure()
    plt.plot(df)
    plt.title('Census Fused Fixed Assets Deflator, {}$-${}'.format(
        *df.index[[0, -1]])
    )
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.show()


def plot_census_c(df: DataFrame, base: tuple[int]) -> None:
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
    _DESCS = [_desc.format(_b) for _desc, _b in zip(_DESCS_RAW, base)]
    _MAPPING = dict(zip(df.columns, _DESCS))
    _COLUMN_LOCS = [_ for _ in range(df.shape[1]) if _ not in range(1, 6)]
    plt.figure(1)
    plt.semilogy(
        df.iloc[:, range(1, 6)],
        label=[_MAPPING[_] for _ in df.columns[range(1, 6)]]
    )
    for _ in range(1, 6):
        plt.axvline(x=base[_], linestyle=':')
    plt.title('Steel Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.semilogy(
        df.iloc[:, _COLUMN_LOCS],
        label=[_MAPPING[_] for _ in df.columns[_COLUMN_LOCS]]
    )
    for _ in _COLUMN_LOCS:
        plt.axvline(x=base[_], linestyle=':')
    plt.title('Rails & Cars Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_d(series_ids: tuple[str]) -> None:
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    df = DataFrame()
    for series_id in series_ids:
        title = extract_usa_census_description(ARCHIVE_NAME, series_id)
        print(f'<{series_id}> {title}')
        chunk = extract_usa_census(ARCHIVE_NAME, series_id)
        df = pd.concat(
            [
                df,
                chunk.div(chunk.iloc[0, :]).mul(100)
            ],
            axis=1, sort=True)
    _title = 'Series P 231$-$300. Physical Output of Selected Manufactured Commodities: {}$-${}'.format(
        *df.index[[0, -1]]
    )
    plt.figure()
    plt.semilogy(df)
    plt.title(_title)
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend(series_ids)
    plt.show()


def plot_census_e(df: DataFrame) -> None:
    plt.figure()
    plt.plot(df)
    plt.title('Total Immigration, {}$-${}'.format(*df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('People')
    plt.grid(True)
    plt.show()


def plot_census_f_a(df: DataFrame) -> None:
    plt.figure(1)
    plt.plot(df.iloc[:, 1])
    plt.title('Unemployment, Percent of Civilian Labor Force')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.figure(2)
    plt.plot(df.iloc[:, [2, 3]], label=['Bureau of Labour', 'Wolman'])
    plt.title('All Manufacturing, Average Full-Time Weekly Hours, 1890-1899=100')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.plot(df.iloc[:, 6])
    plt.title('Implicit Number of Workers')
    plt.xlabel('Period')
    plt.ylabel('Persons')
    plt.grid(True)
    plt.show()


def plot_census_f_b(df: DataFrame) -> None:
    fig, _axs_stoppages = plt.subplots()
    color = 'tab:red'
    _axs_stoppages.set_xlabel('Period')
    _axs_stoppages.set_ylabel('Number', color=color)
    _axs_stoppages.plot(df.iloc[:, 4], color=color, label='Stoppages')
    _axs_stoppages.set_title('Work Conflicts')
    _axs_stoppages.grid(True)
    _axs_stoppages.legend(loc=2)
    _axs_stoppages.tick_params(axis='y', labelcolor=color)
    _axs_workers = _axs_stoppages.twinx()
    color = 'tab:blue'
    _axs_workers.set_ylabel('1,000 People', color=color)
    _axs_workers.plot(df.iloc[:, 5], color=color, label='Workers Involved')
    _axs_workers.legend(loc=1)
    _axs_workers.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()
    plt.show()


def plot_census_g(df: DataFrame) -> None:
    plt.figure()
    plt.plot(df, label=[
        'Gross National Product',
        'Gross National Product Per Capita',
    ])
    plt.title(
        'Gross National Product, Prices {}=100, {}=100'.format(
            1958, df.index[0]
        ))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_h() -> None:
    '''Census 1975, Land in Farms'''
    _kwargs = {
        'archive_name': 'dataset_usa_census1975.zip',
        'series_id': 'K0005',
    }
    plt.figure()
    plt.plot(extract_usa_census(**_kwargs))
    plt.title('Land in Farms')
    plt.xlabel('Period')
    plt.ylabel('1,000 acres')
    plt.grid(True)
    plt.show()


def plot_census_i_a(df: DataFrame) -> None:
    plt.figure()
    plt.plot(df, label=[
        'Exports, U1',
        'Imports, U8',
        'Net Exports, U15',
    ])
    plt.title(
        'Exports & Imports of Goods and Services, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_i_b(df: DataFrame) -> None:
    plt.figure()
    plt.plot(df, label=[
        'Exports, U187',
        'Imports, U188',
        'Net Exports, U189',
    ])
    plt.title(
        'Total Merchandise, Gold and Silver, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_i_c(df: DataFrame) -> None:
    assert df.shape[1] == 58, 'Works on DataFrame Produced with `get_data_census_i_c()`'
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
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.semilogy(df.iloc[:, -len(_LABELS):], label=_LABELS)
    plt.title('Net Exports by Regions to Overall Net Exports')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_j(df: DataFrame) -> None:
    YEAR_BASE = 1915
    plt.figure()
    plt.semilogy(
        df,
        label=[
            'Currency Held by the Public',
            'M1 Money Supply (Currency Plus Demand Deposits)',
            'M2 Money Supply (M1 Plus Time Deposits)',
        ]
    )
    plt.axvline(x=YEAR_BASE, linestyle=':')
    plt.title('Currency Dynamics, {}=100'.format(YEAR_BASE))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_k() -> None:
    '''Census Financial Markets & Institutions Series'''
    ARCHIVE_NAME = 'dataset_usa_census1975.zip'
    SERIES_IDS = (
        'X0410', 'X0411', 'X0412', 'X0413', 'X0414', 'X0415', 'X0416',
        'X0417', 'X0418', 'X0419', 'X0420', 'X0421', 'X0422', 'X0423',
        'X0580', 'X0581', 'X0582', 'X0583', 'X0584', 'X0585', 'X0586',
        'X0587', 'X0610', 'X0611', 'X0612', 'X0613', 'X0614', 'X0615',
        'X0616', 'X0617', 'X0618', 'X0619', 'X0620', 'X0621', 'X0622',
        'X0623', 'X0624', 'X0625', 'X0626', 'X0627', 'X0628', 'X0629',
        'X0630', 'X0631', 'X0632', 'X0633', 'X0741', 'X0742', 'X0743',
        'X0744', 'X0745', 'X0746', 'X0747', 'X0748', 'X0749', 'X0750',
        'X0751', 'X0752', 'X0753', 'X0754', 'X0755', 'X0879', 'X0880',
        'X0881', 'X0882', 'X0883', 'X0884', 'X0885', 'X0886', 'X0887',
        'X0888', 'X0889', 'X0890', 'X0891', 'X0892', 'X0893', 'X0894',
        'X0895', 'X0896', 'X0897', 'X0898', 'X0899', 'X0900', 'X0901',
        'X0902', 'X0903', 'X0904', 'X0905', 'X0906', 'X0907', 'X0908',
        'X0909', 'X0910', 'X0911', 'X0912', 'X0913', 'X0914', 'X0915',
        'X0916', 'X0917', 'X0918', 'X0919', 'X0920', 'X0921', 'X0922',
        'X0923', 'X0924', 'X0925', 'X0926', 'X0927', 'X0928', 'X0929',
        'X0930', 'X0931', 'X0932', 'X0947', 'X0948', 'X0949', 'X0950',
        'X0951', 'X0952', 'X0953', 'X0954', 'X0955', 'X0956',
    )
    for _, series_id in enumerate(SERIES_IDS, start=1):
        df = extract_usa_census(ARCHIVE_NAME, series_id)
        df = df.div(df.iloc[0, :]).mul(100)
        _title = extract_usa_census_description(ARCHIVE_NAME, series_id)
        plt.figure(_)
        plt.plot(df, label=series_id)
        plt.title('{}, {}$-${}'.format(_title, *df.index[[0, -1]]))
        plt.xlabel('Period')
        plt.ylabel('Percentage')
        plt.grid(True)
        plt.legend()
        plt.show()


def plot_approx_linear(df: DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Real Values for Price Deflator
    df.iloc[:, 1]      Nominal Values for Price Deflator
    df.iloc[:, 2]      Regressor
    df.iloc[:, 3]      Regressand
    ================== =================================
    '''
    df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1], errors='coerce')
    df.dropna(inplace=True)
    # =========================================================================
    # TODO: Separate Basic Year Function
    # =========================================================================
    df['__deflator'] = df.iloc[:, 0].div(df.iloc[:, 1]).sub(1).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Deflator
    # =========================================================================
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df[f'{df.columns[2]}_bas'] = df.iloc[:, 2].mul(df.iloc[:, 4]).div(
        df.iloc[0, 2]).div(df.iloc[0, 4]).astype(float)
    df[f'{df.columns[3]}_bas'] = df.iloc[:, 3].mul(df.iloc[:, 4]).div(
        df.iloc[0, 3]).div(df.iloc[0, 4]).astype(float)
    _p1 = np.polyfit(
        df.iloc[:, -2],
        df.iloc[:, -1],
        deg=1
    )
    # =========================================================================
    # Yhat
    # =========================================================================
    df[f'{df.columns[3]}_estimate'] = df.iloc[:, -2].mul(_p1[0]).add(_p1[1])
    print('Period From: {} Through: {}'.format(*df.index[[0, -1]]))
    print('Prices: {}=100'.format(df.index[_b]))
    print('Model: Yhat = {:.4f} + {:.4f}*X'.format(*_p1[::-1]))
    print('Model Parameter: A_0 = {:.4f}'.format(_p1[1]))
    print('Model Parameter: A_1 = {:.4f}'.format(_p1[0]))
    plt.figure()
    plt.title('$Y(X)$, {}=100, {}$-${}'.format(*df.index[[_b, 0, -1]]))
    plt.xlabel(
        'Gross Private Domestic Investment, $X(\\tau)$, {}=100, {}=100'.format(
            *df.index[[_b, 0]]
        )
    )
    plt.ylabel(
        'Gross Domestic Product, $Y(\\tau)$, {}=100, {}=100'.format(
            *df.index[[_b, 0]]
        )
    )
    plt.plot(df.iloc[:, -3], df.iloc[:, -2])
    plt.plot(
        df.iloc[:, -3], df.iloc[:, -1],
        label='$\\hat Y = {:.4f}+{:.4f}X$'.format(*_p1[::-1])
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_approx_log_linear(df: DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Real Values for Price Deflator
    df.iloc[:, 1]      Nominal Values for Price Deflator
    df.iloc[:, 2]      Regressor
    df.iloc[:, 3]      Regressand
    ================== =================================
    '''
    MAP_DESC = {
        'A032RC1': 'National Income',
        'A191RC1': 'Gross Domestic Product',
    }
    df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1], errors='coerce')
    df.dropna(inplace=True)
    # =========================================================================
    # TODO: Separate Basic Year Function
    # =========================================================================
    df['__deflator'] = df.iloc[:, 0].div(df.iloc[:, 1]).sub(1).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    # =========================================================================
    # Deflator
    # =========================================================================
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df[f'{df.columns[2]}_log_bas'] = np.log(df.iloc[:, 2].div(df.iloc[0, 2]))
    df[f'{df.columns[3]}_log_bas'] = np.log(df.iloc[:, 3].mul(df.iloc[:, 4]).div(
        df.iloc[0, 3]).div(df.iloc[0, 4]).astype(float))
    _p1 = np.polyfit(
        df.iloc[:, -2],
        df.iloc[:, -1],
        deg=1
    )
    # =========================================================================
    # Yhat
    # =========================================================================
    df[f'{df.columns[3]}_estimate'] = df.iloc[:, -2].mul(_p1[0]).add(_p1[1])
    # =========================================================================
    # Delivery Block
    # =========================================================================
    print('Period From: {} Through: {}'.format(*df.index[[0, -1]]))
    print('Prices: {}=100'.format(df.index[_b]))
    print('Model: Yhat = {:.4f} + {:.4f}*Ln(X)'.format(*_p1[::-1]))
    print('Model Parameter: A_0 = {:.4f}'.format(_p1[1]))
    print('Model Parameter: A_1 = {:.4f}'.format(_p1[0]))
    plt.figure()
    plt.title(
        '$Y(X)$, {}=100, {}$-${}'.format(
            *df.index[[_b, 0, -1]]
        )
    )
    plt.xlabel('Logarithm Prime Rate, $X(\\tau)$, {}=100'.format(df.index[0]))
    plt.ylabel(
        'Logarithm {}, $Y(\\tau)$, {}=100, {}=100'.format(
            MAP_DESC[df.columns[3]], *df.index[[_b, 0]]
        )
    )
    plt.plot(df.iloc[:, -3], df.iloc[:, -2])
    plt.plot(
        df.iloc[:, -3], df.iloc[:, -1],
        label='$\\hat Y = {:.4f}+{:.4f}X$'.format(*_p1[::-1])
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_block_zer(df: DataFrame) -> None:
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
    df['log_lab_c'] = np.log(df.iloc[:, 0].div(df.iloc[:, 1]))
    df['log_lab_p'] = np.log(df.iloc[:, 2].div(df.iloc[:, 1]))
    plot_simple_linear(
        *simple_linear_regression(df.iloc[:, [3, 4]])
    )
    plot_simple_log(
        *simple_linear_regression(df.iloc[:, [5, 6]])
    )


def plot_block_one(df: DataFrame) -> None:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # TODO: Increase Cohesion
    # =========================================================================
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Valid Only for _k = 2
    # =========================================================================
    _k = 2
    # =========================================================================
    # Odd Frame
    # =========================================================================
    data_frame_o = pd.concat(
        [
            df.iloc[:, [-1]],
            rolling_mean_filter(df.iloc[:, [-1]], _k)[0].iloc[:, [-1]],
            kol_zur_filter(df.iloc[:, [-1]], _k)[0].iloc[:, [-1]],
            df.iloc[:, [-1]].ewm(alpha=0.25, adjust=False).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # Even Frame
    # =========================================================================
    data_frame_e = pd.concat(
        [
            rolling_mean_filter(df.iloc[:, [-1]], _k)[1].iloc[:, [-1]],
            kol_zur_filter(df.iloc[:, [-1]], _k)[1].iloc[:, [-1]],
        ],
        axis=1,
    )
    plt.figure()
    plt.plot(
        data_frame_o.iloc[:, 0],
        linewidth=3,
        label='Labor Capital Intensity'
    )
    plt.plot(
        data_frame_o.iloc[:, 1],
        label=f'Rolling Mean, {1+_k}'
    )
    plt.plot(
        data_frame_o.iloc[:, 2],
        label=f'Kolmogorov--Zurbenko Filter, {1+_k}'
    )
    plt.plot(
        data_frame_o.iloc[:, 3],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.25)
    )
    plt.plot(
        data_frame_e,
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
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_block_two(df: DataFrame) -> None:
    '''
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # TODO: Increase Cohesion
    # =========================================================================
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    _k = 3
    # =========================================================================
    # Odd Frame
    # =========================================================================
    data_frame_o = pd.concat(
        [
            df.iloc[:, [-1]],
            rolling_mean_filter(df.iloc[:, [-1]], _k)[0].iloc[:, [-1]],
            kol_zur_filter(df.iloc[:, [-1]], _k)[0].iloc[:, [1]],
            df.iloc[:, [-1]].ewm(alpha=0.25, adjust=False).mean(),
            df.iloc[:, [-1]].ewm(alpha=0.35, adjust=False).mean(),
            df.iloc[:, [-1]].ewm(alpha=0.45, adjust=False).mean(),
        ],
        axis=1,
    )
    # =========================================================================
    # Even Frame
    # =========================================================================
    data_frame_e = pd.concat(
        [
            rolling_mean_filter(df.iloc[:, [-1]], _k)[1],
            kol_zur_filter(df.iloc[:, [-1]], _k)[1],
        ],
        axis=1,
    )
    plt.figure()
    plt.plot(
        data_frame_o.iloc[:, 0],
        linewidth=3,
        label='Labor Productivity'
    )
    plt.plot(
        data_frame_o.iloc[:, 1],
        label=f'Rolling Mean, {_k}'
    )
    plt.plot(
        data_frame_o.iloc[:, 2],
        label=f'Kolmogorov--Zurbenko Filter, {_k}'
    )
    plt.plot(
        data_frame_o.iloc[:, 3],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.25)
    )
    plt.plot(
        data_frame_o.iloc[:, 4],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.35)
    )
    plt.plot(
        data_frame_o.iloc[:, 5],
        label='Single Exponential Smoothing, Alpha={:,.2f}'.format(0.45)
    )
    plt.plot(
        data_frame_e,
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
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_built_in(module: callable) -> None:
    # =========================================================================
    # TODO: Rework
    # =========================================================================
    FILE_NAMES = (
        'datasetAutocorrelation.txt',
        'CHN_TUR_GDP.zip',
    )
    data = pd.read_csv(FILE_NAMES[0])
    for _, series_id in enumerate(sorted(set(data.iloc[:, 1])), start=1):
        plt.figure(_)
        module(extract_world_bank(data, series_id))
        plt.grid(True)

    data = pd.read_csv(FILE_NAMES[1])
    for _, series_id in enumerate(sorted(set(data.iloc[:, 1])), start=1):
        plt.figure(_)
        module(extract_world_bank(data, series_id))
        plt.grid(True)

    plt.show()


def plot_can_test(df: DataFrame) -> None:
    plt.figure()
    df.plot(logy=True)
    plt.title('Discrepancy')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.show()


def plot_capital_modelling(df: DataFrame, base) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Investment
    df.iloc[:, 1]      Production
    df.iloc[:, 2]      Capital
    df.iloc[:, 3]      Capital Retirement
    ================== =================================
    '''
    _params_i = np.polyfit(
        df.index.to_series(),
        df.iloc[:, 0].div(df.iloc[:, 1]).astype(float),
        deg=1
    )
    _params_t = np.polyfit(
        df.index.to_series(),
        df.iloc[:, 1].div(df.iloc[:, 2]).astype(float),
        deg=1
    )
    _df = df.copy()
    # =========================================================================
    # Gross Fixed Investment to Gross Domestic Product Ratio
    # =========================================================================
    _df['inv_to_pro'] = _df.index.to_series().mul(
        _params_i[0]).add(_params_i[1])
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    _df['c_turnover'] = _df.index.to_series().mul(
        _params_t[0]).add(_params_t[1])
    _df['cap_a'] = calculate_capital(df, _params_i, _params_t, 0.875)
    _df['cap_b'] = calculate_capital(df, _params_i, _params_t, 1)
    _df['cap_c'] = calculate_capital(df, _params_i, _params_t, 1.125)
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
    plt.grid(True)
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
    plt.grid(True)
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
    plt.grid(True)
    plt.legend()
    plt.figure(4)
    plt.title('$K$ for the US, {}$-${}'.format(*_df.index[[0, -2]]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars, {}=100'.format(_df.index[base]))
    plt.semilogy(
        _df.iloc[:, -3:],
        label=['$K\\left(\\pi = \\frac{7}{8}\\right)$',
               '$K\\left(\\pi = 1\\right)$',
               '$K\\left(\\pi = \\frac{9}{8}\\right)$', ]
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_capital_purchases(df: DataFrame) -> None:
    assert df.shape[1] == 27, 'Works on DataFrame Produced with `get_data_capital_purchases()`'
    plt.figure()
    plt.semilogy(
        df.loc[:, [df.columns[0], *df.columns[-3:]]],
        label=[
            '$s^{2;1}_{Cobb-Douglas}$',
            'Total',
            'Structures',
            'Equipment', ]
    )
    plt.title('Fixed Assets Purchases, {}$-${}'.format(*df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Millions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_census_complex(source_frame) -> None:
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    plot_pearson_r_test(source_frame)
    plot_kol_zur_filter(source_frame)
    plot_ewm(source_frame)


def plot_cobb_douglas(df: DataFrame, params: tuple[float], mapping: dict) -> None:
    '''
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    '''
    assert df.shape[1] == 12

    def _lab_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, -k), b)

    def _cap_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, 1-k), b)

    plt.figure(1)
    plt.semilogy(df.iloc[:, range(3)], label=[
        'Fixed Capital',
        'Labor Force',
        'Physical Product',
    ])
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_a'].format(*df.index[[0, -1]],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(df.iloc[:, [2, 9]], label=[
        'Actual Product',
        'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
            params[1],
            1-params[0],
            params[0],
        ),
    ])
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(mapping['fg_b'].format(*df.index[[0, -1]],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(df.iloc[:, [8, 11]], label=[
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
    plt.plot(df.iloc[:, 9].div(df.iloc[:, 2]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_d'].format(*df.index[[0, -1]]))
    plt.grid(True)
    plt.figure(5, figsize=(5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(df.iloc[:, 5], df.iloc[:, 4])
    plt.scatter(df.iloc[:, 5], df.iloc[:, 6])
    plt.plot(lc, _lab_productivity(lc, *params),
             label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, _cap_productivity(lc, *params),
             label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_e'])
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_cobb_douglas_3d(df: DataFrame) -> None:
    '''
    Cobb--Douglas 3D-Plotting
    '''
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
    '''
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    '''
    assert df.shape[1] == 20

    def _lab_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, -k), b)

    def _cap_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, 1-k), b)

    plt.figure(1)
    plt.semilogy(df.iloc[:, range(4)], label=[
        'Fixed Capital',
        'Labor Force',
        'Physical Product',
        'Physical Product, Alternative',
    ])
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_a'].format(*df.index[[0, -1]],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(df.iloc[:, [3, 17]], label=[
        'Actual Product',
        'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
            params[1],
            1-params[0],
            params[0],
        ),
    ])
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(mapping['fg_b'].format(*df.index[[0, -1]],
                                     mapping['year_price']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(df.iloc[:, [15, 18]], label=[
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
    plt.plot(df.iloc[:, 17].div(df.iloc[:, 3]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(mapping['fg_d'].format(*df.index[[0, -1]]))
    plt.grid(True)
    plt.figure(5, figsize=(5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(df.iloc[:, 6], df.iloc[:, 13])
    plt.scatter(df.iloc[:, 6], df.iloc[:, 14])
    plt.plot(lc, _lab_productivity(lc, *params),
             label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, _cap_productivity(lc, *params),
             label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title(mapping['fg_e'])
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_cobb_douglas_complex(source_frame) -> None:
    modified_frame_a = source_frame.reset_index(level=0)
    modified_frame_b = source_frame.iloc[:, [0, 2]]
    modified_frame_b = modified_frame_b.reset_index(level=0)
    plot_cobb_douglas(source_frame)
    plot_cobb_douglas_3d(source_frame)
    plot_lab_prod_polynomial(source_frame)
    plot_block_zer(source_frame)
    plot_block_one(modified_frame_a)
    plot_block_two(modified_frame_a)
    plot_turnover(modified_frame_b)


def plot_cobb_douglas_tight_layout(df: DataFrame, params: tuple[float], mapping: dict) -> None:
    '''
    Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    '''
    assert df.shape[1] == 12

    def _lab_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, -k), b)

    def _cap_productivity(array: np.array, k: float = 0.25, b: float = 1.01) -> np.array:
        return np.multiply(np.power(array, 1-k), b)

    fig, axs = plt.subplots(5, 1)
    axs[0].plot(df.iloc[:, range(3)], label=[
        'Fixed Capital',
        'Labor Force',
        'Physical Product',
    ])
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Indexes')
    axs[0].set_title(mapping['fg_a'].format(*df.index[[0, -1]],
                                            mapping['year_price']))
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(df.iloc[:, [2, 5]], label=[
        'Actual Product',
        'Computed Product, $P\' = {:,.4f}L^{{{:,.4f}}}C^{{{:,.4f}}}$'.format(
            params[1], 1-params[0], params[0]),
    ])
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Production')
    axs[1].set_title(mapping['fg_b'].format(*df.index[[0, -1]],
                                            mapping['year_price']))
    axs[1].legend()
    axs[1].grid(True)
    axs[2].plot(df.iloc[:, [8, 9]],
                label=[
                    'Deviations of $P$',
                    'Deviations of $P\'$',
    ],
        # =========================================================================
        #      TODO: ls=['solid','dashed',]
        # =========================================================================
    )
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage Deviation')
    axs[2].set_title(mapping['fg_c'])
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(df.iloc[:, 5].div(df.iloc[:, 2]).sub(1))
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage Deviation')
    axs[3].set_title(mapping['fg_d'].format(*df.index[[0, -1]]))
    axs[3].grid(True)
    lc = np.arange(0.2, 1.0, 0.005)
    axs[4].scatter(df.iloc[:, 10], df.iloc[:, 4])
    axs[4].scatter(df.iloc[:, 10], df.iloc[:, 11])
    axs[4].plot(lc, _lab_productivity(lc, *params),
                label='$\\frac{3}{4}\\frac{P}{L}$')
    axs[4].plot(lc, _cap_productivity(lc, *params),
                label='$\\frac{1}{4}\\frac{P}{C}$')
    axs[4].set_xlabel('$\\frac{L}{C}$')
    axs[4].set_ylabel('Indexes')
    axs[4].set_title(mapping['fg_e'])
    axs[4].legend()
    axs[4].grid(True)
    plt.tight_layout()
    plt.show()


def plot_douglas(source, dictionary, num, start, stop, step, title, measure, label=None) -> None:
    '''
    source: Source Database,
    dictionary: Dictionary of Series IDs to Series Titles from Source Database,
    num: Plot Number,
    start: Start Series Code,
    stop: Stop Series Code,
    step: Step for Series IDs,
    title: Plot Title,
    measure: Dimenstion for Series,
    label: Additional Sublabels'''
    # =========================================================================
    # TODO: Revise
    # =========================================================================
    plt.figure(num)
    for i in range(start, stop, step):
        plt.plot(extract_usa_classic(
            source, dictionary.iloc[i, 0]), label=dictionary.iloc[i, 1])
    plt.title(title)
    plt.xlabel('Period')
    plt.ylabel(measure)
    plt.grid(True)
    if label is None:
        plt.legend()
    else:
        plt.legend(label)


def plot_elasticity(df: DataFrame) -> None:
    '''
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Real Values for Price Deflator
    df.iloc[:, 1]      Nominal Values for Price Deflator
    df.iloc[:, 2]      Focused Series
    ================== =================================
    '''
    df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1], errors='coerce')
    df.dropna(inplace=True)
    # =========================================================================
    # TODO: Separate Basic Year Function
    # =========================================================================
    df['__deflator'] = df.iloc[:, 0].div(df.iloc[:, 1]).sub(1).abs()
    _b = df.iloc[:, -1].astype(float).argmin()
    df.drop(df.columns[-1], axis=1, inplace=True)
    _title = (
        'National Income' if df.columns[2] == 'A032RC1' else 'Series',
        df.columns[2],
        df.index[_b],
    )
    df[f'{df.columns[2]}_real'] = df.iloc[:, 0].mul(
        df.iloc[:, 2]).div(df.iloc[:, 1])
    df[f'{df.columns[2]}_centered'] = df.iloc[:, 3].rolling(2).mean()
    # =========================================================================
    # \dfrac{x_{k} - x_{k-1}}{\dfrac{x_{k} + x_{k-1}}{2}}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_a'] = df.iloc[:, 3].sub(
        df.iloc[:, 3].shift(1)).div(df.iloc[:, -1])
    # =========================================================================
    # \frac{x_{k+1} - x_{k-1}}{2 x_{k}}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_b'] = df.iloc[:,
                                                  3].shift(-1).sub(df.iloc[:, 3].shift(1)).div(df.iloc[:, 3]).div(2)
    # =========================================================================
    # 2 \times \frac{x_{k+1} - x_{k-1}}{x_{k-1} + 2 x_{k} + x_{k+1}}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_c'] = df.iloc[:, 3].shift(-1).sub(df.iloc[:, 3].shift(1)).div(
        df.iloc[:, 3].mul(2).add(df.iloc[:, 3].shift(-1)).add(df.iloc[:, 3].shift(1))).mul(2)
    # =========================================================================
    # \frac{-x_{k-1} - x_{k} + x_{k+1} + x_{k+2}}{2 \times (x_{k} + x_{k+1})}
    # =========================================================================
    df[f'{df.columns[2]}_elasticity_d'] = df.iloc[:, 3].shift(-1).add(df.iloc[:, 3].shift(-2)).sub(
        df.iloc[:, 3].shift(1)).sub(df.iloc[:, 3]).div(df.iloc[:, 3].add(df.iloc[:, 3].shift(-1)).mul(2))
    plt.figure(1)
    plt.title('{}, {}, {}=100'.format(*_title))
    plt.xlabel('Period')
    plt.ylabel(f'Billions of Dollars, {_title[2]}=100')
    plt.plot(df.iloc[:, [3]], label=f'{_title[1]}')
    plt.plot(
        df.index.to_series().rolling(2).mean(),
        df.iloc[:, 4],
        label=f'{_title[1]}, Rolling Mean, Window = 2'
    )
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Elasticity: {}, {}, {}=100'.format(*_title))
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
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.title('Elasticity: {}, {}, {}=100'.format(*_title))
    plt.xlabel('{}, {}, {}=100'.format(*_title))
    plt.ylabel('Elasticity: {}, {}, {}=100'.format(*_title))
    plt.plot(df.iloc[:, 3], df.iloc[:, 8], label='$\\frac{\\epsilon(X)}{X}$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_ewm(df: DataFrame, step: float = 0.1) -> None:
    '''Single Exponential Smoothing
    Robert Goodell Brown, 1956
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    '''
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
            _smooth.iloc[:, [_]].div(
                _smooth.iloc[:, [_]].shift(-1)).rsub(1).dropna()
            for _ in range(_smooth.shape[1])
        ],
        axis=1
    )
    _deltas.index = _smooth.index.to_series().rolling(2).mean().dropna()
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
    plt.grid(True)
    plt.legend(_labels)
    plt.figure(2)
    plt.title('Deltas of Exponentially Smoothed Series')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(_deltas.index, _deltas.iloc[:, 0])
    plt.plot(_deltas.iloc[:, 1:])
    plt.grid(True)
    plt.legend(_labels)
    plt.show()


def plot_fourier_discrete(df: DataFrame, precision: int = 10) -> None:
    '''
    Discrete Fourier Transform based on Simpson's Rule
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    '''
    _df = df.copy()
    precision += 1
    _p = np.polyfit(
        _df.index,
        _df.iloc[:, 0].astype(float),
        deg=1
    )
    _df['period_calibrated'] = _df.index.to_series().sub(
        _df.index[0]).div(_df.shape[0]).mul(2).mul(np.pi)
    _df[f'{_df.columns[0]}_line'] = _df.index.to_series().mul(_p[0]).add(_p[1])
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
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_grigoriev() -> None:
    FILE_NAME = 'dataset_rus_grigoriev_v.csv'
    df = pd.read_csv(FILE_NAME, index_col=1, usecols=range(2, 5))
    for series_id in sorted(set(df.iloc[:, 0])):
        chunk = df[df.iloc[:, 0] == series_id].iloc[:, [1]]
        chunk.columns = [series_id]
        chunk.sort_index(inplace=True)
        chunk.plot(grid=True)


def plot_growth_elasticity(df: DataFrame) -> None:
    '''Growth Elasticity Plotting
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Series
    ================== =================================
    '''
    # =========================================================================
    # TODO: Increase Cohesion of This Code: Send Plotting to Separate Function
    # =========================================================================
    df.reset_index(level=0, inplace=True)
    _df = DataFrame()
    # =========================================================================
    # Period, Centered
    # =========================================================================
    _df[f'{df.columns[0]}'] = df.iloc[:, [0]].rolling(2).mean()
    df.index.to_series().rolling(2).mean()
    # =========================================================================
    # Series, Centered
    # =========================================================================
    _df[f'{df.columns[1]}_centered'] = df.iloc[:, [1]].rolling(2).mean()
    # =========================================================================
    # Series, Growth Rate
    # =========================================================================
    _df[f'{df.columns[1]}_growth_rate'] = df.iloc[:, [1]].sub(
        df.iloc[:, [1]].shift(2)).div(df.iloc[:, [1]].rolling(2).sum().shift(1))
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
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_increment(df: DataFrame) -> None:
    FLAG = False
    FOLDER = '/home/alexander/science'
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(df.iloc[:, 0], df.iloc[:, 1], label='Curve')
    axs[0].set_xlabel('Labor Capital Intensity')
    axs[0].set_ylabel('Labor Productivity')
    axs[0].set_title('Labor Capital Intensity to Labor Productivity Relation')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(df.iloc[:, 2], df.iloc[:, 3], label='Curve')
    axs[1].set_xlabel('Labor Capital Intensity Increment')
    axs[1].set_ylabel('Labor Productivity Increment')
    axs[1].set_title(
        'Labor Capital Intensity to Labor Productivity Increments Relation')
    axs[1].grid(True)
    axs[1].legend()
    for _ in range(3, df.shape[0], 5):
        axs[0].annotate(df.index[_], (df.iloc[_, 0], df.iloc[_, 1]))
        axs[1].annotate(df.index[_], (df.iloc[_, 2], df.iloc[_, 3]))
    fig.set_size_inches(10., 20.)
    fig.tight_layout()
    if FLAG:
        fig.savefig(
            os.path.join(FOLDER, 'fig_file_name.pdf'),
            format='pdf', dpi=900
        )
    else:
        plt.show()


def plot_is_lm() -> None:
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


def plot_kol_zur_filter(df: DataFrame) -> None:
    '''Kolmogorov--Zurbenko Filter
        df.index: Period,
        df.iloc[:, 0]: Series
    '''
    data_frame_o, data_frame_e, residuals_o, residuals_e = kol_zur_filter(
        df)

    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(
        data_frame_o.iloc[:, [0]].index,
        data_frame_o.iloc[:, [0]],
        label='Original Series'
    )
    plt.plot(
        data_frame_o.iloc[:, 1:],
        label=['$KZF(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in data_frame_o.columns[1:]]
    )
    plt.plot(
        data_frame_e,
        label=['$KZF(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in data_frame_e.columns]
    )
    plt.grid(True)
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
        label=['$\\delta KZF(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_o.columns[1:]]
    )
    plt.plot(
        residuals_e,
        label=['$\\delta KZF(\\lambda = {})$'.format(int(_.split('_')[-1], 16))
               for _ in residuals_e.columns]
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_kurenkov(data_frames: tuple[DataFrame]) -> None:
    '''
    data_frames[0]: Production DataFrame,
    data_frames[1]: Labor DataFrame,
    data_frames[2]: Capital DataFrame,
    data_frames[3]: Capacity Utilization DataFrame'''
    # =========================================================================
    # Plotting
    # =========================================================================
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(
        data_frames[0],
        label=[
            'Kurenkov Data, 1950=100',
            'BEA Data, 1950=100',
            'FRB Data, 1950=100',
        ]
    )
    axs[0].set_title('Production')
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Percentage')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(
        data_frames[1],
        label=[
            'Kurenkov Data',
            'BEA Data',
        ]
    )
    axs[1].set_title('Labor')
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Thousands of Persons')
    axs[1].legend()
    axs[1].grid(True)
    # =========================================================================
    # Revised Capital
    # =========================================================================
    axs[2].plot(
        data_frames[2],
        label=[
            'Kurenkov Data, 1951=100',
            'BEA Data, 1951=100',
        ]
    )
    axs[2].set_title('Capital')
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage')
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(
        data_frames[3],
        label=[
            'Kurenkov Data',
            'FRB Data',
        ]
    )
    axs[3].set_title('Capacity Utilization')
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage')
    axs[3].legend()
    axs[3].grid(True)
    fig.set_size_inches(10., 20.)


def plot_lab_prod_polynomial(df: DataFrame) -> None:
    '''Static Labor Productivity Approximation
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Labor,
    df.iloc[:, 2]: Product
    '''
    # =========================================================================
    # TODO: Increase Cohesion
    # =========================================================================

    def _r2_scores():
        for _ in range(5):
            yield r2_score(df.iloc[:, -1], _df.iloc[:, _])

    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    # =========================================================================
    # Power Function: Labor Productivity
    # =========================================================================
    k, b = np.polyfit(np.log(df.iloc[:, -2]), np.log(df.iloc[:, -1]), deg=1)
    # =========================================================================
    # Polynomials 1, 2, 3 & 4: Labor Productivity
    # =========================================================================
    _p1 = np.polyfit(df.iloc[:, -2], df.iloc[:, -1], deg=1)
    _p2 = np.polyfit(df.iloc[:, -2], df.iloc[:, -1], deg=2)
    _p3 = np.polyfit(df.iloc[:, -2], df.iloc[:, -1], deg=3)
    _p4 = np.polyfit(df.iloc[:, -2], df.iloc[:, -1], deg=4)
    # =========================================================================
    # DataFrame for Approximation Results
    # =========================================================================
    _df = DataFrame()
    _df['pow'] = df.iloc[:, -2].pow(k).mul(np.exp(b))
    _df['p_1'] = _p1[1] + df.iloc[:, -2].mul(_p1[0])
    _df['p_2'] = _p2[2] + df.iloc[:, -
                                  2].mul(_p2[1]) + df.iloc[:, -2].pow(2).mul(_p2[0])
    _df['p_3'] = _p3[3] + df.iloc[:, -2].mul(_p3[2]) + df.iloc[:, -2].pow(
        2).mul(_p3[1]) + df.iloc[:, -2].pow(3).mul(_p3[0])
    _df['p_4'] = _p4[4] + df.iloc[:, -2].mul(_p4[3]) + df.iloc[:, -2].pow(2).mul(
        _p4[2]) + df.iloc[:, -2].pow(3).mul(_p4[1]) + df.iloc[:, -2].pow(4).mul(_p4[0])
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
            *_p1[::-1],
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 2], label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2, R^2 = {:.4f}$'.format(
            2,
            *_p2[::-1],
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 3], label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3, R^2 = {:.4f}$'.format(
            3,
            *_p3[::-1],
            next(r),
        )
    )
    plt.plot(
        _df.iloc[:, 4], label='$\\hat P_{{{}}}(X) = {:.2f}+{:.2f}X {:.2f}X^2+{:.2f}X^3 {:.2f}X^4, R^2 = {:.4f}$'.format(
            4,
            *_p4[::-1],
            next(r),
        )
    )
    plt.title('Labor Capital Intensity & Labor Productivity, {}$-${}'.format(
        *df.index[[0, -1]]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
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
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_pearson_r_test(df: DataFrame) -> None:
    '''
    Left-Side & Right-Side Rolling Means' Calculation & Plotting
    ================== =================================
    df.index           Period
    df.iloc[:, 0]      Target Series
    ================== =================================
    '''
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
            stats.pearsonr(df.iloc[:, 0][_r_frame.notna()], _r_frame.dropna())[0] /
            stats.pearsonr(
                df.iloc[:, 0][_l_frame.notna()], _l_frame.dropna())[0]
        ]
    # =========================================================================
    # Plot 'Window' to 'Right-Side to Left-Side Pearson R
    # =========================================================================
    plt.figure()
    plt.title('Right-Side to Left-Side Pearson R Ratio')
    plt.xlabel('`Window`')
    plt.ylabel('Index')
    plt.plot(_pearson, label='Right-Side to Left-Side Pearson R Ratio')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_rolling_mean_filter(df: DataFrame) -> None:
    '''Rolling Mean Filter
        df.index: Period;
        df.iloc[:, 0]: Series
    '''
    data_frame_o, data_frame_e, residuals_o, residuals_e = rolling_mean_filter(
        df)
    plt.figure(1)
    plt.title(
        f'Rolling Mean {data_frame_o.index[0]}$-${data_frame_o.index[-1]}'
    )
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.scatter(
        data_frame_o.iloc[:, [0]].index,
        data_frame_o.iloc[:, [0]],
        label='Original Series'
    )
    plt.plot(
        data_frame_o.iloc[:, 1:],
        label=['$\\hat Y_{{m = {}}}$'.format(int(_.split('_')[-1], 16))
               for _ in data_frame_o.columns[1:]]
    )
    plt.plot(
        data_frame_e,
        label=['$\\hat Y_{{m = {}}}$'.format(int(_.split('_')[-1], 16))
               for _ in data_frame_e.columns]
    )
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title(
        f'Rolling Mean Residuals {data_frame_o.index[0]}$-${data_frame_o.index[-1]}'
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
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_simple_linear(df: DataFrame, params: tuple[float]) -> None:
    '''
    Labor Productivity on Labor Capital Intensity Plot;
    Predicted Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(
        df.iloc[:, 0],
        df.iloc[:, 1],
        label='Original'
    )
    plt.title(
        '$Labor\ Capital\ Intensity$, $Labor\ Productivity$ Relation, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel('Labor Productivity')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(
        df.iloc[:, 2],
        # =====================================================================
        # TODO:
        # label='$\\frac{{Y}{Y_{0}} = {{:,.4f}}\\frac{{L}{L_{0}}+{{:,.4f}}\\frac{{K}{K_{0}}$'.format(
        #     *params[::-1]
        # )
        # =====================================================================
        label='TBA'
    )
    plt.title(
        'Model: $\\hat Y = {:.4f}+{:.4f}\\times X$, {}$-${}'.format(
            *params[::-1],
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Period')
    plt.ylabel('$\\hat Y = Labor\ Productivity$, $X = Labor\ Capital\ Intensity$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_simple_log(df: DataFrame, params: tuple[float]) -> None:
    '''
    Log Labor Productivity on Log Labor Capital Intensity Plot;
    Predicted Log Labor Productivity Plot
    '''
    plt.figure(1)
    plt.plot(
        df.iloc[:, 0],
        df.iloc[:, 1],
        label='Logarithm'
    )
    plt.title(
        '$\\ln(Labor\ Capital\ Intensity), \\ln(Labor\ Productivity)$ Relation, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('$\\ln(Labor\ Capital\ Intensity)$')
    plt.ylabel('$\\ln(Labor\ Productivity)$')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.plot(
        df.iloc[:, 2],
        # =====================================================================
        # TODO
        # =====================================================================
        label='$\\ln(\\frac{Y}{Y_{0}}) = %f+%f\\ln(\\frac{K}{K_{0}})+%f\\ln(\\frac{L}{L_{0}})$' % (
            *params[::-1],
            1 - params[0]
        )
    )
    plt.title('Model: $\\ln(\\hat Y) = {:.4f}+{:.4f}\\times \\ln(X)$, {}$-${}'.format(
        *params[::-1],
        *df.index[[0, -1]]
    )
    )
    plt.xlabel('Period')
    plt.ylabel(
        '$\\hat Y = \\ln(Labor\ Productivity)$, $X = \\ln(Labor\ Capital\ Intensity)$'
    )
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_turnover(df: DataFrame) -> None:
    '''Static Fixed Assets Turnover Approximation
    df.index: Period,
    df.iloc[:, 0]: Capital,
    df.iloc[:, 1]: Product
    '''
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df['c_turnover'] = df.iloc[:, 1].div(df.iloc[:, 0])
    # =========================================================================
    # Linear: Fixed Assets Turnover
    # =========================================================================
    _lin = np.polyfit(df.index, df.iloc[:, -1], deg=1)
    # =========================================================================
    # Exponential: Fixed Assets Turnover
    # =========================================================================
    _exp = np.polyfit(df.index, np.log(df.iloc[:, -1]), deg=1)
    df['c_turnover_lin'] = df.index.to_series().mul(_lin[0]).add(_lin[1])
    df['c_turnover_exp'] = np.exp(
        df.index.to_series().mul(_exp[0]).add(_exp[1]))
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
    plt.grid(True)
    plt.figure(2)
    plt.scatter(
        df.index,
        df.iloc[:, -5],
        label='Fixed Assets Turnover'
    )
    plt.plot(
        df.iloc[:, [-4]],
        label='$\\hat K_{{l}} = {:.2f} {:.2f} t, R^2 = {:.4f}$'.format(
            *_lin[::-1],
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
    plt.grid(True)
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
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_usa_nber(df_sic: DataFrame, df_naics: DataFrame, agg: str) -> None:
    '''Project V: USA NBER Data Plotting'''
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
        plt.grid(True)
        plt.legend()
        plt.show()


def plot_usa_nber_manager() -> None:
    FILE_NAMES = (
        'dataset_usa_nber_ces_mid_sic5811.csv',
        'dataset_usa_nber_ces_mid_naics5811.csv',
    )
    aggs = ('mean', 'sum')
    for _agg in aggs:
        sic = extract_usa_nber(FILE_NAMES[0], _agg)
        naics = extract_usa_nber(FILE_NAMES[1], _agg)
        plot_usa_nber(sic, naics, _agg)
