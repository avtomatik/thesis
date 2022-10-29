#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:19:54 2022

@author: alexander
"""


ARCHIVE_NAMES_UTILISED = (
    'dataset_douglas.zip',
    'dataset_usa_bea-release-2019-12-19-Survey.zip',
    'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
)
FILE_NAMES_UTILISED = (
    'dataset_usa_bls-2015-02-23-ln.data.1.AllData',
    'dataset_usa_bls-2017-07-06-ln.data.1.AllData',
    'dataset_usa_bls-pc.data.0.Current',
)


def options():
    ARCHIVE_NAME = 'dataset_douglas.zip'
    SERIES_IDS = (
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        'DT24AS01',
        # =====================================================================
        # Not Suitable: Total Capital (in millions of 1880 dollars)
        # =====================================================================
        'DT63AS01',
        # =====================================================================
        # Not Suitable: Annual Increase (in millions of 1880 dollars)
        # =====================================================================
        'DT63AS02',
        # =====================================================================
        # Not Suitable: Percentage Rate of Growth
        # =====================================================================
        'DT63AS03',
    )
    [
        print(extract_usa_classic(ARCHIVE_NAME, series_id))
        for series_id in SERIES_IDS
    ]


def test_data_consistency_a():
    """Project I: Canada Gross Domestic Product Data Comparison"""
    # =========================================================================
    # Expenditure-Based Gross Domestic Product Series Used
    # Income-Based Gross Domestic Product Series Not Used
    # =========================================================================
    ARGS = (
        # =====================================================================
        # Series A: Equals Series D, However, Series D Is Preferred Over Series A As It Is Yearly:
        # v62307282 - 380-0066 Price indexes, gross domestic product; Canada; Implicit price indexes; Gross domestic product at market prices (quarterly, 1961-03-01 to 2017-09-01)
        # =====================================================================
        (3800066, 'v62307282'),
        # =====================================================================
        # Series B: Equals Both Series C & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306896 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Seasonally adjusted at annual rates; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
        # =====================================================================
        (3800084, 'v62306896'),
        # =====================================================================
        # Series C: Equals Both Series B & Series E, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62306938 - 380-0084 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Unadjusted; Gross domestic product at market prices (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)
        # =====================================================================
        (3800084, 'v62306938'),
        # =====================================================================
        # Series D: Equals Series A, However, Series D Is Preferred Over Series A As It Is Yearly: v62471023 - 380-0102 Gross domestic product indexes; Canada; Implicit price indexes; Gross domestic product at market prices (annual, 1961 to 2016)
        # =====================================================================
        (3800102, 'v62471023'),
        # =====================================================================
        # Series E: Equals Both Series B & Series C, However, Series E Is Preferred Over Both Series B & Series C As It Is Yearly: v62471340 - 380-0106 Gross domestic product at 2007 constant prices, expenditure-based; Canada; Gross domestic product at market prices (x 1,000,000) (annual, 1961 to 2016)
        # =====================================================================
        (3800106, 'v62471340'),
        (3800518, 'v96411770'),
        (3800566, 'v96391932'),
        (3800567, 'v96730304'),
        (3800567, 'v96730338'),
    )
    df = pd.concat(
        [
            pd.concat(
                [
                    extract_can_quarter(*_args) for _args in ARGS[:3]
                ],
                axis=1,
                sort=True
            ),
            pd.concat(
                [
                    extract_can_annual(*_args) for _args in ARGS[3:]
                ],
                axis=1,
                sort=True
            ),
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
    plot_can_test(df.iloc[:, [-5, -3]])
    # =========================================================================
    # Option 2
    # =========================================================================
    plot_can_test(df.iloc[:, [-2, -1]])
    # =========================================================================
    # Option 3
    # =========================================================================
    plot_can_test(df.iloc[:, [-4, -1]])
    # =========================================================================
    # Option 4: What?
    # =========================================================================
    # plot_can_test(df.iloc[:, -1].div(df.iloc[:, -1]), df.iloc[:, -3])


def test_data_consistency_b():
    """Project II: USA Fixed Assets Data Comparison"""
    # =========================================================================
    # Fixed Assets Series: k1ntotl1si000, 1925--2016
    # Fixed Assets Series: kcntotl1si000, 1925--2016
    # Not Used: Fixed Assets: k3ntotl1si000, 1925--2016, Table 2.3. Historical-Cost Net Stock of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAME = 'Section2ALL_xls.xls'
    SH_NAMES = (
        '201 Ann',
        '202 Ann',
        '203 Ann',
    )
    SERIES_IDS = (
        'k1ntotl1si000',
        'kcntotl1si000',
        'k3ntotl1si000',
    )
    df = pd.concat(
        [
            extract_read_usa_bea(ARCHIVE_NAME, WB_NAME, sh, _id)
            for sh, _id in zip(SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )
    print(df)


def test_data_consistency_c():
    """Project III: USA BLS Unemployment Rate & Producer Price Index Manufacturing"""
    FILE_NAMES = (
        'dataset_usa_bls-2015-02-23-ln.data.1.AllData',
        'dataset_usa_bls-2017-07-06-ln.data.1.AllData',
        'dataset_usa_bls-pc.data.0.Current',
    )
    SERIES_IDS = (
        # =====================================================================
        # LNU04000000: Bureau of Labor Statistics Unemployment Rate
        # LNU04000000: Bureau of Labor Statistics Unemployment Rate
        # PCUOMFG--OMFG--: Bureau of Labor Statistics Producer Price Index Manufacturing
        # =====================================================================
        'LNU04000000',
        'LNU04000000',
        'PCUOMFG--OMFG',
    )
    [
        print(extract_usa_bls(file_name, series_id))
        for file_name, series_id in zip(FILE_NAMES, SERIES_IDS)
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
                'series_id': _id,
            } for _sh, _id in zip(sheet_names, series_ids)
        ]

    # =========================================================================
    # Tested: `A051RC1` != `A052RC1` + `A262RC1`
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10705-A', 'T11200-A', 'T10705-A',)
    SERIES_IDS = ('A051RC', 'A052RC', 'A262RC',)
    test_procedure(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Tested: `Government` = `Federal` + `State and local`
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A',)
    SERIES_IDS = ('A822RC', 'A823RC', 'A829RC',)
    test_procedure(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30100-A', 'T30200-A', 'T30300-A',)
    SERIES_IDS = ('A955RC', 'A957RC', 'A991RC',)
    test_procedure(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # # =========================================================================
    # # Tested: `Federal` = `National defense` + `Nondefense`
    # # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A',)
    SERIES_IDS = ('A823RC', 'A824RC', 'A825RC',)
    test_procedure(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30200-A', 'T30905-A', 'T30905-A',)
    SERIES_IDS = ('A957RC', 'A997RC', 'A542RC',)
    test_procedure(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Fixed Assets Data Tests
    # =========================================================================
    df = test_read_usa_bea_sfat_series()
    # =========================================================================
    # Tested: `k3n31gd1es000` = `k3n31gd1eq000` + `k3n31gd1ip000` + `k3n31gd1st000`
    # =========================================================================
    test_sub_a(df)
    # =========================================================================
    # Comparison of `k3n31gd1es000` out of control_frame with `k3n31gd1es000` out of test_frame
    # =========================================================================
    test_sub_b(df)
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
    _kwargs = (
        {
            'archive_name': 'dataset_uscb.zip',
            'series_id': 'J0014',
        },
        {
            'archive_name': 'dataset_douglas.zip',
            'series_id': 'DT24AS01',
        },
    )
    df = pd.concat(
        [
            partial(read_usa_hist, **_kwargs[0])(),
            partial(extract_usa_classic, **_kwargs[1])(),
        ],
        axis=1
    )
    _loc = _kwargs[0]['series_id']
    df.loc[:, [_loc]] = df.loc[:, [_loc]].div(
        df.loc[1899, [_loc]]).mul(100).round(0)
    df['dif'] = df.iloc[:, 1].sub(df.iloc[:, 0])
    df.dropna().plot(title='Cobb--Douglas Data Comparison', legend=True, grid=True)
    _kwargs = (
        {
            # =================================================================
            # Cobb C.W., Douglas P.H. Capital Series: Total Fixed Capital in 1880 dollars (4)
            # =================================================================
            'archive_name': 'dataset_usa_cobb-douglas.zip',
            'series_id': 'CDT2S4',
        },
        {
            'archive_name': 'dataset_douglas.zip',
            'series_id': 'DT63AS01',
        },
    )
    df = pd.concat(
        [
            partial(extract_usa_classic, **kwargs)() for kwargs in _kwargs
        ],
        axis=1
    )
    df['div'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df.dropna().plot(title='Cobb--Douglas Data Comparison', legend=True, grid=True)


def test_procedure(kwargs_list: list[dict]) -> None:
    df = pd.concat(
        [
            extract_read_usa_bea(**_kwargs) for _kwargs in kwargs_list
        ],
        axis=1,
        sort=True
    )
    df['diff_abs'] = df.iloc[:, 0].sub(df.iloc[:, 1]).sub(df.iloc[:, 2])
    df.iloc[:, [-1]].dropna(axis=0).plot(grid=True)


def test_sub_a(df: DataFrame):
    df['delta_sm'] = df.iloc[:, 0].sub(df.iloc[:, [3, 4, 5]].sum(axis=1))
    df.dropna(axis=0, inplace=True)
    autocorrelation_plot(df.iloc[:, [-1]])


def test_sub_b(df: DataFrame):
    # df['delta_eq'] = df.iloc[:, 0].sub(df.iloc[:, -1])
    df['delta_eq'] = df.iloc[:, 0].mul(4).div(
        df.iloc[:, 0].add(df.iloc[:, -1])).sub(2)
    df.dropna(axis=0, inplace=True)
    df.iloc[:, [-1]].plot(grid=True)


def test_read_usa_bea_sfat_series() -> DataFrame:
    ARCHIVE_NAME = 'dataset_usa_bea-nipa-selected.zip'
    SERIES_ID = 'k3n31gd1es000'
    _df = pd.read_csv(ARCHIVE_NAME, usecols=[0, *range(8, 11)])
    _df = _df[_df.iloc[:, 1] == SERIES_ID]
    control_frame = DataFrame()
    for source_id in sorted(set(_df.iloc[:, 0])):
        chunk = _df[_df.iloc[:, 0] == source_id].iloc[:, [2, 3]]
        chunk.columns = [chunk.columns[0],
                         ''.join((source_id.split()[1].replace('.', '_'), SERIES_ID))]
        chunk.set_index(chunk.columns[0], inplace=True, verify_integrity=True)
        control_frame = pd.concat([control_frame, chunk], axis=1, sort=True)

    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAME = 'Section4ALL_xls.xls'
    SH_NAME = '403 Ann'
    # =========================================================================
    # Fixed Assets Series, 1925--2016
    # =========================================================================
    SERIES_IDS = ('k3n31gd1es000', 'k3n31gd1eq000',
                  'k3n31gd1ip000', 'k3n31gd1st000',)
    test_frame = pd.concat(
        [
            extract_read_usa_bea(ARCHIVE_NAME, WB_NAME, SH_NAME, series_id)
            for series_id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    return pd.concat([test_frame, control_frame], axis=1, sort=True)
