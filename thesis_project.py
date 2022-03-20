#-*- coding: utf-8 -*-
'''
Created on Tue Mar 10 22:29:22 2020

Thesis Project

@author: Alexander Mikhailov
'''


def get_series_ids(file_name):
    '''Returns Dictionary for Series from Douglas's & Kendrick's Databases'''
    series_dict = pd.read_csv(file_name, usecols=range(3, 5))
    series_dict = series_dict.drop_duplicates()
    series_dict = series_dict[series_dict.columns[[1, 0]]]
    series_dict = series_dict.sort_values('vector')
    series_dict = series_dict.reset_index(drop=True)
    return series_dict


def fetch_can_fixed_assets(series_ids):
# =============================================================================
# Fetch <series_ids> from CANSIM Table 031-0004: Flows and stocks of fixed
# non-residential capital, total all industries, by asset, provinces and
# territories, annual (dollars x 1,000,000)
# =============================================================================
    file_name = 'dataset_can_00310004-eng.zip'
    data_frame = pd.read_csv(file_name, usecols=[0, 6, 8])
    data_frame = data_frame[data_frame.iloc[:, 1].isin(series_ids)]
    data_frame.iloc[:, 2] = pd.to_numeric(data_frame.iloc[:, 2], errors='coerce')
    result_frame = pd.DataFrame()
    for series_id in series_ids:
        current_frame = data_frame[data_frame.iloc[:, 1] == series_id].iloc[:,[0, 2]]
        current_frame.columns = [current_frame.columns[0].upper(), series_id]
        current_frame.set_index(current_frame.columns[0],
                                inplace=True,
                                verify_integrity=True)
        result_frame = pd.concat([result_frame, current_frame], axis=1, sort=True)
    result_frame['sum'] = result_frame.sum(axis=1)
    return result_frame.iloc[:,[-1]]


def fetch_can_capital_query_archived():
# =============================================================================
# TODO: Consider Using sqlalchemy
# =============================================================================
# =============================================================================
# https://blog.panoply.io/how-to-read-a-sql-query-into-a-pandas-dataframe
# =============================================================================
# =============================================================================
# Fetch <series_ids> from CANSIM Table 031-0004: Flows and stocks of fixed
# non-residential capital, total all industries, by asset, provinces and
# territories, annual (dollars x 1,000,000)
# =============================================================================
    file_name = 'dataset_can_00310004-eng.zip'
    df = pd.read_csv(file_name, usecols=[2, 4, 5, 6])
    query = (df.iloc[:, 0].str.contains('2007 constant prices')) & \
            (df.iloc[:, 1] == 'Geometric (infinite) end-year net stock') & \
            (df.iloc[:, 2].str.contains('industrial', flags=re.IGNORECASE))
    df = df[ query ]
    return df.iloc[:, -1].unique().tolist()


def data_сombined_archived():
    '''Version: 02 December 2013'''
    '''Nominal Investment Series: A006RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A006RC1')
    '''Nominal Investment Series: A006RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A006RC1')
    semi_frame_a = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Implicit Price Deflator Series: A006RD3, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10109 Ann', 'A006RD3')
    '''Implicit Price Deflator Series: A006RD3, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10109 Ann', 'A006RD3')
    semi_frame_b = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Gross private domestic investment -- Nonresidential: A008RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A008RC1')
    '''Gross private domestic investment -- Nonresidential: A008RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A008RC1')
    semi_frame_c = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD3, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10109 Ann', 'A008RD3')
    '''Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD3, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10109 Ann', 'A008RD3')
    semi_frame_d = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Nominal National income Series: A032RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10705 Ann', 'A032RC1')
    '''Nominal National income Series: A032RC1, 1969--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10705 Ann', 'A032RC1')
    semi_frame_e = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Gross Domestic Product, 2005=100: B191RA3, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10103 Ann', 'B191RA3')
    '''Gross Domestic Product, 2005=100: B191RA3, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10103 Ann', 'B191RA3')
    semi_frame_f = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    '''Nominal Nominal Gross Domestic Product Series: A191RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    semi_frame_g = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_h = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Labor Series'''
    semi_frame_i = fetch_usa_bea_labor()
    '''Gross Domestic Investment, W170RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section5ALL_Hist.xls', '50100 Ann', 'W170RC1')
    '''Gross Domestic Investment, W170RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section5all_xls.xls', '50100 Ann', 'W170RC1')
    semi_frame_j = sub_frame_a.append(sub_frame_b)

    '''Gross Domestic Investment, W170RX1, 1967--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section5ALL_Hist.xls', '50206 Ann', 'W170RX1')
    '''Gross Domestic Investment, W170RX1, 1969--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section5all_xls.xls', '50206 Ann', 'W170RX1')
    semi_frame_k = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''`K160491` Replaced with `K10070` in `data_сombined()`'''
    '''Fixed Assets Series: K160491, 1951--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section5ALL_Hist.xls', '50900 Ann', 'K160491')
    '''Fixed Assets Series: K160491, 1969--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section5all_xls.xls', '50900 Ann', 'K160491')
    semi_frame_l = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Investment in Fixed Assets and Consumer Durable Goods, Private, i3ptotl1es000, 1901--2011'''
    file_name = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
    semi_frame_m = fetch_usa_bea(file_name, 'Section1ALL_xls.xls', '105 Ann', 'i3ptotl1es000')
    '''Chain-Type Quantity Indexes for Investment in Fixed Assets and Consumer Durable Goods, Private, icptotl1es000, 1901--2011'''
    file_name = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
    semi_frame_n = fetch_usa_bea(file_name, 'Section1ALL_xls.xls', '106 Ann', 'icptotl1es000')
    '''Current-Cost Net Stock of Fixed Assets and Consumer Durable Goods, Private, k1ptotl1es000, 1925--2011'''
    file_name = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
    semi_frame_o = fetch_usa_bea(file_name, 'Section1ALL_xls.xls', '101 Ann', 'k1ptotl1es000')
    '''Historical-Cost Net Stock of Private Fixed Assets, Equipment and Software, and Structures by Type, Private fixed assets, k3ptotl1es000, 1925--2011'''
    file_name = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
    semi_frame_p = fetch_usa_bea(file_name, 'Section2ALL_xls.xls', '203 Ann', 'k3ptotl1es000')
    '''Chain-Type Quantity Indexes for Net Stock of Private Fixed Assets, Equipment and Software, and Structures by Type, Private fixed assets, kcptotl1es000, 1925--2011'''
    file_name = 'dataset_usa_bea-sfat-release-2012-08-15-SectionAll_xls.zip'
    semi_frame_q = fetch_usa_bea(file_name, 'Section2ALL_xls.xls', '202 Ann', 'kcptotl1es000')
    file_name = 'dataset_usa_0022_m1.txt'
    semi_frame_r = pd.read_csv(file_name)
    semi_frame_r.columns = semi_frame_r.columns.str.title()
    semi_frame_r = semi_frame_r.set_index('Period')
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_s = fetch_census(file_name, 'X0414')
    semi_frame_t = fetch_usa_frb_ms()
    file_name = 'dataset_usa_0025_p_r.txt'
    semi_frame_u = pd.read_csv(file_name)
    semi_frame_u.columns = semi_frame_u.columns.str.title()
    semi_frame_u = semi_frame_u.set_index('Period')
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e, \
                           semi_frame_f, semi_frame_g, semi_frame_h, semi_frame_i, semi_frame_j, \
                           semi_frame_k, semi_frame_l, semi_frame_m, semi_frame_n, semi_frame_o, \
                           semi_frame_p, semi_frame_q, semi_frame_r, semi_frame_s, semi_frame_t, \
                           semi_frame_u], axis=1, sort=True)
    return result_frame


def get_dataset_archived():
    base = 54 # # Year 2005
    semi_frame_a = fetch_usa_bls_cpiu()
    semi_frame_a = semi_frame_a.set_index('Period')
    '''Nominal Investment Series: A006RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A006RC1')
    '''Nominal Investment Series: A006RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A006RC1')
    semi_frame_b = sub_frame_a.append(sub_frame_b)

    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_c = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''`K160491` Replaced with `K10070` in `data_сombined()`'''
    '''Fixed Assets Series: K160491, 1951--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section5ALL_Hist.xls', '50900 Ann', 'K160491')
    '''Fixed Assets Series: K160491, 1969--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section5all_xls.xls', '50900 Ann', 'K160491')
    semi_frame_d = sub_frame_a.append(sub_frame_b).drop_duplicates()

    source_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d], axis=1, sort=True).dropna()

    '''Deflator, 2005=100'''
    source_frame['def'] = sp.cumprod(1 + source_frame.iloc[:, 0])
    source_frame.iloc[:, 4] = source_frame.iloc[:, 4].rdiv(source_frame.iloc[base, 4])
    '''Investment, 2005=100'''
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 4]
    '''Capital, 2005=100'''
    source_frame['cap'] = source_frame.iloc[:, 3]*source_frame.iloc[:, 4]
    '''Capital Retirement Ratio'''
    source_frame['rto'] = 1 + (1*source_frame.iloc[:, 5]-source_frame.iloc[:, 6].shift(-1)).div(source_frame.iloc[:, 6])
    result_frame_a = source_frame[source_frame.columns[[5, 2, 6, 7]]]
    result_frame_b = source_frame[source_frame.columns[[7]]]
    result_frame_a.dropna().reset_index(level=0, inplace=True)
    result_frame_b.dropna().reset_index(level=0, inplace=True)
    return result_frame_a, result_frame_b, base


def data_fetch_a():
    base = 28 # # 1980
    result_frame = fetch_usa_mcconnel('Валовой внутренний продукт, млрд долл. США')
    result_frame = result_frame[base:].reset_index(level=0)
    return result_frame


def data_fetch_b():
    base = 28 # # 1980
    semi_frame_a = fetch_usa_mcconnel('Ставка прайм-рейт, %')
    semi_frame_a.rename(columns={'Value': 'PrimeRate'}, inplace=True)
    semi_frame_b = fetch_usa_mcconnel('Национальный доход, млрд долл. США')
    semi_frame_b.rename(columns={'Value': 'A032RC1'}, inplace=True)
    result_frame = pd.concat([semi_frame_a, semi_frame_b], axis=1, sort=True)

    result_frame = result_frame[base:].reset_index(level=0)
    return result_frame


def data_fetch_c():
    base = 28 # # 1980
    semi_frame_a = fetch_usa_mcconnel('Ставка прайм-рейт, %')
    semi_frame_a.rename(columns={'Value': 'PrimeRate'}, inplace=True)
    semi_frame_b = fetch_usa_mcconnel('Валовой объем внутренних частных инвестиций, млрд долл. США')
    semi_frame_b.rename(columns={'Value': 'A006RC1'}, inplace=True)
    result_frame = pd.concat([semi_frame_a, semi_frame_b], axis=1, sort=True)

    result_frame = result_frame[base:].reset_index(level=0)
    return result_frame


def data_fetch_census_b_b():
    '''Returns Census Fused Capital Deflator'''
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_a = fetch_census(file_name, 'P0107') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_b = fetch_census(file_name, 'P0108') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_c = fetch_census(file_name, 'P0109') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_d = fetch_census(file_name, 'P0110') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_e = fetch_census(file_name, 'P0111') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_f = fetch_census(file_name, 'P0112') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_g = fetch_census(file_name, 'P0113') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_h = fetch_census(file_name, 'P0114') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_i = fetch_census(file_name, 'P0115') # Nominal
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_j = fetch_census(file_name, 'P0116') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_k = fetch_census(file_name, 'P0117') # 1958=100
    file_name = 'dataset_usa_census1975.zip'
    semi_frame_l = fetch_census(file_name, 'P0118') # 1958=100
    source_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e, \
                          semi_frame_f, semi_frame_g, semi_frame_h, semi_frame_i, semi_frame_j, \
                          semi_frame_k, semi_frame_l], axis=1, sort=True)

    source_frame['pur_total'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 3])
    source_frame['pur_structures'] = source_frame.iloc[:, 1].div(source_frame.iloc[:, 4])
    source_frame['pur_equipment'] = source_frame.iloc[:, 2].div(source_frame.iloc[:, 5])
    source_frame['dep_total'] = source_frame.iloc[:, 6].div(source_frame.iloc[:, 9])
    source_frame['dep_structures'] = source_frame.iloc[:, 7].div(source_frame.iloc[:, 10])
    source_frame['dep_equipment'] = source_frame.iloc[:, 8].div(source_frame.iloc[:, 11])
    source_frame = source_frame[16:]
    semi_frame_a = processing(source_frame, 12)
    semi_frame_b = processing(source_frame, 13)
    semi_frame_c = processing(source_frame, 14)
    semi_frame_d = processing(source_frame, 15)
    semi_frame_e = processing(source_frame, 16)
    semi_frame_f = processing(source_frame, 17)
    interim_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e, \
                          semi_frame_f], axis=1, sort=True)

    interim_frame['census_fused'] = interim_frame.mean(1)
    result_frame = interim_frame[interim_frame.columns[[6]]]
    return result_frame


def dataset_canada():
    '''A. Fixed Assets Block: `Industrial buildings`, `Industrial machinery` for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, `New Brunswick`, \
    `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    '''2007 constant prices'''
    '''Geometric (infinite) end-year net stock'''
    '''Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    '''Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    capital = fetch_can_fixed_assets(fetch_can_capital_query_archived())
    '''B. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly'''
    '''`v2523012` - 282-0012 Labour Force Survey Estimates (LFS), employment by class of worker, North American Industry Classification System (NAICS)\
    and sex; Canada; Total employed, all class of workers; Manufacturing; Both sexes (x 1,000) (annual, 1987 to 2017)'''
    labor = fetch_can_annually('02820012', 'v2523012')
    '''C. Production Block: `v65201809`'''
    '''`v65201809` - 379-0031 Gross domestic product (GDP) at basic prices, by North American Industry Classification System (NAICS); Canada; Trading-day\
    adjusted; 2007 constant prices; Manufacturing (x 1,000,000) (monthly, 1997-01-01 to 2017-10-01)'''
    product = fetch_can_quarterly('03790031', 'v65201809')
    result_frame = pd.concat([capital, labor, product], axis=1, sort=True)
    result_frame = result_frame.dropna()
    result_frame.rename(columns={0:'capital', 'v2523012':'labor', 'v65201809':'product'}, inplace=True)
    return result_frame


def fetch_usa_frb_ms():
    '''Indexed Money Stock Measures (H.6) Series:
    https://www.federalreserve.gov/datadownload/Download.aspx?rel=h6&series=5398d8d1734b19f731aba3105eb36d47&filetype = csv&label=include&layout = seriescolumn&from = 01/01/1959&to = 12/31/2018'''
    file_name = 'dataset_usa_FRB_H6.csv'
    data_frame = pd.read_csv(file_name, skiprows=5, usecols=range(2))
    data_frame[['period',
                'month',]] = data_frame.iloc[:, 0].str.split('-', expand=True)
    data_frame.columns = [re.sub(r"[,@\'?\.$%_]",
                                 "",
                                 column) for column in data_frame.columns]
    return data_frame.groupby(data_frame.columns[-2]).mean()


def fetch_local():
    '''Nominal Investment Series: A006RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A006RC1')
    '''Nominal Investment Series: A006RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A006RC1')
    semi_frame_a = sub_frame_a.append(sub_frame_b)

    '''Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10105 Ann', 'A191RC1')
    '''Nominal Nominal Gross Domestic Product Series: A191RC1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10105 Ann', 'A191RC1')
    semi_frame_b = sub_frame_a.append(sub_frame_b).drop_duplicates()

    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section1ALL_Hist.xls', '10106 Ann', 'A191RX1')
    '''Real Gross Domestic Product Series, 2005=100: A191RX1, 1969--2012'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section1all_xls.xls', '10106 Ann', 'A191RX1')
    semi_frame_c = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_d = fetch_usa_frb_cu()
    '''`K160491` Replaced with `K10070` in `data_сombined()`'''
    '''Fixed Assets Series: K160491, 1951--1969'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip'
    sub_frame_a = fetch_usa_bea(file_name, 'Section5ALL_Hist.xls', '50900 Ann', 'K160491')
    '''Fixed Assets Series: K160491, 1969--2011'''
    file_name = 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip'
    sub_frame_b = fetch_usa_bea(file_name, 'Section5all_xls.xls', '50900 Ann', 'K160491')
    semi_frame_e = sub_frame_a.append(sub_frame_b).drop_duplicates()

    semi_frame_f = fetch_usa_bea_labor()
    result_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e, \
                           semi_frame_f], axis=1, sort=True)
    return result_frame


def preprocessing_f(testing_frame):
    '''testing_frame: test _frame'''
    '''control _frame'''
    file_name = 'dataset_usa_reference_ru_kurenkov-yu-v.csv'
    control_frame = pd.read_csv(file_name)
    control_frame = control_frame.set_index('Period')
    '''Data Fetch'''
    '''Production'''
    semi_frame_aa = control_frame[control_frame.columns[[0]]]
    semi_frame_ab = testing_frame[testing_frame.columns[[7]]].dropna()
    semi_frame_ac = fetch_usa_frb_ip()
    result_frame_a = pd.concat([semi_frame_aA, semi_frame_aB, semi_frame_aC], axis=1, sort=True)
    result_frame_a = result_frame_a.div(result_frame_a.iloc[31, :]/100)
    '''Labor'''
    semi_frame_ba = control_frame[control_frame.columns[[1]]]
    semi_frame_bb = testing_frame[testing_frame.columns[[8]]].dropna()
    result_frame_b = pd.concat([semi_frame_bA, semi_frame_bB], axis=1, sort=True)
    '''Capital'''
    semi_frame_ca = control_frame[control_frame.columns[[2]]]
    semi_frame_cb = testing_frame[testing_frame.columns[[11]]].dropna()
    result_frame_c = pd.concat([semi_frame_ca, semi_frame_cb], axis=1, sort=True)
    result_frame_c = result_frame_c.div(result_frame_c.iloc[1, :]/100)
    '''Capacity Utilization'''
    semi_frame_dA = control_frame[control_frame.columns[[3]]]
    semi_frame_dB = fetch_usa_frb_cu()
    result_frame_d = pd.concat([semi_frame_dA, semi_frame_dB], axis=1, sort=True)
    return result_frame_a, result_frame_b, result_frame_c, result_frame_d


def get_dataset_updated():
    semi_frame_a = fetch_bea_usa('dataset_usa_bea_nipadataa.txt', 'A006RC')
    semi_frame_b = fetch_bea_usa('dataset_usa_bea_nipadataa.txt', 'A006RD')
    semi_frame_c = fetch_bea_usa('dataset_usa_bea_nipadataa.txt', 'A191RC')
    semi_frame_d = fetch_bea_usa('dataset_usa_bea_nipadataa.txt', 'A191RX')
    '''Fixed Assets: kcn31gd1es000, 1925--2016, Table 4.2. Chain-Type Quantity Indexes for Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_e = fetch_usa_bea(file_name, 'Section4ALL_xls.xls', '402 Ann', 'kcn31gd1es000')
    '''Not Used: Fixed Assets: k3n31gd1es000, 1925--2016, Table 4.3. Historical-Cost Net Stock of Private Nonresidential Fixed Assets by Industry Group and Legal Form of Organization'''
    file_name = 'dataset_usa_bea-sfat-release-2017-08-23-SectionAll_xls.zip'
    semi_frame_f = fetch_usa_bea(file_name, 'Section4ALL_xls.xls', '403 Ann', 'k3n31gd1es000')
    source_frame = pd.concat([semi_frame_a, semi_frame_b, semi_frame_c, semi_frame_d, semi_frame_e, semi_frame_f], axis=1, sort=True).dropna()

    base = 58 # # Year 2009
    '''Investment, 2009=100'''
    source_frame['inv'] = source_frame.iloc[base, 0]*source_frame.iloc[:, 1].div(100)
    '''Capital, 2009=100'''
    source_frame['cap'] = 1000*source_frame.iloc[base, 5]*source_frame.iloc[:, 4].div(100)
    '''Capital Retirement Ratio'''
    source_frame['rto'] = 1 + (1*source_frame.iloc[:, 6]-source_frame.iloc[:, 7].shift(-1)).div(source_frame.iloc[:, 7])
    result_frame_a = source_frame[source_frame.columns[[6, 3, 7, 8]]]
    result_frame_b = source_frame[source_frame.columns[[8]]]
    result_frame_a.dropna().reset_index(level=0, inplace=True)
    result_frame_b.dropna().reset_index(level=0, inplace=True)
    return result_frame_a, result_frame_b, base


def capital(source_frame, A, B, C, D, Pi):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Investment,
    source_frame.iloc[:, 2]: Production,
    source_frame.iloc[:, 3]: Capital,
    source_frame.iloc[:, 4]: Capital Retirement,
    A: S - Gross Fixed Investment to Gross Domestic Product Ratio - Absolute Term over Period,
    B: S - Gross Fixed Investment to Gross Domestic Product Ratio - Slope over Period,
    C: Λ - Fixed Assets Turnover Ratio - Absolute Term over Period,
    D: Λ - Fixed Assets Turnover Ratio - Slope over Period,
    Pi: Investment to Capital Conversion Ratio
    '''
    series = source_frame.iloc[:, 3].shift(1)*(1 + (B*source_frame.iloc[:, 0].shift(1) + A)*(D*source_frame.iloc[:, 0].shift(1) + C)*Pi-source_frame.iloc[:, 4].shift(1))
    return series


def m_spline_ea(source_frame, intervals, k):
    '''Exponential Spline, Type A
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    A, K, S = [], [], []
    for j in range(intervals): # # Coefficient Section
        A.append(((source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[0], 0])*sp.log(source_frame.iloc[k[j], 1])-(source_frame.iloc[k[j], 0]-source_frame.iloc[k[0], 0])*sp.log(source_frame.iloc[k[1 + j], 1]))/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        if j == 0:
            K.append((sp.log(source_frame.iloc[k[1 + j], 1])-sp.log(source_frame.iloc[k[j], 1]))/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        else:
            K.append(K[j-1] + sp.log(source_frame.iloc[k[1 + j], 1])/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0])-\
                     (source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j-1], 0])*sp.log(source_frame.iloc[k[j], 1])/((source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0])*(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0])) + \
                     sp.log(source_frame.iloc[k[j-1], 1])/(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0]))
        if j == intervals-1: # # Spline Section
            for i in range(k[j], 1 + k[1 + j]):
                S.append(sp.exp(A[j] + K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0])))
        else:
            for i in range(k[j], k[1 + j]):
                S.append(sp.exp(A[j] + K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0])))
    S = pd.DataFrame(S, columns=['Spline']) # # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return K, result_frame


def m_spline_eb(source_frame, intervals, k):
    '''Exponential Spline, Type B
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    K, S = [], []
    for j in range(intervals): # # Coefficient Section
        K.append((sp.log(source_frame.iloc[k[1 + j], 1])-sp.log(source_frame.iloc[k[j], 1]))/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        if j == intervals-1: # # Spline Section
            for i in range(k[j], 1 + k[1 + j]):
                S.append(source_frame.iloc[k[j], 1]*sp.exp(K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0])))
        else:
            for i in range(k[j], k[1 + j]):
                S.append(source_frame.iloc[k[j], 1]*sp.exp(K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0])))
    S = pd.DataFrame(S, columns=['Spline']) # # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return K, result_frame


def m_spline_la(source_frame, intervals, k):
    '''Linear Spline, Type A
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    A, K, S = [], [], []
    for j in range(intervals):
        A.append(((source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[0], 0])*source_frame.iloc[k[j], 1]-(source_frame.iloc[k[j], 0]-source_frame.iloc[k[0], 0])*source_frame.iloc[k[1 + j], 1])/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        if j == 0:
            K.append((source_frame.iloc[k[1 + j], 1]-source_frame.iloc[k[j], 1])/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        else:
            K.append(K[j-1] + source_frame.iloc[k[1 + j], 1]/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0])-\
                     (source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j-1], 0])*source_frame.iloc[k[j], 1]/((source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0])*(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0])) + \
                     source_frame.iloc[k[j-1], 1]/(source_frame.iloc[k[j], 0]-source_frame.iloc[k[j-1], 0]))
        if j == intervals-1:
            for i in range(k[j], 1 + k[1 + j]):
                S.append(A[j] + K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0]))
        else:
            for i in range(k[j], k[1 + j]):
                S.append(A[j] + K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[0, 0]))
    S = pd.DataFrame(S, columns=['Spline']) # # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return K, result_frame


def m_spline_lb(source_frame, intervals, k):
    '''Linear Spline, Type B
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    K, S = [], []
    for j in range(intervals):
        K.append((source_frame.iloc[k[1 + j], 1]-source_frame.iloc[k[j], 1])/(source_frame.iloc[k[1 + j], 0]-source_frame.iloc[k[j], 0]))
        if j == intervals-1:
            for i in range(k[j], 1 + k[1 + j]):
                S.append(source_frame.iloc[k[j], 1] + K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0]))
        else:
            for i in range(k[j], k[1 + j]):
                S.append(source_frame.iloc[k[j], 1] + K[j]*(source_frame.iloc[i, 0]-source_frame.iloc[k[j], 0]))
    S = pd.DataFrame(S, columns=['Spline']) # # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return K, result_frame


def m_spline_lls(source_frame, intervals, k):
    '''Linear Spline, Linear Regression Kernel
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Target Series,
    intervals: Number of Intervals,
    k: Interpolation Knots'''
    A, K, S = [], [], []
    for j in range(intervals):
        S1, S2, S3, S4 = 0, 0, 0, 0 # # X, Y, X**2, XY # # Summarize
        if j == intervals-1:
            for i in range(k[j], 1 + k[1 + j]):
                S1 += source_frame.iloc[i, 0]
                S2 += source_frame.iloc[i, 1]
                S3 += (source_frame.iloc[i, 0])**2
                S4 += source_frame.iloc[i, 0]*source_frame.iloc[i, 1]
            A.append(((1 + k[1 + j]-k[j])*S4-S1*S2)/((1 + k[1 + j]-k[j])*S3-S1**2))
        else:
            for i in range(k[j], k[1 + j]):
                S1 += source_frame.iloc[i, 0]
                S2 += source_frame.iloc[i, 1]
                S3 += (source_frame.iloc[i, 0])**2
                S4 += source_frame.iloc[i, 0]*source_frame.iloc[i, 1]
            if j == 0:
                A.append((S2*S3-S1*S4)/((k[1 + j]-k[j])*S3-S1**2))
            A.append(((k[1 + j]-k[j])*S4-S1*S2)/((k[1 + j]-k[j])*S3-S1**2))
    for j in range(intervals):
        if j == 0:
            K.append(A[j])
        else:
            K.append(K[j-1] + (A[j]-A[1 + j])*source_frame.iloc[k[j], 0])
        if j == intervals-1:
            for i in range(k[j], 1 + k[1 + j]):
                S.append(K[j] + A[1 + j]*source_frame.iloc[i, 0])
        else:
            for i in range(k[j], k[1 + j]):
                S.append(K[j] + A[1 + j]*source_frame.iloc[i, 0])
    S = pd.DataFrame(S, columns=['Spline']) # # Convert List to Dataframe
    result_frame = pd.concat([source_frame, S], axis=1, sort=True)
    return A, result_frame


def SES(source_frame, window=5, alpha=0.5):
    '''Single Exponential Smoothing
    Robert Goodell Brown, 1956
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series
    '''
    S = source_frame.iloc[:window, 1]
    S = S.mean() # # Average of Window-First Entries
    ses = []
    ses.append(alpha*source_frame.iloc[0, 1] + (1-alpha)*S)
    for i in range(1, source_frame.shape[0]):
        ses.append(alpha*source_frame.iloc[i, 1] + (1-alpha)*ses[i-1])
    cap = 'ses{:02d}_{:, .6f}'.format(window, alpha)
    ses = pd.DataFrame(ses, columns=[cap])
    result_frame = pd.concat([source_frame, ses], axis=1, sort=True)
    result_frame = result_frame.set_index('Period')
    return result_frame


def approx_power_function_a(source_frame, q1, q2, alpha):
    '''
    source_frame.iloc[:, 0]: Regressor: = Period,
    source_frame.iloc[:, 1]: Regressand,
    q1, q2, alpha: Parameters
    '''
    result_frame = source_frame.iloc[:, 0] # # DataFrame for Based Log-Linear Approximation Results
    calcul_frame = [] # # Blank List for Calculation Results

    for i in range(source_frame.shape[0]):
        XAA = q1 + q2*(1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha # # {RESULT}(Yhat) = Y0 + A*(T-T0)**alpha
        XBB = (q1 + q2*(1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha-source_frame.iloc[i, 1])**2 # # (Yhat-Y)**2
        XCC = (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(alpha-1) # # (T-T0)**(alpha-1)
        XDD = (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha # # (T-T0)**alpha
        XEE = ((1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha)*math.log(1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0]) # # ((T-T0)**alpha)*LN(T-T0)
        XFF = source_frame.iloc[i, 1]*(1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha # # Y*(T-T0)**alpha
        XGG = source_frame.iloc[i, 1]*((1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**alpha)*math.log(1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0]) # # Y*((T-T0)**alpha)*LN(T-T0)
        XHH = (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(2*alpha) # # (T-T0)**(2*alpha)
        XII = (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(2*alpha)*math.log(1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0]) # # (T-T0)**(2*alpha)*LN(T-T0)
        XJJ = (1 + source_frame.iloc[i, 0]-source_frame.iloc[0, 0])**(2*alpha-1) # # (T-T0)**(2*alpha-1)
        calcul_frame.append({'XAA': XAA, 'XBB': XBB, 'XCC': XCC, 'XDD': XDD, 'XEE': XEE, 'XFF': XFF, 'XGG': XGG, 'XHH': XHH, 'XII': XII, 'XJJ': XJJ})

    calcul_frame = pd.DataFrame(calcul_frame) # # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    Z = q1 + q2*(1 + source_frame.iloc[:, 0]-source_frame.iloc[0, 0])**alpha

    print('Model Parameter: T0 = {}'.format((source_frame.iloc[0, 0]-1)))
    print('Model Parameter: Y0 = {}'.format(q1))
    print('Model Parameter: A = {:.4f}'.format(q2))
    print('Model Parameter: Alpha = {:.4f}'.format(alpha))
    print('Estimator Result: Mean Value: {:,.4f}'.format(sp.mean(Z)))
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f}'.format(mean_squared_error(source_frame.iloc[:, 1], Z)))
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}'.format(math.sqrt(mean_squared_error(source_frame.iloc[:, 1], Z))))


def approx_power_function_b(source_frame, q1, q2, q3, q4, alpha):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Regressor,
    source_frame.iloc[:, 2]: Regressand,
    q1, q2, q3, q4, alpha: Parameters
    '''
    result_frame = source_frame.iloc[:, 0] # # DataFrame for Approximation Results
    calcul_frame = [] # # Blank List for Calculation Results
    for i in range(source_frame.shape[0]):
        XAA = source_frame.iloc[i, 1] # # '{X}'
        XBB = q3 + ((q4-q3)/(q2-q1)**alpha)*(source_frame.iloc[i, 1]-q1)**alpha # # '{RESULT}(Yhat) = U1 + ((U2-U1)/(TAU2-TAU1)**Alpha)*({X}-TAU1)**Alpha'
        XCC = (source_frame.iloc[i, 2]-(q3 + ((q4-q3)/(q2-q1)**alpha)*(source_frame.iloc[i, 1]-q1)**alpha))**2 # # '(Yhat-Y)**2'
        XDD = abs(source_frame.iloc[i, 2]-(q3 + ((q4-q3)/(q2-q1)**alpha)*(source_frame.iloc[i, 1]-q1)**alpha)) # # 'ABS(Yhat-Y)'
        calcul_frame.append({'XAA': XAA, 'XBB': XBB, 'XCC': XCC, 'XDD': XDD})

    calcul_frame = pd.DataFrame(calcul_frame) # # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    Z = q3 + ((q4-q3)/(q2-q1)**alpha)*(source_frame.iloc[:, 1]-q1)**alpha


    print('Model Parameter: TAU1 = {}'.format(q1))
    print('Model Parameter: TAU2 = {}'.format(q2))
    print('Model Parameter: U1 = {}'.format(q3))
    print('Model Parameter: U2 = {}'.format(q4))
    print('Model Parameter: Alpha = {:.4f}'.format(alpha))
    print('Model Parameter: A: = (U2-U1)/(TAU2-TAU1)**Alpha = {:,.4f}'.format((q4-q3)/(q2-q1)**alpha))
    print('Estimator Result: Mean Value: {:,.4f}'.format(sp.mean(Z)))
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f}'.format(mean_squared_error(source_frame.iloc[:, 2], Z)))
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}'.format(math.sqrt(mean_squared_error(source_frame.iloc[:, 2], Z))))


def approx_power_function_c(source_frame, q1, q2, q3, q4):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Regressor,
    source_frame.iloc[:, 2]: Regressand,
    q1, q2, q3, q4: Parameters
    '''

    alpha = math.log(q4/q3)/math.log(q1/q2)
    result_frame = source_frame.iloc[:, 0] # # DataFrame for Approximation Results
    calcul_frame = [] # # Blank List for Calculation Results
    for i in range(source_frame.shape[0]):
        XAA = source_frame.iloc[i, 1] # # '{X}'
        XBB = q3*(q1/source_frame.iloc[i, 1])**alpha # # '{RESULT}{Hat}{Y} = Y1*(X1/{X})**Alpha'
        XCC = source_frame.iloc[i, 2]-q3*(q1/source_frame.iloc[i, 1])**alpha # # '{Hat-1}{Y}'
        XDD = abs(source_frame.iloc[i, 2]-q3*(q1/source_frame.iloc[i, 1])**alpha) # # 'ABS({Hat-1}{Y})'
        XEE = (source_frame.iloc[i, 2]-q3*(q1/source_frame.iloc[i, 1])**alpha)**2 # # '({Hat-1}{Y})**2'
        calcul_frame.append({'XAA': XAA, 'XBB': XBB, 'XCC': XCC, 'XDD': XDD, 'XEE': XEE})

    calcul_frame = pd.DataFrame(calcul_frame) # # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    Z = q3*(source_frame.iloc[:, 1].rdiv(q1))**alpha


    print('Model Parameter: X1 = {:.4f}'.format(q1))
    print('Model Parameter: X2 = {}'.format(q2))
    print('Model Parameter: Y1 = {:.4f}'.format(q3))
    print('Model Parameter: Y2 = {}'.format(q4))
    print('Model Parameter: Alpha: = LN(Y2/Y1)/LN(X1/X2) = {:.4f}'.format(alpha))
    print('Estimator Result: Mean Value: {:,.4f}'.format(sp.mean(Z)))
    print('Estimator Result: Mean Squared Deviation, MSD: {:,.4f}'.format(mean_squared_error(source_frame.iloc[:, 2], Z)))
    print('Estimator Result: Root-Mean-Square Deviation, RMSD: {:,.4f}'.format(math.sqrt(mean_squared_error(source_frame.iloc[:, 2], Z))))


def error_metrics(source_frame):
    '''Error Metrics Module'''
    DX = (source_frame.iloc[:, 2]-source_frame.iloc[:, 1]).div(source_frame.iloc[:, 1])
    DX = DX.abs()
    C = sp.mean(DX)
    print('Criterion, C: {:.6f}'.format(C))


def results_delivery_a(intervals, coefficients):
    '''Results Delivery Module
    intervals (1 + N): 1 + Number of Intervals
    coefficients: A-Coefficients'''
    for i in range(1 + intervals):
        print('Model Parameter: A{:02d} = {:.6f}'.format(i, coefficients[i]))


def results_delivery_k(intervals, coefficients):
    '''Results Delivery Module
    intervals: Number of Intervals
    coefficients: K-Coefficients'''
    for i in range(intervals):
        print('Model Parameter: K{:02d} = {:.6f}'.format(1 + i, coefficients[i]))


def capital_aquisitions(source_frame):
    '''
    source_frame.iloc[:, 0]: Period
    source_frame.iloc[:, 1]: Nominal Investment
    source_frame.iloc[:, 2]: Nominal Production
    source_frame.iloc[:, 3]: Real Production
    source_frame.iloc[:, 4]: Maximum Real Production
    source_frame.iloc[:, 5]: Nominal Capital
    source_frame.iloc[:, 6]: Labor
    '''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 3])>1:
        i -= 1
        base = i # # Basic Year
    '''Calculate Static Values'''
    XAA = source_frame.iloc[:, 3].div(source_frame.iloc[:, 5]) # # Fixed Assets Turnover Ratio
    XBB = source_frame.iloc[:, 1].div(source_frame.iloc[:, 3]) # # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    XCC = source_frame.iloc[:, 5].div(source_frame.iloc[:, 6]) # # Labor Capital Intensity
    XDD = source_frame.iloc[:, 3].div(source_frame.iloc[:, 6]) # # Labor Productivity
    XBB = XBB.div(XBB[0])
    XCC = XCC.div(XCC[0])
    XDD = XDD.div(XDD[0])
    XEE = sp.log(XCC) # # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    XFF = sp.log(XDD) # # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    XGG = source_frame.iloc[:, 4].div(source_frame.iloc[:, 5]) # # Max: Fixed Assets Turnover Ratio
    XHH = source_frame.iloc[:, 1].div(source_frame.iloc[:, 4]) # # Max: Investment to Gross Domestic Product Ratio
    XII = source_frame.iloc[:, 4].div(source_frame.iloc[:, 6]) # # Max: Labor Productivity
    XHH = XHH.div(XHH[0])
    XII = XII.div(XII[0])
    XJJ = sp.log(XII) # # Max: Log Labor Productivity
    XEE = pd.DataFrame(XEE, columns=['XEE']) # # Convert List to Dataframe
    XFF = pd.DataFrame(XFF, columns=['XFF']) # # Convert List to Dataframe
    XJJ = pd.DataFrame(XJJ, columns=['XJJ']) # # Convert List to Dataframe
    '''Calculate Dynamic Values'''
    N = int(input('Define Number of Line Segments for Pi: ')) # # Number of Periods
    if N >= 1:
        print('Number of Periods Provided: {}'.format(N))
        pi, knt = [], [] # # Pi Switch Points & Pi
        knt.append(0)
        i = 0
        if N == 1:
            knt.append(source_frame.shape[0]-1)
            pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i]-1, 0]))))
        elif N >= 2:
            while i<N:
                if i == N-1:
                    knt.append(source_frame.shape[0]-1)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i]-1, 0]))))
                    i += 1
                else:
                    y = int(input('Select Row for Year, Should Be More Than {}: = {}: '.format(0, source_frame.iloc[0, 0])))
                    if y>knt[i]:
                        knt.append(y)
                        pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0]))))
                        i += 1
        else:
            print('Error')
        XKK = []
        for i in range(1):
            XKK.append(sp.nan)
        if N == 1:
            j = 0
            for i in range(knt[j], knt[1 + j]):
                XKK.append(source_frame.iloc[1 + i, 5]-source_frame.iloc[i, 5] + pi[j]*source_frame.iloc[1 + i, 1]) # # Estimate: GCF[-] or CA[ + ]
        else:
            for j in range(N):
                if j == N-1:
                    for i in range(knt[j], knt[1 + j]):
                        XKK.append(source_frame.iloc[1 + i, 5]-source_frame.iloc[i, 5] + pi[j]*source_frame.iloc[1 + i, 1]) # # Estimate: GCF[-] or CA[ + ]
                else:
                    for i in range(knt[j], knt[1 + j]):
                        XKK.append(source_frame.iloc[1 + i, 5]-source_frame.iloc[i, 5] + pi[j]*source_frame.iloc[1 + i, 1]) # # Estimate: GCF[-] or CA[ + ]
        XKK = pd.DataFrame(XKK, columns=['XKK']) # # Convert List to Dataframe
        result_frame = pd.DataFrame(source_frame.iloc[:, 0], columns=['Period'])
        result_frame = pd.concat([result_frame, XAA, XBB, XCC, XDD, XEE, XFF, XGG, XHH, XII, XJJ, XKK], axis=1)
        result_frame.columns = ['Period', 'XAA', 'XBB', 'XCC', 'XDD', 'XEE', 'XFF', 'XGG', 'XHH', 'XII', 'XJJ', 'XKK']
        '''
        `-` Gross Capital Formation
        `+` Capital Acquisitions
        '''
        for i in range(N):
            if i == N-1:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i]-1, 0], pi[i]))
            else:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0], pi[i]))
        plt.figure(1)
        plt.plot(XCC, XDD)
        plt.plot(XCC, XII)
        plt.title('Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Labor Capital Intensity')
        plt.ylabel('Labor Productivity, {}=100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(2)
        plt.plot(XEE, XFF)
        plt.plot(XEE, XJJ)
        plt.title('Log Labor Productivity, Observed & Max, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Log Labor Capital Intensity')
        plt.ylabel('Log Labor Productivity, {}=100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(3)
        plt.plot(source_frame.iloc[:, 0], XAA)
        plt.plot(source_frame.iloc[:, 0], XGG)
        plt.title('Fixed Assets Turnover ($\\lambda$), Observed & Max, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Period')
        plt.ylabel('Fixed Assets Turnover ($\\lambda$), {}=100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(4)
        plt.plot(source_frame.iloc[:, 0], XBB)
        plt.plot(source_frame.iloc[:, 0], XHH)
        plt.title('Investment to Gross Domestic Product Ratio, \nObserved & Max, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio, {}=100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.figure(5)
        plt.plot(source_frame.iloc[:, 0], XKK)
        plt.title('Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[knt[0], 0], source_frame.iloc[knt[N]-1, 0]))
        plt.xlabel('Period')
        plt.ylabel('GCF or CA, {}=100'.format(source_frame.iloc[base, 0]))
        plt.grid(True)
        plt.show()
    else:
        print('N >= 1 is Required, N = {} Was Provided'.format(N))


def capital_retirement(source_frame):
    '''
    source_frame.iloc[:, 0]: Period
    source_frame.iloc[:, 1]: Nominal Investment
    source_frame.iloc[:, 2]: Nominal Production
    source_frame.iloc[:, 3]: Real Production
    source_frame.iloc[:, 4]: Nominal Capital
    source_frame.iloc[:, 5]: Labor
    '''
    '''Define Basic Year for Deflator'''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 3])>1:
        i -= 1
        base = i # # Basic Year
    '''Calculate Static Values'''
    YAA = source_frame.iloc[:, 4].div(source_frame.iloc[:, 5])
    YAA = sp.log(YAA.div(YAA[0])) # # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    YBB = source_frame.iloc[:, 3].div(source_frame.iloc[:, 5])
    YBB = sp.log(YBB.div(YBB[0])) # # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    YCC = source_frame.iloc[:, 1].div(source_frame.iloc[:, 3])
    YCC = YCC.div(YCC[0]) # # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    YDD = source_frame.iloc[:, 3].div(source_frame.iloc[:, 4]) # # Fixed Assets Turnover Ratio
    YAA = pd.DataFrame(YAA, columns=['YAA']) # # Convert List to Dataframe
    YBB = pd.DataFrame(YBB, columns=['YBB']) # # Convert List to Dataframe
    N = int(input('Define Number of Line Segments for Pi: ')) # # Number of Periods
    if N >= 1:
        print('Number of Periods Provided: {}'.format(N))
        pi, knt = [], [] # # Pi Switch Points & Pi
        knt.append(0)
        i = 0
        if N == 1:
            knt.append(source_frame.shape[0]-1)
            pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[:, 0][knt[1 + i]]))))
        elif N >= 2:
            while i<N:
                if i == N-1:
                    knt.append(source_frame.shape[0]-1)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0]))))
                    i += 1
                else:
                    y = int(input('Select Row for Year: '))
                    if y>knt[i]:
                        knt.append(y)
                        pi.append(float(input('Define Pi for Period from {} to {}: '.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0]))))
                        i += 1
        else:
            print('Error')
        YEE = []
        YFF = []
        YEE.append(sp.nan) # # Fixed Assets Retirement Value
        YFF.append(sp.nan) # # Fixed Assets Retirement Ratio
        '''Calculate Dynamic Values'''
        if N == 1:
            j = 0
            for i in range(knt[j], knt[1 + j]):
                YEE.append(source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j]*source_frame.iloc[i, 1]) # # Fixed Assets Retirement Value
                YFF.append((source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j]*source_frame.iloc[i, 1])/source_frame.iloc[1 + i, 4]) # # Fixed Assets Retirement Ratio
        else:
            for j in range(N):
                if j == N-1:
                    for i in range(knt[j], knt[1 + j]):
                        YEE.append(source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j]*source_frame.iloc[i, 1]) # # Fixed Assets Retirement Value
                        YFF.append((source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j]*source_frame.iloc[i, 1])/source_frame.iloc[1 + i, 4]) # # Fixed Assets Retirement Ratio
                else:
                    for i in range(knt[j], knt[1 + j]):
                        YEE.append(source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j]*source_frame.iloc[i, 1]) # # Fixed Assets Retirement Value
                        YFF.append((source_frame.iloc[i, 4]-source_frame.iloc[1 + i, 4] + pi[j]*source_frame.iloc[i, 1])/source_frame.iloc[1 + i, 4]) # # Fixed Assets Retirement Ratio
        YEE = pd.DataFrame(YEE, columns=['YEE']) # # Convert List to Dataframe
        YFF = pd.DataFrame(YFF, columns=['YFF']) # # Convert List to Dataframe
        result_frame = pd.DataFrame(source_frame.iloc[:, 0], columns=['Period'])
        result_frame = pd.concat([result_frame, YAA, YBB, YCC, YDD, YEE, YFF], axis=1, sort=True)
        result_frame.columns = ['Period', 'YAA', 'YBB', 'YCC', 'YDD', 'YEE', 'YFF']
        result_frame['YGG'] = result_frame['YFF']-result_frame['YFF'].mean()
        result_frame['YGG'] = result_frame['YGG'].abs()
        result_frame['YHH'] = result_frame['YFF']-result_frame['YFF'].shift(1)
        result_frame['YHH'] = result_frame['YHH'].abs()
        for i in range(N):
            if i == N-1:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0], pi[i]))
            else:
                print('Model Parameter: Pi for Period from {} to {}: {:.6f}'.format(source_frame.iloc[knt[i], 0], source_frame.iloc[knt[1 + i], 0], pi[i]))
        plt.figure(1)
        plt.title('Product, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Product, {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3])
        plt.grid(True)
        plt.figure(2)
        plt.title('Capital, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Capital, {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 4])
        plt.grid(True)
        plt.figure(3)
        plt.title('Fixed Assets Turnover ($\\lambda$), {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Fixed Assets Turnover ($\\lambda$), {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3].div(source_frame.iloc[:, 4]))
        plt.grid(True)
        plt.figure(4)
        plt.title('Investment to Gross Domestic Product Ratio, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('Investment to Gross Domestic Product Ratio, {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], YCC)
        plt.grid(True)
        plt.figure(5)
        plt.title('$\\alpha(t)$, Fixed Assets Retirement Ratio, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Period')
        plt.ylabel('$\\alpha(t)$, {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(source_frame.iloc[:, 0], YFF)
        plt.grid(True)
        plt.figure(6)
        plt.title('Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('$\\alpha(t)$, {}=100'.format(source_frame.iloc[base, 0]))
        plt.ylabel('Fixed Assets Retirement Value, {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(YFF, YEE)
        plt.grid(True)
        plt.figure(7)
        plt.title('Labor Capital Intensity, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[knt[N], 0]))
        plt.xlabel('Labor Capital Intensity, {}=100'.format(source_frame.iloc[base, 0]))
        plt.ylabel('Labor Productivity, {}=100'.format(source_frame.iloc[base, 0]))
        plt.plot(sp.exp(YAA), sp.exp(YBB))
        plt.grid(True)
        plt.show()
    else:
        print('N >= 1 is Required, N = {} Was Provided'.format(N))


def data_fetch_plot_a(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Gross Domestic Investment,
    source_frame.iloc[:, 2]: National Income,
    source_frame.iloc[:, 3]: Nominal Gross Domestic Product,
    source_frame.iloc[:, 4]: Real Gross Domestic Product
    '''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 4].div(source_frame.iloc[:, 3])
    '''`Real` Production'''
    source_frame['prd'] = source_frame.iloc[:, 2]*source_frame.iloc[:, 4].div(source_frame.iloc[:, 3])
    plt.figure()
    plt.title('Gross Private Domestic Investment & National Income, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5], label='Gross Private Domestic Investment')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 6], label='National Income')
    plt.xlabel('Period')
    plt.ylabel('Index')
    source_frame.iloc[:, 0] = (source_frame.iloc[:, 0].shift(-1) + source_frame.iloc[:, 0])/2
    X = (source_frame.iloc[:, 5].shift(-1) + source_frame.iloc[:, 5])/2
    Y = (source_frame.iloc[:, 6].shift(-1) + source_frame.iloc[:, 6])/2
    plt.plot(source_frame.iloc[:, 0], X, '--', source_frame.iloc[:, 0], Y, '--')
    plt.grid()
    plt.legend()
    plt.show()


def data_fetch_plot_b(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Gross Domestic Investment,
    source_frame.iloc[:, 2]: Nominal Gross Domestic Product,
    source_frame.iloc[:, 3]: Real Gross Domestic Product,
    source_frame.iloc[:, 4]: Prime Rate
    '''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])
    plt.figure()
    plt.plot(source_frame.iloc[:, 4], source_frame.iloc[:, 5])
    plt.title('Gross Private Domestic Investment, A006RC, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Percentage')
    plt.ylabel('Millions of Dollars')
    plt.grid(True)
    plt.show()


def data_fetch_plot_c(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Gross Domestic Investment,
    source_frame.iloc[:, 2]: Nominal Gross Domestic Product,
    source_frame.iloc[:, 3]: Real Gross Domestic Product,
    source_frame.iloc[:, 4]: M1
    '''
    '''`Real` Investment'''
    source_frame['inv'] = source_frame.iloc[:, 1]*source_frame.iloc[:, 3].div(source_frame.iloc[:, 2])
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3], label='Real Gross Domestic Product')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5], label='`Real` Gross Domestic Investment')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 4], label='Money Supply')
    plt.title('Indexes, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.legend()
    plt.grid(True)
    plt.show()


def data_fetch_plot_census_d(series_ids):
    '''series_ids: List for Series'''
    file_name = 'dataset_usa_census1975.zip'
    result_frame = pd.DataFrame()
    for series_id in series_ids:
        title = fetch_census_description(file_name, series_id)
        print(f'<{series_id}> {title}')
        data_frame = fetch_census(file_name, series_id)
        data_frame = data_frame.div(data_frame.iloc[0, :]/100)
        result_frame = pd.concat([result_frame, data_frame], axis=1, sort=True)

    plt.figure()
    plt.semilogy(result_frame)
    plt.title('Series P 231$-$300. Physical Output of Selected Manufactured Commodities: {}$-${}'.format(result_frame.index[0], result_frame.index[-1]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend(series_ids)
    plt.show()


def data_fetch_plot_census_h():
    '''Census 1975, Land in Farms'''
    file_name = 'dataset_usa_census1975.zip'
    result_frame = fetch_census(file_name, 'K0005')
    plt.figure()
    plt.plot(result_frame.index, result_frame.iloc[:, 0])
    plt.title('Land in Farms')
    plt.xlabel('Period')
    plt.ylabel('1,000 acres')
    plt.grid()
    plt.show()


def data_fetch_plot_d(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Gross Domestic Investment,
    source_frame.iloc[:, 2]: Gross Domestic Investment Price Index,
    source_frame.iloc[:, 3]: Fixed Investment,
    source_frame.iloc[:, 4]: Fixed Investment Price Index,
    source_frame.iloc[:, 5]: Real Gross Domestic Product
    '''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-100)>0.1:
        i -= 1
        base = i # # Basic Year
    '''Real Investment, Billions'''
    source_frame['inv'] = source_frame.iloc[base, 1]*source_frame.iloc[:, 2].div(100*1000)
    '''Real Fixed Investment, Billions'''
    source_frame['fnv'] = source_frame.iloc[base, 3]*source_frame.iloc[:, 4].div(100*1000)
    source_frame.iloc[:, 5] = source_frame.iloc[:, 5].div(1000)
    plt.figure(1)
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 6], label='Real Gross Private Domestic Investment $GPDI$')
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 7], color = 'red', label='Real Gross Private Fixed Investment, Nonresidential $GPFI(n)$')
    plt.title('Real Indexes, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.legend()
    plt.grid(True)
    plt.figure(2)
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 5])
    plt.title('Real Gross Domestic Product $GDP$, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(3)
    plt.plot(source_frame.iloc[:, 6], source_frame.iloc[:, 5])
    plt.title('$GPDI$ & $GPFI(n)$, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.figure(4)
    plt.plot(source_frame.iloc[:, 7], source_frame.iloc[:, 5])
    plt.title('$GPFI(n)$ & $GDP$, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Billions of Dollars')
    plt.ylabel('Billions of Dollars')
    plt.grid(True)
    plt.show()


def plot_approx_linear(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Real Values for Price Deflator,
    source_frame.iloc[:, 2]: Nominal Values for Price Deflator,
    source_frame.iloc[:, 3]: Regressor,
    source_frame.iloc[:, 4]: Regressand
    '''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 1])>1:
        i -= 1
        base = i # # Basic Year
    D = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]) # # Deflator
    result_frame = source_frame.iloc[:, 0] # # DataFrame for Based Linear Approximation Results
    calcul_frame = [] # # Blank List for Calculation Results
    for i in range(source_frame.shape[0]):
        X = source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0])
        Y = source_frame.iloc[i, 4]*D[i]/(source_frame.iloc[0, 4]*D[0])
        calcul_frame.append({'X': X, 'Y': Y})

    calcul_frame = pd.DataFrame(calcul_frame) # # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    S1, S2, S3, S4 = 0, 0, 0, 0 # # X, Y, X**2, XY # # Summarize
    for i in range(source_frame.shape[0]):
        S1 += source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0])
        S2 += source_frame.iloc[i, 4]*D[i]/(source_frame.iloc[0, 4]*D[0])
        S3 += (source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0]))**2
        S4 += source_frame.iloc[i, 3]*source_frame.iloc[i, 4]*(D[i])**2/(source_frame.iloc[0, 3]*source_frame.iloc[0, 4]*(D[0]**2))
    '''Approximation'''
    A0 = (S2*S3-S1*S4)/(source_frame.shape[0]*S3-S1**2)
    A1 = (source_frame.shape[0]*S4-S1*S2)/(source_frame.shape[0]*S3-S1**2)
    calcul_frame = [] # # Blank List for Calculation Results
    for i in range(source_frame.shape[0]):
        Y = A0 + A1*source_frame.iloc[i, 3]*D[i]/(source_frame.iloc[0, 3]*D[0])
        calcul_frame.append({'YH': Y})

    calcul_frame = pd.DataFrame(calcul_frame) # # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    print('Period From: {} Through: {}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    print('Prices: {}=100'.format(source_frame.iloc[base, 0]))
    print('Model: Yhat = {:.4f}+{:.4f}*X'.format(A0, A1))
    print('Model Parameter: A0 = {:.4f}'.format(A0))
    print('Model Parameter: A1 = {:.4f}'.format(A1))
    plt.figure()
    plt.title('$Y(X)$, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Gross Private Domestic Investment, $X(\\tau)$, {}=100, {}=100'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0]))
    plt.ylabel('Gross Domestic Product, $Y(\\tau)$, {}=100, {}=100'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0]))
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 2])
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 3], label='$\\hat Y = {:.4f}+{:.4f}X$'.format(A0, A1))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_approx_log_linear(source_frame):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Real Values for Price Deflator,
    source_frame.iloc[:, 2]: Nominal Values for Price Deflator,
    source_frame.iloc[:, 3]: Regressor,
    source_frame.iloc[:, 4]: Regressand
    '''
    i = source_frame.shape[0]-1
    while abs(source_frame.iloc[i, 2]-source_frame.iloc[i, 1])>1:
        i -= 1
        base = i # # Basic Year
    D = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]) # # Deflator
    result_frame = source_frame.iloc[:, 0] # # DataFrame for Based Log-Linear Approximation Results
    calcul_frame = [] # # Blank List for Calculation Results

    for i in range(source_frame.shape[0]):
        X = math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3])
        Y = math.log(source_frame.iloc[i, 4]) + math.log(D[i])-math.log(source_frame.iloc[0, 4])-math.log(D[0])
        calcul_frame.append({'X': X, 'Y': Y})

    calcul_frame = pd.DataFrame(calcul_frame) # # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    S1, S2, S3, S4 = 0, 0, 0, 0 # # Summarize
    for i in range(source_frame.shape[0]):
        S1 += math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3])
        S2 += math.log(source_frame.iloc[i, 4]) + math.log(D[i])-math.log(source_frame.iloc[0, 4])-math.log(D[0])
        S3 += (math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3]))**2
        S4 += (math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3]))*(math.log(D[i]) + math.log(source_frame.iloc[i, 4])-math.log(D[0])-math.log(source_frame.iloc[0, 4]))
    '''Approximation'''
    A0 = (S2*S3-S1*S4)/(source_frame.shape[0]*S3-S1**2)
    A1 = (source_frame.shape[0]*S4-S1*S2)/(source_frame.shape[0]*S3-S1**2)
    calcul_frame = [] # # Blank List for Calculation Results
    for i in range(source_frame.shape[0]):
        Y = A0 + A1*(math.log(source_frame.iloc[i, 3])-math.log(source_frame.iloc[0, 3])) # # Yhat
        calcul_frame.append({'YH': Y})

    calcul_frame = pd.DataFrame(calcul_frame) # # Convert List to Dataframe
    result_frame = pd.concat([result_frame, calcul_frame], axis=1, sort=True)

    print('Period From: {} Through: {}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    print('Prices: {}=100'.format(source_frame.iloc[base, 0]))
    print('Model: Yhat = {:.4f}+{:.4f}*Ln(X)'.format(A0, A1))
    print('Model Parameter: A0 = {:.4f}'.format(A0))
    print('Model Parameter: A1 = {:.4f}'.format(A1))
    plt.figure()
    plt.title('$Y(X)$, {}=100, {}$-${}'.format(source_frame.iloc[base, 0], source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Logarithm Prime Rate, $X(\\tau)$, {}=100'.format(source_frame.iloc[0, 0]))
    if source_frame.columns[4][:7] == 'A032RC1':
        desc = 'National Income'
    elif source_frame.columns[4][:7] == 'A191RC1':
        desc = 'Gross Domestic Product'
    plt.ylabel('Logarithm {}, $Y(\\tau)$, {}=100, {}=100'.format(desc, source_frame.iloc[base, 0], source_frame.iloc[0, 0]))
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 2])
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 3], label='$\\hat Y = {:.4f}+{:.4f}X$'.format(A0, A1))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_built_in(module):
    file_name = 'datasetAutocorrelation.txt'
    source_frame = pd.read_csv(file_name)
    source_frame = source_frame[source_frame.columns[[1, 0, 2]]]
    series_ids = source_frame.iloc[:, 0].sort_values().unique()

    for i, series_id in enumerate(series_ids):
        current = fetch_world_bank('datasetAutocorrelation.txt', series_id)
        plt.figure(1 + i)
        module(current.iloc[:, 1])
        plt.grid(True)


    file_name = 'chn_tur_gdp.zip'
    source_frame = pd.read_csv(file_name)
    source_frame = source_frame[source_frame.columns[[1, 0, 2]]]
    series_ids = source_frame.iloc[:, 0].sort_values().unique()

    for i, series_id in enumerate(series_ids):
        current = fetch_world_bank('chn_tur_gdp.zip', series_id)
        plt.figure(5 + i)
        module(current.iloc[:, 1])
        plt.grid(True)


    plt.show()


def plot_capital_modelling(source_frame, base):
    '''
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Investment,
    source_frame.iloc[:, 2]: Production,
    source_frame.iloc[:, 3]: Capital,
    source_frame.iloc[:, 4]: Capital Retirement
    '''
    QS = sp.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]), 1)
    QL = sp.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 2].div(source_frame.iloc[:, 3]), 1)
    '''Gross Fixed Investment to Gross Domestic Product Ratio'''
    S = QS[1] + QS[0]*source_frame.iloc[:, 0]
    '''Fixed Assets Turnover'''
    L = QL[1] + QL[0]*source_frame.iloc[:, 0]
    KA = capital(source_frame, QS[1], QS[0], QL[1], QL[0], 0.875)
    KB = capital(source_frame, QS[1], QS[0], QL[1], QL[0], 1)
    KC = capital(source_frame, QS[1], QS[0], QL[1], QL[0], 1.125)
    plt.figure(1)
    plt.title('Fixed Assets Turnover ($\\lambda$) for the US, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 2].div(source_frame.iloc[:, 3]), label='$\\lambda$')
    if QL[0]<0:
        plt.plot(source_frame.iloc[:, 0], L, label='$\\lambda = {1:, .4f}\\ {0:, .4f}\\times t$'.format(QL[0], QL[1]))
    else:
        plt.plot(source_frame.iloc[:, 0], L, label='$\\lambda = {1:, .4f} + {0:, .4f} \\times t$'.format(QL[0], QL[1]))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Gross Fixed Investment as Percentage of GDP ($S$) for the US, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 1].div(source_frame.iloc[:, 2]), label='$S$')
    if QS[0]<0:
        plt.plot(source_frame.iloc[:, 0], S, label='$S = {1:, .4f}\\ {0:, .4f}\\times t$'.format(QS[0], QS[1]))
    else:
        plt.plot(source_frame.iloc[:, 0], S, label='$S = {1:, .4f} + {0:, .4f} \\times t$'.format(QS[0], QS[1]))
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.title('$\\alpha$ for the US, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-2, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 4], label='$\\alpha$')
    plt.grid(True)
    plt.legend()
    plt.figure(4)
    plt.title('$K$ for the US, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-2, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars, {}=100'.format(source_frame.iloc[base, 0]))
    plt.semilogy(source_frame.iloc[:, 0], KA, label='$K\\left(\\pi = \\frac{7}{8}\\right)$')
    plt.semilogy(source_frame.iloc[:, 0], KB, label='$K\\left(\\pi = 1\\right)$')
    plt.semilogy(source_frame.iloc[:, 0], KC, label='$K\\left(\\pi = \\frac{9}{8}\\right)$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_fourier_discrete(source_frame, precision=10):
    '''
    source_frame.iloc[:, 0]: Period;
    source_frame.iloc[:, 1]: Series
    Discrete Fourier Transform based on Simpson's Rule
    '''
    f1p = sp.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1], 1)
    LX = f1p[1] + f1p[0]*source_frame.iloc[:, 0]
    Q = [] # # Blank List for Fourier Coefficients
    for i in range(1 + precision):
        c = 2*(source_frame.iloc[:, 1]-LX)*sp.cos(2*sp.pi*i*(source_frame.iloc[:, 0]-source_frame.iloc[0, 0]).div(source_frame.shape[0]))
        s = 2*(source_frame.iloc[:, 1]-LX)*sp.sin(2*sp.pi*i*(source_frame.iloc[:, 0]-source_frame.iloc[0, 0]).div(source_frame.shape[0]))
        Q.append({'cos': c.mean(), 'sin': s.mean()})

    Q = pd.DataFrame(Q) # # Convert List to Dataframe
    Q['cos'][0] = Q['cos'][0]/2
    EX = pd.DataFrame(1, index = range(1 + source_frame.shape[0]), columns=['EX'])
    EX = Q['cos'][0]
    plt.figure()
    plt.title('$\\alpha$ for the US, {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 1], label='$\\alpha$')
    for i in range(1, 1 + precision):
        EX = EX + Q['cos'][i]*sp.cos(2*sp.pi*i*(source_frame.iloc[:, 0]-source_frame.iloc[0, 0]).div(source_frame.shape[0])) + Q['sin'][i]*sp.sin(2*sp.pi*i*(source_frame.iloc[:, 0]-source_frame.iloc[0, 0]).div(source_frame.shape[0]))
        plt.plot(source_frame.iloc[:, 0], LX + EX, label='$FT_{{{:02}}}(\\alpha)$'.format(i))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_elasticity(source):
    '''
    source.iloc[:, 0]: Period,
    source.iloc[:, 1]: Real Values for Price Deflator,
    source.iloc[:, 2]: Nominal Values for Price Deflator,
    source.iloc[:, 3]: Focused Series
    '''
    if source.columns[3] == 'A032RC1':
        desc = 'National Income'
    else:
        desc = 'Series'
    i = source.shape[0]-1
    while abs(source.iloc[i, 2]-source.iloc[i, 1])>1:
        i -= 1
        base = i
    source['ser'] = source.iloc[:, 1]*source.iloc[:, 3].div(source.iloc[:, 2])
    source['sma'] = source.iloc[:, 4].rolling(window=2).mean() # # source['sma'] = (source.iloc[:, 4] + source.iloc[:, 4].shift(1))/2
    source['ela'] = 2*(source.iloc[:, 4]-source.iloc[:, 4].shift(1)).div(source.iloc[:, 4] + source.iloc[:, 4].shift(1))
    source['elb'] = (source.iloc[:, 4].shift(-1)-source.iloc[:, 4].shift(1)).div(2*source.iloc[:, 4])
    source['elc'] = 2*(source.iloc[:, 4].shift(-1)-source.iloc[:, 4].shift(1)).div(source.iloc[:, 4].shift(1) + 2*source.iloc[:, 4] + source.iloc[:, 4].shift(-1))
    source['eld'] = (-source.iloc[:, 4].shift(1)-source.iloc[:, 4] + source.iloc[:, 4].shift(-1) + source.iloc[:, 4].shift(-2)).div(2*source.iloc[:, 4] + 2*source.iloc[:, 4].shift(-1))
    result_frame = source[source.columns[[0, 4, 5, 6, 7, 8, 9]]]
    plt.figure(1)
    plt.title('{}, {}, {}=100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.xlabel('Period')
    plt.ylabel('Billions of Dollars, {}=100'.format(result_frame.iloc[base, 0]))
    plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 1], label='{}'.format(source.columns[3]))
    plt.plot(result_frame.iloc[:, 0].rolling(window=2).mean(), result_frame.iloc[:, 2], label='A032RC1, Rolling Mean, Window = 2')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Elasticity: {}, {}, {}=100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.plot(result_frame.iloc[:, 0].rolling(window=2).mean(), result_frame.iloc[:, 3], label='$\\overline{E}_{T+\\frac{1}{2}}$')
    plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 4], label='$E_{T+1}$')
    plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 5], label='$\\overline{E}_{T+1}$')
    plt.plot(result_frame.iloc[:, 0].rolling(window=2).mean(), result_frame.iloc[:, 6], label='$\\overline{\\epsilon(E_{T+\\frac{1}{2}})}$')
    plt.grid(True)
    plt.legend()
    plt.figure(3)
    plt.title('Elasticity: {}, {}, {}=100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.xlabel('{}, {}, {}=100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.ylabel('Elasticity: {}, {}, {}=100'.format(desc, source.columns[3], result_frame.iloc[base, 0]))
    plt.plot(result_frame.iloc[:, 1], result_frame.iloc[:, 6], label='$\\frac{\\epsilon(X)}{X}$')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_kzf(source_frame):
    '''Kolmogorov--Zurbenko Filter
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series'''

    '''DataFrame for Kolmogorov--Zurbenko Filter Results'''
    result_frame_a = source_frame
    '''DataFrame for Kolmogorov--Zurbenko Filter Residuals'''
    result_frame_b = pd.concat([source_frame.iloc[:, 0], source_frame.iloc[:, 0].rolling(window=2).mean()], axis=1, sort=False)
    result_frame_b = pd.concat([result_frame_b, (source_frame.iloc[:, 1]-source_frame.iloc[:, 1].shift(1)).div(source_frame.iloc[:, 1].shift(1))], axis=1, sort=False)
    for k in range(1, 1 + source_frame.shape[0]//2):
        cap = 'col{:02d}'.format(k)
        result_frame_a[cap] = sp.nan
        for j in range(1, 1 + source_frame.shape[0]-k):
            vkz = 0
            for i in range(1 + k):
                vkz += result_frame_a.iloc[i + j-1, 1]*scipy.special.binom(k, i)/(2**k)
            result_frame_a.iloc[i + j-(k//2)-1, 1 + k] = vkz
        if k%2 == 0:
            result_frame_b = pd.concat([result_frame_b, (source_frame.iloc[:, 1 + k]-source_frame.iloc[:, 1 + k].shift(1)).div(source_frame.iloc[:, 1 + k].shift(1))], axis=1, sort=False)
        else:
            result_frame_b = pd.concat([result_frame_b, (source_frame.iloc[:, 1 + k].shift(-1)-source_frame.iloc[:, 1 + k]).div(source_frame.iloc[:, 1 + k])], axis=1, sort=False)
    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(result_frame_a.iloc[:, 0], result_frame_a.iloc[:, 1], label='Original Series')
    for i in range(2, 1 + source_frame.shape[0]//2):
        if i%2 == 0:
            plt.plot(result_frame_a.iloc[:, 0].rolling(window=2).mean(), result_frame_a.iloc[:, i], label='$KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frame_a.iloc[:, 0], result_frame_a.iloc[:, i], label='$KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Kolmogorov$-$Zurbenko Filter Residuals')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(result_frame_b.iloc[:, 1], result_frame_b.iloc[:, 2], label='Residuals')
    for i in range(3, 2 + source_frame.shape[0]//2):
        if i%2 == 0:
            plt.plot(result_frame_b.iloc[:, 1], result_frame_b.iloc[:, i], label='$\\delta KZF(\\lambda = {})$'.format(i-1))
        else:
            plt.plot(result_frame_b.iloc[:, 0], result_frame_b.iloc[:, i], label='$\\delta KZF(\\lambda = {})$'.format(i-1))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_pearson_r_test(source_frame):
    '''Left-Side & Right-Side Rolling Means' Calculation & Plotting
    source_frame.index: Period,
    source_frame.iloc[:, 0]: Series'''

    result_frame = pd.DataFrame(columns=['window'])
    for i in range(1 + source_frame.shape[0]//2):
        '''Shift Mean Values to Left'''
        L_frame = source_frame.iloc[:, 0].rolling(window=1 + i).mean().shift(-i)
        '''Shift Mean Values to Right'''
        R_frame = source_frame.iloc[:, 0].rolling(window=1 + i).mean()
        numerator = stats.pearsonr(source_frame.iloc[:, 0][R_frame.notna()].tolist(), R_frame.dropna().tolist())[0]
        denominator = stats.pearsonr(source_frame.iloc[:, 0][L_frame.notna()].tolist(), L_frame.dropna().tolist())[0]
        result_frame = result_frame.append({'window':numerator/denominator}, ignore_index=True)
    '''Plot 'Window' to 'Right-Side to Left-Side Pearson R'''
    plt.figure()
    plt.title('Right-Side to Left-Side Pearson R Ratio')
    plt.xlabel('`Window`')
    plt.ylabel('Index')
    plt.plot(result_frame, label='Right-Side to Left-Side Pearson R Ratio')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_rmf(source_frame):
    '''
    source_frame.iloc[:, 0]: Period;
    source_frame.iloc[:, 1]: Series
    Rolling Mean Filter'''
    plt.figure(1)
    plt.title('Moving Average {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    source_frame['sma'] = source_frame.iloc[:, 1].rolling(window=1, center=True).mean()
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 2], label='$Y$')
    '''Smoothed Series Calculation'''
    for i in range(1, source_frame.shape[0]//2):
        source_frame.iloc[:, 2] = source_frame.iloc[:, 1].rolling(window=1 + i, center=True).mean()
        if i%2 == 0:
            plt.plot(0.5 + source_frame.iloc[:, 0], source_frame.iloc[:, 2], label='$\\bar Y_{{m = {}}}$'.format(i))
        else:
            plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 2], label='$\\bar Y_{{m = {}}}$'.format(i))
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.title('Moving Average Deviations {}$-${}'.format(source_frame.iloc[0, 0], source_frame.iloc[source_frame.shape[0]-1, 0]))
    plt.xlabel('Period')
    plt.ylabel('Deviations ($\\delta$), Percent')
    source_frame['del'] = (source_frame.iloc[:, 1].rolling(window=1, center=True).mean().shift(-1)-source_frame.iloc[:, 1].rolling(window=1, center=True).mean()).div(source_frame.iloc[:, 1].rolling(window=1, center=True).mean())
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 3], label='$\\delta(Y)$')
    '''Deviations Calculation'''
    for i in range(1, source_frame.shape[0]//2):
        source_frame.iloc[:, 3] = (source_frame.iloc[:, 1].rolling(window=1 + i, center=True).mean().shift(-1)-source_frame.iloc[:, 1].rolling(window=1 + i, center=True).mean()).div(source_frame.iloc[:, 1].rolling(window=1 + i, center=True).mean())
        if i%2 == 0:
            plt.plot(0.5 + source_frame.iloc[:, 0], source_frame.iloc[:, 3], label='$\\delta(\\bar Y_{{m = {}}})$'.format(i))
        else:
            plt.plot(source_frame.iloc[:, 0], source_frame.iloc[:, 3], label='$\\delta(\\bar Y_{{m = {}}})$'.format(i))
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_ses(source_frame, window, step):
    '''Single Exponential Smoothing
    Robert Goodell Brown, 1956
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series'''
    '''Average of Window-First Entries'''
    S = source_frame.iloc[:window, 1].mean()
    '''DataFrame for Exponentially Smoothed Series'''
    smooth_frame = pd.DataFrame(source_frame.iloc[:, 0])
    '''DataFrame for Deltas of Exponentially Smoothed Series'''
    deltas_frame = pd.DataFrame(0.5 + source_frame.iloc[:(source_frame.shape[0]-1), 0])
    delta = (source_frame.iloc[:, 1].shift(-1)-source_frame.iloc[:, 1]).div(source_frame.iloc[:, 1].shift(-1))
    delta = delta[:(len(delta)-1)]
    deltas_frame = pd.concat([deltas_frame, delta], axis=1, sort=False)
    plt.figure()
    plt.title('Deltas of Exponentially Smoothed Series')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.scatter(source_frame.iloc[:, 0], source_frame.iloc[:, 1], label='Original Series')
    k = 0
    while True:
        k += 1
        alpha=0.25 + step*(k-1)
        ses, dse = [], []
        ses.append(alpha*source_frame.iloc[0, 1] + (1-alpha)*S)
        for i in range(1, source_frame.shape[0]):
            ses.append(alpha*source_frame.iloc[i, 1] + (1-alpha)*ses[i-1])
            dse.append((ses[i]-ses[i-1])/ses[i-1])
            cap = 'col{:02d}'.format(k)
        ses = pd.DataFrame(ses, columns=[cap])
        dse = pd.DataFrame(dse, columns=[cap])
        smooth_frame = pd.concat([smooth_frame, ses], axis=1, sort=False)
        deltas_frame = pd.concat([deltas_frame, dse], axis=1, sort=False)
        plt.plot(source_frame.iloc[:, 0], ses, label='Smoothing: $w = {}, \\alpha={:, .2f}$'.format(window, alpha))

        if k >= 0.5 + 0.75/step: # # 0.25 + step*(k-0.5) >= 1
            break
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_census_a(source_frame, base):
    plt.figure()
    plt.plot(source_frame.iloc[:, 0], label='Fabricant S., Shiskin J., NBER')
    plt.plot(source_frame.iloc[:, 1], color = 'red', linewidth = 4, label='W.M. Persons')
    plt.plot(source_frame.iloc[:, 2], label='E. Frickey')
    plt.axvline(x = source_frame.index[base], linestyle = ':')
    plt.title('US Manufacturing Indexes Of Physical Production Of Manufacturing, {}=100'.format(source_frame.index[base]))
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid()
    plt.legend()
    plt.show()


def plot_census_c(source_frame, base):
    plt.figure(1)
    plt.semilogy(source_frame.index, source_frame.iloc[:, 1], label='P265 - Raw Steel Produced - Total, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 2], label='P266 - Raw Steel Produced - Bessemer, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 3], label='P267 - Raw Steel Produced - Open Hearth, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 4], label='P268 - Raw Steel Produced - Crucible, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 5], label='P269 - Raw Steel Produced - Electric and All Other, {}=100'.format(source_frame.index[base[2]]))
    plt.axvline(x = source_frame.index[base[0]], linestyle = ':')
    plt.axvline(x = source_frame.index[base[2]], linestyle = ':')
    plt.title('Steel Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.figure(2)
    plt.semilogy(source_frame.index, source_frame.iloc[:, 0], label='P262 - Rails Produced, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 6], label='P293 - Locomotives Produced, {}=100'.format(source_frame.index[base[1]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 7], label='P294 - Railroad Passenger Cars Produced, {}=100'.format(source_frame.index[base[0]]))
    plt.semilogy(source_frame.index, source_frame.iloc[:, 8], label='P295 - Railroad Freight Cars Produced, {}=100'.format(source_frame.index[base[0]]))
    plt.axvline(x = source_frame.index[base[0]], linestyle = ':')
    plt.axvline(x = source_frame.index[base[1]], linestyle = ':')
    plt.title('Rails & Cars Production')
    plt.xlabel('Period')
    plt.ylabel('Percentage')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_e(source_frame):
    '''
    source_frame.iloc[:, 0]: Investment,
    source_frame.iloc[:, 1]: Production,
    source_frame.iloc[:, 2]: Capital
    '''
    '''Investment to Production Ratio'''
    source_frame['S'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
    '''Fixed Assets Turnover Ratio'''
    source_frame['L'] = source_frame.iloc[:, 1].div(source_frame.iloc[:, 2])
    QS = sp.polyfit(source_frame.iloc[:, 0], source_frame.iloc[:, 1], 1)
    QL = sp.polyfit(source_frame.iloc[:, 1], source_frame.iloc[:, 2], 1)
    source_frame['RS'] = QS[1] + QS[0]*source_frame.iloc[:, 0]
    source_frame['RL'] = QL[1] + QL[0]*source_frame.iloc[:, 2]
    plt.figure()
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 1])
    plt.semilogy(source_frame.iloc[:, 0], source_frame.iloc[:, 5])
    plt.title('Investment to Production Ratio, {}$-${}'.format(source_frame.index[0], source_frame.index[-1]))
    plt.xlabel('Investment, Billions of Dollars')
    plt.ylabel('Gross Domestic Product, Billions of Dollars')
    plt.grid(True)
    plt.legend(['$P(I)$', '$\\hat P(I) = %.4f+%.4f I$' %(QS[1], QS[0])])
    print(source_frame.iloc[:, 3].describe())
    print(QS)
    print(source_frame.iloc[:, 4].describe())
    print(QL)
    plt.show()


def plot_f(source_frame_a, source_frame_b, source_frame_c, source_frame_d):
    '''
    source_frame_a: Production _frame,
    source_frame_b: Labor _frame,
    source_frame_c: Capital _frame,
    source_frame_d: Capacity Utilization _frame'''
    base = (31, 1)
    '''Plotting'''
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(source_frame_a.index, source_frame_a.iloc[:, 0], label='Kurenkov Data, {}=100'.format(source_frame_a.index[base[0]]))
    axs[0].plot(source_frame_a.index, source_frame_a.iloc[:, 1], label='BEA Data, {}=100'.format(source_frame_a.index[base[0]]))
    axs[0].plot(source_frame_a.index, source_frame_a.iloc[:, 2], label='FRB Data, {}=100'.format(source_frame_a.index[base[0]]))
    axs[0].set_title('Production')
    axs[0].set_xlabel('Period')
    axs[0].set_ylabel('Percentage')
    axs[0].legend()
    axs[0].grid(True)
    axs[1].plot(source_frame_b.index, source_frame_b.iloc[:, 0], label='Kurenkov Data')
    axs[1].plot(source_frame_b.index, source_frame_b.iloc[:, 1], label='BEA Data')
    axs[1].set_title('Labor')
    axs[1].set_xlabel('Period')
    axs[1].set_ylabel('Thousands of Persons')
    axs[1].legend()
    axs[1].grid(True)
    '''Revised Capital'''
    axs[2].plot(source_frame_c.index, source_frame_c.iloc[:, 0], label='Kurenkov Data, {}=100'.format(source_frame_c.index[base[1]]))
    axs[2].plot(source_frame_c.index, source_frame_c.iloc[:, 1], label='BEA Data, {}=100'.format(source_frame_c.index[base[1]]))
    axs[2].set_title('Capital')
    axs[2].set_xlabel('Period')
    axs[2].set_ylabel('Percentage')
    axs[2].legend()
    axs[2].grid(True)
    axs[3].plot(source_frame_d.index, source_frame_d.iloc[:, 0], label='Kurenkov Data')
    axs[3].plot(source_frame_d.index, source_frame_d.iloc[:, 1], label='FRB Data')
    axs[3].set_title('Capacity Utilization')
    axs[3].set_xlabel('Period')
    axs[3].set_ylabel('Percentage')
    axs[3].legend()
    axs[3].grid(True)
    fig.set_size_inches(10., 20.)


def plot_census_complex(source_frame):
    plot_pearson_r_test(source_frame)
    source_frame.reset_index(level=0, inplace=True)
    plot_kzf(source_frame)
    plot_ses(source_frame, 5, 0.1)


def processing_spline(source_frame, kernelModule, deliveryModule):
    source_frame.columns = ['Period', 'Original']
    N = int(input('Define Number of Interpolation Intervals: ')) # # Number of Periods
    if N >= 2:
        print('Number of Periods Provided: {}'.format(N))
        knt = [] # # Switch Points
        knt.append(0)
        i = 0
        if N == 1:
            knt.append(source_frame.shape[0]-1)
        elif N >= 2:
            while i<N:
                if i == N-1:
                    knt.append(source_frame.shape[0]-1)
                    i += 1
                else:
                    y = int(input('Select Row for Year: '))-1
                    if y>knt[i]:
                        knt.append(y)
                        i += 1
        else:
            print('Error') # # Should Never Happen
        K, result_frame = kernelModule(source_frame, N, knt)
        deliveryModule(N, K)
        error_metrics(result_frame)
        plt.figure()
        plt.scatter(result_frame.iloc[:, 0], result_frame.iloc[:, 1])
        plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 2], color = 'red', label='$s_{%d}(\\tau)$' %(0,))
        gonogo = input('Does the Resulting Value Need an Improvement?, Y: ')
        if gonogo == 'Y':
            Q = []
            assert len(knt) == 1 + N
            for i in range(len(knt)):
                Q.append(float(input('Correction of Knot {:02d}: '.format(1 + i))))
            modified = source_frame.iloc[:, 1].copy() # # Series Modification
            for i in range(len(knt)):
                modified[knt[i]] = Q[i]*modified[knt[i]]

            source_frame = pd.concat([source_frame.iloc[:, 0], modified], axis=1, sort=True)
            source_frame.columns = ['Period', 'Original']
            K, result_frame = kernelModule(source_frame, N, knt)
            deliveryModule(N, K)
            error_metrics(result_frame)
            plt.plot(result_frame.iloc[:, 0], result_frame.iloc[:, 2], color = 'g', label='$s_{%d}(\\tau)$' %(1,))
            plt.grid(True)
            plt.legend()
            plt.show()
        else:
            plt.grid(True)
            plt.legend()
            plt.show()
            pass
    else:
        print('N >= 2 is Required, N = {} Was Provided'.format(N))


print(__doc__)
'''Subproject I. Approximation'''
'''
`plot_approx_linear`: Linear Approximation,
`plot_approx_log_linear`: Log-Linear Approximation,
`approx_power_function_a`: Power Function Approximation,
`approx_power_function_b`: Power Function Approximation,
`approx_power_function_c`: Power Function Approximation
'''
source_frame = data_сombined_archived()
result_frame_a = source_frame[source_frame.columns[[7, 6, 0, 6]]]
result_frame_a = result_frame_a.dropna()
result_frame_a.reset_index(level=0, inplace=True)
result_frame_b = source_frame[source_frame.columns[[7, 6, 20, 4]]]
result_frame_b = result_frame_b.dropna()
result_frame_b.reset_index(level=0, inplace=True)
result_frame_c = source_frame[source_frame.columns[[7, 6, 20, 6]]]
result_frame_c = result_frame_c.dropna()
result_frame_c.reset_index(level=0, inplace=True)
plot_approx_linear(result_frame_a)
plot_approx_log_linear(result_frame_b)
plot_approx_log_linear(result_frame_c)

source_frame = data_fetch_a()
approx_power_function_a(source_frame, 2800, 0.01, 0.5)

source_frame = data_fetch_b()
approx_power_function_b(source_frame, 4, 12, 9000, 3000, 0.87)

source_frame = data_fetch_c()
approx_power_function_c(source_frame, 1.5, 19, 1.7, 1760)

'''Subproject II. Capital'''
'''
Project: Fixed Assets Dynamics Modelling:
Fixed Assets Turnover Linear Approximation
Gross Fixed Investment to Gross Domestic Product Ratio Linear Approximation
Alpha: Investment to Capital Conversion Ratio Dynamics
Original Result on Archived Data: {s1;s2} = {-7.28110931679034e-05;0.302917968959722}
Original Result on Archived Data: {λ1;λ2} = {-0.000413347827690062;1.18883834418742}
'''
result_frame_a, result_frame_b, A = get_dataset_archived()
result_frame_c, result_frame_d, B = get_dataset_updated()
plot_capital_modelling(result_frame_a, a)
plot_capital_modelling(result_frame_c, b)
'''Project: Discrete Fourier Transform based on Simpson's Rule Applied to Fixed Assets of the US'''
plot_fourier_discrete(result_frame_b)
plot_fourier_discrete(result_frame_d)

'''Subproject III. Capital Interactive'''
'''
Alpha: Capital Retirement Ratio
Pi: Investment to Capital Conversion Ratio
**************************************************
Project: Interactive Capital Acquisitions
**************************************************
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
**************************************************
Project: Interactive Capital Retirement
**************************************************
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
result_frame = fetch_local()
'''Nominal Investment'''
result_frame['IRU'] = result_frame.iloc[:, 0]*result_frame.iloc[:, 2].div(result_frame.iloc[:, 1])
'''Nominal Product'''
result_frame['PNU'] = result_frame.iloc[:, 1]
'''Real Product'''
result_frame['PRU'] = result_frame.iloc[:, 2]
'''Maximum Nominal Product'''
result_frame['PNM'] = result_frame.iloc[:, 1].div(result_frame.iloc[:, 3]/100)
'''Maximum Real Product'''
result_frame['PRM'] = result_frame.iloc[:, 2].div(result_frame.iloc[:, 3]/100)
'''Labor'''
result_frame.rename(columns={'Labor':'LUU'}, inplace=True)
'''Fixed Assets, End-Period'''
result_frame['CRU'] = result_frame.iloc[:, 4]*result_frame.iloc[:, 2].div(result_frame.iloc[:, 1])
result_frame_a = result_frame[result_frame.columns[[6, 7, 8, 10, 11, 5]]].dropna()
result_frame_b = result_frame[result_frame.columns[[6, 7, 8, 11, 5]]].dropna()
result_frame_c = result_frame[result_frame.columns[[6, 9, 10, 11, 5]]].dropna()
result_frame_a.reset_index(level=0, inplace=True)
result_frame_b.reset_index(level=0, inplace=True)
result_frame_c.reset_index(level=0, inplace=True)
capital_aquisitions(result_frame_a)
capital_retirement(result_frame_b)
capital_retirement(result_frame_c)

'''Subproject IV. Cobb--Douglas'''
'''On Original Dataset'''
source_frame = get_dataset_cobb_douglas()
result_frame_a = source_frame[source_frame.columns[[0, 1, 2]]]
result_frame_b = source_frame[source_frame.columns[[0, 1, 3]]]
result_frame_c = source_frame[source_frame.columns[[0, 1, 4]]]
'''On Expanded Dataset'''
result_frame_d, result_frame_e = get_dataset_version_a()
result_frame_f, result_frame_g, result_frame_h = get_dataset_version_b()
result_frame_i = dataset_version_c()
plot_cobb_douglas_complex(result_frame_a)
plot_cobb_douglas_complex(result_frame_b)
plot_cobb_douglas_complex(result_frame_c)
'''No Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_d)
'''Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_e)
'''Option: 1929--2013, No Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_f)
'''Option: 1967--2013, No Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_g)
'''Option: 1967--2012, Capacity Utilization Adjustment'''
plot_cobb_douglas_complex(result_frame_h)
plot_cobb_douglas_complex(result_frame_i)

'''Subproject V. Cobb--Douglas CAN'''
'''First Figure: Exact Correspondence with `Note INTH05 2014-07-10.docx`'''
source_frame = dataset_canada()
source_frame = source_frame.div(source_frame.iloc[0, :])
cobb_douglas_canada(source_frame)
cobb_douglas_3d(source_frame)

'''Subproject VI. Elasticity'''
source_frame = data_сombined_archived()
result_frame_a = source_frame[source_frame.columns[[7, 6, 4]]]
result_frame_b = source_frame[source_frame.columns[[4]]]
result_frame_a = result_frame_a.dropna()
result_frame_b = result_frame_b.dropna()
result_frame_a.reset_index(level=0, inplace=True)
result_frame_b.reset_index(level=0, inplace=True)
plot_elasticity(result_frame_a)
plot_growth_elasticity(result_frame_b)

'''Subproject VII. MSpline'''
'''Makeshift Splines'''
result_frame = get_dataset_cobb_douglas()
result_frame['turnover'] = result_frame.iloc[:, 2].div(result_frame.iloc[:, 0]) # # Fixed Assets Turnover
result_frame = result_frame[result_frame.columns[[5]]]
result_frame.reset_index(level=0, inplace=True)
'''Option 1'''
processing_spline(result_frame, m_spline_lls, results_delivery_a)
'''Option 2.1.1'''
processing_spline(result_frame, m_spline_ea, results_delivery_k)
'''Option 2.1.2'''
processing_spline(result_frame, m_spline_eb, results_delivery_k)
'''Option 2.2.1'''
processing_spline(result_frame, m_spline_la, results_delivery_k)
'''Option 2.2.2'''
processing_spline(result_frame, m_spline_lb, results_delivery_k)

'''Subproject VIII. Multiple'''
source_frame = get_dataset_cobb_douglas()
source_frame['lab_cap_int'] = source_frame.iloc[:, 0].div(source_frame.iloc[:, 1])
source_frame['lab_product'] = source_frame.iloc[:, 2].div(source_frame.iloc[:, 1])
result_frame_a = source_frame[source_frame.columns[[0]]]
result_frame_b = source_frame[source_frame.columns[[1]]]
result_frame_c = source_frame[source_frame.columns[[2]]]
result_frame_d = source_frame[source_frame.columns[[5]]]
result_frame_e = source_frame[source_frame.columns[[6]]]
plot_census_complex(result_frame_a)
plot_census_complex(result_frame_b)
plot_census_complex(result_frame_c)
plot_census_complex(result_frame_d)
plot_census_complex(result_frame_e)

series_ids = ('D0004', 'D0130', 'F0003', 'F0004', 'P0110',
              'U0001', 'U0008', 'X0414', 'X0415',)
for series_id in series_ids:
    print('Processing {}'.format(series_id))
    source_frame = fetch_census('dataset_usa_census1975.zip', series_id)
    plot_pearson_r_test(source_frame)

    source_frame = fetch_census('dataset_usa_census1975.zip', series_id, False)
    plot_kzf(source_frame)
    plot_ses(source_frame, 5, 0.1)

'''Subproject IX. USA BEA'''
source_frame_a = data_сombined_archived()
source_frame_b = data_сombined()
'''Project: Initial Version Dated: 05 October 2012'''
result_frame_ab = preprocessing_a(source_frame_a)
result_frame_ac = preprocessing_a(source_frame_b)
data_fetch_plot_a(result_frame_ab)
data_fetch_plot_a(result_frame_ac)
'''Project: Initial Version Dated: 23 November 2012'''
result_frame_bb = preprocessing_b(source_frame_a)
result_frame_bc = preprocessing_b(source_frame_b)
data_fetch_plot_b(result_frame_bb)
data_fetch_plot_b(result_frame_bc)
'''Project: Initial Version Dated: 16 June 2013'''
result_frame_cb = preprocessing_c(source_frame_a)
result_frame_cc = preprocessing_c(source_frame_b)
data_fetch_plot_c(result_frame_cb)
data_fetch_plot_c(result_frame_cc)
'''Project: Initial Version Dated: 15 June 2015'''
result_frame_d = preprocessing_d(source_frame_b)
data_fetch_plot_d(result_frame_d)
'''Project: Initial Version Dated: 17 February 2013'''
result_frame_ea, result_frame_eb = preprocessing_e(source_frame_a)
plot_e(result_frame_ea)
plot_e(result_frame_eb)
'''Project: BEA Data Compared with Kurenkov Yu.V. Data'''
result_frame_fa, result_frame_fb, result_frame_fc, result_frame_fd = preprocessing_f(source_frame_a)
plot_f(result_frame_fa, result_frame_fb, result_frame_fc, result_frame_fd)

'''Subproject X. USA Census'''
result_frame, base = data_fetch_census_a()
plot_census_a(result_frame, base)
capital = data_fetch_census_b_a()
deflator = data_fetch_census_b_b()
plot_census_b(capital, deflator)
result_frame, base = data_fetch_census_c()
plot_census_c(result_frame, base)
'''Census Production Series'''
series_ids = ('P0248', 'P0249', 'P0250', 'P0251', 'P0262', 'P0265', 'P0266',
              'P0267', 'P0268','P0269', 'P0293', 'P0294', 'P0295')
alternative = ('P0231', 'P0232', 'P0233', 'P0234', 'P0235', 'P0236', 'P0237', 'P0238', \
             'P0239', 'P0240', 'P0241', 'P0244', 'P0247', 'P0248', 'P0249', 'P0250', \
             'P0251', 'P0252', 'P0253', 'P0254', 'P0255', 'P0256', 'P0257', 'P0258', \
             'P0259', 'P0260', 'P0261', 'P0262', 'P0263', 'P0264', 'P0265', 'P0266', \
             'P0267', 'P0268', 'P0269', 'P0270', 'P0271', 'P0277', 'P0279', 'P0281', \
             'P0282', 'P0283', 'P0284', 'P0286', 'P0288', 'P0290', 'P0293', 'P0294', \
             'P0295', 'P0296', 'P0297', 'P0298', 'P0299', 'P0300')
data_fetch_plot_census_d(series_ids)
result_frame = data_fetch_census_e()
plot_census_e(result_frame)
result_frame = data_fetch_census_f()
plot_census_f_a(result_frame)
plot_census_f_b(result_frame)
result_frame = data_fetch_census_g()
plot_census_g(result_frame)
data_fetch_plot_census_h()
result_frame_a, result_frame_b, result_frame_c = data_fetch_census_i()
plot_census_i(result_frame_a, result_frame_b, result_frame_c)
result_frame, base = data_fetch_census_j()
plot_census_j(result_frame, base)
data_fetch_plot_census_k()

'''Subproject XI. USA Census J14'''
file_name = 'dataset_usa_census1949.zip'
plot_growth_elasticity(fetch_census(file_name, 'J0014', False))
file_name = 'dataset_usa_census1949.zip'
plot_rmf(fetch_census(file_name, 'J0014', False))
'''Subproject XII. USA Douglas Kendrick'''
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
series_dict = get_series_ids('dataset_usa_kendrick.zip')
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
