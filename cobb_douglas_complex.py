# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:17:13 2020

@author: Mastermind
"""


import os
from collect.lib import collect_cobb_douglas
from plot.lib import plot_cobb_douglas_complex


DIR = '/media/alexander/321B-6A94'
os.chdir(DIR)
# =============================================================================
# On Original Dataset
# =============================================================================
_df = collect_cobb_douglas()
_df_a = _df.iloc[:, [0, 1, 2]]
_df_b = _df.iloc[:, [0, 1, 3]]
_df_c = _df.iloc[:, [0, 1, 4]]
# =============================================================================
# On Expanded Dataset
# =============================================================================
_df_d, _df_e = collect_version_a()
_df_f, _df_g, _df_h = collect_version_b()
_df_i = collect_version_c()
plot_cobb_douglas_complex(_df_a)
plot_cobb_douglas_complex(_df_b)
plot_cobb_douglas_complex(_df_c)
# =============================================================================
# No Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(_df_d)
# =============================================================================
# Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(_df_e)
# =============================================================================
# Option: 1929--2013, No Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(_df_f)
# =============================================================================
# Option: 1967--2013, No Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(_df_g)
# =============================================================================
# Option: 1967--2012, Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(_df_h)
plot_cobb_douglas_complex(_df_i)
