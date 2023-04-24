# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 22:29:22 2020

Thesis Project

@author: Alexander Mikhailov
"""


import cobb_douglas_can
import cobb_douglas_complex
import elasticity
import plot_usa_bea
import plot_usa_manufacturing
import usa_bea_approximation
import usa_capital
import usa_complex
import usa_mc_connell

import lash_up_spline
from thesis.src.common import get_fig_map_us_ma
from thesis.src.lib.plot import plot_cobb_douglas, plot_douglas
from thesis.src.lib.stockpile import stockpile_usa_hist
from thesis.src.lib.transform import transform_cobb_douglas


def main():
    
    usa_bea_approximation()

    usa_mc_connell()

    usa_capital()

    cobb_douglas_complex()

    cobb_douglas_can()

    elasticity()

    lash_up_spline()

    usa_complex()

    # =========================================================================
    # Subproject IX. USA BEA
    # =========================================================================
    plot_usa_bea()
    # =========================================================================
    # Subproject X. USA Census
    # =========================================================================
    # =========================================================================
    # Subproject XI. USA Census J14
    # =========================================================================
    plot_usa_manufacturing()
    # =========================================================================
    # Subproject XII. USA Douglas & Kendrick
    # =========================================================================
    # =========================================================================
    # Douglas European Demographics & Growth of US Capital
    # =========================================================================
    ARCHIVE_NAME = 'dataset_douglas.zip'
    # GROUP_ITERS = (
    #     0,
    #     12,
    #     23,
    #     34,
    #     45,
    #     55,
    #     66,
    #     76,
    #     86,
    #     89,
    #     90,
    #     93,
    #     96,
    #     99,
    #     102,
    #     105,
    #     111,
    #     114,
    #     117,
    #     121,
    #     124,
    #     90,
    #     115,
    # )
    GROUP_ITERS = (
        # =====================================================================
        # TODO: Confirm
        # Table XXVII Birth, Death And Net Fertility Rates For Denmark, 1800-1931, Source: Danmarks Statistik, Statistisk Aarbog.
        # DT27BS01
        # DT27BS02
        # DT27BS03
        #
        # Table 62 Estimated Total British Capital In Terms Of The 1865 Price Level Invested Inside And Outside The United Kingdom By Years From 1865 To 1909, And Rate Of Growth Of This Capital
        # DT62AS01
        # DT62AS02
        # DT62AS03
        # DT62AS04
        #
        # Table 63 Growth Of Capital In The United States, 1880-1922
        # DT63AS01
        # DT63AS01
        # DT63AS02
        # =====================================================================
        0,
        12,
        23,
        34,
        45,
        55,
        66,
        76,
        86,
        89,
        90,
        93,
        96,
        99,
        102,
        105,
        111,
        114,
        117,
        121,
        124,
        99,
        124,
    )
    TITLES = (
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
        'Chart 67. Birth, Death, and Net Fertility Rates in Sweden, 1750$-$1931\nTable XXV Birth, Death and Net Fertility Rates for Sweden, 1750$-$1931,\nSource: Computed from data given in the Statistisk ?rsbok for Sverige.',
        'Chart 68. Birth, Death, and Net Fertility Rates in Norway, 1801$-$1931\nTable XXVI Birth, Death and Net Fertility Rates for Norway, 1801$-$1931,\nSource: Statistisk ?rbok for Kongeriket Norge.',
        'Chart 69. Birth, Death, and Net Fertility Rates in Denmark, 1800$-$1931\nTable XXVII Birth, Death and Net Fertility Rates for Denmark, 1800$-$1931,\nSource: Danmarks Statistik, Statistisk Aarbog.',
        'Chart 70. Birth, Death, and Net Fertility Rates in Great Britain, 1850$-$1932\nTable XXVIII Birth, Death and Net Fertility Rates for England and Wales, 1850$-$1932,\nSource: Statistical Abstract for the United Kingdom.',
        'Chart 71. Birth, Death, and Net Fertility Rates in France, 1801$-$1931\nTable XXIX Birth, Death and Net Fertility Rates for France, 1801$-$1931,\nSource: Statistique generale de la France: Mouvement de la Population.',
        'Chart 72$\'$. Birth, Death, and Net Fertility Rates in Germany, 1871$-$1931\nTable XXX Birth, Death And Net Fertility Rates For:\n(A) Germany, 1871$-$1931\n(B) Prussia, 1816$-$1930\nSource: Statistisches Jahrbuch fur das Deutsche Reich.',
        'Chart 73. Birth, Death, and Net Fertility Rates in Switzerland, 1871$-$1931\nTable XXXI Birth, Death and Net Fertility Rates for Switzerland, 1871$-$1931,\nSource: Statistisches Jahrbuch der Schweiz.',
        'Chart 74. Birth, Death, and Net Fertility Rates in Italy, 1862$-$1931\nTable XXXII Birth, Death and Net Fertility Rates for Italy, 1862$-$1931,\nSource: Annuario Statistico Italiano.',
        'Table 62 Estimated Total British Capital In Terms of the 1865 Price Level\nInvested Inside and Outside the United Kingdom by Years From\n1865 to 1909, and Rate of Growth of This Capital',
        'Table 63 Growth of Capital in the United States, 1880$-$1922',
        'Birth Rates by Countries',
    )
    TITLES_DEU = (
        'Germany Birth Rate', 'Germany Death Rate', 'Germany Net Fertility Rate',
        'Prussia Birth Rate', 'Prussia Death Rate', 'Prussia Net Fertility Rate',
    )
    TITLES_EUR = (
        'Sweden', 'Norway', 'Denmark', 'England & Wales', 'France', 'Germany',
        'Prussia', 'Switzerland', 'Italy',
    )
    MEASURES = (
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
        'Births Rate Per 1000 People',
    )

    LABELS = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        TITLES_DEU,
        None,
        None,
        None,
        None,
        TITLES_EUR,
    )

    plot_douglas(
        ARCHIVE_NAME,
        GROUP_ITERS[:-2],
        TITLES[:-1],
        MEASURES[:-1],
        LABELS
    )
    plot_douglas(
        ARCHIVE_NAME,
        GROUP_ITERS[-2:],
        (TITLES[-1],),
        (MEASURES[-1],),
        (LABELS[-1],),
        len(TITLES),
        3
    )

    # =========================================================================
    # Douglas Production Function
    # =========================================================================
    # =========================================================================
    # Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928 & P.H. Douglas. The Theory of Wages, 1934;
    # =========================================================================
    YEAR_BASE = 1899
    MAP_FIG_US_MA = get_fig_map_us_ma(YEAR_BASE)
    SERIES_IDS = {
        'DT19AS03': 'dataset_douglas.zip',
        'DT19AS02': 'dataset_douglas.zip',
        'DT19AS01': 'dataset_douglas.zip'
    }
    plot_cobb_douglas(
        *stockpile_usa_hist(SERIES_IDS).pipe(transform_cobb_douglas, year_base=YEAR_BASE), MAP_FIG_US_MA)
    # =========================================================================
    # Kendrick Macroeconomic Series
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
    GROUP_ITERS = (
        0,
        8,
        19,
        30,
        38,
        46,
        54,
        60,
        72,
        84,
        96,
        100,
        111,
        118,
    )
    TITLES = (
        'Table A-I Gross And Net National Product, Adjusted Kuznets Concepts, Peacetime And National Security Version, 1869$-$1957 (Millions Of 1929 Dollars)',
        'Table A-IIa Gross National Product, Commerce Concept, Derivation From Kuznets Estimates, 1869$-$1957 (Millions Of 1929 Dollars)',
        'Table A-IIb Gross National Product, Commerce Concept, Derivation From Kuznets Estimates, 1869$-$1929; And Reconciliation With Kuznets Estimates, 1937, 1948, And 1953 (Millions Of Current Dollars)',
        'Table A-III National Product, Commerce Concept, By Sector, 1869$-$1957 (Millions Of 1929 Dollars)',
        'Table A-VI National Economy. Persons Engaged, By Major Sector, 1869$-$1957 (Thousands)',
        'Table A-X National Economy: Manhours, By Major Sector, 1869$-$1957 (Millions)',
        'Table A-XV National Economy: Real Capital Stocks, By Major Sector, 1869$-$1957 (Millions Of 1929 Dollars)',
        'Table A-XVI Domestic Economy And Private Sectors: Real Capital Stocks, By Major Type, 1869$-$1953 (Millions Of 1929 Dollars)',
        'Table A-XIX National Economy: Real Net Product, Inputs, And Productivity Ratios, Kuznets Concept, National Security Version, 1869$-$1957 (1929=100)',
        'Table A-XXII Private Domestic Economy. Real Gross Product, Inputs, And Productivity Ratios, Commerce Concept, 1869$-$1957 (1929=100)',
        'Table A-XXII: Supplement Private Domestic Economy: Productivity Ratios Based On Unweighted Inputs, 1869$-$1957 (1929=100)',
        'Table A-XXIII Private Domestic Nonfarm Economy: Real Gross Product, Inputs, And Productivity Ratios, Commerce Concept, 1869$-$1957 (1929=100)',
        'Table D-II. Manufacturing: Output, Labor Inputs, and Labor Productivity Ratios, 1869-1957 (1929=100)',
    )
    MEASURES = (
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
        'Percentage',
    )

    plot_douglas(ARCHIVE_NAME, GROUP_ITERS, TITLES, MEASURES)


if __name__ == '__main__':
    main()
