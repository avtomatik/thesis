def preprocessing_douglas():
    '''Douglas Data Preprocessing'''
    file_name = 'dataset_douglas.zip'
    semi_frame_a = fetch_classic(file_name, 'DT19AS03')
    file_name = 'dataset_douglas.zip'
    semi_frame_b = fetch_classic(file_name, 'DT19AS02')
    file_name = 'dataset_douglas.zip'
    semi_frame_c = fetch_classic(file_name, 'DT19AS01')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c], axis=1, sort=True)
    result_frame = result_frame.div(result_frame.iloc[9, :])
    return result_frame


def plot_douglas(source, dictionary, num, start, stop, step, title, measure, label=None):
    '''
    source: Source Database,
    dictionary: Dictionary of Series IDs to Series Titles from Source Database,
    num: Plot Number,
    start: Start Series Code,
    stop: Stop Series Code,
    step: Step for Series IDs,
    title: Plot Title,
    measure: Dimenstion for Series,
    label: Additional Sublabels'''
    plt.figure(num)
    for i in range(start, stop, step):
        plt.plot(fetch_classic(source, dictionary.iloc[i, 0]), label=dictionary.iloc[i, 1])
    plt.title(title)
    plt.xlabel('Period')
    plt.ylabel(measure)
    plt.grid(True)
    if label == None:
        plt.legend()
    else:
        plt.legend(label)


def cobb_douglas_modified(source_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928 & P.H. Douglas. The Theory of Wages, 1934;
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Capital,
    source_frame.iloc[:, 1]: Labor,
    source_frame.iloc[:, 2]: Product
    '''
    figures_dict = {'figure_a':'Chart 15 Relative Increase in Capital, Labor, and Physical Product in Manufacturing Industries of Massachussets, %d$-$%d (%d=100)',
                'figure_b':'Chart 16 Theoretical and Actual Curves of Production, Massachusetts, %d$-$%d (%d=100)',
                'figure_c':'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines, Massachusetts\nTrend Lines = 3 Year Moving Average',
                'figure_d':'Chart 17 The Percentage Deviations of the Computed Product ($P\'$) from the Actual Product ($P$) in Massachusetts Manufacturing, %d$-$%d',
                'priceyear':1899}
    X = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    Y = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])
    X = sp.log(X)
    Y = sp.log(Y)
    f1p = sp.polyfit(X, Y, 1)
    a1, a0 = f1p # # Original: a1 = 0.25
    a0 = sp.exp(a0)
    PP = a0*(source_frame.iloc[:, 1]**(1-a1))*(source_frame.iloc[:, 0]**a1)
    PR = source_frame.iloc[:, 2].rolling(window=3, center=True).mean()
    PPR = PP.rolling(window=3, center=True).mean()
    plt.figure(1)
    plt.plot(source_frame.index, source_frame.iloc[:, 0], label='Fixed Capital')
    plt.plot(source_frame.index, source_frame.iloc[:, 1], label='Labor Force')
    plt.plot(source_frame.index, source_frame.iloc[:, 2], label='Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(figures_dict['figure_a'] %(source_frame.index[0], source_frame.index[-1], figures_dict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.index, source_frame.iloc[:, 2], label='Actual Product')
    plt.plot(source_frame.index, PP, label='Computed Product, $P\' = %fL^{%f}C^{%f}$' %(a0, 1-a1, a1))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(figures_dict['figure_b'] %(source_frame.index[0], source_frame.index[-1], figures_dict['priceyear']))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.index, source_frame.iloc[:, 2]-PR, label='Deviations of $P$')
    plt.plot(source_frame.index, PP-PPR, '--', label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(figures_dict['figure_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.index, PP.div(source_frame.iloc[:, 2])-1)
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(figures_dict['figure_d'] %(source_frame.index[0], source_frame.index[-1]))
    plt.grid(True)
    plt.show()


'''Douglas European Demographics & Growth of US Capital'''
file_name = 'dataset_douglas.zip'
series_dict = get_series_ids(file_name)
titles_deu = ['Germany Birth Rate', 'Germany Death Rate', 'Germany Net Fertility Rate', 'Prussia Birth Rate', 'Prussia Death Rate', 'Prussia Net Fertility Rate']
titles_eur = ['Sweden', 'Norway', 'Denmark', 'England & Wales', 'France', 'Germany', 'Prussia', 'Switzerland', 'Italy']
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
plot_douglas(file_name, series_dict, 11, 90, 93, 1, titles[10], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 12, 93, 96, 1, titles[11], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 13, 96, 99, 1, titles[12], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 14, 99, 102, 1, titles[13], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 15, 102, 105, 1, titles[14], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 16, 105, 111, 1, titles[15], 'Rate Per 1000', titles_deu)
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 17, 111, 114, 1, titles[16], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 18, 114, 117, 1, titles[17], 'Rate Per 1000')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 19, 117, 121, 1, titles[18], 'Mixed')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 20, 121, 124, 1, titles[19], 'Millions of Dollars')
file_name = 'dataset_douglas.zip'
plot_douglas(file_name, series_dict, 21, 90, 115, 3, titles[20], 'Births Rate Per 1000 People', titles_eur)
plt.show()

'''Douglas Production Function'''
result_frame = preprocessing_douglas()
cobb_douglas_modified(result_frame)
'''Kendrick Macroeconomic Series'''
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
plot_douglas(file_name, series_dict, 1, 0, 8, 1, titles[0], 'Millions Of 1929 Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 2, 8, 19, 1, titles[1], 'Millions Of 1929 Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 3, 19, 30, 1, titles[2], 'Millions Of Current Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 4, 30, 38, 1, titles[3], 'Millions Of 1929 Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 5, 38, 46, 1, titles[4], 'Thousands')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 6, 46, 54, 1, titles[5], 'Millions')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 7, 54, 60, 1, titles[6], 'Millions Of 1929 Dollars')
file_name = 'dataset_usa_kendrick.zip'
plot_douglas(file_name, series_dict, 8, 60, 72, 1, titles[7], 'Millions Of 1929 Dollars')
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

