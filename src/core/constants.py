#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:18:11 2023

@author: green-machine
"""


FILE_NAMES_UTILISED = (
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


TITLES_DOUGLAS = (
    'Table I Indexes of Physical Production, 1899=100 [1899$-$1926]',
    'Table II Wholesale Price Indexes, 1899=100 [1899$-$1928]',
    'Table III Exchange Value = Ratio of Wholesale Prices to General Price Level: Nine Groups and Manufacturing [1899$-$1928]',
    'Table IV Relative Total Value Product for Nine Groups and All Manufacturing [1899$-$1926]',
    'Table V Employment Index: Nine Industries and Manufacturing, 1899$-$1927',
    'Table VI Value Product Per Employee: Nine Industries and Manufacturing, 1899$-$1926',
    'Table VII Index of Money Wages: Nine Groups and Manufacturing, 1899$-$1927',
    'Table VIII Index of Real Wages: Nine Groups and Manufacturing, 1899$-$1926',
    'Table 19 The Movement of Labor, Capital, and Product In\nMassachusetts Manufacturing, 1890$-$1926, 1899=100',
    'Table 24 The Revised Index of Physical Production for\nAll Manufacturing in the United States, 1899$-$1926',
    '\n'.join(
        [
            'Chart 67. Birth, Death, and Net Fertility Rates in Sweden, 1750$-$1931.',
            'Table XXV Birth, Death and Net Fertility Rates for Sweden, 1750$-$1931.',
            'Source: Computed from data given in the Statistisk årsbok för Sverige.'
        ]
    ),
    '\n'.join(
        [
            'Chart 68. Birth, Death, and Net Fertility Rates in Norway, 1801$-$1931.',
            'Table XXVI Birth, Death and Net Fertility Rates for Norway, 1801$-$1931.',
            'Source: Statistisk årbok for Kongeriket Norge.'
        ]
    ),
    '\n'.join(
        [
            'Chart 69. Birth, Death, and Net Fertility Rates in Denmark, 1800$-$1931.',
            'Table XXVII Birth, Death and Net Fertility Rates for Denmark, 1800$-$1931.',
            'Source: Danmarks Statistik, Statistisk Aarbog.'
        ]
    ),
    '\n'.join(
        [
            'Chart 70. Birth, Death, and Net Fertility Rates in Great Britain, 1850$-$1932.',
            'Table XXVIII Birth, Death and Net Fertility Rates for England and Wales, 1850$-$1932.',
            'Source: Statistical Abstract for the United Kingdom.'
        ]
    ),
    '\n'.join(
        [
            'Chart 71. Birth, Death, and Net Fertility Rates in France, 1801$-$1931.',
            'Table XXIX Birth, Death and Net Fertility Rates for France, 1801$-$1931.',
            'Source: Statistique générale de la France: Mouvement de la Population.'
        ]
    ),
    '\n'.join(
        [
            'Chart 72$\'$. Birth, Death, and Net Fertility Rates in Germany, 1871$-$1931.',
            'Table XXX Birth, Death And Net Fertility Rates For:',
            '(A) Germany, 1871$-$1931;',
            '(B) Prussia, 1816$-$1930.',
            'Source: Statistisches Jahrbuch für das Deutsche Reich.'
        ]
    ),
    '\n'.join(
        [
            'Chart 73. Birth, Death, and Net Fertility Rates in Switzerland, 1871$-$1931.',
            'Table XXXI Birth, Death and Net Fertility Rates for Switzerland, 1871$-$1931.',
            'Source: Statistisches Jahrbuch der Schweiz.'
        ]
    ),
    '\n'.join(
        [
            'Chart 74. Birth, Death, and Net Fertility Rates in Italy, 1862$-$1931.',
            'Table XXXII Birth, Death and Net Fertility Rates for Italy, 1862$-$1931.',
            'Source: Annuario Statistico Italiano.'
        ]
    ),
    '\n'.join(
        [
            'Table 62 Estimated Total British Capital In Terms of the 1865 Price Level.',
            'Invested Inside and Outside the United Kingdom by Years From 1865 to 1909, and Rate of Growth of This Capital'
        ]
    ),
    'Table 63 Growth of Capital in the United States, 1880$-$1922',
)


DATA_PLOT_DOUGLAS = {
    "TITLES_DOUGLAS": TITLES_DOUGLAS
}


TITLES_DEU = [
    'Germany Birth Rate',
    'Germany Death Rate',
    'Germany Net Fertility Rate',
    'Prussia Birth Rate',
    'Prussia Death Rate',
    'Prussia Net Fertility Rate',
]


COUNTRIES = [
    'Sweden',
    'Norway',
    'Denmark',
    'England And Wales',
    'France',
    'Germany',
    'Prussia',
    'Switzerland',
    'Italy'
]


TITLES_KENDRICK = (
    'Table A-I Gross And Net National Product, Adjusted Kuznets Concepts, Peacetime And National Security Version, 1869$-$1957 (Millions Of 1929 Dollars)',
    'Table A-IIa Gross National Product, Commerce Concept, Derivation From Kuznets Estimates, 1869$-$1957 (Millions Of 1929 Dollars)',
    'Table A-IIb Gross National Product, Commerce Concept, Derivation From Kuznets Estimates, 1869$-$1929; And Reconciliation With Kuznets Estimates, 1937, 1948, And 1953 (Millions Of Current Dollars)',
    'Table A-III National Product, Commerce Concept, By Sector, 1869$-$1957 (Millions Of 1929 Dollars)',
    'Table A-VI National Economy. Persons Engaged, By Major Sector, 1869$-$1957 (Thousands)',
    'Table A-X National Economy: Manhours, By Major Sector, 1869$-$1957 (Millions)',
    'Table A-XV National Economy: Real Capital Stocks, By Major Sector, 1869$-$1957 (Millions Of 1929 Dollars)',
    'Table A-XVI Domestic Economy And Private Sectors: Real Capital Stocks, By Major Type, 1869$-$1953 (Millions Of 1929 Dollars)',
    'Table A-XIX National Economy: Real Net Product, Inputs, And Productivity Ratios, Kuznets Concept, National Security Version, 1869$-$1957 (1929=100)',
    '\n'.join(
        [
            'Table A-XXII Private Domestic Economy. Real Gross Product, Inputs, And Productivity Ratios, Commerce Concept, 1869$-$1957 (1929=100)',
            'Table A-XXII: Supplement Private Domestic Economy: Productivity Ratios Based On Unweighted Inputs, 1869$-$1957 (1929=100)'
        ]
    ),
    'Table A-XXIII Private Domestic Nonfarm Economy: Real Gross Product, Inputs, And Productivity Ratios, Commerce Concept, 1869$-$1957 (1929=100)',
    'Table D-II. Manufacturing: Output, Labor Inputs, and Labor Productivity Ratios, 1869-1957 (1929=100)',
)


YLABELS_DOUGLAS = (
    'Percentage',
    'Percentage',
    'Percentage',
    'Percentage',
    'Percentage',
    'Percentage',
    'Percentage',
    'Percentage',
    'Percentage',
    'Percentage',
    'Rate Per 1000',
    'Rate Per 1000',
    'Rate Per 1000',
    'Rate Per 1000',
    'Rate Per 1000',
    'Rate Per 1000',
    'Rate Per 1000',
    'Rate Per 1000',
    'Mixed',
    'Millions of Dollars',
)


YLABELS_KENDRICK = (
    'Millions Of 1929 Dollars',
    'Millions Of 1929 Dollars',
    'Millions Of Current Dollars',
    'Millions Of 1929 Dollars',
    'Thousands',
    'Millions',
    'Millions Of 1929 Dollars',
    'Millions Of 1929 Dollars',
    'Percentage',
    'Percentage',
    'Percentage',
    'Percentage',
)


MAP_READ_CAN = {
    310004: dict(zip(['category', 'component', 'period', 'prices', 'series_id', 'value'], [4, 5, 0, 2, 6, 8])),
    2820011: dict(zip(['classofworker', 'geo', 'industry', 'period', 'series_id', 'sex', 'value'], [2, 1, 3, 0, 5, 4, 7])),
    2820012: dict(zip(['period', 'series_id', 'value'], [0, 5, 7])),
    3790031: dict(zip(['geo', 'naics', 'period', 'prices', 'seas', 'series_id', 'value'], [1, 4, 0, 3, 2, 5, 7])),
    3800084: dict(zip(['est', 'geo', 'period', 'seas', 'series_id', 'value'], [3, 1, 0, 2, 4, 6])),
    3800102: dict(zip(['period', 'series_id', 'value'], [0, 4, 6])),
    3800106: dict(zip(['period', 'series_id', 'value'], [0, 3, 5])),
    3800518: dict(zip(['period', 'series_id', 'value'], [0, 4, 6])),
    3800566: dict(zip(['period', 'series_id', 'value'], [0, 3, 5])),
    3800567: dict(zip(['period', 'series_id', 'value'], [0, 4, 6])),
    14100027: dict(zip(['period', 'series_id', 'value'], [0, 10, 12])),
    14100235: dict(zip(['period', 'series_id', 'value'], [0, 8, 10])),
    16100053: dict(zip(['period', 'series_id', 'value'], [0, 9, 11])),
    36100096: dict(zip(['category', 'component', 'geo', 'industry', 'period', 'prices', 'series_id', 'value'], [5, 6, 1, 4, 0, 3, 11, 13])),
    36100207: dict(zip(['period', 'series_id', 'value'], [0, 9, 11])),
    36100303: dict(zip(['period', 'series_id', 'value'], [0, 9, 11])),
    36100305: dict(zip(['period', 'series_id', 'value'], [0, 9, 11])),
    36100434: dict(zip(['period', 'series_id', 'value'], [0, 10, 12]))
}


SERIES_IDS_PRCH = {
    'P0107': 'dataset_uscb.zip',
    'P0110': 'dataset_uscb.zip',
}


ARCHIVE_NAME = 'dataset_uscb.zip'

SERIES_IDS = [
    'E0007',
    'E0023',
    'E0040',
    'E0068',
    # =========================================================================
    # Warren & Pearson
    # =========================================================================
    'L0002' or 'E0052',
    'L0015',
] + [
    # =========================================================================
    # Less Preferrable
    # =========================================================================
    'E0008',
    # =========================================================================
    # Snyder-Tucker
    # =========================================================================
    'L0001',
] + [
    # =========================================================================
    # Least Preferrable
    # =========================================================================
    'E0009',
    'L0037',
]

SERIES_IDS_CB = dict.fromkeys(SERIES_IDS, ARCHIVE_NAME)
