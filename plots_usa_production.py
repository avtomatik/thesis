# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:45:44 2019

@author: Mastermind
"""


import os
from extract.lib import extract_usa_census
from plot.lib import plot_rolling_mean_filter
from plot.lib import plot_growth_elasticity


FOLDER = '/media/alexander/321B-6A94'
ARCHIVE_NAME = 'dataset_usa_census1949.zip'
SERIES_ID = 'J0014'


os.chdir(FOLDER)
df = extract_usa_census(ARCHIVE_NAME, SERIES_ID)
plot_growth_elasticity(df)
plot_rolling_mean_filter(df)
