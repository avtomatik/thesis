# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 00:37:30 2020

@author: Mastermind
"""

import os
import pandas as pd
os.chdir('D:')
for file in os.listdir():
    if file.startswith('dataset CHE'):
        if file.endswith('.xls'):
            xl = pd.ExcelFile(file)
            for sheet in xl.sheet_names:
#                source_frame = pd.read_excel(xl,  sheet)
                pass