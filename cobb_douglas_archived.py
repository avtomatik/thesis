# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 22:19:02 2020
@author: Mastermind
"""


import os
from prepare.lib import get_data_usa_bea_labor_mfg
from prepare.lib import get_data_usa_frb_cu
from prepare.lib import get_data_version_a
from prepare.lib import get_data_version_b
from prepare.lib import get_data_capital_purchases
from plot.lib import plot_capital_purchases
from plot.lib import plot_cobb_douglas_alt
from prepare.lib import transform_cobb_douglas
from toolkit.lib import calculate_curve_fit_params
from prepare.lib import get_data_cobb_douglas


FOLDER = '/media/alexander/321B-6A94'
os.chdir(FOLDER)


print(__doc__)
# =============================================================================
# Project I. Classified
# =============================================================================
df = get_data_cobb_douglas()
# result_frame_b = df.iloc[:, [0, 1, 2, 4]]
plot_cobb_douglas_alt(df)
plot_cobb_douglas_alt(result_frame_b)

result_frame_a = df.iloc[:, [0, 1, 2]]
result_frame_b = df.iloc[:, [0, 1, 3]]
result_frame_c = df.iloc[:, [0, 1, 4]]
result_frame_d, result_frame_e = get_data_version_a()
result_frame_f, result_frame_g, result_frame_h = get_data_version_b()
result_frame_i = dataset_version_c()
calculate_curve_fit_params(result_frame_a)
calculate_curve_fit_params(result_frame_b)
calculate_curve_fit_params(result_frame_c)
calculate_curve_fit_params(result_frame_d)
calculate_curve_fit_params(result_frame_e)
calculate_curve_fit_params(result_frame_f)
calculate_curve_fit_params(result_frame_g)
calculate_curve_fit_params(result_frame_h)
calculate_curve_fit_params(result_frame_i)
calculate_curve_fit_params(result_frame_a)
calculate_curve_fit_params(result_frame_b)
calculate_curve_fit_params(result_frame_c)
# =============================================================================
# No Capacity Utilization Adjustment
# =============================================================================
calculate_curve_fit_params(result_frame_d)
# =============================================================================
# Capacity Utilization Adjustment
# =============================================================================
calculate_curve_fit_params(result_frame_e)
# =============================================================================
# Option: 1929--2013, No Capacity Utilization Adjustment
# =============================================================================
calculate_curve_fit_params(result_frame_f)
# =============================================================================
# Option: 1967--2013, No Capacity Utilization Adjustment
# =============================================================================
calculate_curve_fit_params(result_frame_g)
# =============================================================================
# Option: 1967--2012, Capacity Utilization Adjustment
# =============================================================================
calculate_curve_fit_params(result_frame_h)
calculate_curve_fit_params(result_frame_i)
# =============================================================================
# Project II. Scipy Signal Median Filter, Non-Linear Low-Pass Filter
# =============================================================================
procedure(result_frame_a)
procedure(result_frame_b)
procedure(result_frame_c)
procedure(result_frame_d)
procedure(result_frame_e)
procedure(result_frame_f)
procedure(result_frame_g)
procedure(result_frame_h)
procedure(result_frame_i)
procedure(result_frame_a)
procedure(result_frame_b)
procedure(result_frame_c)
# =============================================================================
# Project III. Scipy Signal Wiener Filter
# =============================================================================
purchases_frame = get_dataset_capital_purchases()
plot_capital_purchases(purchases_frame)
