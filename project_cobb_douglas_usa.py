# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:46:08 2021

@author: Mastermind
"""


def fetch_bea_from_url(url):
    '''Downloading zip file from url'''
    r = requests.get(url)
    with open(url.split('/')[-1], 'wb') as s:
        s.write(r.content)
    with open(url.split('/')[-1]) as f:
        print(f'{url}: Complete')
        return pd.read_csv(f, thousands=',')


def fetch_bea_from_loaded(data_frame, series_id):
    '''`NipaDataA.txt`: U.S. Bureau of Economic Analysis'''
    data_frame = data_frame[data_frame.iloc[:, 0] == series_id].iloc[:, [1, 2]]
    data_frame.columns = [data_frame.columns[0].lower(), series_id]
    return data_frame.set_index(data_frame.columns[0], verify_integrity=True)


def get_dataset_usa_frb_ip():
    '''Indexed Manufacturing Series: FRB G17 IP, AIPMA_SA_IX, 1919--2018'''
    file_name = 'dataset_usa_frb-US3_IP 2018-09-02.csv'
    series_id = 'AIPMA_SA_IX'
    data_frame = pd.read_csv(file_name, skiprows=7, parse_dates=[0])
    data_frame.columns = [column.strip() for column in data_frame.columns]
    data_frame = data_frame.loc[:, [data_frame.columns[0], series_id]]
    data_frame['period'] = data_frame.iloc[:, 0].dt.year
    return data_frame.groupby(data_frame.columns[-1]).mean()


def get_dataset_usa_frb_fa():
    '''Returns Frame of Manufacturing Fixed Assets Series, Billion USD:
    result_frame.iloc[:,0]: Nominal;
    result_frame.iloc[:,1]: Real
    '''
    file_name = 'dataset_usa_frb-invest_capital.csv'
    source_frame = pd.read_csv(file_name,
                               skiprows=4, skipfooter=688, engine='python')
    source_frame.columns = source_frame.columns.to_series().replace(
        {'Manufacturing': 'Period'})
    source_frame = source_frame.set_index(source_frame.columns[0]).transpose()
    source_frame['frb_nominal'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 2].div(1000*source_frame.iloc[:, 0]) + \
        source_frame.iloc[:, 4]*source_frame.iloc[:,
                                                  5].div(1000*source_frame.iloc[:, 3])
    source_frame['frb_real'] = source_frame.iloc[:, 2].div(1000) + \
        source_frame.iloc[:, 5].div(1000)
    source_frame.index = pd.to_numeric(source_frame.index,
                                       errors='ignore',
                                       downcast='integer')
    result_frame = source_frame.iloc[:, [6, 7]]
    return result_frame


def get_dataset_usa_frb_fa_def():
    '''Returns Frame of Deflator for Manufacturing Fixed Assets Series, Index:
    result_frame.iloc[:,0]: Deflator
    '''
    file_name = 'dataset_usa_frb-invest_capital.csv'
    source_frame = pd.read_csv(file_name,
                               skiprows=4, skipfooter=688, engine='python')
    source_frame.columns = source_frame.columns.to_series().replace(
        {'Manufacturing': 'Period'})
    source_frame = source_frame.set_index(source_frame.columns[0]).transpose()
    source_frame.index = pd.to_numeric(source_frame.index,
                                       errors='ignore',
                                       downcast='integer')
    source_frame['fa_def_frb'] = (source_frame.iloc[:, 1] + source_frame.iloc[:, 4]).div(
        source_frame.iloc[:, 0] + source_frame.iloc[:, 3])
    result_frame = source_frame.iloc[:, [6]]
    return result_frame


def get_dataset_usa_capital():
    '''Series Not Used - `k3ntotl1si00`'''
    file_name = 'dataset_usa_cobb-douglas.zip'
    # Annual Increase in Terms of Cost Price (1)
    semi_frame_a = fetch_classic(file_name, 'CDT2S1')
    file_name = 'dataset_usa_cobb-douglas.zip'
    # Annual Increase in Terms of 1880 dollars (3)
    semi_frame_b = fetch_classic(file_name, 'CDT2S3')
    file_name = 'dataset_usa_cobb-douglas.zip'
    # Total Fixed Capital in 1880 dollars (4)
    semi_frame_c = fetch_classic(file_name, 'CDT2S4')
    loaded_frame = fetch_bea_from_url(
        'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt')
    '''Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net\
    Stock of Private Nonresidential Fixed Assets by Industry Group and\
    Legal Form of Organization'''
    semi_frame_d = fetch_bea_from_loaded(loaded_frame, 'k1n31gd1es00')
    '''Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3.\
    Historical-Cost Net Stock of Private Nonresidential Fixed Assets by\
    Industry Group and Legal Form of Organization'''
    semi_frame_e = fetch_bea_from_loaded(loaded_frame, 'k3n31gd1es00')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_f = fetch_census(file_name, 'P0107')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_g = fetch_census(file_name, 'P0110')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_h = fetch_census(file_name, 'P0119')
    '''Kendrick J.W., Productivity Trends in the United States, Page 320'''
    file_name = 'dataset_usa_kendrick.zip'
    semi_frame_i = fetch_classic(file_name, 'KTA15S08')
    '''Douglas P.H., Theory of Wages, Page 332'''
    file_name = 'dataset_douglas.zip'
    semi_frame_j = fetch_classic(file_name, 'DT63AS01')
    '''FRB Data'''
    semi_frame_k = get_dataset_usa_frb_fa()
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,
                              semi_frame_d, semi_frame_e, semi_frame_f,
                              semi_frame_g, semi_frame_h, semi_frame_i,
                              semi_frame_j, semi_frame_k], axis=1, sort=True)
    return result_frame


def get_cobb_douglas_extension_capital():
    '''Existing Capital Dataset'''
    source_frame = get_dataset_usa_capital()
    '''Convert Capital Series into Current (Historical) Prices'''
    source_frame['nominal_cbb_dg'] = source_frame.iloc[:, 0] * \
        source_frame.iloc[:, 2].div(1000*source_frame.iloc[:, 1])
    source_frame['nominal_census'] = source_frame.iloc[:, 5] * \
        source_frame.iloc[:, 7].div(source_frame.iloc[:, 6])
    source_frame['nominal_dougls'] = source_frame.iloc[:, 0] * \
        source_frame.iloc[:, 9].div(1000*source_frame.iloc[:, 1])
    source_frame['nominal_kndrck'] = source_frame.iloc[:, 5] * \
        source_frame.iloc[:, 8].div(1000*source_frame.iloc[:, 6])
    source_frame.iloc[:, 15] = source_frame.iloc[66, 6] * \
        source_frame.iloc[:, 15].div(source_frame.iloc[66, 5])
    '''Douglas P.H. -- Kendrick J.W. (Blended) Series'''
    source_frame['nominal_doug_kndrck'] = source_frame.iloc[:, 14:16].mean(1)
    '''Cobb C.W., Douglas P.H. -- FRB (Blended) Series'''
    source_frame['nominal_cbb_dg_frb'] = source_frame.iloc[:, [12, 10]].mean(1)
    '''Capital Structure Series: `Cobb C.W., Douglas P.H. -- FRB (Blended)\
    Series` to `Douglas P.H. -- Kendrick J.W. (Blended) Series`'''
    source_frame['struct_ratio'] = source_frame.iloc[:, 17].div(
        source_frame.iloc[:, 16])
    '''Filling the Gaps within Capital Structure Series'''
    source_frame.iloc[6:36, 18].fillna(source_frame.iloc[36, 18], inplace=True)
    source_frame.iloc[36:, 18].fillna(0.275, inplace=True)
    '''Patch Series `Douglas P.H. -- Kendrick J.W. (Blended) Series`\
    Multiplied by `Capital Structure Series`'''
    source_frame['nominal_patch'] = source_frame.iloc[:, 16].mul(
        source_frame.iloc[:, 18])
    '''`Cobb C.W., Douglas P.H. -- FRB (Blended) Series` Patched with `Patch Series`'''
    source_frame['nominal_extended'] = source_frame.iloc[:, [17, 19]].mean(1)
    source_frame = source_frame.iloc[:, [20]]
    source_frame.dropna(inplace=True)
    return source_frame


def get_cobb_douglas_deflator():
    '''Fixed Assets Deflator, 2009=100'''
    base = (84, 177, 216)  # 2009, 1970, 2009
    '''Combine L2, L15, E7, E23, E40, E68 & P107/P110'''
    '''Bureau of Labor Statistics
    Data Not Used As It Covers Only Years of 1998--2017'''
    '''Results:
        file_name = 'dataset_usa_census1949.zip'
    fetch_census(file_name, 'L0036') Offset with\
        file_name = 'dataset_usa_census1975.zip'
        fetch_census(file_name, 'E0183')
        file_name = 'dataset_usa_census1949.zip'
    fetch_census(file_name, 'L0038') Offset with\
        file_name = 'dataset_usa_census1975.zip'
        fetch_census(file_name, 'E0184')
        file_name = 'dataset_usa_census1949.zip'
    fetch_census(file_name, 'L0039') Offset with\
        file_name = 'dataset_usa_census1975.zip'
        fetch_census(file_name, 'E0185')
        file_name = 'dataset_usa_census1975.zip'
    fetch_census(file_name, 'E0052') Offset With\
        file_name = 'dataset_usa_census1949.zip'
        fetch_census(file_name, 'L0002')'''
    '''Cost-Of-Living Indexes'''
    '''E183: Federal Reserve Bank, 1913=100'''
    '''E184: Burgess, 1913=100'''
    '''E185: Douglas, 1890-99=100'''
    file_name = 'dataset_usa_cobb-douglas.zip'
    sub_frame_a = fetch_classic(file_name, 'CDT2S1')
    file_name = 'dataset_usa_cobb-douglas.zip'
    sub_frame_b = fetch_classic(file_name, 'CDT2S3')
    file_name = 'dataset_usa_census1949.zip'
    sub_frame_c = fetch_census(file_name, 'L0001')
    file_name = 'dataset_usa_census1949.zip'
    sub_frame_d = fetch_census(file_name, 'L0002')
    file_name = 'dataset_usa_census1949.zip'
    sub_frame_e = fetch_census(file_name, 'L0015')
    file_name = 'dataset_usa_census1949.zip'
    sub_frame_f = fetch_census(file_name, 'L0037')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_g = fetch_census(file_name, 'E0007')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_h = fetch_census(file_name, 'E0008')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_i = fetch_census(file_name, 'E0009')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_j = fetch_census(file_name, 'E0023')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_k = fetch_census(file_name, 'E0040')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_l = fetch_census(file_name, 'E0068')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_m = fetch_census(file_name, 'E0183')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_n = fetch_census(file_name, 'E0184')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_o = fetch_census(file_name, 'E0185')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_p = fetch_census(file_name, 'E0186')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_q = fetch_census(file_name, 'P0107')
    file_name = 'dataset_usa_census1975.zip'
    sub_frame_r = fetch_census(file_name, 'P0110')
    sub_frame_s = get_dataset_usa_frb_fa_def()
    sub_frame_q = sub_frame_q[22:]
    sub_frame_r = sub_frame_r[22:]
    basis_frame = pd.concat([sub_frame_a, sub_frame_b, sub_frame_c,
                             sub_frame_d, sub_frame_e, sub_frame_f,
                             sub_frame_g, sub_frame_h, sub_frame_i,
                             sub_frame_j, sub_frame_k, sub_frame_l,
                             sub_frame_m, sub_frame_n, sub_frame_o,
                             sub_frame_p, sub_frame_q, sub_frame_r,
                             sub_frame_s], axis=1, sort=True)
    basis_frame['fa_def_cd'] = basis_frame.iloc[:, 0].div(
        basis_frame.iloc[:, 1])
    basis_frame['fa_def_cn'] = basis_frame.iloc[:, 16].div(
        basis_frame.iloc[:, 17])
    '''Cobb--Douglas'''
    semi_frame_a = processing(basis_frame, 19)
    '''Bureau of Economic Analysis'''
    loaded_frame = fetch_bea_from_url(
        'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt')
    '''Fixed Assets: k1n31gd1es00, 1925--2019, Table 4.1. Current-Cost Net\
        Stock of Private Nonresidential Fixed Assets by Industry Group and\
            Legal Form of Organization'''
    sub_frame_a = fetch_bea_from_loaded(loaded_frame, 'k1n31gd1es00')
    '''Fixed Assets: kcn31gd1es00, 1925--2019, Table 4.2. Chain-Type Quantity\
        Indexes for Net Stock of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    sub_frame_b = fetch_bea_from_loaded(loaded_frame, 'kcn31gd1es00')
    '''Not Used: Not Used: Fixed Assets: k3n31gd1es00, 1925--2019, Table 4.3.\
        Historical-Cost Net Stock of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    sub_frame_c = fetch_bea_from_loaded(loaded_frame, 'k3n31gd1es00')
    '''Not Used: Fixed Assets: k3ntotl1si00, 1925--2019, Table 2.3.\
        Historical-Cost Net Stock of Private Fixed Assets, Equipment,\
            Structures, and Intellectual Property Products by Type'''
    sub_frame_d = fetch_bea_from_loaded(loaded_frame, 'k3ntotl1si00')
    '''Not Used: mcn31gd1es00, 1925--2019, Table 4.5. Chain-Type Quantity\
        Indexes for Depreciation of Private Nonresidential Fixed Assets by\
            Industry Group and Legal Form of Organization'''
    sub_frame_e = fetch_bea_from_loaded(loaded_frame, 'mcn31gd1es00')
    '''Not Used: mcntotl1si00, 1925--2019, Table 2.5. Chain-Type Quantity\
        Indexes for Depreciation of Private Fixed Assets, Equipment,\
            Structures, and Intellectual Property Products by Type'''
    sub_frame_f = fetch_bea_from_loaded(loaded_frame, 'mcntotl1si00')
    '''Real Values'''
    semi_frame_b = pd.concat([sub_frame_a, sub_frame_b], axis=1, sort=True)
    semi_frame_b['ppi_bea'] = 100*semi_frame_b.iloc[:,
                                                    0].div(semi_frame_b.iloc[base[0], 0]*semi_frame_b.iloc[:, 1])
    semi_frame_b.iloc[:, 2] = processing(semi_frame_b, 2)
    semi_frame_b = semi_frame_b.iloc[:, [2]]
    '''Bureau of the Census'''
    '''Correlation Test:
    `kendall_frame = result_frame.corr(method='kendall')`
    `pearson_frame = result_frame.corr(method='pearson')`
    `spearman_frame = result_frame.corr(method='spearman')`
    Correlation Test Result: kendall & pearson & spearman: L2, L15, E7, E23, E40, E68'''
    sub_frame_a = processing(basis_frame, 3)
    sub_frame_b = processing(basis_frame, 4)
    sub_frame_c = processing(basis_frame, 6)
    sub_frame_d = processing(basis_frame, 9)
    sub_frame_e = processing(basis_frame, 10)
    sub_frame_f = processing(basis_frame, 11)
    sub_frame_g = processing(basis_frame, 20)
    semi_frame_c = pd.concat([sub_frame_a, sub_frame_b, sub_frame_c,
                              sub_frame_d, sub_frame_e, sub_frame_f,
                              sub_frame_g], axis=1, sort=True)
    semi_frame_c['ppi_census_fused'] = semi_frame_c.mean(1)
    semi_frame_c = semi_frame_c.iloc[:, [7]]
    '''Federal Reserve'''
    semi_frame_d = processing(basis_frame, 18)
    '''Robert C. Sahr, 2007'''
    semi_frame_e = get_dataset_infcf()
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,
                              semi_frame_d, semi_frame_e], axis=1, sort=True)

    result_frame = result_frame[128:]
    result_frame['def_cum_bea'] = np.cumprod(1 + result_frame.iloc[:, 1])
    result_frame['def_cum_cen'] = np.cumprod(1 + result_frame.iloc[:, 2])
    result_frame['def_cum_frb'] = np.cumprod(1 + result_frame.iloc[:, 3])
    result_frame['def_cum_sah'] = np.cumprod(1 + result_frame.iloc[:, 4])
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(
        result_frame.iloc[base[1], 5])
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(
        result_frame.iloc[base[1], 6])
    result_frame.iloc[:, 7] = result_frame.iloc[:, 7].div(
        result_frame.iloc[base[1], 7])
    result_frame.iloc[:, 8] = result_frame.iloc[:, 8].div(
        result_frame.iloc[base[1], 8])
    result_frame['def_cum_com'] = result_frame.iloc[:, [5, 6, 7]].mean(1)
    result_frame['fa_def_com'] = processing(result_frame, 9)
    result_frame.iloc[:, 9] = result_frame.iloc[:, 9].div(
        result_frame.iloc[base[2], 9])
    result_frame = result_frame.iloc[:, [9]]
    result_frame.dropna(inplace=True)
    return result_frame


def get_cobb_douglas_extension_labor():
    base = 14  # 1899
    '''Manufacturing Laborers` Series Comparison
    semi_frame_a: Cobb C.W., Douglas P.H. Labor Series
    semi_frame_b: Census Bureau 1949, D69
    semi_frame_c: Census Bureau 1949, J4
    semi_frame_d: Census Bureau 1975, D130
    semi_frame_e: Census Bureau 1975, P5
    semi_frame_f: Census Bureau 1975, P62
    semi_frame_g: Bureau of Economic Analysis, H4313C & J4313C & A4313C & N4313C
    semi_frame_h: J.W. Kendrick, Productivity Trends in the United States,\
        Table D-II, `Persons Engaged` Column, pp. 465--466
    semi_frame_i: Yu.V. Kurenkov
    Bureau of Labor Statistics
    Federal Reserve Board'''
    file_name = 'dataset_usa_cobb-douglas.zip'
    # Average Number Employed (in thousands)
    semi_frame_a = fetch_classic(file_name, 'CDT3S1')
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_b = fetch_census(file_name, 'D0069')
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_c = fetch_census(file_name, 'J0004')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_d = fetch_census(file_name, 'D0130')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_e = fetch_census(file_name, 'P0005')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_f = fetch_census(file_name, 'P0062')
    loaded_frame = fetch_bea_from_url(
        'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt')
    sub_frame_a = fetch_bea_from_loaded(loaded_frame, 'H4313C')
    sub_frame_b = fetch_bea_from_loaded(loaded_frame, 'J4313C')
    sub_frame_c = fetch_bea_from_loaded(loaded_frame, 'A4313C')
    sub_frame_d = fetch_bea_from_loaded(loaded_frame, 'N4313C')
    semi_frame_g = pd.concat([sub_frame_a, sub_frame_b, sub_frame_c, sub_frame_d],
                             axis=1, sort=True)

    semi_frame_g = semi_frame_g.mean(1)
    semi_frame_g = semi_frame_g.to_frame(name='BEA')
    file_name = 'dataset_usa_kendrick.zip'
    semi_frame_h = fetch_classic(file_name, 'KTD02S02')
    file_name = 'dataset_usa_reference_ru_kurenkov-yu-v.csv'
    semi_frame_i = pd.read_csv(file_name, index_col=0, usecols=[0, 2])
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,
                              semi_frame_d, semi_frame_e, semi_frame_f,
                              semi_frame_g, semi_frame_h, semi_frame_i],
                             axis=1, sort=True)
    result_frame['kendrick'] = result_frame.iloc[base, 0] * \
        result_frame.iloc[:, 7].div(result_frame.iloc[base, 7])
    result_frame['labor'] = result_frame.iloc[:, [0, 1, 3, 6, 8, 9]].mean(1)
    result_frame = result_frame.iloc[:, [10]]
    result_frame.dropna(inplace=True)
    result_frame = result_frame[2:]
    return result_frame


def get_cobb_douglas_extension_product():
    base = (109, 149)  # 1899, 1939
    '''Bureau of the Census, 1949, Page 179, J13: National Bureau of Economic\
        Research Index of Physical Output, All Manufacturing Industries.'''
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_a = fetch_census(file_name, 'J0013')
    '''Bureau of the Census, 1949, Page 179, J14: Warren M. Persons, Index of\
        Physical Production of Manufacturing'''
    file_name = 'dataset_usa_census1949.zip'
    semi_frame_b = fetch_census(file_name, 'J0014')
    '''Bureau of the Census, 1975, Page 667, P17: Edwin Frickey Index of\
        Manufacturing Production'''
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_c = fetch_census(file_name, 'P0017')
    '''The Revised Index of Physical Production for All Manufacturing In the\
        United States, 1899--1926'''
    file_name = 'dataset_douglas.zip'
    semi_frame_d = fetch_classic(file_name, 'DT24AS01')
    '''Federal Reserve, AIPMASAIX'''
    semi_frame_e = get_dataset_usa_frb_ip()
    '''Joseph H. Davis Production Index'''
    file_name = 'dataset_usa_davis-j-h-ip-total.xls'
    semi_frame_f = pd.read_excel(file_name, index_col=0, skiprows=4)
    semi_frame_f.index.rename('period', inplace=True)
    semi_frame_f.columns = ['davis_index']
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c,
                              semi_frame_d, semi_frame_e, semi_frame_f],
                             axis=1, sort=True)
    result_frame.iloc[:, 1] = result_frame.iloc[:, 1].div(
        result_frame.iloc[base[0], 1]).mul(100)
    result_frame.iloc[:, 5] = result_frame.iloc[:, 5].div(
        result_frame.iloc[base[0], 5]).mul(100)
    result_frame['fused_classic'] = result_frame.iloc[:,
                                                      [0, 1, 2, 3, 5]].mean(1)
    result_frame.iloc[:, 4] = result_frame.iloc[:, 4].div(
        result_frame.iloc[base[1], 4]).mul(100)
    result_frame.iloc[:, 6] = result_frame.iloc[:, 6].div(
        result_frame.iloc[base[1], 6]).mul(100)
    result_frame['fused'] = result_frame.iloc[:, [4, 6]].mean(1)
    result_frame = result_frame.iloc[:, [7]]
    return result_frame


def get_dataset():
    '''Data Fetch'''
    '''Data Fetch for Capital'''
    capital_frame_a = get_cobb_douglas_extension_capital()
    '''Data Fetch for Capital Deflator'''
    capital_frame_b = get_cobb_douglas_deflator()
    capital_frame = pd.concat(
        [capital_frame_a, capital_frame_b], axis=1, sort=True)
    capital_frame.dropna(inplace=True)
    capital_frame['capital_real'] = capital_frame.iloc[:, 0].div(
        capital_frame.iloc[:, 1])
    '''Data Fetch for Labor'''
    labor_frame = get_cobb_douglas_extension_labor()
    '''Data Fetch for Product'''
    product_frame = get_cobb_douglas_extension_product()
    result_frame = pd.concat([capital_frame.iloc[:, 2], labor_frame, product_frame],
                             axis=1, sort=True).dropna()
    result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


def plot_cobb_douglas(data_frame):
    '''Cobb--Douglas Algorithm as per C.W. Cobb, P.H. Douglas. A Theory of Production, 1928;
    data_frame.index: Period,
    data_frame.iloc[:, 0]: Capital,
    data_frame.iloc[:, 1]: Labor,
    data_frame.iloc[:, 2]: Product
    '''
    def pl(series, k=0.25, b=1.01):
        return b*series**(-k)

    def pc(series, k=0.25, b=1.01):
        return b*series**(1-k)

    FIGURES = {
        'fig_a': 'Chart I Progress in Manufacturing {}$-${} ({}=100)',
        'fig_b': 'Chart II Theoretical and Actual Curves of Production {}$-${} ({}=100)',
        'fig_c': 'Chart III Percentage Deviations of $P$ and $P\'$ from Their Trend Lines\nTrend Lines=3 Year Moving Average',
        'fig_d': 'Chart IV Percentage Deviations of Computed from Actual Product {}$-${}',
    }
    X = data_frame.iloc[:, 0].div(data_frame.iloc[:, 1])
    Y = data_frame.iloc[:, 2].div(data_frame.iloc[:, 1])

    X = log(X.astype('float64'))
    Y = log(Y.astype('float64'))
# =============================================================================
# Original: k=0.25
# =============================================================================
    k, b = np.polyfit(X, Y, 1)
    b = np.exp(b)
    data_frame['prod_comp'] = b * \
        (data_frame.iloc[:, 0]**k)*(data_frame.iloc[:, 1]**(1-k))
    data_frame['prod_roll'] = data_frame.iloc[:,
                                              2].rolling(window=3, center=True).mean()
    data_frame['prod_roll_comp'] = data_frame.iloc[:,
                                                   3].rolling(window=3, center=True).mean()
    data_frame['sub_prod'] = data_frame.iloc[:, 2].sub(data_frame.iloc[:, 4])
    data_frame['sub_comp'] = data_frame.iloc[:, 3].sub(data_frame.iloc[:, 5])
    data_frame['dev_prod'] = data_frame.iloc[:, 3].div(
        data_frame.iloc[:, 2]).sub(1)
    plt.figure(1)
    plt.semilogy(data_frame.iloc[:, 0], label='Fixed Capital')
    plt.semilogy(data_frame.iloc[:, 1], label='Labor Force')
    plt.semilogy(data_frame.iloc[:, 2], label='Physical Product')
    plt.xlabel('Period')
    plt.ylabel('Indexes')
    plt.title(FIGURES['fig_a'].format(data_frame.index[0],
                                      data_frame.index[-1],
                                      data_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.semilogy(data_frame.iloc[:, 2], label='Actual Product')
    plt.semilogy(
        data_frame.iloc[:, 3], label='Computed Product, $P\'=%fL^{%f}C^{%f}$' % (b, 1-k, k))
    plt.xlabel('Period')
    plt.ylabel('Production')
    plt.title(FIGURES['fig_b'].format(data_frame.index[0],
                                      data_frame.index[-1],
                                      data_frame.index[0]))
    plt.legend()
    plt.grid(True)
    plt.figure(3)
    plt.plot(data_frame.iloc[:, 6], label='Deviations of $P$')
    plt.plot(data_frame.iloc[:, 7], '--', label='Deviations of $P\'$')
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(FIGURES['fig_c'])
    plt.legend()
    plt.grid(True)
    plt.figure(4)
    plt.plot(data_frame.iloc[:, 3].div(data_frame.iloc[:, 2]).sub(1))
    plt.xlabel('Period')
    plt.ylabel('Percentage Deviation')
    plt.title(FIGURES['fig_d'].format(data_frame.index[0],
                                      data_frame.index[-1]))
    plt.grid(True)
    plt.figure(5, figsize=(5, 8))
    lc = np.arange(0.2, 1.0, 0.005)
    plt.scatter(data_frame.iloc[:, 1].div(data_frame.iloc[:, 0]),
                data_frame.iloc[:, 2].div(data_frame.iloc[:, 1]))
    plt.scatter(data_frame.iloc[:, 1].div(data_frame.iloc[:, 0]),
                data_frame.iloc[:, 2].div(data_frame.iloc[:, 0]))
    plt.plot(lc, pl(lc, k=k, b=b), label='$\\frac{3}{4}\\frac{P}{L}$')
    plt.plot(lc, pc(lc, k=k, b=b), label='$\\frac{1}{4}\\frac{P}{C}$')
    plt.xlabel('$\\frac{L}{C}$')
    plt.ylabel('Indexes')
    plt.title('Relative Final Productivities of Labor and Capital')
    plt.legend()
    plt.grid(True)
    plt.show()


result_frame = get_dataset()
plot_cobb_douglas(result_frame)
