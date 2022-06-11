# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:17:48 2020

@author: Mastermind
"""


def get_data_combined():
    '''Most Up-To-Date Version'''
    # =========================================================================
    # TODO: Refactor It
    # =========================================================================
    URL = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    _data = extract_usa_bea_from_url(URL)
    SERIES_IDS = (
        'A006RC',
        'A006RD',
        'A008RC',
        'A008RD',
        'A032RC',
        'A191RA',
        'A191RC',
        'A191RX',
        'W170RC',
        'W170RX',
    )
    _data_nipa = pd.concat(
        [
            extract_usa_bea_from_loaded(_data, _id) for _id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    SERIES_IDS = (
        'H4313C',
        'J4313C',
        'A4313C',
        'N4313C',
    )
    _labor_frame = pd.concat(
        [
            extract_usa_bea_from_loaded(_data, _id) for _id in SERIES_IDS
        ],
        axis=1,
        sort=True
    )
    _labor_frame['mfg_labor'] = _labor_frame.mean(axis=1)
    _labor_frame = _labor_frame.iloc[:, [-1]]
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    )
    WB_NAMES = (
        'Section5ALL_Hist.xls',
        'Section5all_xls.xls',
    )
    SH_NAME, SERIES_ID = ('51000 Ann', 'K100701',)
    # =========================================================================
    # Fixed Assets Series: K100701, 1951--2013
    # =========================================================================
    _data_sfat = pd.concat(
        [
            extract_usa_bea(_archive, _wb, SH_NAME, SERIES_ID) for _archive, _wb in zip(ARCHIVE_NAMES, WB_NAMES)
        ],
        sort=True
    ).drop_duplicates()
    # =========================================================================
    # US BEA Fixed Assets Series Tests
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    WB_NAMES = (
        'Section1ALL_xls.xls',
        'Section2ALL_xls.xls',
    )
    SH_NAMES = (
        '105 Ann',
        '106 Ann',
        '101 Ann',
        '203 Ann',
        '202 Ann',
    )
    SERIES_IDS = (
        # =====================================================================
        # Investment in Fixed Assets, Private, i3ptotl1es000, 1901--2016
        # =====================================================================
        'i3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Index for Investment in Fixed Assets, Private, icptotl1es000, 1901--2016
        # =====================================================================
        'icptotl1es000',
        # =====================================================================
        # Current-Cost Net Stock of Fixed Assets, Private, k1ptotl1es000, 1925--2016
        # =====================================================================
        'k1ptotl1es000',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es000, 1925--2016
        # =====================================================================
        'k3ptotl1es000',
        # =====================================================================
        # Chain-Type Quantity Indexes for Net Stock of Fixed Assets, Private, kcptotl1es000, 1925--2016
        # =====================================================================
        'kcptotl1es000',
    )
    _data_sfat_ = pd.concat(
        [
            extract_usa_bea(ARCHIVE_NAME, _wb, _sh, _id) for _wb, _sh, _id in zip(
                tuple(WB_NAMES[_ // 3] for _ in range(len(SERIES_IDS))), SH_NAMES, SERIES_IDS)
        ],
        axis=1,
        sort=True
    )
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    return pd.concat(
        [
            _data_nipa,
            _labor_frame,
            _data_sfat,
            _data_sfat_,
            get_data_usa_frb_ms(),
            get_data_usa_frb_ms(),
            get_data_usa_frb_ms(),
            pd.read_csv(FILE_NAME, index_col=0),
        ],
        axis=1,
        sort=True
    )


def transform_a(df: pd.DataFrame) -> pd.DataFrame:
    df = df.iloc[:, [0, 4, 6, 7]].dropna()
    return df.div(df.iloc[0, :])


def transform_b(df: pd.DataFrame) -> pd.DataFrame:
    return df.iloc[:, [0, 6, 7, 20]].dropna()


def transform_c(df: pd.DataFrame) -> pd.DataFrame:
    df_production = df.iloc[:, [0, 6, 7]].dropna()
    df_production = df_production.div(df_production.iloc[0, :])
    df_money = df.iloc[:, range(18, 20)].dropna(how='all')
    df_money['m1_fused'] = df_money.mean(axis=1)
    df_money = df_money.iloc[:, -1].div(df_money.iloc[0, -1])
    _df = pd.concat(
        [
            df_production,
            df_money
        ],
        axis=1).dropna()
    return _df.div(_df.iloc[0, :])


def transform_d(df: pd.DataFrame) -> pd.DataFrame:
    # =========================================================================
    # TODO: Eliminate This Function
    # =========================================================================
    return df.iloc[:, [0, 1, 2, 3, 7]].dropna()


def transform_e(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    assert df.shape[1] == 21, 'Works on DataFrame Produced with `get_data_combined_archived()`'
    # =========================================================================
    # `Real` Investment
    # =========================================================================
    df['inv'] = df.iloc[:, 0].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    # =========================================================================
    # `Real` Capital
    # =========================================================================
    df['cap'] = df.iloc[:, 11].mul(df.iloc[:, 7]).div(df.iloc[:, 6])
    return (
        # =====================================================================
        # DataFrame Nominal
        # =====================================================================
        df.iloc[:, [0, 6, 11]].dropna(),
        # =====================================================================
        # DataFrame `Real`
        # =====================================================================
        df.iloc[:, [-2, 7, -1]].dropna(),
    )


source_frame_a = get_dataset_combined_archived()
source_frame_b = get_dataset_combined()
# =============================================================================
# Project: Initial Version Dated: 05 October 2012
# =============================================================================
result_frame_a_b = transform_a(source_frame_a)
result_frame_a_c = transform_a(source_frame_b)
plot_a(result_frame_a_b)
plot_a(result_frame_a_c)
# =============================================================================
# Project: Initial Version Dated: 23 November 2012
# =============================================================================
result_frame_b_b = transform_b(source_frame_a)
result_frame_b_c = transform_b(source_frame_b)
plot_b(result_frame_b_b)
plot_b(result_frame_b_c)
# =============================================================================
# Project: Initial Version Dated: 16 June 2013
# =============================================================================
result_frame_c_b = transform_c(source_frame_a)
result_frame_c_c = transform_c(source_frame_b)
plot_c(result_frame_c_b)
plot_c(result_frame_c_c)
# =============================================================================
# Project: Initial Version Dated: 15 June 2015
# =============================================================================
result_frame_d = transform_d(source_frame_b)
plot_d(result_frame_d)
# =============================================================================
# Project: Initial Version Dated: 17 February 2013
# =============================================================================
result_frame_e_a, result_frame_e_b = transform_e(source_frame_a)
plot_e(result_frame_e_a)
plot_e(result_frame_e_b)
# =============================================================================
# Project: BEA Data Compared with Kurenkov Yu.V. Data
# =============================================================================
result_frame_f_a, result_frame_f_b, result_frame_f_c, result_frame_f_d = transform_f(
    source_frame_a)
plot_f(result_frame_f_a, result_frame_f_b, result_frame_f_c, result_frame_f_d)
