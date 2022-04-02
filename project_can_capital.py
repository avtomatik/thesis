# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 22:05:32 2021

@author: Mastermind
"""


def fetch_can(data_frame, series_id):
    # =============================================================================
    # Data Frame Fetching from CANSIM Zip Archives
    # =============================================================================
    data_frame = data_frame[data_frame.iloc[:, 10]
                            == series_id].iloc[:, [0, 12]]
    data_frame.iloc[:, 0] = data_frame.iloc[:, 0].astype(int)
    data_frame.iloc[:, 1] = data_frame.iloc[:, 1].astype(float)
    data_frame.columns = [data_frame.columns[0], series_id]
    return data_frame.set_index(data_frame.columns[0])


def fetch_can_capital_query():
    # =============================================================================
    # Fetch <SERIES_IDS> from Statistics Canada. Table: 36-10-0238-01 (formerly
    # CANSIM 031-0004): Flows and stocks of fixed non-residential capital, total
    # all industries, by asset, provinces and territories, annual
    # (dollars x 1,000,000)
    # =============================================================================
    url = 'https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip'
    df = fetch_from_url(url, usecols=[3, 4, 5, 11])
    query = (df.iloc[:, 0].str.contains('2012 constant prices')) & \
            (df.iloc[:, 1].str.contains('manufacturing', flags=re.IGNORECASE)) & \
            (df.iloc[:, 2] == 'Linear end-year net stock')
    df = df[query]
    return df.iloc[:, -1].unique().tolist()


def fetch_can_capital(series_ids):
    # =============================================================================
    # Fetch <pd.DataFrame> from Statistics Canada. Table: 36-10-0238-01 (formerly
    # CANSIM 031-0004): Flows and stocks of fixed non-residential capital, total
    # all industries, by asset, provinces and territories, annual
    # (dollars x 1,000,000)
    # =============================================================================
    url = 'https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip'
    data_frame = fetch_from_url(url, usecols=[0, 11, 13])
    data_frame = data_frame[data_frame.iloc[:, 1].isin(series_ids)]
    result_frame = pd.DataFrame()
    for series_id in series_ids:
        current_frame = data_frame[data_frame.iloc[:, 1]
                                   == series_id].iloc[:, [0, 2]]
        current_frame.columns = [current_frame.columns[0], series_id]
        current_frame.set_index(current_frame.columns[0],
                                inplace=True,
                                verify_integrity=True)
        result_frame = pd.concat(
            [result_frame, current_frame], axis=1, sort=True)
    result_frame['sum'] = result_frame.sum(axis=1)
    return result_frame.iloc[:, [-1]]


def get_dataset_can():
    # =============================================================================
    # '''A. Fixed Assets Block: `Industrial buildings`, `Industrial machinery`\
    # for `Newfoundland and Labrador`, `Prince Edward Island`, `Nova Scotia`, \
    # `New Brunswick`, `Quebec`, `Ontario`, `Manitoba`, `Saskatchewan`, `Alberta`, \
    # `British Columbia`, `Yukon`, `Northwest Territories`, `Nunavut`'''
    # '''2007 constant prices'''
    # '''Geometric (infinite) end-year net stock'''
    # '''Industrial buildings (x 1,000,000): `v43975603`, `v43977683`, `v43978099`, \
    # `v43978515`, `v43978931`, `v43979347`, `v43979763`, `v43980179`, `v43980595`, \
    # `v43976019`, `v43976435`, `v43976851`, `v43977267`'''
    # '''Industrial machinery (x 1,000,000): `v43975594`, `v43977674`, `v43978090`, \
    # `v43978506`, `v43978922`, `v43979338`, `v43979754`, `v43980170`, `v43980586`, \
    # `v43976010`, `v43976426`, `v43976842`, `v43977258`'''
    # '''Table: 36-10-0238-01 (formerly CANSIM 031-0004): Flows and stocks of\
    # fixed non-residential capital, total all industries, by asset, provinces\
    # and territories, annual (dollars x 1,000,000)'''
    # =============================================================================
    capital = fetch_from_url(
        'https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip')
    capital = fetch_can_capital(fetch_can_capital_query())
# =============================================================================
# '''B. Labor Block: `v2523012`, Preferred Over `v3437501` Which Is Quarterly'''
# '''`v2523012` - Table: 14-10-0027-01 (formerly CANSIM 282-0012): Employment\
# by class of worker, annual (x 1,000)'''
# =============================================================================
    labor = fetch_from_url(
        'https://www150.statcan.gc.ca/n1/tbl/csv/14100027-eng.zip')
    labor = fetch_can(labor, 'v2523012')
# =============================================================================
# '''C. Production Block: `v65201809`'''
# '''`v65201809` - Table: 36-10-0434-01 (formerly CANSIM 379-0031): Gross\
# domestic product (GDP) at basic prices, by industry, monthly (x 1,000,000)'''
# =============================================================================
    product = fetch_from_url(
        'https://www150.statcan.gc.ca/n1/tbl/csv/36100434-eng.zip')
    product = fetch_can_quarterly(product, 'v65201809')
    result_frame = pd.concat([capital, labor, product], axis=1, sort=True)
    # result_frame = result_frame.dropna()
    result_frame.columns = ['capital', 'labor', 'product']
    # result_frame = result_frame.div(result_frame.iloc[0, :])
    return result_frame


# result_frame = get_dataset_can()
# capital = fetch_from_url('https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip')
# # for column, _ in enumerate(capital.columns):
# #     values = capital.iloc[:, column].unique()
# #     print(_)
# #     print(values)
# capital = fetch_can_capital(fetch_can_capital_query())
# capital = fetch_from_url('https://www150.statcan.gc.ca/n1/en/tbl/csv/36100096-eng.zip')
