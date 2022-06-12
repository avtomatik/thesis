#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:24:57 2022

@author: alexander
"""

from extract.lib import extract_usa_bea


# =============================================================================
# Separate Chunk of Code
# =============================================================================
def append_series_ids(df, chunk, series_ids):
    for series_id in series_ids:
        chunk = pd.concat(
            [
                chunk,
                df.loc[:, [series_id]].dropna(axis=0)
            ],
            axis=1, sort=False)
    return chunk


def append_series_ids_sum(df, chunk, series_ids):
    for series_id in series_ids:
        _chunk = pd.concat(
            [
                _chunk,
                df.loc[:, [series_id]].dropna(axis=0)
            ],
            axis=1, sort=False)
    series_ids.extend(['sum'])
    _chunk['_'.join(series_ids)] = _chunk.sum(1)
    return pd.concat(
        [
            chunk,
            _chunk.iloc[:, [-1]]
        ],
        axis=1, sort=False)


def convert_url(string):
    return '/'.join(('https://www150.statcan.gc.ca/n1/tbl/csv', '{}-eng.zip'.format(string.split('=')[1][:-2])))


def string_to_url(string):
    return f'https://www150.statcan.gc.ca/n1/tbl/csv/{string}'


# =============================================================================
# Section5ALL_Hist
# =============================================================================
# =============================================================================
# www.bea.gov/histdata/Releases/GDP_and_PI/2012/Q1/Second_May-31-2012/Section5ALL_Hist.xls
# =============================================================================
# =============================================================================
# Metadata: `Section5ALL_Hist.xls`@[`dataset_usa_bea-release-2010-08-05 Section5ALL_Hist.xls` Offsets `dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip`]'''
# =============================================================================
# =============================================================================
# Fixed Assets Series: K160021, 1951--1969
# =============================================================================
kwargs = {
    'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
    'wb_name': 'Section5ALL_Hist.xls',
    'sh_name': '50900 Ann',
    'series_id': 'K160021',
}
sub_frame_a = extract_usa_bea(**kwargs)


# =============================================================================
# Gross fixed capital formation Data Block
# =============================================================================
'''Not Clear: v62143969 - 380-0068 Gross fixed capital formation; Canada; Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial\
machinery and equipment (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
'''Not Clear: v62143990 - 380-0068 Gross fixed capital formation; Canada; Chained (2007) dollars; Seasonally adjusted at annual rates; Industrial\
machinery and equipment (x 1,000,000) (quarterly, 1961-03-01 to 2017-09-01)'''
# fetch_can_quarterly('03800068', 'v62143969')
# fetch_can_quarterly('03800068', 'v62143990')
# fetch_can_group_b('5245628780870031920', 3)
# fetch_can_group_a('7931814471809016759', 241)
# fetch_can_group_a('8448814858763853126', 81)
# =============================================================================
# Not Clear
# =============================================================================
# FILE_NAME = 'dataset_can_cansim-{}-eng-{}.csv'.format(0310003, 7591839622055840674)
# frame = pd.read_csv(FILE_NAME, skiprows=3)
# =============================================================================
# Unallocated
# =============================================================================
# =============================================================================
# Fixed Assets Series: k3n31gd1es000, 1947--2011
# =============================================================================
kwargs = {
    'archive_name': 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip',
    'wb_name': 'Section3ALL_xls.xls',
    'sh_name': '303ES Ann',
    'series_id': 'k3n31gd1es000',
}
semi_frame_c = extract_usa_bea(**kwargs)
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1929--1969
# =============================================================================
kwargs = {
    'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
    'wb_name': 'Section1ALL_Hist.xls',
    'sh_name': '10105 Ann',
    'series_id': 'A191RC1',
}
sub_frame_a = extract_usa_bea(**kwargs)
# =============================================================================
# Nominal Gross Domestic Product Series: A191RC1, 1969--2014
# =============================================================================
kwargs = {
    'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
    'wb_name': 'Section1all_xls.xls',
    'sh_name': '10105 Ann',
    'series_id': 'A191RC1',
}
sub_frame_b = extract_usa_bea(**kwargs)
semi_frame_d = pd.concat(
    [
        sub_frame_a,
        sub_frame_b,
    ],
    sort=True).drop_duplicates()
