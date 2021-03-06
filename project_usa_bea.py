# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:17:48 2020

@author: Mastermind
"""


import os
from collect.lib import collect_combined
from collect.lib import collect_combined_archived
from collect.lib import transform_a
from collect.lib import transform_b
from collect.lib import transform_c
from collect.lib import transform_d
from collect.lib import transform_e
from collect.lib import transform_kurenkov
from plot.lib import plot_a
from plot.lib import plot_b
from plot.lib import plot_c
from plot.lib import plot_d
from plot.lib import plot_e
from plot.lib import plot_kurenkov


DIR = '/media/alexander/321B-6A94'
os.chdir(DIR)
_df_a = collect_combined_archived()
_df_b = collect_combined()
# =============================================================================
# Project: Initial Version Dated: 05 October 2012
# =============================================================================
df_a_a = transform_a(_df_a)
df_a_b = transform_a(_df_b)
plot_a(df_a_a)
plot_a(df_a_b)
# =============================================================================
# Project: Initial Version Dated: 23 November 2012
# =============================================================================
df_b_a = transform_b(_df_a)
df_b_b = transform_b(_df_b)
plot_b(df_b_a)
plot_b(df_b_b)
# =============================================================================
# Project: Initial Version Dated: 16 June 2013
# =============================================================================
df_c_a = transform_c(_df_a)
df_c_b = transform_c(_df_b)
plot_c(df_c_a)
plot_c(df_c_b)
# =============================================================================
# Project: Initial Version Dated: 15 June 2015
# =============================================================================
plot_d(transform_d(_df_b))
# =============================================================================
# Project: Initial Version Dated: 17 February 2013
# =============================================================================
df_e_a, df_e_b = transform_e(_df_a)
plot_e(df_e_a)
plot_e(df_e_b)
# =============================================================================
# Project: BEA Data Compared with Kurenkov Yu.V. Data
# =============================================================================
plot_kurenkov(transform_kurenkov(_df_a))
