# -*- coding: utf-8 -*-
'''
Created on Tue Mar 10 22:29:22 2020

Thesis Project

@author: Alexander Mikhailov
'''


import os
from collect.lib import collect_archived
from collect.lib import collect_can
from collect.lib import collect_census_a
from collect.lib import collect_census_b_a
from collect.lib import collect_census_b_b
from collect.lib import collect_census_c
from collect.lib import collect_census_e
from collect.lib import collect_census_f
from collect.lib import collect_census_g
from collect.lib import collect_census_i_a
from collect.lib import collect_census_i_b
from collect.lib import collect_census_i_c
from collect.lib import collect_census_j
from collect.lib import collect_cobb_douglas
from collect.lib import collect_combined
from collect.lib import collect_combined_archived
from collect.lib import collect_douglas
from collect.lib import collect_updated
from collect.lib import collect_usa_mcconnel
from collect.lib import collect_version_a
from collect.lib import collect_version_b
from collect.lib import collect_version_c
from collect.lib import transform_a
from collect.lib import transform_b
from collect.lib import transform_c
from collect.lib import transform_cobb_douglas
from collect.lib import transform_d
from collect.lib import transform_e
from collect.lib import transform_kurenkov
from extract.lib import extract_series_ids
from extract.lib import extract_usa_census
from plot.lib import plot_a
from plot.lib import plot_approx_linear
from plot.lib import plot_approx_log_linear
from plot.lib import plot_b
from plot.lib import plot_c
from plot.lib import plot_capital_modelling
from plot.lib import plot_census_a
from plot.lib import plot_census_b_capital
from plot.lib import plot_census_b_deflator
from plot.lib import plot_census_c
from plot.lib import plot_census_complex
from plot.lib import plot_census_d
from plot.lib import plot_census_e
from plot.lib import plot_census_f_a
from plot.lib import plot_census_f_b
from plot.lib import plot_census_g
from plot.lib import plot_census_h
from plot.lib import plot_census_i_a
from plot.lib import plot_census_i_b
from plot.lib import plot_census_i_c
from plot.lib import plot_census_j
from plot.lib import plot_census_k
from plot.lib import plot_cobb_douglas
from plot.lib import plot_cobb_douglas_3d
from plot.lib import plot_cobb_douglas_complex
from plot.lib import plot_d
from plot.lib import plot_douglas
from plot.lib import plot_e
from plot.lib import plot_elasticity
from plot.lib import plot_ewm
from plot.lib import plot_fourier_discrete
from plot.lib import plot_growth_elasticity
from plot.lib import plot_kol_zur_filter
from plot.lib import plot_kurenkov
from plot.lib import plot_pearson_r_test
from plot.lib import plot_rolling_mean_filter
from toolkit.lib import calculate_power_function_fit_params_a
from toolkit.lib import calculate_power_function_fit_params_b
from toolkit.lib import calculate_power_function_fit_params_c
from toolkit.lib import m_spline_ea
from toolkit.lib import m_spline_eb
from toolkit.lib import m_spline_la
from toolkit.lib import m_spline_lb
from toolkit.lib import m_spline_lls
from toolkit.lib import m_spline_manager


ARCHIVE_NAMES_UTILISED = (
    'CHN_TUR_GDP.zip',
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
    'dataset_usa_census1949.zip',
    'dataset_usa_census1975.zip',
    'dataset_usa_cobb-douglas.zip',
    'dataset_usa_infcf16652007.zip',
    'dataset_usa_kendrick.zip',
    'dataset_usa_mc_connell_brue.zip',
)
FILE_NAMES_UTILISED = (
    'datasetAutocorrelation.txt',
    'dataset_rus_grigoriev_v.csv',
    'dataset_usa_0022_m1.txt',
    'dataset_usa_0025_p_r.txt',
    'dataset_usa_bea-GDPDEF.xls',
    'dataset_usa_bls-2015-02-23-ln.data.1.AllData',
    'dataset_usa_bls-2017-07-06-ln.data.1.AllData',
    'dataset_usa_bls-pc.data.0.Current',
    'dataset_usa_bls_cpiai.txt',
    'dataset_usa_davis-j-h-ip-total.xls',
    'dataset_usa_frb_g17_all_annual_2013_06_23.csv',
    'dataset_usa_frb_invest_capital.csv',
    'dataset_usa_frb_us3_ip_2018_09_02.csv',
    'dataset_usa_nber_ces_mid_naics5811.csv',
    'dataset_usa_nber_ces_mid_sic5811.csv',
    'dataset_usa_reference_ru_kurenkov_yu_v.csv',
)


print(__doc__)


def main():
    FOLDER = '/media/alexander/321B-6A94'
    os.chdir(FOLDER)
    # =========================================================================
    # Subproject I. Approximation
    # =========================================================================
    # =============================================================================
    # `plot_approx_linear`: Linear Approximation,
    # `plot_approx_log_linear`: Log-Linear Approximation,
    # `calculate_power_function_fit_params_a`: Power Function Approximation,
    # `calculate_power_function_fit_params_b`: Power Function Approximation,
    # `calculate_power_function_fit_params_c`: Power Function Approximation
    # =============================================================================
    _df = collect_combined_archived()
    plot_approx_linear(_df.iloc[:, [7, 6, 0, 6]].dropna())
    plot_approx_log_linear(_df.iloc[:, [7, 6, 20, 4]].dropna())
    plot_approx_log_linear(_df.iloc[:, [7, 6, 20, 6]].dropna())

    SERIES_IDS = ('A191RC1',)
    calculate_power_function_fit_params_a(
        collect_usa_mcconnel(SERIES_IDS), (2800, 0.01, 0.5,)
    )
    SERIES_IDS = ('prime_rate', 'A032RC1',)
    calculate_power_function_fit_params_b(
        collect_usa_mcconnel(SERIES_IDS), (4, 12, 9000, 3000, 0.87,)
    )
    SERIES_IDS = ('prime_rate', 'A006RC1',)
    calculate_power_function_fit_params_c(
        collect_usa_mcconnel(SERIES_IDS), (1.5, 19, 1.7, 1760,)
    )

    # =========================================================================
    # Subproject II. Capital
    # =========================================================================
    # =============================================================================
    # Project: Fixed Assets Dynamics Modelling:
    # Fixed Assets Turnover Linear Approximation
    # Gross Fixed Investment to Gross Domestic Product Ratio Linear Approximation
    # Alpha: Investment to Capital Conversion Ratio Dynamics
    # Original Result on Archived Data:
    # {
    #     's_1': -7.28110931679034e-05,
    #     's_2': 0.302917968959722,
    # }
    # Original Result on Archived Data:
    # {
    #     'λ1': -0.000413347827690062,
    #     'λ2': 1.18883834418742,
    #
    # }
    # =============================================================================
    df_a, df_b = collect_archived()
    df_c, df_d = collect_updated()
    plot_capital_modelling(df_a, 2005)
    plot_capital_modelling(df_c, 2012)
    # =============================================================================
    # Project: Discrete Fourier Transform based on Simpson's Rule Applied to Fixed Assets of the US
    # =============================================================================
    plot_fourier_discrete(df_b)
    plot_fourier_discrete(df_d)

    # =========================================================================
    # Subproject IV. Cobb--Douglas
    # =========================================================================
    # =========================================================================
    # On Original Dataset
    # =========================================================================
    _df = collect_cobb_douglas(5)
    df_a = _df.iloc[:, range(3)]
    df_b = _df.iloc[:, [0, 1, 3]]
    df_c = _df.iloc[:, [0, 1, 4]]
    # =========================================================================
    # On Expanded Dataset
    # =========================================================================
    df_d, df_e = collect_version_a()
    df_f, df_g, df_h = collect_version_b()
    plot_cobb_douglas_complex(df_a)
    plot_cobb_douglas_complex(df_b)
    plot_cobb_douglas_complex(df_c)
    # =========================================================================
    # No Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_d)
    # =========================================================================
    # Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_e)
    # =========================================================================
    # Option: 1929--2013, No Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_f)
    # =========================================================================
    # Option: 1967--2013, No Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_g)
    # =========================================================================
    # Option: 1967--2012, Capacity Utilization Adjustment
    # =========================================================================
    plot_cobb_douglas_complex(df_h)
    # plot_cobb_douglas_complex(collect_version_c())

    # =========================================================================
    # Subproject V. Cobb--Douglas CAN
    # =========================================================================
    # =========================================================================
    # First Figure: Exact Correspondence with `Note INTH05 2014-07-10.docx`
    # =========================================================================
    MAP_FIG = {
        'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_price': 2007,
    }
    _df = collect_can()
    _df = _df.div(_df.iloc[0, :])
    plot_cobb_douglas(
        *transform_cobb_douglas(_df),
        MAP_FIG
    )
    plot_cobb_douglas_3d(_df.iloc[:, range(3)])

    # =========================================================================
    # Subproject VI. Elasticity
    # =========================================================================
    _df = collect_combined_archived()
    df_a = _df.iloc[:, [7, 6, 4]].dropna()
    df_b = _df.iloc[:, [4]].dropna()
    plot_elasticity(df_a)
    # plot_growth_elasticity(df_b)

    # =========================================================================
    # Subproject VII. MSpline
    # =========================================================================
    # =========================================================================
    # Makeshift Splines
    # =========================================================================
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df = transform_cobb_douglas(collect_cobb_douglas())[0].iloc[:, [6]]
    # =========================================================================
    # Option 1
    # =========================================================================
    m_spline_manager(df, m_spline_lls)
    # =========================================================================
    # Option 2.1.1
    # =========================================================================
    m_spline_manager(df, m_spline_ea)
    # =========================================================================
    # Option 2.1.2
    # =========================================================================
    m_spline_manager(df, m_spline_eb)
    # =========================================================================
    # Option 2.2.1
    # =========================================================================
    m_spline_manager(df, m_spline_la)
    # =========================================================================
    # Option 2.2.2
    # =========================================================================
    m_spline_manager(df, m_spline_lb)

    # =========================================================================
    # Subproject VIII. Multiple
    # =========================================================================
    df = collect_cobb_douglas()

    for _, column in enumerate(df.columns):
        plot_census_complex(df.iloc[:, [_]])

    SERIES_IDS = (
        'D0004', 'D0130', 'F0003', 'F0004', 'P0110', 'U0001', 'U0008', 'X0414', 'X0415',
    )
    for series_id in SERIES_IDS:
        print(f'Processing {series_id}')
        df = extract_usa_census('dataset_usa_census1975.zip', series_id)
        _df = df.copy(deep=True)
        plot_pearson_r_test(_df)
        _df = df.copy(deep=True)
        plot_kol_zur_filter(_df)
        _df = df.copy(deep=True)
        plot_ewm(_df)

    # =========================================================================
    # Subproject IX. USA BEA
    # =========================================================================
    _df_a = collect_combined_archived()
    _df_b = collect_combined()
    # =========================================================================
    # Project: Initial Version Dated: 05 October 2012
    # =========================================================================
    df_a_a = transform_a(_df_a)
    df_a_b = transform_a(_df_b)
    plot_a(df_a_a)
    plot_a(df_a_b)
    # =========================================================================
    # Project: Initial Version Dated: 23 November 2012
    # =========================================================================
    df_b_a = transform_b(_df_a)
    df_b_b = transform_b(_df_b)
    plot_b(df_b_a)
    plot_b(df_b_b)
    # =========================================================================
    # Project: Initial Version Dated: 16 June 2013
    # =========================================================================
    df_c_a = transform_c(_df_a)
    df_c_b = transform_c(_df_b)
    plot_c(df_c_a)
    plot_c(df_c_b)
    # =========================================================================
    # Project: Initial Version Dated: 15 June 2015
    # =========================================================================
    plot_d(transform_d(_df_b))
    # =========================================================================
    # Project: Initial Version Dated: 17 February 2013
    # =========================================================================
    df_e_a, df_e_b = transform_e(_df_a)
    plot_e(df_e_a)
    plot_e(df_e_b)
    # =========================================================================
    # Project: BEA Data Compared with Kurenkov Yu.V. Data
    # =========================================================================
    plot_kurenkov(transform_kurenkov(_df_a))

    # =========================================================================
    # Subproject X. USA Census
    # =========================================================================
    plot_census_a(*collect_census_a())
    plot_census_b_capital(collect_census_b_a())
    plot_census_b_deflator(collect_census_b_b())
    plot_census_c(*collect_census_c())
    # =========================================================================
    # Census Production Series
    # =========================================================================
    SERIES_IDS = (
        'P0248', 'P0249', 'P0250', 'P0251', 'P0262',
        'P0265', 'P0266', 'P0267', 'P0268', 'P0269',
        'P0293', 'P0294', 'P0295',
    )
    ids = itertools.chain(
        range(231, 242),
        range(244, 245),
        range(247, 272),
        range(277, 278),
        range(279, 280),
        range(281, 285),
        range(286, 287),
        range(288, 289),
        range(290, 291),
        range(293, 301),
    )
    SERIES_IDS_ALT = tuple(f'P{_id:04n}' for _id in ids)

    plot_census_d(SERIES_IDS)
    plot_census_e(collect_census_e())
    df = collect_census_f()
    plot_census_f_a(df)
    plot_census_f_b(df)
    plot_census_g(collect_census_g())
    plot_census_h()
    plot_census_i_a(collect_census_i_a())
    plot_census_i_b(collect_census_i_b())
    plot_census_i_c(collect_census_i_c())
    plot_census_j(collect_census_j())
    plot_census_k()

    # =========================================================================
    # Subproject XI. USA Census J14
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_census1949.zip'
    SERIES_ID = 'J0014'

    df = extract_usa_census(ARCHIVE_NAME, SERIES_ID)
    _df = df.copy(deep=True)
    plot_growth_elasticity(_df)
    _df = df.copy(deep=True)
    plot_rolling_mean_filter(_df)
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
        'Chart 67. Birth, Death, and Net Fertility Rates in Sweden, 1750$-$1931\nTable XXV Birth, Death and Net Fertility Rates for Sweden, 1750$-$1931, \nSource: Computed from data given in the Statistisk ?rsbok for Sverige.',
        'Chart 68. Birth, Death, and Net Fertility Rates in Norway, 1801$-$1931\nTable XXVI Birth, Death and Net Fertility Rates for Norway, 1801$-$1931, \nSource: Statistisk ?rbok for Kongeriket Norge.',
        'Chart 69. Birth, Death, and Net Fertility Rates in Denmark, 1800$-$1931\nTable XXVII Birth, Death and Net Fertility Rates for Denmark, 1800$-$1931, \nSource: Danmarks Statistik, Statistisk Aarbog.',
        'Chart 70. Birth, Death, and Net Fertility Rates in Great Britain, 1850$-$1932\nTable XXVIII Birth, Death and Net Fertility Rates for England and Wales, 1850$-$1932, \nSource: Statistical Abstract for the United Kingdom.',
        'Chart 71. Birth, Death, and Net Fertility Rates in France, 1801$-$1931\nTable XXIX Birth, Death and Net Fertility Rates for France, 1801$-$1931, \nSource: Statistique generale de la France: Mouvement de la Population.',
        'Chart 72$\'$. Birth, Death, and Net Fertility Rates in Germany, 1871$-$1931\nTable XXX Birth, Death And Net Fertility Rates For:\n(A) Germany, 1871$-$1931\n(B) Prussia, 1816$-$1930\nSource: Statistisches Jahrbuch fur das Deutsche Reich.',
        'Chart 73. Birth, Death, and Net Fertility Rates in Switzerland, 1871$-$1931\nTable XXXI Birth, Death and Net Fertility Rates for Switzerland, 1871$-$1931, \nSource: Statistisches Jahrbuch der Schweiz.',
        'Chart 74. Birth, Death, and Net Fertility Rates in Italy, 1862$-$1931\nTable XXXII Birth, Death and Net Fertility Rates for Italy, 1862$-$1931, \nSource: Annuario Statistico Italiano.',
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
    MAP_FIG = {
        'fg_a': 'Chart 15 Relative Increase in Capital, Labor, and Physical Product in Manufacturing Industries of Massachussets, {}$-${} ({}=100',
        'fg_b': 'Chart 16 Theoretical and Actual Curves of Production, Massachusetts, {}$-${} ({}=100',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines, Massachusetts\nTrend Lines = 3 Year Moving Average',
        'fg_d': 'Chart 17 The Percentage Deviations of the Computed Product ($P\'$) from the Actual Product ($P$) in Massachusetts Manufacturing, {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_price': 1899,
    }
    plot_cobb_douglas(*transform_cobb_douglas(collect_douglas()), MAP_FIG)
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
