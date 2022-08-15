# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 00:13:17 2020

@author: Mastermind
"""


import os
import itertools
from collect.lib import collect_uscb_production
from collect.lib import collect_uscb_cap
from collect.lib import collect_uscb_cap_deflator
from collect.lib import collect_uscb_metals
from collect.lib import collect_uscb_immigration
from collect.lib import collect_uscb_employment
from collect.lib import collect_uscb_gnp
from collect.lib import collect_uscb_trade
from collect.lib import collect_uscb_trade_gold_silver
from collect.lib import collect_uscb_trade_by_countries
from collect.lib import collect_uscb_money_stock
from plot.lib import plot_uscb_production
from plot.lib import plot_uscb_cap
from plot.lib import plot_uscb_cap_deflator
from plot.lib import plot_uscb_metals
from plot.lib import plot_uscb_commodities
from plot.lib import plot_uscb_immigration
from plot.lib import plot_uscb_unemployment_hours_worked
from plot.lib import plot_uscb_employment_conflicts
from plot.lib import plot_uscb_gnp
from plot.lib import plot_uscb_farm_lands
from plot.lib import plot_uscb_trade
from plot.lib import plot_uscb_trade_gold_silver
from plot.lib import plot_uscb_trade_by_countries
from plot.lib import plot_uscb_money_stock
from plot.lib import plot_uscb_finance


def main():
    DIR = '/media/alexander/321B-6A94'

    os.chdir(DIR)
    plot_uscb_production(*collect_uscb_production())
    plot_uscb_cap(collect_uscb_cap())
    plot_uscb_cap_deflator(collect_uscb_cap_deflator())
    plot_uscb_metals(*collect_uscb_metals())
    # =========================================================================
    # Census Production Series
    # =========================================================================
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

    plot_uscb_commodities(SERIES_IDS)
    plot_uscb_immigration(collect_uscb_immigration())
    df = collect_uscb_employment()
    plot_uscb_unemployment_hours_worked(df)
    plot_uscb_employment_conflicts(df)
    plot_uscb_gnp(collect_uscb_gnp())
    plot_uscb_farm_lands()
    plot_uscb_trade(collect_uscb_trade())
    plot_uscb_trade_gold_silver(collect_uscb_trade_gold_silver())
    plot_uscb_trade_by_countries(collect_uscb_trade_by_countries())
    plot_uscb_money_stock(collect_uscb_money_stock())
    plot_uscb_finance()


if __name__ == '__main__':
    main()
