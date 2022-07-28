# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 00:13:17 2020

@author: Mastermind
"""


import os
import itertools
from collect.lib import collect_census_a
from collect.lib import collect_census_b_a
from collect.lib import collect_census_b_b
from collect.lib import collect_census_c
from collect.lib import collect_census_e
from collect.lib import collect_census_f
from collect.lib import collect_census_g
from collect.lib import collect_census_i_a
from collect.lib import collect_census_i_b
from collect.lib import collect_census_i_c
from collect.lib import collect_census_j
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


def main():
    DIR = '/media/alexander/321B-6A94'

    os.chdir(DIR)
    plot_census_a(*collect_census_a())
    plot_census_b_capital(collect_census_b_a())
    plot_census_b_deflator(collect_census_b_b())
    plot_census_c(*collect_census_c())
    # =============================================================================
    # Census Production Series
    # =============================================================================
    SERIES_IDS = (
        'P0248', 'P0249', 'P0250', 'P0251', 'P0262',
        'P0265', 'P0266', 'P0267', 'P0268', 'P0269',
        'P0293', 'P0294', 'P0295',
    )
    ids = itertools.chain(
        range(231, 242),
        range(244, 245),
        range(247, 272),
        range(277, 278),
        range(279, 280),
        range(281, 285),
        range(286, 287),
        range(288, 289),
        range(290, 291),
        range(293, 301),
    )
    SERIES_IDS_ALT = tuple(f'P{_id:04n}' for _id in ids)

    plot_census_d(SERIES_IDS)
    plot_census_e(collect_census_e())
    df = collect_census_f()
    plot_census_f_a(df)
    plot_census_f_b(df)
    plot_census_g(collect_census_g())
    plot_census_h()
    plot_census_i_a(collect_census_i_a())
    plot_census_i_b(collect_census_i_b())
    plot_census_i_c(collect_census_i_c())
    plot_census_j(collect_census_j())
    plot_census_k()


if __name__ == '__main__':
    main()
