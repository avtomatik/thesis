#-*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:10:29 2021

@author: Mastermind
"""


def prices_cobb_douglas():
file_name = 'dataset_usa_cobb-douglas.zip'
    data = pd.read_csv(file_name)
    vectors = ('CDT2S1', 'CDT2S3')
    combined = pd.DataFrame()
    for vector in vectors:
        chunk = data[data.iloc[:, 5] == vector].iloc[:, [6, 7]]
        chunk.set_index(chunk.columns[0], inplace=True)
        chunk.rename_axis('REF_DATE', inplace=True)
        chunk.columns = [vector]
        combined = pd.concat([combined, chunk],
                              axis=1,
                              sort=False)
    combined['def'] = combined.iloc[:, 0].div(combined.iloc[:, 1])
    combined['prc'] = combined.iloc[:, 2].div(combined.iloc[:, 2].shift(1))-1
    combined.dropna(inplace=True)
    return combined.iloc[:, [3]]


def prices_census():
file_name = 'dataset_usa_census1975.zip'
    data = pd.read_csv(file_name)
    vectors = ('P0107', 'P0110')
    combined = pd.DataFrame()
    for vector in vectors:
        chunk = data[data.iloc[:, 8] == vector].iloc[:, [9, 10]]
        chunk = chunk.apply(pd.to_numeric)
        chunk.set_index(chunk.columns[0], inplace=True)
        chunk.sort_index(inplace=True)
        chunk.rename_axis('REF_DATE', inplace=True)
        chunk.columns = [vector]
        combined = pd.concat([combined, chunk],
                              axis=1,
                              sort=False)
    combined['def'] = combined.iloc[:, 0].div(combined.iloc[:, 1])
    combined['prc'] = combined.iloc[:, 2].div(combined.iloc[:, 2].shift(1))-1
    combined.dropna(inplace=True)
    return combined.iloc[:, [3]]


def prices_canada_a():
    file_name = '/home/alexander/projects/stat_can_cap.xlsx'
    data = pd.read_excel(file_name)
    data.set_index(data.columns[0], inplace=True)
    groups = [[[i, 5 + i] for i in range(5)],
              # [[i, 10 + i] for i in range(5)],
              [[i, 5 + i] for i in range(35, 39)],
              # [[i, 10 + i] for i in range(35, 40)],
              ]
    combined = pd.DataFrame()
    for pairs in groups:
        for pair in pairs:
            chunk = data.iloc[:, pair].dropna()
            chunk['def'] = chunk.iloc[:, 0].div(chunk.iloc[:, 1])
            chunk['prc'] = chunk.iloc[:, 2].div(chunk.iloc[:, 2].shift(1))-1
            chunk.dropna(inplace=True)
            combined = pd.concat([combined, chunk.iloc[:, [3]]],
                                  axis=1,
                                  sort=False)
            combined.plot(grid=True)
    # return combined


# def prices_canada_b():
file_name = '/home/alexander/projects/stat_can_cap.xlsx'
#     data = pd.read_excel(file_name)
#     data.set_index(data.columns[0], inplace=True)
#     combined = pd.DataFrame()
#     for i in [i for i in range(21, 24)]:
#         chunk = data.iloc[:, [i]].dropna()
#         chunk[f'{data.columns[i]}_prc'] = chunk.iloc[:, 0].div(chunk.iloc[:, 0].shift(1))-1
#         chunk.dropna(inplace=True)
#         combined = pd.concat([combined, chunk.iloc[:, [1]]],
#                           axis=1,
#                           sort=False)
#     return combined


def append_vectors(source_frame, data_frame, vectors):
    for vector in vectors:
        chunk = source_frame.loc[:, [vector]]
        chunk.dropna(inplace=True)
        data_frame = pd.concat([data_frame, chunk], axis=1, sort=False)
    return data_frame


# # data = pd.DataFrame()
# # CALLS = {
# #         # 'cobb_douglas':prices_cobb_douglas(),
# #         # 'census':prices_census(),
# #         'canada_a':prices_canada_a(),
# #         'canada_b':prices_canada_b(),
# #           }
# # for key, chunk in CALLS.items():
# #     data = pd.concat([data, chunk], axis=1, sort=False)
# # data['mean']     = data.mean(1)
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
file_name = '/home/alexander/projects/stat_can_prd.xlsx'
# data = pd.read_excel(file_name)
# data.set_index(data.columns[0], inplace=True)
# # =============================================================================
# # Capital cost
# # =============================================================================
# vectors = [
#             'v41713243',
#             'v41708375',
#             'v42189907',
#             ]
# combined = append_vectors(data, combined, vectors = vectors)
# combined = combined.div(combined.loc[1997]).mul(100)
# combined['mean_comb'] = combined.mean(1)
# combined = combined.iloc[:, [-1]]
# result = pd.concat([result, combined], axis=1, sort=False)
# # combined.plot(grid=True).get_figure().savefig('view.pdf', format='pdf', dpi=900)
# # combined.to_excel('/media/alexander/321B-6A94/result.xlsx')


file_name = '/home/alexander/projects/stat_can_cap.xlsx'
# data = pd.read_excel(file_name)
# data.set_index(data.columns[0], inplace=True)
# data = data.div(data.loc[1997]).mul(100)
# combined = pd.concat([data, combined], axis=1, sort=False)
# combined.plot(grid=True).get_figure().savefig('view.pdf', format = 'pdf', dpi = 900)


# # data = combined
file_name = '/home/alexander/projects/stat_can_cap.xlsx'
# data = pd.read_excel(file_name)
# data.set_index(data.columns[0], inplace=True)
#
#
# result = pd.DataFrame(columns=['vector1', 'vector2', 'r2'])
# for i, pair in enumerate(combinations(data.columns, 2)):
#     chunk = data.loc[:, list(pair)]
#     chunk.dropna(inplace=True)
#     if not chunk.empty:
#         result = result.append({'vector1': pair[0],
#                                 'vector2': pair[1],
#                                 'r2': r2_score(chunk.iloc[:, 0], chunk.iloc[:, 1])},
#                                 ignore_index=True)
# result.to_excel('result.xlsx', index=False)


# # combined = pd.DataFrame()
file_name = '/home/alexander/projects/stat_can_prd.xlsx'
# # data = pd.read_excel(file_name)
# # data.set_index(data.columns[0], inplace=True)
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
# # # vectors = [
# # #             'v86718697',
# # #             'v41707475',
# # #             'v42189127',
# # #             'v11567',
# # #             ]
# # # combined = append_vectors(data, combined, vectors = vectors)
# # # combined = combined.div(combined.loc[1961]).mul(100)

# # # =============================================================================
# # # Gross Output
# # # =============================================================================
# # vectors = [
# #             'v86719219',
# #             'v41708195',
# #             'v42189751',
# #             'v64602050',
# #             ]
# # combined = append_vectors(data, combined, vectors = vectors)
# # combined = combined.div(combined.loc[1997]).mul(100)
# # combined.plot(grid=True).get_figure().savefig('view.pdf', format = 'pdf', dpi = 900)
# # combined.to_excel('/media/alexander/321B-6A94/result.xlsx')


file_name = '/home/alexander/projects/stat_can_cap.xlsx'
# data = pd.read_excel(file_name)
# data.set_index(data.columns[0], inplace=True)
# combined = pd.DataFrame()
# for i in range(30, 35):
#     chunk = data.iloc[:, [i]].dropna()
#     combined = pd.concat([combined, chunk],
#                           axis=1,
#                           sort=False)
# combined = combined.div(combined.loc[1997]).mul(100)
# combined['mean'] = combined.sum(1)
# combined = combined.iloc[:, [-1]]
# result = pd.concat([result, combined], axis=1, sort=False)
# result.plot(grid=True).get_figure().savefig('view.pdf', format = 'pdf', dpi = 900)


file_name = '/home/alexander/projects/stat_can_cap_matching.xlsx'
# data = pd.read_excel(file_name)
# data = data[data.iloc[:, 5] != 'Information and communication technologies machinery and equipment']
# data = data[data.iloc[:, 5] != 'Land']
# data = data[data.iloc[:, 6] != 'Intellectual property products']
# data.set_index(data.columns[0], inplace=True)
# # data.dropna(axis = 0, how='all', inplace=True)
# data.to_excel('/home/alexander/projects/stat_can_cap_matching_alpha.xlsx', index=True)

file_name = '/home/alexander/projects/stat_can_cap.xlsx'
data = pd.read_excel(file_name)
data.set_index(data.columns[0], inplace=True)
vectors = (
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
for vector in vectors[::3]:
    chunk = data.loc[:, [vector]]
    chunk.dropna(axis = 0, how='all', inplace=True)
    chunk.plot(grid=True).get_figure().savefig('temporary.pdf', format='pdf', dpi=900)
# for vector in vectors[1::3]:
#     chunk = data.loc[:, [vector]]
#     chunk.dropna(axis = 0, how='all', inplace=True)
#     chunk.plot(grid=True)
# for vector in vectors[2::3]:
#     chunk = data.loc[:, [vector]]
#     chunk.dropna(axis = 0, how='all', inplace=True)
#     chunk.plot(grid=True)