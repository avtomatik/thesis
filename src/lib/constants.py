#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:18:11 2023

@author: green-machine
"""


SERIES_IDS_LAB = {
    # =========================================================================
    # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
    # =========================================================================
    # =========================================================================
    # 1929--1948
    # =========================================================================
    'H4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =========================================================================
    # 1948--1987
    # =========================================================================
    'J4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =========================================================================
    # 1987--2000
    # =========================================================================
    'A4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =========================================================================
    # 1998--2020
    # =========================================================================
    'N4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
}
ARCHIVE_NAMES_UTILISED = (
    'dataset_can_00310004-eng.zip',
    'dataset_douglas.zip',
    'dataset_rus_m1.zip',
    'dataset_usa_bea-nipa-2015-05-01.zip',
    'dataset_usa_bea-nipa-selected.zip',
    'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
    'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
    'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    'dataset_usa_bea-release-2019-12-19-Survey.zip',
    'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip',
    'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip',
    'dataset_usa_brown.zip',
    'dataset_uscb.zip',
    'dataset_usa_cobb-douglas.zip',
    'dataset_usa_infcf16652007.zip',
    'dataset_usa_kendrick.zip',
    'dataset_usa_mc_connell_brue.zip',
)
FILE_NAMES_UTILISED = (
    'dataset_rus_grigoriev_v.csv',
    'dataset_usa_0025_p_r.txt',
    'dataset_usa_bls-2015-02-23-ln.data.1.AllData',
    'dataset_usa_bls-2017-07-06-ln.data.1.AllData',
    'dataset_usa_bls-pc.data.0.Current',
    'dataset_usa_davis-j-h-ip-total.xls',
    'dataset_usa_frb_g17_all_annual_2013_06_23.csv',
    'dataset_usa_frb_invest_capital.csv',
    'dataset_usa_frb_us3_ip_2018_09_02.csv',
    'dataset_usa_nber_ces_mid_naics5811.csv',
    'dataset_usa_nber_ces_mid_sic5811.csv',
    'dataset_usa_reference_ru_kurenkov_yu_v.csv',
)
ARCHIVE_NAMES_UTILISED = (
    'dataset_douglas.zip',
    'dataset_usa_brown.zip',
    'dataset_uscb.zip',
    'dataset_usa_cobb-douglas.zip',
    'dataset_usa_kendrick.zip',
)
FILE_NAMES_UTILISED = (
    'dataset_usa_0025_p_r.txt',
    'dataset_usa_reference_ru_kurenkov_yu_v.csv',
)
ARCHIVE_NAMES_UTILISED = (
    'dataset_uscb.zip',
)
FILE_NAMES_UTILISED = (
    'dataset_usa_nber_ces_mid_naics5811.csv',
    'dataset_usa_nber_ces_mid_sic5811.csv',
)
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
