# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:22:23 2021

@author: Mastermind
"""

def convert_url(string):
    return '/'.join(('https://www150.statcan.gc.ca/n1/tbl/csv',  '{}-eng.zip'.format(string.split(' = ')[1][:-2])))


def fetch_from_url(url):
# =============================================================================
#     '''Downloading zip file from url'''
# =============================================================================
    print('{}: Processing'.format(url))
    r = requests.get(url)
    with open(url.split('/')[-1],  'wb') as s:
        s.write(r.content)
    if zipfile.is_zipfile(url.split('/')[-1]):
        with zipfile.ZipFile(url.split('/')[-1],  'r') as z:
            with z.open(url.split('/')[-1].replace('-eng.zip',  '.csv')) as f:
              data_frame = pd.read_csv(f)
        print('{}: Complete'.format(url))
        return data_frame


import os
import pandas as pd
import requests
import zipfile
os.chdir('C:\\Projects')
df = pd.read_excel('stat_can_selected.xlsx')
# urls = set()
# for i in range(df.shape[0]):
#     try:
#         urls.add(convert_url(df.iloc[i, 8]))
#     except:
#         pass


# filedict = {url.split('/')[-1]: url for url in urls}


# downloaded = set()
# for filename in os.listdir():
#     if filename.endswith(('-eng.zip')):
#         downloaded.add(filename)


# difference = set(filedict.keys()) - downloaded


# urls = []
# for filename in difference:
#     urls.append(filedict[filename])


# with open('output_b.txt',  'w') as f:
#     for url in sorted(urls):
#         data = fetch_from_url(url)
#         print(url,  file = f)
#         print('Periods Length {}'.format(len(data['REF_DATE'].unique())),  file = f)
#         print(data['REF_DATE'].unique(),  file = f)
# # # # urls = sorted(list(urls))
# # # # with open('output.txt',  'w') as f:
# # # #     for url in urls:
# # # #         data = fetch_from_url(url)
# # # #         print(url,  file = f)
# # # #         print('Periods Length {}'.format(len(data['REF_DATE'].unique())),  file = f)
# # # #         print(data['REF_DATE'].unique(),  file = f)
# # # # # df.dropna(how = 'all',  inplace=True)
# # # # # df.to_excel('stat_can_selected.xlsx',  index = False)