# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 22:29:22 2020

Thesis Project

@author: Alexander Mikhailov
"""


from thesis.src.lib.combine import (combine_can, combine_cobb_douglas,
                                    combine_usa_investment_turnover,
                                    combine_usa_investment_turnover_bls,
                                    combine_usa_manufacturing_three_fold,
                                    combine_usa_manufacturing_two_fold)
from thesis.src.lib.plot import (plot_approx_linear, plot_approx_linear_log,
                                 plot_cobb_douglas, plot_cobb_douglas_3d,
                                 plot_cobb_douglas_complex, plot_douglas,
                                 plot_elasticity, plot_fourier_discrete,
                                 plot_growth_elasticity, plot_model_capital,
                                 plot_uscb_complex)
from thesis.src.lib.stockpile import (stockpile_usa_bea, stockpile_usa_hist,
                                      stockpile_usa_mcconnel)
from thesis.src.lib.tools import (calculate_power_function_fit_params_a,
                                  calculate_power_function_fit_params_b,
                                  calculate_power_function_fit_params_c,
                                  lash_up_spline_ea, lash_up_spline_eb,
                                  lash_up_spline_la, lash_up_spline_lb,
                                  lash_up_spline_lls, run_lash_up_spline)
from thesis.src.lib.transform import transform_cobb_douglas


def main():
    # =========================================================================
    # Subproject I. Approximation
    # =========================================================================
    # =========================================================================
    # 'plot_approx_linear': Linear Approximation,
    # 'plot_approx_linear_log': Log-Linear Approximation,
    # 'calculate_power_function_fit_params_a': Power Function Approximation,
    # 'calculate_power_function_fit_params_b': Power Function Approximation,
    # 'calculate_power_function_fit_params_c': Power Function Approximation
    # =========================================================================
    SERIES_IDS = {
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    plot_approx_linear(*stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(transform_approx_linear))

    SERIES_IDS = {
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'kcptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    plot_approx_linear_log(*stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(transform_approx_linear_log))

    SERIES_IDS = {
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'kcptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    plot_approx_linear_log(*stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(transform_approx_linear_log))

    SERIES_IDS = ('Валовой внутренний продукт, млрд долл. США',)
    PARAMS = (2800, 0.01, 0.5)
    stockpile_usa_mcconnel(SERIES_IDS).pipe(
        calculate_power_function_fit_params_a, PARAMS
    )

    SERIES_IDS = (
        'Ставка прайм-рейт, %',
        'Национальный доход, млрд долл. США',
    )
    PARAMS = (4, 12, 9000, 3000, 0.87)
    stockpile_usa_mcconnel(SERIES_IDS).pipe(
        calculate_power_function_fit_params_b, PARAMS
    )

    SERIES_IDS = (
        'Ставка прайм-рейт, %',
        'Валовой объем внутренних частных инвестиций, млрд долл. США',
    )
    PARAMS = (1.5, 19, 1.7, 1760)
    stockpile_usa_mcconnel(SERIES_IDS).pipe(
        calculate_power_function_fit_params_c, PARAMS
    )


    # =========================================================================
    # Subproject II. Capital
    # =========================================================================
    # =========================================================================
    # Project: Fixed Assets Dynamics Modelling:
    # Fixed Assets Turnover Linear Approximation
    # Gross Fixed Investment to Gross Domestic Product Ratio Linear Approximation
    # Alpha: Investment to Capital Conversion Ratio Dynamics
    # =========================================================================
    # =========================================================================
    # Original Result on Archived Data:
    # =========================================================================
    {
        's_1': -7.28110931679034e-05,
        's_2': 0.302917968959722,
    }
    # =========================================================================
    # Original Result on Archived Data:
    # =========================================================================
    {
        'λ1': -0.000413347827690062,
        'λ2': 1.18883834418742,
    }
    df, df_b = combine_usa_investment_turnover_bls()
    df_c, df_d = combine_usa_investment_turnover()
    df.pipe(plot_model_capital, year_base=2005)
    df_c.pipe(plot_model_capital, year_base=2012)
    # =========================================================================
    # Project: Discrete Fourier Transform based on Simpson's Rule Applied to Fixed Assets of the US
    # =========================================================================
    df_b.pipe(plot_fourier_discrete)
    df_d.pipe(plot_fourier_discrete)

    # =========================================================================
    # Subproject IV. Cobb--Douglas
    # =========================================================================
    # =========================================================================
    # cobb_douglas_complex.py
    # =========================================================================

    # =========================================================================
    # Subproject V. Cobb--Douglas CAN
    # =========================================================================
    # =========================================================================
    # First Figure: Exact Correspondence with 'note_incomplete_th05_2014_07_10.docx'
    # =========================================================================
    MAP_FIG = {
        'fg_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fg_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fg_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_base': 2007,
    }
    ARCHIVE_IDS = {
        # =====================================================================
        # Capital
        # =====================================================================
        310004: (2007, "Geometric (infinite) end-year net stock", "industrial"),
        # =====================================================================
        # Labor : "v2523012", Preferred Over "v3437501" Which Is Quarterly
        # =====================================================================
        'v2523012': 2820012,
        # =====================================================================
        # Manufacturing
        # =====================================================================
        'v65201809': 3790031,
    }
    ARCHIVE_IDS = {
        # =====================================================================
        # Capital
        # =====================================================================
        36100096: (
            2012,
            "Manufacturing",
            "Linear end-year net stock",
            (
                "Non-residential buildings",
                "Engineering construction",
                "Machinery and equipment"
            )
        ),
        # =====================================================================
        # Labor : "v2523012", Preferred Over "v3437501" Which Is Quarterly
        # =====================================================================
        'v2523012': 14100027,
        # =====================================================================
        # Manufacturing
        # =====================================================================
        'v65201809': 36100434,
    }
    df = combine_can(ARCHIVE_IDS)
    plot_cobb_douglas(
        *df.pipe(transform_cobb_douglas, year_base=2007),
        MAP_FIG
    )
    df.pipe(plot_cobb_douglas_3d)

    # =========================================================================
    # Subproject VI. Elasticity
    # =========================================================================
    SERIES_IDS = {
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    plot_elasticity(*stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(transform_elasticity))

    SERIES_IDS = {
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(plot_growth_elasticity)

    # =========================================================================
    # Subproject VII. Lash-Up Spline
    # =========================================================================
    # =========================================================================
    # Lash-Up Splines
    # =========================================================================
    # =========================================================================
    # Fixed Assets Turnover
    # =========================================================================
    df = combine_cobb_douglas().pipe(transform_cobb_douglas,
                                       year_base=1899)[0].iloc[:, [6]]
    # =========================================================================
    # Option 1
    # =========================================================================
    df.pipe(run_lash_up_spline, kernel=lash_up_spline_lls)
    # =========================================================================
    # Option 2.1.1
    # =========================================================================
    df.pipe(run_lash_up_spline, kernel=lash_up_spline_ea)
    # =========================================================================
    # Option 2.1.2
    # =========================================================================
    df.pipe(run_lash_up_spline, kernel=lash_up_spline_eb)
    # =========================================================================
    # Option 2.2.1
    # =========================================================================
    df.pipe(run_lash_up_spline, kernel=lash_up_spline_la)
    # =========================================================================
    # Option 2.2.2
    # =========================================================================
    df.pipe(run_lash_up_spline, kernel=lash_up_spline_lb)

    # =========================================================================
    # Subproject VIII. Complex
    # =========================================================================
    df = combine_cobb_douglas().pipe(
        transform_cobb_douglas, year_base=1899).iloc[:, range(5)]

    for col in df.columns:
        df.loc[:, [col]].pipe(plot_uscb_complex)

    SERIES_IDS = (
        {'D0004': 'dataset_uscb.zip'}, {'D0130': 'dataset_uscb.zip'},
        {'F0003': 'dataset_uscb.zip'}, {'F0004': 'dataset_uscb.zip'},
        {'P0110': 'dataset_uscb.zip'}, {'U0001': 'dataset_uscb.zip'},
        {'U0008': 'dataset_uscb.zip'}, {'X0414': 'dataset_uscb.zip'},
        {'X0415': 'dataset_uscb.zip'}
    )

    for series_id in SERIES_IDS:
        print(f'Processing {series_id}')
        stockpile_usa_hist(series_id).pipe(plot_uscb_complex)

    # =========================================================================
    # Subproject IX. USA BEA
    # =========================================================================
    import plot_usa_bea
    # =========================================================================
    # Subproject X. USA Census
    # =========================================================================
    # =========================================================================
    # Subproject XI. USA Census J14
    # =========================================================================
    import plot_usa_manufacturing

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
    MAP_FIG = {
        'fg_a': 'Chart 15 Relative Increase in Capital, Labor, and Physical Product in Manufacturing Industries of Massachussets, {}$-${} ({}=100)',
        'fg_b': 'Chart 16 Theoretical and Actual Curves of Production, Massachusetts, {}$-${} ({}=100)',
        'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines, Massachusetts\nTrend Lines = 3 Year Moving Average',
        'fg_d': 'Chart 17 The Percentage Deviations of the Computed Product ($P\'$) from the Actual Product ($P$) in Massachusetts Manufacturing, {}$-${}',
        'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
        'year_base': 1899,
    }
    SERIES_IDS = {
        'DT19AS03': 'dataset_douglas.zip',
        'DT19AS02': 'dataset_douglas.zip',
        'DT19AS01': 'dataset_douglas.zip'
    }
    plot_cobb_douglas(
        *stockpile_usa_hist(SERIES_IDS).pipe(transform_cobb_douglas, year_base=1899), MAP_FIG)
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
