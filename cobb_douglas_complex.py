# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:17:13 2020

@author: Mastermind
"""


import os
from prepare.lib import get_data_cobb_douglas
from plot.lib import plot_turnover
from plot.lib import plot_cobb_douglas_complex
from toolkit.lib import simple_linear_regression
from plot.lib import plot_block_two
from plot.lib import plot_block_one
from plot.lib import plot_block_zer
from toolkit.lib import rolling_mean_filter
from toolkit.lib import kol_zur_filter
from plot.lib import plot_lab_prod_polynomial
from plot.lib import plot_simple_linear
from plot.lib import plot_simple_log


FOLDER = '/media/alexander/321B-6A94'
os.chdir(FOLDER)
# =============================================================================
# On Original Dataset
# =============================================================================
source_frame = get_data_cobb_douglas()
result_frame_a = source_frame.iloc[:, [0, 1, 2]]
result_frame_b = source_frame.iloc[:, [0, 1, 3]]
result_frame_c = source_frame.iloc[:, [0, 1, 4]]
# =============================================================================
# On Expanded Dataset
# =============================================================================
result_frame_d, result_frame_e = get_dataset_version_a()
result_frame_f, result_frame_g, result_frame_h = get_dataset_version_b()
result_frame_i = dataset_version_c()
plot_cobb_douglas_complex(result_frame_a)
plot_cobb_douglas_complex(result_frame_b)
plot_cobb_douglas_complex(result_frame_c)
# =============================================================================
# No Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_d)
# =============================================================================
# Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_e)
# =============================================================================
# Option: 1929--2013, No Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_f)
# =============================================================================
# Option: 1967--2013, No Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_g)
# =============================================================================
# Option: 1967--2012, Capacity Utilization Adjustment
# =============================================================================
plot_cobb_douglas_complex(result_frame_h)
plot_cobb_douglas_complex(result_frame_i)
