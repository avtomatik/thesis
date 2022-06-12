from prepare.lib import get_data_douglas
from plot.lib import plot_douglas
from plot.lib import plot_cobb_douglas


# =============================================================================
# Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928 & P.H. Douglas. The Theory of Wages, 1934;
# =============================================================================
FIG_MAP = {
    'fg_a': 'Chart 15 Relative Increase in Capital, Labor, and Physical Product in Manufacturing Industries of Massachussets, {}$-${} ({}=100',
    'fg_b': 'Chart 16 Theoretical and Actual Curves of Production, Massachusetts, {}$-${} ({}=100',
    'fg_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines, Massachusetts\nTrend Lines = 3 Year Moving Average',
    'fg_d': 'Chart 17 The Percentage Deviations of the Computed Product ($P\'$) from the Actual Product ($P$) in Massachusetts Manufacturing, {}$-${}',
    'fg_e': 'Chart V Relative Final Productivities of Labor and Capital',
    'year_price': 1899
}


# =============================================================================
# Douglas European Demographics & Growth of US Capital
# =============================================================================
ARCHIVE_NAME = 'dataset_douglas.zip'
series_dict = get_series_ids(ARCHIVE_NAME)
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
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 1, 0, 12, 1, titles[0], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 2, 12, 23, 1, titles[1], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 3, 23, 34, 1, titles[2], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 4, 34, 45, 1, titles[3], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 5, 45, 55, 1, titles[4], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 6, 55, 66, 1, titles[5], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 7, 66, 76, 1, titles[6], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 8, 76, 86, 1, titles[7], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 9, 86, 89, 1, titles[8], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 10, 89, 90, 1, titles[9], 'Percentage')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 11, 90,
             93, 1, titles[10], 'Rate Per 1000')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 12, 93,
             96, 1, titles[11], 'Rate Per 1000')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 13, 96,
             99, 1, titles[12], 'Rate Per 1000')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 14, 99,
             102, 1, titles[13], 'Rate Per 1000')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 15, 102,
             105, 1, titles[14], 'Rate Per 1000')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 16, 105, 111, 1,
             titles[15], 'Rate Per 1000', titles_deu)
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 17, 111,
             114, 1, titles[16], 'Rate Per 1000')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 18, 114,
             117, 1, titles[17], 'Rate Per 1000')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 19, 117, 121, 1, titles[18], 'Mixed')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 20, 121, 124,
             1, titles[19], 'Millions of Dollars')
ARCHIVE_NAME = 'dataset_douglas.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 21, 90, 115, 3,
             titles[20], 'Births Rate Per 1000 People', titles_eur)
plt.show()

# =============================================================================
# Douglas Production Function
# =============================================================================
plot_cobb_douglas(get_dataset_douglas())
# =============================================================================
# Kendrick Macroeconomic Series
# =============================================================================
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
series_dict = get_series_ids(ARCHIVE_NAME)
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
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 1, 0, 8, 1,
             titles[0], 'Millions Of 1929 Dollars')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 2, 8, 19, 1,
             titles[1], 'Millions Of 1929 Dollars')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 3, 19, 30, 1,
             titles[2], 'Millions Of Current Dollars')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 4, 30, 38, 1,
             titles[3], 'Millions Of 1929 Dollars')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 5, 38, 46, 1, titles[4], 'Thousands')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 6, 46, 54, 1, titles[5], 'Millions')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 7, 54, 60, 1,
             titles[6], 'Millions Of 1929 Dollars')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 8, 60, 72, 1,
             titles[7], 'Millions Of 1929 Dollars')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 9, 72, 84, 1, titles[8], 'Percentage')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 10, 84, 96, 1, titles[9], 'Percentage')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 11, 96, 100, 1, titles[10], 'Percentage')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 12, 100, 111, 1, titles[11], 'Percentage')
ARCHIVE_NAME = 'dataset_usa_kendrick.zip'
plot_douglas(ARCHIVE_NAME, series_dict, 13, 111, 118, 1, titles[12], 'Percentage')
plt.show()
