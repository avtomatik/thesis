# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 21:33:18 2020

@author: Mastermind
"""

import os
import pandas as pd
import zipfile


def save_zip(data_frame,  string):
    data_frame.to_csv('{}.csv'.format(string),  index = True,  encoding = 'utf-8-sig')
    with zipfile.ZipFile('{}.zip'.format(string),  'w') as archive:
	    archive.write('{}.csv'.format(string),  compress_type = zipfile.ZIP_DEFLATED)
        os.unlink('{}.csv'.format(string))    


def ad_hoc_preprocessing(data_frame):
    data_frame['desc'] = data_frame.columns[1]
    data_frame = data_frame[data_frame.columns[[0, 2, 1]]]
    data_frame.columns = ['period',  'desc',  'value']
    result_frame = data_frame.set_index('period')
    return result_frame


file_names = ['dataset-usa-0000-Public-Debt.txt', 
                'dataset-usa-0022-M1.txt', 
                'dataset-usa-0025-P-R.txt']
os.chdir('D:')
file_name = file_names.pop(0)
base_set = pd.read_csv(file_name)
base_set = ad_hoc_preprocessing(base_set)
for file_name in file_names:
    current_set = pd.read_csv('{}'.format(file_name))
    current_set = ad_hoc_preprocessing(current_set)
    base_set = base_set.append(current_set,  sort = False)
os.chdir('C:\\Projects')
save_zip(base_set,  'dataset-usa-misc')