# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:10:29 2021

@author: Mastermind
"""


import os
import pandas as pd
from pandas import DataFrame
from prepare.lib import get_data_cobb_douglas_price
from prepare.lib import get_data_census_price
from prepare.lib import get_data_can_price_a
from prepare.lib import get_data_can_price_b


def append_series_ids(df: DataFrame, chunk: DataFrame, series_ids: tuple[str]) -> DataFrame:
    for series_id in series_ids:
        chunk = pd.concat(
            [
                chunk,
                df.loc[:, [series_id]].dropna(axis=0)
            ],
            axis=1)
    return chunk


DIR = '/home/alexander/science'
# # data = pd.DataFrame()
# # CALLS = {
# #     # 'cobb_douglas':price_cobb_douglas(),
# #     # 'census':price_census(),
# #     'canada_a': price_canada_a(),
# #     'canada_b': price_canada_b(),
# # }
# # for key, chunk in CALLS.items():
# #     data = pd.concat([data, chunk], axis=1)
# # data['mean'] = data.mean(1)
# # data['cum_mean'] = np.cumprod(1 + data.iloc[:, -1])
# # data = data.div(data.loc[2012])


# # =============================================================================
# # Product
# # =============================================================================
# # =============================================================================
# # v21573668 # Not Useful: Real Gross Domestic Product
# # v142817 # Not Useful: Capacity Utilization
# # v37482 # Not Useful: Capacity Utilization
# # v4331088 # Not Useful: Capacity Utilization
# # v41713056 # Not Useful: Capital Input
# # v41713073 # Not Useful: Capital Input
# # v41707775 # Not Useful: Capital Input
# # v42189387 # Not Useful: Capital Input
# # =============================================================================
# result = pd.DataFrame()
# combined = pd.DataFrame()
FILE_NAME = 'stat_can_prd.xlsx'
# data = pd.read_excel(os.path.join(DIR, FILE_NAME), index_col=0)
# # =============================================================================
# # Capital cost
# # =============================================================================
# SERIES_IDS = (
#     'v41713243',
#     'v41708375',
#     'v42189907',
# )
# combined = append_series_ids(data, combined, SERIES_IDS)
# combined = combined.div(combined.loc[1997]).mul(100)
# combined['mean_comb'] = combined.mean(1)
# combined = combined.iloc[:, [-1]]
# result = pd.concat([result, combined], axis=1)
# # combined.plot(grid=True).get_figure().savefig('view.pdf', format='pdf', dpi=900)
# # combined.to_excel('/media/alexander/321B-6A94/result.xlsx')


FILE_NAME = 'stat_can_cap.xlsx'
# data = pd.read_excel(os.path.join(DIR, FILE_NAME), index_col=0)
# data = data.div(data.loc[1997]).mul(100)
# combined = pd.concat([data, combined], axis=1)
# combined.plot(grid=True).get_figure().savefig('view.pdf', format='pdf', dpi=900)


# # data = combined
FILE_NAME = 'stat_can_cap.xlsx'
# data = pd.read_excel(os.path.join(DIR, FILE_NAME), index_col=0)
#
#
# result = pd.DataFrame(columns=['series_id_1', 'series_id_2', 'r_2'])
# for pair in combinations(data.columns, 2):
#     chunk = data.loc[:, list(pair)].dropna(axis=0)
#     if not chunk.empty:
#         result = result.append({'series_id_1': pair[0],
#                                 'series_id_2': pair[1],
#                                 'r_2': r2_score(chunk.iloc[:, 0], chunk.iloc[:, 1])},
#                                 ignore_index=True)
# result.to_excel('result.xlsx', index=False)


# # combined = pd.DataFrame()
FILE_NAME = 'stat_can_prd.xlsx'
# # data = pd.read_excel(os.path.join(DIR, FILE_NAME), index_col=0)
# # # =============================================================================
# # # Production Indexes
# # # =============================================================================
# # # =============================================================================
# # # v11567 # Production Indexes
# # # v41707475 # Production Indexes
# # # v41708195 # Gross Output
# # # v42189127 # Production Indexes
# # # v42189751 # Gross Output
# # # v64602050 # Gross Output
# # # v86718697 # Production Indexes
# # # v86719219 # Gross Output
# # # =============================================================================
# # # SERIES_IDS = (
# # #     'v86718697',
# # #     'v41707475',
# # #     'v42189127',
# # #     'v11567',
# # # )
# # # combined = append_series_ids(data, combined, SERIES_IDS)
# # # combined = combined.div(combined.loc[1961]).mul(100)

# # # # =============================================================================
# # # # Gross Output
# # # # =============================================================================
# # # SERIES_IDS = (
# # #     'v86719219',
# # #     'v41708195',
# # #     'v42189751',
# # #     'v64602050',
# # # )
# # # combined = append_series_ids(data, combined, SERIES_IDS)
# # # combined = combined.div(combined.loc[1997]).mul(100)
# # # combined.plot(grid=True).get_figure().savefig(
# # #     'view.pdf', format='pdf', dpi=900)
# # # combined.to_excel('/media/alexander/321B-6A94/result.xlsx')


FILE_NAME = 'stat_can_cap.xlsx'
# data = pd.read_excel(os.path.join(DIR, FILE_NAME), index_col=0)
# combined = pd.DataFrame()
# for _ in range(30, 35):
#     chunk = data.iloc[:, [_]].dropna()
#     combined = pd.concat([combined, chunk],
#                           axis=1,
#                           sort=False)
# combined = combined.div(combined.loc[1997]).mul(100)
# combined['mean'] = combined.sum(1)
# combined = combined.iloc[:, [-1]]
# result = pd.concat([result, combined], axis=1)
# result.plot(grid=True).get_figure().savefig('view.pdf', format='pdf', dpi=900)


FILE_NAME = 'stat_can_cap_matching.xlsx'
# data = pd.read_excel(os.path.join(DIR, FILE_NAME), index_col=0)
# data = data[data.iloc[:, 5] != 'Information and communication technologies machinery and equipment']
# data = data[data.iloc[:, 5] != 'Land']
# data = data[data.iloc[:, 6] != 'Intellectual property products']
# # data.dropna(axis = 0, how='all', inplace=True)
# data.to_excel('DIR/stat_can_cap_matching_alpha.xlsx', index=True)

FILE_NAME = 'stat_can_cap.xlsx'
data = pd.read_excel(os.path.join(DIR, FILE_NAME), index_col=0)
SERIES_IDS = (
    'v46444624',
    'v46444685',
    'v46444746',
    'v46444990',
    'v46445051',
    'v46445112',
    'v46445356',
    'v46445417',
    'v46445478',
    'v46445722',
    'v46445783',
    'v46445844',
)
for series_id in SERIES_IDS[::3]:
    chunk = data.loc[:, [series_id]]
    chunk.dropna(axis=0, how='all', inplace=True)
    chunk.plot(grid=True)
    # chunk.plot(grid=True).get_figure().savefig(
    #     'temporary.pdf', format='pdf', dpi=900)
# for series_id in SERIES_IDS[1::3]:
#     chunk = data.loc[:, [series_id]]
#     chunk.dropna(axis = 0, how='all', inplace=True)
#     chunk.plot(grid=True)
# for series_id in SERIES_IDS[2::3]:
#     chunk = data.loc[:, [series_id]]
#     chunk.dropna(axis = 0, how='all', inplace=True)
#     chunk.plot(grid=True)
