#-*- coding: utf-8 -*-
"""
Created on Tue Nov  2 21:10:29 2021

@author: Mastermind
"""


# =============================================================================
# Labor
# =============================================================================
# =============================================================================
# v41707595 # Not Useful: Labour input
# v41712954 # Not Useful: Labour input
# v42189231 # Not Useful: Labour input
# v65522120 # Not Useful
# v65522415 # Not Useful
# =============================================================================

def append_series_ids_sum(source_frame, data_frame, series_ids):
    chunk = pd.DataFrame()
    for series_id in series_ids:
        _ = source_frame.loc[:, [series_id]]
        _.dropna(inplace=True)
        chunk = pd.concat([chunk, _], axis=1, sort=False)
    series_ids.extend(['sum'])
    chunk['_'.join(series_ids)] = chunk.sum(1)
    data_frame = pd.concat([data_frame, chunk.iloc[:, [-1]]], axis=1, sort=False)
    return data_frame


def find_mean_for_min_std():
    # =============================================================================
    # Determine Year & Mean Value for Base Vectors for Year with Minimum StandardError
    # =============================================================================
    # =============================================================================
    # Base Vector v123355112
    # Base Vector v1235071986
    # Base Vector v2057609
    # Base Vector v2057818
    # Base Vector v2523013
    # =============================================================================
    result = pd.DataFrame()
    file_name = '/home/alexander/projects/stat_can_lab.xlsx'
    _ = pd.read_excel(file_name)
    _.set_index(_.columns[0], inplace=True)
    series_ids = [
                'v123355112',
                'v1235071986',
                'v2057609',
                'v2057818',
                'v2523013',
                ]
    for series_id in series_ids:
        chunk = _.loc[:, [series_id]]
        chunk.dropna(inplace=True)
        result = pd.concat([result, chunk], axis=1, sort=False)
    result.dropna(inplace=True)
    result['std'] = result.std(axis=1)
    return (result.iloc[:, [-1]].idxmin()[0],
            result.loc[result.iloc[:, [-1]].idxmin()[0], :][:-1].mean())


result = pd.DataFrame()


combined = pd.DataFrame()
file_name = '/home/alexander/projects/stat_can_prd.xlsx'
data = pd.read_excel(file_name)
data.set_index(data.columns[0], inplace=True)
series_ids = [
            'v716397', # Total number of jobs
            'v718173',
            'v719421', # Total number of jobs
            ]
combined = append_series_ids(data, combined, series_ids = series_ids)
series_ids = [
            'v535579',
            'v535593',
            'v535663',
            'v535677',
            ]
combined = append_series_ids_sum(data, combined, series_ids = series_ids)
file_name = '/home/alexander/projects/stat_can_lab.xlsx'
data = pd.read_excel(file_name)
data.set_index(data.columns[0], inplace=True)
series_ids = [
            'v74989',
            'v2057609',
            'v123355112',
            'v2057818',
            ]
combined = append_series_ids(data, combined, series_ids = series_ids)
combined = combined.div(combined.loc[1982]).mul(100)
combined['mean'] = combined.mean(1)
result = pd.concat([result, combined.iloc[:, [-1]]], axis=1, sort=False)


combined = pd.DataFrame()
file_name = '/home/alexander/projects/stat_can_prd.xlsx'
data = pd.read_excel(file_name)
data.set_index(data.columns[0], inplace=True)
series_ids = [
            'v21573686', # Total number of jobs
            'v111382232', # Total number of jobs
            ]
combined = append_series_ids(data, combined, series_ids = series_ids)
series_ids = [
            'v761808',
            'v761927',
            ]
combined = append_series_ids_sum(data, combined, series_ids = series_ids)
file_name = '/home/alexander/projects/stat_can_lab.xlsx'
data = pd.read_excel(file_name)
data.set_index(data.columns[0], inplace=True)
series_ids = [
            'v249139',
            'v2523013',
            'v1596771',
            'v78931172',
            'v65521825',
            ]
combined = append_series_ids(data, combined, series_ids = series_ids)
series_ids = [
            'v249703',
            'v250265',
            ]
combined = append_series_ids_sum(data, combined, series_ids = series_ids)
series_ids = [
            'v78931174',
            'v78931173',
            ]
combined = append_series_ids_sum(data, combined, series_ids = series_ids)
combined = combined.div(combined.loc[2000]).mul(100)
combined['mean'] = combined.mean(1)
result = pd.concat([result, combined.iloc[:, [-1]]], axis=1, sort=False)


combined = pd.DataFrame()
file_name = '/home/alexander/projects/stat_can_lab.xlsx'
data = pd.read_excel(file_name)
data.set_index(data.columns[0], inplace=True)
series_ids = [
            'v1235071986',
            ]
combined = append_series_ids(data, combined, series_ids = series_ids)
series_ids = [
            'v54027148',
            'v54027152',
            ]
combined = append_series_ids_sum(data, combined, series_ids = series_ids)
combined = combined.div(combined.loc[2006]).mul(100)
combined['mean'] = combined.mean(1)
result = pd.concat([result, combined.iloc[:, [-1]]], axis=1, sort=False)


result = result.div(result.iloc[result.index.get_loc(2001), :]).mul(100)
result['mean_comb'] = result.mean(1)
result = result.iloc[:, [-1]]
year, value = find_mean_for_min_std()
result['workers'] = result.div(result.loc[year, :]).mul(value)
result = result.iloc[:, [-1]].round(1)
result.plot(grid=True).get_figure().savefig('view_canada.pdf', format = 'pdf', dpi = 900)
# result.to_excel('/media/alexander/321B-6A94/result.xlsx')
# print(result)

file_name = '/home/alexander/projects/series_ids.xlsx'
data = pd.read_excel(file_name)
data.dropna(axis = 0, how='all', inplace=True)
data.dropna(axis=1, how='all', inplace=True)
# data.to_excel('/home/alexander/projects/series_ids.xlsx', index=False)

data.fillna('None', inplace=True)
version = sorted(data.iloc[:, 0].unique())[0]
chunk = data[data.iloc[:, 0] ==version].iloc[:, 1:]
chunk = chunk[chunk.iloc[:, 0] =="# Labor"].iloc[:, 1:]
initial = set(chunk.iloc[:, 0])
version = sorted(data.iloc[:, 0].unique())[2]
chunk = data[data.iloc[:, 0] ==version].iloc[:, 1:]
chunk = chunk[chunk.iloc[:, 0] =="# Labor"].iloc[:, 1:]
refactd = set(chunk.iloc[:, 0])
# for item in sorted(initial and refactd):
#     print(item)


file_name = '/home/alexander/projects/stat_can_cap.xlsx'
data = pd.read_excel(file_name)
a = set(data.T.index)
a.remove('REF_DATE')
file_name = '/home/alexander/projects/stat_can_lab.xlsx'
data = pd.read_excel(file_name)
b = set(data.T.index)
b.remove('REF_DATE')
file_name = '/home/alexander/projects/stat_can_prd.xlsx'
data = pd.read_excel(file_name)
c = set(data.T.index)
c.remove('REF_DATE')


a -= refactd
b -= refactd
c -= refactd
print(a)
print(b)
print(c)

