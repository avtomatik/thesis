# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:17:48 2020

@author: Mastermind
"""


import os
from prepare.lib import get_data_combined
from prepare.lib import get_data_combined_archived
from prepare.lib import transform_a
from prepare.lib import transform_b
from prepare.lib import transform_c
from prepare.lib import transform_d
from prepare.lib import transform_e
from plot.lib import plot_a
from plot.lib import plot_b
from plot.lib import plot_c
from plot.lib import plot_d
from plot.lib import plot_e
from plot.lib import plot_kurenkov


FOLDER = '/media/alexander/321B-6A94'
os.chdir(FOLDER)
source_frame_a = get_data_combined_archived()
source_frame_b = get_data_combined()
# =============================================================================
# Project: Initial Version Dated: 05 October 2012
# =============================================================================
result_frame_a_b = transform_a(source_frame_a)
result_frame_a_c = transform_a(source_frame_b)
plot_a(result_frame_a_b)
plot_a(result_frame_a_c)
# =============================================================================
# Project: Initial Version Dated: 23 November 2012
# =============================================================================
result_frame_b_b = transform_b(source_frame_a)
result_frame_b_c = transform_b(source_frame_b)
plot_b(result_frame_b_b)
plot_b(result_frame_b_c)
# =============================================================================
# Project: Initial Version Dated: 16 June 2013
# =============================================================================
result_frame_c_b = transform_c(source_frame_a)
result_frame_c_c = transform_c(source_frame_b)
plot_c(result_frame_c_b)
plot_c(result_frame_c_c)
# =============================================================================
# Project: Initial Version Dated: 15 June 2015
# =============================================================================
result_frame_d = transform_d(source_frame_b)
plot_d(result_frame_d)
# =============================================================================
# Project: Initial Version Dated: 17 February 2013
# =============================================================================
result_frame_e_a, result_frame_e_b = transform_e(source_frame_a)
plot_e(result_frame_e_a)
plot_e(result_frame_e_b)
# =============================================================================
# Project: BEA Data Compared with Kurenkov Yu.V. Data
# =============================================================================
result_frame_f_a, result_frame_f_b, result_frame_f_c, result_frame_f_d = transform_f(
    source_frame_a)
plot_kurenkov(result_frame_f_a, result_frame_f_b, result_frame_f_c, result_frame_f_d)
