#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:19:54 2022

@author: Alexander Mikhailov
"""


import pandas as pd
from pandas import DataFrame
from pandas.plotting import autocorrelation_plot

from thesis.src.lib.collect import stockpile_usa_hist
from thesis.src.lib.plot import plot_can_test
from thesis.src.lib.pull import pull_by_series_id, transform_agg_sum
from thesis.src.lib.read import read_can, read_usa_bea_excel, read_usa_bls


def options_reviewed():
    SERIES_IDS = (
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        {'DT24AS01': 'dataset_douglas.zip'},
        # =====================================================================
        # Not Suitable: Total Capital (in millions of 1880 dollars)
        # =====================================================================
        {'DT63AS01': 'dataset_douglas.zip'},
        # =====================================================================
        # Not Suitable: Annual Increase (in millions of 1880 dollars)
        # =====================================================================
        {'DT63AS02': 'dataset_douglas.zip'},
        # =====================================================================
        # Not Suitable: Percentage Rate of Growth
        # =====================================================================
        {'DT63AS03': 'dataset_douglas.zip'}
    )

    for series_id in SERIES_IDS:
        print(stockpile_usa_hist(series_id))


def test_data_can():
    """Project I: Canada Gross Domestic Product Data Comparison"""
    # =========================================================================
    # Expenditure-Based Gross Domestic Product Series Used
    # Income-Based Gross Domestic Product Series Not Used
    # =========================================================================
    SERIES_IDS = {
        # =====================================================================
        # Series A: Equals Series D, However, Series D Is Preferred Over Series A As It Is Yearly:
        # v62307282 - 380-0066 Price indexes, gross domestic product; Canada; Implicit price indexes; Gross domestic product at market prices (quarterly, 1961-03-01 to 2017-09-01)
        # =====================================================================
        'v62307282': 3800066,
        # =====================================================================
        # Series B: Equals Both Series C & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306896 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Seasonally adjusted at annual rates; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
        # =====================================================================
        'v62306896': 3800084,
        # =====================================================================
        # Series C: Equals Both Series B & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306938 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Unadjusted; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
        # =====================================================================
        'v62306938': 3800084,
        # =====================================================================
        # Series D: Equals Series A, However, Series D Is Preferred Over Series A As It Is Yearly: v62471023 - 380-0102 Gross domestic product indexes; Canada; Implicit price indexes; Gross domestic product at market prices (annual, 1961 to 2016)
        # =====================================================================
        'v62471023': 3800102,
        # =====================================================================
        # Series E: Equals Both Series B & Series C, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62471340 - 380-0106 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Gross domestic product at market prices (x 1,000,000) (annual, 1961 to 2016)
        # =====================================================================
        'v62471340': 3800106,
        'v96411770': 3800518,
        'v96391932': 3800566,
        'v96730304': 3800567,
        'v96730338': 3800567
    }
    df = pd.concat(
        [
            pd.concat(
                [
                    read_can(_args[0]).pipe(transform_agg_sum, _args[1])
                    for _args in ARGS[:3]
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    read_can(_args[0]).pipe(pull_by_series_id, _args[1])
                    for _args in ARGS[3:]
                ],
                axis=1,
                sort=True
            ).apply(pd.to_numeric, errors='coerce'),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    df['series_0x0'] = df.iloc[:, 0].div(df.iloc[0, 0])
    df['series_0x1'] = df.iloc[:, 4].div(df.iloc[0, 4])
    df['series_0x2'] = df.iloc[:, 5].div(df.iloc[0, 5])
    df['series_0x3'] = df.iloc[:, 7].div(
        df.iloc[:, 6]).div(df.iloc[:, 5]).mul(100)
    df['series_0x4'] = df.iloc[:, 8].div(df.iloc[0, 8])
    # =========================================================================
    # Option 1
    # =========================================================================
    plot_can_test(df.iloc[:, (-5, -3)])
    # =========================================================================
    # Option 2
    # =========================================================================
    plot_can_test(df.iloc[:, (-2, -1)])
    # =========================================================================
    # Option 3
    # =========================================================================
    plot_can_test(df.iloc[:, (-4, -1)])
    # =========================================================================
    # Option 4: What?
    # =========================================================================
    # plot_can_test(df.iloc[:, -1].div(df.iloc[:, -1]), df.iloc[:, -3])


def test_data_usa_bea():
    """Project II: USA Fixed Assets Data Comparison"""
    SERIES_IDS = {
        # =====================================================================
        # Fixed Assets Series: k1ntotl1si00, 1925--2016
        # =====================================================================
        'k1ntotl1si00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Fixed Assets Series: kcntotl1si00, 1925--2016
        # =====================================================================
        'kcntotl1si00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Not Used: Fixed Assets: k3ntotl1si00, 1925--2016, Table 2.3. Historical-Cost Net Stock of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
        # =====================================================================
        'k3ntotl1si00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    return stockpile_usa_bea(SERIES_IDS)


def test_data_usa_bls():
    """Project III: USA BLS Unemployment Rate & Producer Price Index Manufacturing"""
    SERIES_IDS = {
        # =========================================================================
        # LNU04000000: Bureau of Labor Statistics Unemployment Rate
        # =========================================================================
        'dataset_usa_bls-2015-02-23-ln.data.1.AllData': 'LNU04000000',
        # =========================================================================
        # LNU04000000: Bureau of Labor Statistics Unemployment Rate
        # =========================================================================
        'dataset_usa_bls-2017-07-06-ln.data.1.AllData': 'LNU04000000',
        # =========================================================================
        # PCUOMFG--OMFG--: Bureau of Labor Statistics Producer Price Index Manufacturing
        # =========================================================================
        'dataset_usa_bls-pc.data.0.Current': 'PCUOMFG--OMFG'
    }
    [
        print(read_usa_bls(filepath_or_buffer).pipe(
            pull_by_series_id, series_id))
        for filepath_or_buffer, series_id in SERIES_IDS.items()
    ]


def test_data_consistency_d():
    """Project IV: USA Macroeconomic & Fixed Assets Data Tests"""
    # =========================================================================
    # Macroeconomic Data Tests
    # =========================================================================
    def _generate_kwargs_list(
            archive_name: str,
            wb_name: str,
            sheet_names: tuple[str],
            series_ids: tuple[str]
    ) -> list[dict]:
        return [
            {
                'archive_name': archive_name,
                'wb_name': wb_name,
                'sh_name': _sh,
                'series_id': series_id,
            } for _sh, series_id in zip(sheet_names, series_ids)
        ]

    # =========================================================================
    # Tested: "A051RC" != "A052RC" + "A262RC"
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10705-A', 'T11200-A', 'T10705-A')
    SERIES_IDS = ('A051RC', 'A052RC', 'A262RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Tested: "Government" = "Federal" + "State and local"
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A')
    SERIES_IDS = ('A822RC', 'A823RC', 'A829RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30100-A', 'T30200-A', 'T30300-A')
    SERIES_IDS = ('A955RC', 'A957RC', 'A991RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Tested: "Federal" = "National defense" + "Nondefense"
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A')
    SERIES_IDS = ('A823RC', 'A824RC', 'A825RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30200-A', 'T30905-A', 'T30905-A')
    SERIES_IDS = ('A957RC', 'A997RC', 'A542RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Fixed Assets Data Tests
    # =========================================================================
    df = test_usa_bea_sfat_series_ids()

    test_subtract_a()
    # =========================================================================
    # Comparison of "k3n31gd1es00" out of df_control with "k3n31gd1es00" out of df_test
    # =========================================================================
    test_subtract_b(df)
    # =========================================================================
    # Future Project: Test Ratio of Manufacturing Fixed Assets to Overall Fixed Assets
    # =========================================================================
    # =========================================================================
    # TODO:
    # =========================================================================


def test_douglas() -> None:
    """
    Data Consistency Test

    Returns
    -------
    None

    """
    SERIES_IDS = {
        'J0014': 'dataset_uscb.zip',
        'DT24AS01': 'dataset_douglas.zip'
    }
    df = stockpile_usa_hist(SERIES_IDS)
    df.loc[:, [0]] = df.loc[:, [0]].div(df.loc[1899, [0]]).mul(100).round(0)
    df['dif'] = df.iloc[:, 1].sub(df.iloc[:, 0])
    df.dropna(axis=0).plot(
        title='Cobb--Douglas Data Comparison', legend=True, grid=True)
    SERIES_IDS = {
        # =================================================================
        # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
        # =================================================================
        'CDT2S4': 'dataset_usa_cobb-douglas.zip',
        'DT63AS01': 'dataset_douglas.zip'
    }
    df = stockpile_usa_hist(SERIES_IDS)
    df['div'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df.dropna(axis=0).plot(
        title='Cobb--Douglas Data Comparison', legend=True, grid=True)


def test_usa_bea_subtract(kwargs_list: list[dict]) -> None:
    df = pd.concat(
        [
            # =================================================================
            # TODO: UPDATE ACCORDING TO NEW SIGNATURE
            # =================================================================
            read_usa_bea_excel(**_kwargs) for _kwargs in kwargs_list
        ],
        axis=1,
        sort=True
    )
    df['diff_abs'] = df.iloc[:, 0].sub(df.iloc[:, 1]).sub(df.iloc[:, 2])
    df.iloc[:, [-1]].dropna(axis=0).plot(grid=True)


def test_subtract_a():
    """
    Tested: "k3n31gd1es00" = "k3n31gd1eq00" + "k3n31gd1ip00" + "k3n31gd1st00"
    """
    SERIES_ID = {
        'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    }
    SERIES_IDS = {
        'k3n31gd1eq00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'k3n31gd1ip00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'k3n31gd1st00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    }
    df = stockpile_usa_bea(SERIES_ID | SERIES_IDS)
    df["sum"] = df.loc[:, list(SERIES_IDS)].sum(axis=1)
    df["delta"] = df.iloc[:, 0].sub(df.iloc[:, -1])
    df.iloc[:, [-1]].pipe(autocorrelation_plot)


def test_subtract_b(df: DataFrame):
    # =========================================================================
    # df['delta_eq'] = df.iloc[:, 0].sub(df.iloc[:, -1])
    # =========================================================================
    df['delta_eq'] = df.iloc[:, 0].mul(4).div(
        df.iloc[:, 0].add(df.iloc[:, -1])).sub(2)
    df.iloc[:, [-1]].dropna(axis=0).plot(grid=True)


def test_usa_bea_sfat_series_ids(
    path_src: str = '/media/green-machine/KINGSTON',
    file_name: str = 'dataset_usa_bea-nipa-selected.zip',
    source_id: str = 'Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization',
    series_id: str = 'k3n31gd1es000'
) -> DataFrame:
    """
    Earlier Version of 'k3n31gd1es000'
    """
    # =========================================================================
    # Fixed Assets Series, 1925--2016
    # Test if Ratio of Manufacturing Fixed Assets to Overall Fixed Assets
    # =========================================================================
    SERIES_IDS = {
        'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'k3n31gd1eq00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'k3n31gd1ip00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'k3n31gd1st00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    }
    df_test = stockpile_usa_bea(SERIES_IDS)

    kwargs = {
        'filepath_or_buffer': Path(path_src).joinpath(file_name),
        'header': 0,
        'names': ('source_id', 'series_id', 'period', 'value'),
        'index_col': 2,
        'usecols': (0, 8, 9, 10),
    }
    df = pd.read_csv(**kwargs)
    # =========================================================================
    # Option I
    # =========================================================================
    df = df[df.iloc[:, 1] == series_id]

    df_control = DataFrame()
    for source_id in sorted(set(df.iloc[:, 0])):
        chunk = df[df.iloc[:, 0] == source_id].iloc[:, [2]]
        chunk.columns = [
            ''.join((source_id.split()[1].replace('.', '_'), series_id))
        ]
        df_control = pd.concat([df_control, chunk], axis=1, sort=True)

    # =========================================================================
    # # =========================================================================
    # # Option II
    # # =========================================================================
    # df_control = df[
    #     (df.loc[:, 'source_id'] == source_id) &
    #     (df.loc[:, 'series_id'] == series_id)
    # ].iloc[:, [-1]].rename(columns={"value": series_id})
    # =========================================================================

    return pd.concat([df_test, df_control], axis=1, sort=True)


def test_usa_brown_kendrick() -> DataFrame:
    """
    Fetch Data from:
        <reference_ru_brown_m_0597_088.pdf>, Page 193 &
        Out of Kendrick J.W. Data & Table 2. of <reference_ru_brown_m_0597_088.pdf>

    FN:Murray Brown
    ORG:University at Buffalo;Economics
    TITLE:Professor Emeritus, Retired
    EMAIL;PREF;INTERNET:mbrown@buffalo.edu

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    SERIES_IDS = {f'brown_{hex(_)}': 'dataset_usa_brown.zip' for _ in range(6)}
    df_b = stockpile_usa_hist(SERIES_IDS)
    SERIES_IDS = {
        'KTA03S07': 'dataset_usa_kendrick.zip',
        'KTA03S08': 'dataset_usa_kendrick.zip',
        'KTA10S08': 'dataset_usa_kendrick.zip',
        'KTA15S07': 'dataset_usa_kendrick.zip',
        'KTA15S08': 'dataset_usa_kendrick.zip'
    }
    df_k = stockpile_usa_hist(SERIES_IDS).truncate(
        before=1889).truncate(after=1954)
    df = pd.concat(
        [
            # =================================================================
            # Omit Two Last Rows
            # =================================================================
            df_k[~df_k.index.duplicated(keep='first')],
            # =================================================================
            # Первая аппроксимация рядов загрузки мощностей, полученная с помощью метода Уортонской школы
            # =================================================================
            df_b.loc[:, ["brown_0x4"]].truncate(after=1953)
        ],
        axis=1,
        sort=True
    )
    df = df.assign(
        brown_0x0=df.iloc[:, 0].sub(df.iloc[:, 1]),
        brown_0x1=df.iloc[:, 3].add(df.iloc[:, 4]),
        brown_0x2=df.iloc[:, [3, 4]].sum(axis=1).rolling(
            2).mean().mul(df.iloc[:, 5]).div(100),
        brown_0x3=df.iloc[:, 2]
    )
    return pd.concat(
        [
            df.iloc[:, -4:].dropna(axis=0),
            # =================================================================
            # Brown M. Numbers Not Found in Kendrick J.W. For Years Starting From 1954 Inclusive
            # =================================================================
            df_b.iloc[:, range(4)].truncate(before=1954)
        ]
    ).round()
