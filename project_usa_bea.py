# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:17:48 2020

@author: Mastermind
"""


import os
from collect.lib import collect_usa_general
from collect.lib import transform_a
from collect.lib import transform_b
from collect.lib import transform_production_money
from collect.lib import transform_d
from collect.lib import transform_e
from collect.lib import transform_kurenkov
from plot.lib import plot_investment_production
from plot.lib import plot_investment
from plot.lib import plot_c
from plot.lib import plot_d
from plot.lib import plot_e
from plot.lib import plot_kurenkov


def main():
    DIR = '/media/alexander/321B-6A94'

    os.chdir(DIR)
    _df_a = collect_usa_general()
    # =========================================================================
    # Project: Initial Version Dated: 05 October 2012
    # =========================================================================
    df_a_a = transform_a(_df_a)
    plot_investment_production(df_a_a)
    # =========================================================================
    # Project: Initial Version Dated: 23 November 2012
    # =========================================================================
    df_b_a = transform_b(_df_a)
    plot_investment(df_b_a)
    # =========================================================================
    # Project: Initial Version Dated: 16 June 2013
    # =========================================================================
    df_c_a = transform_production_money(_df_a)
    plot_c(df_c_a)
    # =========================================================================
    # Project: Initial Version Dated: 15 June 2015
    # =========================================================================
    plot_d(transform_d(_df_a))
    # =========================================================================
    # Project: Initial Version Dated: 17 February 2013
    # =========================================================================
    df_e_a, df_e_b = transform_e(_df_a)
    plot_e(df_e_a)
    plot_e(df_e_b)
    # =========================================================================
    # Project: BEA Data Compared with Kurenkov Yu.V. Data
    # =========================================================================
    plot_kurenkov(transform_kurenkov(_df_a))


if __name__ == '__main__':
    main()
