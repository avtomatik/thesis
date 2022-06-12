# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 20:39:06 2020

@author: Mastermind
"""

# =============================================================================
# TODO: Refactor
# =============================================================================


from extract.lib import extract_can_annual
from extract.lib import extract_can_group_a
from extract.lib import extract_can_group_b
from extract.lib import extract_can_quarter
from extract.lib import extract_usa_bea
from extract.lib import extract_usa_bls
from extract.lib import extract_usa_nber
from load.lib import load_data_frame_listing
from plot.lib import plot_can_test
from plot.lib import plot_usa_nber
from plot.lib import plot_usa_nber_manager
from test.lib import test_data_consistency_a
from test.lib import test_data_consistency_b
from test.lib import test_data_consistency_c
from test.lib import test_data_consistency_d
from test.lib import test_procedure
from test.lib import test_sub_a
from test.lib import test_sub_b


def test_dataset_capital_combined_archived():
    '''Data Test'''
    # =========================================================================
    # Nominal Investment Series: A006RC1, 1929--1969
    # =========================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A006RC1')
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1929--1969
    # =========================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    control_frame = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)

    # =========================================================================
    # Nominal Investment Series: A006RC1, 1929--1969
    # =========================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A006RC1')
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1929--1969
    # =========================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    test_frame = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)

    if control_frame.equals(test_frame):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1929--1969')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')

    # =========================================================================
    # Nominal Investment Series: A006RC1, 1969--2012
    # =========================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10105 Ann', 'A006RC1')
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1969--2012
    # =========================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    control_frame = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)

    # =========================================================================
    # Nominal Investment Series: A006RC1, 1969--2012
    # =========================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_a = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10105 Ann', 'A006RC1')
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1969--2012
    # =========================================================================
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(
        file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    test_frame = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)

    if control_frame.equals(test_frame):
        print('Series `A006RC1` & `A191RC1` @ Worksheet `10105 Ann` Equals Series `A006RC1` & `A191RC1` @ Worksheet `10505 Ann` for Period 1969--2012')
    else:
        print('Data Varies from Worksheet `10105 Ann` to Worksheet `10505 Ann`')


def fetch_usa_bea_sfat_series():
    archive_name = 'dataset_usa_bea-nipa-selected.zip'
    series_id = 'k3n31gd1es000'
    data_frame = pd.read_csv(archive_name, usecols=[0, *range(8, 11)])
    data_frame = data_frame[data_frame.iloc[:, 1] == series_id]
    control_frame = pd.DataFrame()
    for source_id in data_frame.iloc[:, 0].unique():
        current_frame = data_frame[data_frame.iloc[:, 0]
                                   == source_id].iloc[:, [2, 3]]
        current_frame.columns = [current_frame.columns[0],
                                 '{}{}'.format(source_id.split()[1].replace('.', '_'), series_id)]
        current_frame.set_index(
            current_frame.columns[0], inplace=True, verify_integrity=True)
        control_frame = pd.concat(
            [control_frame, current_frame], axis=1, sort=True)

    archive_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    wb_name = 'Section4ALL_xls.xls'
    sh_name = '403 Ann'
    # =========================================================================
    # Fixed Assets Series, 1925--2016
    # =========================================================================
    SERIES_IDS = ('k3n31gd1es000', 'k3n31gd1eq000',
                  'k3n31gd1ip000', 'k3n31gd1st000',)
    test_frame = pd.concat(
        [fetch_usa_bea(archive_name, wb_name, sh_name, series_id)
         for series_id in SERIES_IDS],
        axis=1,
        sort=True)

    return pd.concat([test_frame, control_frame], axis=1, sort=True)


test_data_consistency_a()
test_data_consistency_b()
test_data_consistency_c()
test_data_consistency_d()
plot_usa_nber_manager()
