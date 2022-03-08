# -*- coding: utf-8 -*-
"""
Created on Sat May  2 22:26:24 2020

@author: Mastermind
"""

import os
import pandas as pd
os.chdir('D:')
"""https://unstats.un.org/unsd/snaama/Index"""
source_frame = pd.read_excel('dataset World United Nations Download-GDPcurrent-USD-countries.xls',  skiprows=2)
source_frame = source_frame[source_frame.iloc[:, 1] =='Gross Domestic Product (GDP)']
source_frame.drop(['IndicatorName'],  axis = 1,  inplace=True)
source_frame = source_frame.set_index('Country').transpose()
result_frame = source_frame.iloc[:, 206].div(source_frame.mean(1))
result_frame.plot(grid = True)