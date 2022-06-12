# -*- coding: utf-8 -*-
'''
Created on Tue Mar 10 22:29:22 2020

Thesis Project

@author: Alexander Mikhailov
'''


from export.lib import extract_series_ids
from export.lib import extract_can_fixed_assets
from export.lib import extract_can_capital_query_archived
from prepare.lib import get_data_combined_archived
from prepare.lib import get_data_archived
from prepare.lib import get_data_usa_mcconnel_a
from prepare.lib import get_data_usa_mcconnel_b
from prepare.lib import get_data_usa_mcconnel_c
from prepare.lib import get_data_census_b_a
from prepare.lib import get_data_census_b_b
from prepare.lib import get_data_can
from prepare.lib import get_data_usa_frb_ms
from prepare.lib import get_data_local
from prepare.lib import transform_kurenkov
from prepare.lib import get_data_updated
from toolkit.lib import calculate_capital
from toolkit.lib import m_spline_ea
from toolkit.lib import m_spline_eb
from toolkit.lib import m_spline_la
from toolkit.lib import m_spline_lb
from toolkit.lib import m_spline_lls
from toolkit.lib import calculate_power_function_fit_params_a
from toolkit.lib import calculate_power_function_fit_params_b
from toolkit.lib import calculate_power_function_fit_params_c
from toolkit.lib import _m_spline_error_metrics
from toolkit.lib import _m_spline_print_params
from toolkit.lib import calculate_capital_acquisition
from toolkit.lib import calculate_capital_retirement
from plot.lib import plot_a
from plot.lib import plot_b
from plot.lib import plot_c
from plot.lib import plot_d
from plot.lib import plot_approx_linear
from plot.lib import plot_approx_log_linear
from plot.lib import plot_built_in
from plot.lib import plot_capital_modelling
from plot.lib import plot_fourier_discrete
from plot.lib import plot_elasticity
from plot.lib import plot_kzf
from plot.lib import plot_pearson_r_test
from plot.lib import plot_rmf
from plot.lib import plot_ses
from plot.lib import plot_e
from plot.lib import plot_kurenkov
from plot.lib import plot_census_complex
from toolkit.lib import m_spline_manager


print(__doc__)
# =============================================================================
# Subproject I. Approximation
# =============================================================================
'''
`plot_approx_linear`: Linear Approximation,
`plot_approx_log_linear`: Log-Linear Approximation,
`calculate_power_function_fit_params_a`: Power Function Approximation,
`calculate_power_function_fit_params_b`: Power Function Approximation,
`calculate_power_function_fit_params_c`: Power Function Approximation
'''
source_frame = get_data_combined_archived()
result_frame_a = source_frame.iloc[:, [7, 6, 0, 6]]
result_frame_a = result_frame_a.dropna()
result_frame_a.reset_index(level=0, inplace=True)
result_frame_b = source_frame.iloc[:, [7, 6, 20, 4]]
result_frame_b = result_frame_b.dropna()
result_frame_b.reset_index(level=0, inplace=True)
result_frame_c = source_frame.iloc[:, [7, 6, 20, 6]]
result_frame_c = result_frame_c.dropna()
result_frame_c.reset_index(level=0, inplace=True)
plot_approx_linear(result_frame_a)
plot_approx_log_linear(result_frame_b)
plot_approx_log_linear(result_frame_c)

source_frame = get_data_usa_mcconnel_a()
calculate_power_function_fit_params_a(source_frame, 2800, 0.01, 0.5)

source_frame = get_data_usa_mcconnel_b()
calculate_power_function_fit_params_b(source_frame, 4, 12, 9000, 3000, 0.87)

source_frame = get_data_usa_mcconnel_c()
calculate_power_function_fit_params_c(source_frame, 1.5, 19, 1.7, 1760)

# =============================================================================
# Subproject II. Capital
# =============================================================================
'''
Project: Fixed Assets Dynamics Modelling:
Fixed Assets Turnover Linear Approximation
Gross Fixed Investment to Gross Domestic Product Ratio Linear Approximation
Alpha: Investment to Capital Conversion Ratio Dynamics
Original Result on Archived Data: {s_1;s_2} = {-7.28110931679034e-05;0.302917968959722}
Original Result on Archived Data: {λ1;λ2} = {-0.000413347827690062;1.18883834418742}
'''
result_frame_a, result_frame_b, A = get_data_archived()
result_frame_c, result_frame_d, B = get_data_updated()
plot_capital_modelling(result_frame_a, a)
plot_capital_modelling(result_frame_c, b)
'''Project: Discrete Fourier Transform based on Simpson's Rule Applied to Fixed Assets of the US'''
plot_fourier_discrete(result_frame_b)
plot_fourier_discrete(result_frame_d)

# =============================================================================
# Subproject III. Capital Interactive
# =============================================================================
'''
Alpha: Capital Retirement Ratio
Pi: Investment to Capital Conversion Ratio
# =============================================================================
# Project: Interactive Capital Acquisitions
# =============================================================================
Option 1
    Define Number of Line Segments for Pi: 1
    Number of Periods Provided: 1
    Pi for Period from 1968 to 2010: 0
Option 2
    Define Number of Line Segments for Pi: 1
    Number of Periods Provided: 1
    Pi for Period from 1968 to 2010: 1
Option 3
    Define Number of Line Segments for Pi: 2
    Number of Periods Provided: 2
    Pi for Period from 1968 to 1981: 1
    Pi for Period from 1982 to 2010: 0
Option 4
    Define Number of Line Segments for Pi: 4
    Number of Periods Provided: 4
    Pi for Period from 1968 to 1981: 1
    Pi for Period from 1982 to 1991: 0.537711622818944
    Pi for Period from 1992 to 2001: 0.815869779361117
    Pi for Period from 2002 to 2010: 0.956084835528969
# =============================================================================
# Project: Interactive Capital Retirement
# =============================================================================
Option 1
    Define Number of Line Segments for Pi: 1
    Number of Periods Provided: 1
    Define Pi for Period from 1951 to 2011: 0
Option 2
    Define Number of Line Segments for Pi: 2
    Number of Periods Provided: 2
    Select Row for Year: 52
    Define Pi for Period from 1951 to 2003: 1
    Define Pi for Period from 2003 to 2011: 1.4
Option 3
    Define Number of Line Segments for Pi: 2
    Number of Periods Provided: 2
    Select Row for Year: 11
    Define Pi for Period from 1951 to 1962: 0.0493299706940006
    Define Pi for Period from 1962 to 2011: 0.0168837249983057
'''
result_frame = get_data_local()
# =============================================================================
# Nominal Investment
# =============================================================================
result_frame['IRU'] = result_frame.iloc[:, 0].mul(
    result_frame.iloc[:, 2]).div(result_frame.iloc[:, 1])
# =============================================================================
# Nominal Product
# =============================================================================
result_frame['PNU'] = result_frame.iloc[:, 1]
# =============================================================================
# Real Product
# =============================================================================
result_frame['PRU'] = result_frame.iloc[:, 2]
# =============================================================================
# Maximum Nominal Product
# =============================================================================
result_frame['PNM'] = result_frame.iloc[:, 1].div(
    result_frame.iloc[:, 3]).mul(100)
# =============================================================================
# Maximum Real Product
# =============================================================================
result_frame['PRM'] = result_frame.iloc[:, 2].div(
    result_frame.iloc[:, 3]).mul(100)
# =============================================================================
# Labor
# =============================================================================
result_frame.rename(columns={'Labor': 'LUU'}, inplace=True)
# =============================================================================
# Fixed Assets, End-Period
# =============================================================================
result_frame['CRU'] = result_frame.iloc[:, 4].mul(
    result_frame.iloc[:, 2]).div(result_frame.iloc[:, 1])
result_frame_a = result_frame.iloc[:, [6, 7, 8, 10, 11, 5]].dropna()
result_frame_b = result_frame.iloc[:, [6, 7, 8, 11, 5]].dropna()
result_frame_c = result_frame.iloc[:, [6, 9, 10, 11, 5]].dropna()
result_frame_a.reset_index(level=0, inplace=True)
result_frame_b.reset_index(level=0, inplace=True)
result_frame_c.reset_index(level=0, inplace=True)
calculate_capital_acquisition(result_frame_a)
calculate_capital_retirement(result_frame_b)
calculate_capital_retirement(result_frame_c)

# =============================================================================
# Subproject IV. Cobb--Douglas
# =============================================================================
# =============================================================================
# On Original Dataset
# =============================================================================
source_frame = get_data_cobb_douglas()
result_frame_a = source_frame.iloc[:, [0, 1, 2]]
result_frame_b = source_frame.iloc[:, [0, 1, 3]]
result_frame_c = source_frame.iloc[:, [0, 1, 4]]
# =============================================================================
# On Expanded Dataset
# =============================================================================
result_frame_d, result_frame_e = get_data_version_a()
result_frame_f, result_frame_g, result_frame_h = get_data_version_b()
result_frame_i = dataset_version_c()
plot_cobb_douglas_complex(result_frame_a)
plot_cobb_douglas_complex(result_frame_b)
plot_cobb_douglas_complex(result_frame_c)
# =============================================================================
# No Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_d)
# =============================================================================
# Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_e)
# =============================================================================
# Option: 1929--2013, No Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_f)
# =============================================================================
# Option: 1967--2013, No Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_g)
# =============================================================================
# Option: 1967--2012, Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_h)
plot_cobb_douglas_complex(result_frame_i)

# =============================================================================
# Subproject V. Cobb--Douglas CAN
# =============================================================================
# =============================================================================
# First Figure: Exact Correspondence with `Note INTH05 2014-07-10.docx`
# =============================================================================
source_frame = get_data_can()
source_frame = source_frame.div(source_frame.iloc[0, :])
plot_cobb_douglas_canada(source_frame)
plot_cobb_douglas_3d(source_frame)

# =============================================================================
# Subproject VI. Elasticity
# =============================================================================
source_frame = get_data_combined_archived()
result_frame_a = source_frame.iloc[:, [7, 6, 4]]
result_frame_b = source_frame.iloc[:, [4]]
result_frame_a = result_frame_a.dropna()
result_frame_b = result_frame_b.dropna()
result_frame_a.reset_index(level=0, inplace=True)
result_frame_b.reset_index(level=0, inplace=True)
plot_elasticity(result_frame_a)
plot_growth_elasticity(result_frame_b)

# =============================================================================
# Subproject VII. MSpline
# =============================================================================
# =============================================================================
# Makeshift Splines
# =============================================================================
result_frame = get_data_cobb_douglas()
result_frame['turnover'] = result_frame.iloc[:, 2].div(
    result_frame.iloc[:, 0])  # Fixed Assets Turnover
result_frame = result_frame.iloc[:, [5]]
result_frame.reset_index(level=0, inplace=True)
# =============================================================================
# Option 1
# =============================================================================
m_spline_manager(result_frame, m_spline_lls, results_delivery_a)
# =============================================================================
# Option 2.1.1
# =============================================================================
m_spline_manager(result_frame, m_spline_ea, results_delivery_k)
# =============================================================================
# Option 2.1.2
# =============================================================================
m_spline_manager(result_frame, m_spline_eb, results_delivery_k)
# =============================================================================
# Option 2.2.1
# =============================================================================
m_spline_manager(result_frame, m_spline_la, results_delivery_k)
# =============================================================================
# Option 2.2.2
# =============================================================================
m_spline_manager(result_frame, m_spline_lb, results_delivery_k)

# =============================================================================
# Subproject VIII. Multiple
# =============================================================================
source_frame = get_data_cobb_douglas()
source_frame['lab_cap_int'] = source_frame.iloc[:, 0].div(
    source_frame.iloc[:, 1])
source_frame['lab_product'] = source_frame.iloc[:, 2].div(
    source_frame.iloc[:, 1])
result_frame_a = source_frame.iloc[:, [0]]
result_frame_b = source_frame.iloc[:, [1]]
result_frame_c = source_frame.iloc[:, [2]]
result_frame_d = source_frame.iloc[:, [5]]
result_frame_e = source_frame.iloc[:, [6]]
plot_census_complex(result_frame_a)
plot_census_complex(result_frame_b)
plot_census_complex(result_frame_c)
plot_census_complex(result_frame_d)
plot_census_complex(result_frame_e)

SERIES_IDS = ('D0004', 'D0130', 'F0003', 'F0004', 'P0110',
              'U0001', 'U0008', 'X0414', 'X0415',)
for series_id in SERIES_IDS:
    print('Processing {}'.format(series_id))
    source_frame = fetch_census('dataset_usa_census1975.zip', series_id)
    plot_pearson_r_test(source_frame)

    source_frame = fetch_census('dataset_usa_census1975.zip', series_id, False)
    plot_kzf(source_frame)
    plot_ses(source_frame, 5, 0.1)

# =============================================================================
# Subproject IX. USA BEA
# =============================================================================
source_frame_a = get_data_combined_archived()
source_frame_b = get_data_combined()
# =============================================================================
# Project: Initial Version Dated: 05 October 2012
# =============================================================================
result_frame_a_b = preprocessing_a(source_frame_a)
result_frame_a_c = preprocessing_a(source_frame_b)
plot_a(result_frame_a_b)
plot_a(result_frame_a_c)
# =============================================================================
# Project: Initial Version Dated: 23 November 2012
# =============================================================================
result_frame_b_b = preprocessing_b(source_frame_a)
result_frame_b_c = preprocessing_b(source_frame_b)
plot_b(result_frame_b_b)
plot_b(result_frame_b_c)
# =============================================================================
# Project: Initial Version Dated: 16 June 2013
# =============================================================================
result_frame_c_b = preprocessing_c(source_frame_a)
result_frame_c_c = preprocessing_c(source_frame_b)
plot_c(result_frame_c_b)
plot_c(result_frame_c_c)
# =============================================================================
# Project: Initial Version Dated: 15 June 2015
# =============================================================================
result_frame_d = preprocessing_d(source_frame_b)
plot_d(result_frame_d)
# =============================================================================
# Project: Initial Version Dated: 17 February 2013
# =============================================================================
result_frame_e_a, result_frame_e_b = preprocessing_e(source_frame_a)
plot_e(result_frame_e_a)
plot_e(result_frame_e_b)
# =============================================================================
# Project: BEA Data Compared with Kurenkov Yu.V. Data
# =============================================================================
result_frame_f_a, result_frame_f_b, result_frame_f_c, result_frame_f_d = transform_kurenkov(
    source_frame_a)
plot_kurenkov(result_frame_f_a, result_frame_f_b,
              result_frame_f_c, result_frame_f_d)

# =============================================================================
# Subproject X. USA Census
# =============================================================================
plot_census_a(*get_data_census_a())
plot_census_b(get_data_census_b_a(), get_data_census_b_b())
plot_census_c(*get_data_census_c())
# =============================================================================
# Census Production Series
# =============================================================================
SERIES_IDS = (
    'P0248', 'P0249', 'P0250', 'P0251', 'P0262',
    'P0265', 'P0266', 'P0267', 'P0268', 'P0269',
    'P0293', 'P0294', 'P0295',
)
alternative = (
    'P0231', 'P0232', 'P0233', 'P0234', 'P0235',
    'P0236', 'P0237', 'P0238', 'P0239', 'P0240',
    'P0241', 'P0244', 'P0247', 'P0248', 'P0249',
    'P0250', 'P0251', 'P0252', 'P0253', 'P0254',
    'P0255', 'P0256', 'P0257', 'P0258', 'P0259',
    'P0260', 'P0261', 'P0262', 'P0263', 'P0264',
    'P0265', 'P0266', 'P0267', 'P0268', 'P0269',
    'P0270', 'P0271', 'P0277', 'P0279', 'P0281',
    'P0282', 'P0283', 'P0284', 'P0286', 'P0288',
    'P0290', 'P0293', 'P0294', 'P0295', 'P0296',
    'P0297', 'P0298', 'P0299', 'P0300',
)
plot_census_d(SERIES_IDS)
plot_census_e(get_data_census_e())
result_frame = get_data_census_f()
plot_census_f_a(result_frame)
plot_census_f_b(result_frame)
plot_census_g(get_data_census_g())
plot_census_h()
plot_census_i(*get_data_census_i())
plot_census_j(*get_data_census_j())
plot_census_k()

# =============================================================================
# Subproject XI. USA Census J14
# =============================================================================
file_name = 'dataset_usa_census1949.zip'
plot_growth_elasticity(fetch_census(file_name, 'J0014', False))
file_name = 'dataset_usa_census1949.zip'
plot_rmf(fetch_census(file_name, 'J0014', False))
# =============================================================================
# Subproject XII. USA Douglas Kendrick
# =============================================================================
# =============================================================================
# Douglas European Demographics & Growth of US Capital
# =============================================================================
file_name = 'dataset_douglas.zip'
series_dict = get_series_ids(file_name)
titles_deu = ['Germany Birth Rate', 'Germany Death Rate', 'Germany Net Fertility Rate',
              'Prussia Birth Rate', 'Prussia Death Rate', 'Prussia Net Fertility Rate']
titles_eur = ['Sweden', 'Norway', 'Denmark', 'England & Wales',
              'France', 'Germany', 'Prussia', 'Switzerland', 'Italy']
titles = ['Table I Indexes of Physical Production, 1899=100 [1899$-$1926]',
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
          'Birth Rates by Countries']
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 1, 0, 12, 1, titles[0], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 2, 12, 23, 1, titles[1], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 3, 23, 34, 1, titles[2], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 4, 34, 45, 1, titles[3], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 5, 45, 55, 1, titles[4], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 6, 55, 66, 1, titles[5], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 7, 66, 76, 1, titles[6], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 8, 76, 86, 1, titles[7], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 9, 86, 89, 1, titles[8], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 10, 89, 90, 1, titles[9], 'Percentage')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 11, 90,
             93, 1, titles[10], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 12, 93,
             96, 1, titles[11], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 13, 96,
             99, 1, titles[12], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 14, 99,
             102, 1, titles[13], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 15, 102,
             105, 1, titles[14], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 16, 105, 111, 1,
             titles[15], 'Rate Per 1000', titles_deu)
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 17, 111,
             114, 1, titles[16], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 18, 114,
             117, 1, titles[17], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 19, 117, 121, 1, titles[18], 'Mixed')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 20, 121, 124,
             1, titles[19], 'Millions of Dollars')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 21, 90, 115, 3,
             titles[20], 'Births Rate Per 1000 People', titles_eur)
plt.show()

# =============================================================================
# Douglas Production Function
# =============================================================================
plot_cobb_douglas_modified(get_data_douglas())
# =============================================================================
# Kendrick Macroeconomic Series
# =============================================================================
file_name = 'dataset_usa_kendrick.zip'
series_dict = get_series_ids(file_name)
titles = ['Table A-I Gross And Net National Product, Adjusted Kuznets Concepts, Peacetime And National Security Version, 1869$-$1957 (Millions Of 1929 Dollars)',
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
          'Table D-II. Manufacturing: Output, Labor Inputs, and Labor Productivity Ratios, 1869-1957 (1929=100)']
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 1, 0, 8, 1,
             titles[0], 'Millions Of 1929 Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 2, 8, 19, 1,
             titles[1], 'Millions Of 1929 Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 3, 19, 30, 1,
             titles[2], 'Millions Of Current Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 4, 30, 38, 1,
             titles[3], 'Millions Of 1929 Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 5, 38, 46, 1, titles[4], 'Thousands')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 6, 46, 54, 1, titles[5], 'Millions')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 7, 54, 60, 1,
             titles[6], 'Millions Of 1929 Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 8, 60, 72, 1,
             titles[7], 'Millions Of 1929 Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 9, 72, 84, 1, titles[8], 'Percentage')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 10, 84, 96, 1, titles[9], 'Percentage')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 11, 96, 100, 1, titles[10], 'Percentage')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 12, 100, 111, 1, titles[11], 'Percentage')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 13, 111, 118, 1, titles[12], 'Percentage')
plt.show()
