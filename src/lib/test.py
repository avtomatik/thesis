#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:19:54 2022

@author: Alexander Mikhailov
"""


from thesis.src.lib.pull import pull_by_series_id
from thesis.src.lib.read import read_usa_bls
from thesis.src.lib.stockpile import stockpile_usa_bea, stockpile_usa_hist


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
    for filepath_or_buffer, series_id in SERIES_IDS.items():
        print(
            read_usa_bls(filepath_or_buffer).pipe(pull_by_series_id, series_id)
        )
