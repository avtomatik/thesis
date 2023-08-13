#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:19:54 2022

@author: Alexander Mikhailov
"""


from .backend import stockpile
from .read import read_usa_bls


def options_reviewed():
    SERIES_IDS = (
        # =====================================================================
        # The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
        # =====================================================================
        [SeriesID('DT24AS01', Dataset.DOUGLAS)],
        # =====================================================================
        # Not Suitable: Total Capital (in millions of 1880 dollars)
        # =====================================================================
        [SeriesID('DT63AS01', Dataset.DOUGLAS)],
        # =====================================================================
        # Not Suitable: Annual Increase (in millions of 1880 dollars)
        # =====================================================================
        [SeriesID('DT63AS02', Dataset.DOUGLAS)],
        # =====================================================================
        # Not Suitable: Percentage Rate of Growth
        # =====================================================================
        [SeriesID('DT63AS03', Dataset.DOUGLAS)]
    )

    for series_id in SERIES_IDS:
        print(stockpile(series_id))


def test_data_usa_bea():
    """Project II: USA Fixed Assets Data Comparison"""

    SERIES_IDS = {
        # =====================================================================
        # Fixed Assets Series: k1ntotl1si00, 1925--2016
        # =====================================================================
        'k1ntotl1si00': URL.FIAS,
        # =====================================================================
        # Fixed Assets Series: kcntotl1si00, 1925--2016
        # =====================================================================
        'kcntotl1si00': URL.FIAS,
        # =====================================================================
        # Not Used: Fixed Assets: k3ntotl1si00, 1925--2016, Table 2.3. Historical-Cost Net Stock of Private Fixed Assets, Equipment, Structures, and Intellectual Property Products by Type
        # =====================================================================
        'k3ntotl1si00': URL.FIAS,
    }
    return stockpile(SERIES_IDS)


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
