# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 22:20:54 2021

@author: Mastermind
"""


# =============================================================================
# Capital
# # 16100077-eng.xlsx: NO;
# # 16100088-eng.xlsx: NO;
# # 16100118-eng.xlsx: NO;
# # 34100278-eng.xlsx: NO;
# # 34100279-eng.xlsx: NO;
# # 36100096-eng.xlsx: YES;
# # 36100097-eng.xlsx: NO;
# # 36100109-eng.xlsx: NO;
# # 36100174-eng.xlsx: NO;
# # 36100210-eng.xlsx: NO;
# # 36100236-eng.xlsx: YES ALTERNATIVE;
# # 36100237-eng.xlsx: YES ALTERNATIVE;
# # 36100238-eng.xlsx: NO;
# =============================================================================
# =============================================================================
# Labor
# # 14100027-eng.xlsx: YES;
# # 14100036-eng.xlsx: NO;
# # 14100221-eng.xlsx: NO;
# # 14100235-eng.xlsx: YES;
# # 14100238-eng.xlsx: NO;
# # 14100242-eng.xlsx: NO;
# # 14100243-eng.xlsx: NO;
# # 14100259-eng.xlsx: MAYBE;
# # 14100265-eng.xlsx: YES;
# # 14100355-eng.xlsx: MAYBE;
# # 14100392-eng.xlsx: NO;
# # 36100489-eng.xlsx: NO;
# =============================================================================
# =============================================================================
# Production
# # 10100094-eng.xlsx: Capacity utilization rates (Bank of Canada calculated series), seasonally adjusted
# # 16100013-eng.xlsx: NO;
# # 16100038-eng.xlsx: NO;
# # 16100047-eng.xlsx: NO;
# # 16100052-eng.xlsx: NO;
# # 16100053-eng.xlsx: NO;
# # 16100054-eng.xlsx: NO;
# # 16100056-eng.xlsx: NO;
# # 16100079-eng.xlsx: NO;
# # 16100109-eng.xlsx: Industrial capacity utilization rates, by industry
# # 16100111-eng.xlsx: Industrial capacity utilization rates, by Standard Industrial Classification, 1980 (SIC)
# # 16100117-eng.xlsx: NO;
# # 16100119-eng.xlsx: NO;
# # 36100207-eng.xlsx: NO;
# # 36100208-eng.xlsx: Capital stock: v41713073;
# # 36100217-eng.xlsx: NO;
# # 36100303-eng.xlsx: NO;
# # 36100305-eng.xlsx: NO;
# # 36100309-eng.xlsx: NO;
# # 36100310-eng.xlsx: NO;
# # 36100383-eng.xlsx: NO;
# # 36100384-eng.xlsx: NO;
# # 36100385-eng.xlsx: YES;
# # 36100386-eng.xlsx: YES;
# # 36100480-eng.xlsx: Total number of jobs: v111382232;
# # 36100488-eng.xlsx: Output, by sector and industry, provincial and territorial: v64602050;
# =============================================================================


from toolkit.lib import procedure
from toolkit.lib import mean_by_year
from load.lib import load_files_to_zip


def data_filter(data, query):
    for column, value in query['filter'].items():
        data = data[data.iloc[:, column] == value]
    return data


def string_to_url(string):
    return f'https://www150.statcan.gc.ca/n1/tbl/csv/{string}'


def string_to_numeric(string):
    y, m = string.split('-')
    return int(y) + (int(m) - 0.5) / 12


CAPITAL = (
    {'file_name': '36100096-eng.zip',
     'series_ids':
     ['v90968617', 'v90968618', 'v90968619', 'v90968620', 'v90968621',
      'v90971177', 'v90971178', 'v90971179', 'v90971180', 'v90971181',
      'v90973737', 'v90973738', 'v90973739', 'v90973740', 'v90973741', ], },
    {'file_name': '36100210-eng.zip',
     'series_ids':
     ['v46444563', 'v46444624', 'v46444685', 'v46444746', 'v46444807',
      'v46444929', 'v46444990', 'v46445051', 'v46445112', 'v46445173',
      'v46445295', 'v46445356', 'v46445417', 'v46445478', 'v46445539',
      'v46445661', 'v46445722', 'v46445783', 'v46445844', 'v46445905', ], },
    {'file_name': '36100236-eng.zip',
     'series_ids':
     ['v1071434', 'v1071435', 'v1071436', 'v1071437', 'v64498363',
      'v1119722', 'v1119723', 'v1119724', 'v1119725', 'v64498371',
      'v4421025', 'v4421026', 'v4421027', 'v4421028', 'v64498379', ], },
)
LABOUR = (
    {'file_name': '14100027-eng.zip',
     'series_ids':
     ['v2523013', ], },
    {'file_name': '14100221-eng.zip',
     'series_ids':
     ['v54027148', 'v54027152', ], },
    {'file_name': '14100235-eng.zip',
     'series_ids':
     ['v74989', ], },
    {'file_name': '14100238-eng.zip',
     'series_ids':
     ['v1596771', ], },
    {'file_name': '14100243-eng.zip',
     'series_ids':
     ['v78931172', 'v78931174', 'v78931173', ], },
    {'file_name': '14100265-eng.zip',
     'series_ids':
     ['v249139', 'v249703', 'v250265', ], },
    {'file_name': '14100355-eng.zip',
     'series_ids':
     ['v2057609', 'v123355112', 'v2057818', ], },
    {'file_name': '14100392-eng.zip',
     'series_ids':
     ['v1235071986', ], },
    {'file_name': '36100489-eng.zip',
     'series_ids':
     ['v65521825',
      # 'v65522120', # Not Useful
      # 'v65522415', # Not Useful
      ], },
)
PRODUCT = ({'file_name': '10100094-eng.zip',
            'series_ids': ['v37482', ], },
           {'file_name': '16100053-eng.zip',
            'series_ids': ['v535579', 'v535593', 'v535663', 'v535677', ], },
           {'file_name': '16100054-eng.zip',
            'series_ids': ['v761808', 'v761927', ], },
           {'file_name': '16100109-eng.zip',
            'series_ids': ['v4331088', ], },
           {'file_name': '16100111-eng.zip',
            'series_ids': ['v142817', ], },
           {'file_name': '36100207-eng.zip',
            'series_ids': ['v21573668', 'v21573686', ], },
           {'file_name': '36100208-eng.zip',
            'series_ids': [
                # 'v41712954', # Not Useful: Labour input
                'v41713056', 'v41713073', 'v41713243', ], },
           {'file_name': '36100217-eng.zip',
            'series_ids': ['v86718697', 'v86719219', ], },
           {'file_name': '36100303-eng.zip',
            'series_ids': ['v716397', 'v718173', ], },
           {'file_name': '36100305-eng.zip',
            'series_ids': ['v719421', ], },
           {'file_name': '36100309-eng.zip',
            'series_ids': ['v41707475',
                           # 'v41707595', # Not Useful: Labour input
                           'v41707775', 'v41708195', 'v41708375', ], },
           {'file_name': '36100310-eng.zip',
            'series_ids': ['v42189127',
                           # 'v42189231', # Not Useful: Labour input
                           'v42189387', 'v42189751', 'v42189907', ], },
           {'file_name': '36100386-eng.zip',
            'series_ids': ['v11567', ], },
           {'file_name': '36100480-eng.zip',
            'series_ids': ['v111382232', ], },
           {'file_name': '36100488-eng.zip',
            'series_ids': ['v64602050', ], },
           )


file_names = [
    '/home/alexander/projects/stat_can_cap.xlsx',
    '/home/alexander/projects/stat_can_lab.xlsx',
    '/home/alexander/projects/stat_can_prd.xlsx',
]
procedure('/home/alexander/projects/stat_can_cap.xlsx', CAPITAL)
procedure('/home/alexander/projects/stat_can_lab.xlsx', LABOUR)
procedure('/home/alexander/projects/stat_can_prd.xlsx', PRODUCT)
combined = pd.DataFrame()
for file_name in file_names:
    data = pd.read_excel(file_name)
    data.rename(columns={'Unnamed: 0': 'REF_DATE'}, inplace=True)
    data.set_index(data.columns[0], inplace=True)
    combined = pd.concat([combined, data],
                         axis=1,
                         sort=False)
combined.sort_index(inplace=True)
file_name = '/home/alexander/projects/stat_can_desc.xlsx'
titles = pd.read_excel(file_name)
combined = pd.merge(titles.set_index(titles.columns[0]),
                    combined.T,
                    left_index=True,
                    right_index=True,
                    sort=False)
combined.T.to_excel('/home/alexander/projects/stat_can_combined.xlsx')
