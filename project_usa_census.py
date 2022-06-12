# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 00:13:17 2020

@author: Mastermind
"""


import os
from prepare.lib import get_data_census_a
from prepare.lib import get_data_census_b_a
from prepare.lib import get_data_census_b_b
from prepare.lib import get_data_census_c
from prepare.lib import get_data_census_e
from prepare.lib import get_data_census_f
from prepare.lib import get_data_census_g
from prepare.lib import get_data_census_i_a
from prepare.lib import get_data_census_i_b
from prepare.lib import get_data_census_i_c
from prepare.lib import get_data_census_j
from plot.lib import plot_census_a
from plot.lib import plot_census_b_capital
from plot.lib import plot_census_b_deflator
from plot.lib import plot_census_c
from plot.lib import plot_census_d
from plot.lib import plot_census_e
from plot.lib import plot_census_f_a
from plot.lib import plot_census_f_b
from plot.lib import plot_census_g
from plot.lib import plot_census_h
from plot.lib import plot_census_i_a
from plot.lib import plot_census_i_b
from plot.lib import plot_census_i_c
from plot.lib import plot_census_j
from plot.lib import plot_census_k


FOLDER = '/media/alexander/321B-6A94'
SERIES_IDS = (
    'P0248', 'P0249', 'P0250', 'P0251', 'P0262', 'P0265', 'P0266', 'P0267',
    'P0268', 'P0269', 'P0293', 'P0294', 'P0295',
)
ALTERNATIVE_IDS = (
    'P0231', 'P0232', 'P0233', 'P0234', 'P0235', 'P0236', 'P0237', 'P0238',
    'P0239', 'P0240', 'P0241', 'P0244', 'P0247', 'P0248', 'P0249', 'P0250',
    'P0251', 'P0252', 'P0253', 'P0254', 'P0255', 'P0256', 'P0257', 'P0258',
    'P0259', 'P0260', 'P0261', 'P0262', 'P0263', 'P0264', 'P0265', 'P0266',
    'P0267', 'P0268', 'P0269', 'P0270', 'P0271', 'P0277', 'P0279', 'P0281',
    'P0282', 'P0283', 'P0284', 'P0286', 'P0288', 'P0290', 'P0293', 'P0294',
    'P0295', 'P0296', 'P0297', 'P0298', 'P0299', 'P0300',
)


os.chdir(FOLDER)
plot_census_a(*get_data_census_a())
plot_census_b_capital(get_data_census_b_a())
plot_census_b_deflator(get_data_census_b_b())
plot_census_c(*get_data_census_c())
# =============================================================================
# Census Production Series
# =============================================================================
plot_census_d(SERIES_IDS)
plot_census_e(get_data_census_e())
result_frame = get_data_census_f()
plot_census_f_a(result_frame)
plot_census_f_b(result_frame)
plot_census_g(get_data_census_g())
plot_census_h()
plot_census_i_a(get_data_census_i_a())
plot_census_i_b(get_data_census_i_b())
plot_census_i_c(get_data_census_i_c())
plot_census_j(get_data_census_j())
plot_census_k()
