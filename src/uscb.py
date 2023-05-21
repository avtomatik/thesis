#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:26:36 2023

@author: green-machine

Subproject X. USA Census
"""

import itertools

from thesis.src.lib.combine import (combine_uscb_employment_conflicts,
                                    combine_uscb_trade_by_countries,
                                    combine_uscb_unemployment_hours_worked)
from thesis.src.lib.plot import (plot_uscb_employment_conflicts,
                                 plot_uscb_finance, plot_uscb_gnp,
                                 plot_uscb_immigration, plot_uscb_money_stock,
                                 plot_uscb_trade, plot_uscb_trade_by_countries,
                                 plot_uscb_trade_gold_silver,
                                 plot_uscb_unemployment_hours_worked)
from thesis.src.lib.stockpile import stockpile_usa_hist
from thesis.src.lib.transform import transform_sum
from thesis.src.uscb_capital import uscb_capital
from thesis.src.uscb_commodities import uscb_commodities
from thesis.src.uscb_farm_lands import uscb_farm_lands
from thesis.src.uscb_manufacturing import uscb_manufacturing
from thesis.src.uscb_metals import uscb_metals

uscb_manufacturing()

uscb_capital()

uscb_metals()

uscb_commodities()

ARCHIVE_NAME = 'dataset_uscb.zip'
SERIES_IDS = {
    f'C{_:04n}': ARCHIVE_NAME
    for _ in itertools.chain(
        range(91, 102),
        range(103, 110),
        range(111, 116),
        range(117, 120),
    )
}
stockpile_usa_hist(SERIES_IDS).pipe(
    transform_sum, name="C0089"
).pipe(plot_uscb_immigration)

combine_uscb_unemployment_hours_worked().pipe(
    plot_uscb_unemployment_hours_worked
)

combine_uscb_employment_conflicts().pipe(plot_uscb_employment_conflicts)

SERIES_IDS = {
    # =========================================================================
    # Census Gross National Product Series
    # =========================================================================
    'F0003': 'dataset_uscb.zip', 'F0004': 'dataset_uscb.zip'
}
df = stockpile_usa_hist(SERIES_IDS).truncate(before=1889)
df.div(df.iloc[0, :]).mul(100).pipe(plot_uscb_gnp)

uscb_farm_lands()

SERIES_IDS = {
    # =========================================================================
    # Census Foreign Trade Series
    # =========================================================================
    'U0001': 'dataset_uscb.zip', 'U0008': 'dataset_uscb.zip', 'U0015': 'dataset_uscb.zip'
}
stockpile_usa_hist(SERIES_IDS).pipe(plot_uscb_trade)

SERIES_IDS = {
    # =========================================================================
    # Census Foreign Trade Series
    # =========================================================================
    'U0187': 'dataset_uscb.zip', 'U0188': 'dataset_uscb.zip', 'U0189': 'dataset_uscb.zip'
}
stockpile_usa_hist(SERIES_IDS).pipe(plot_uscb_trade_gold_silver)

combine_uscb_trade_by_countries().pipe(plot_uscb_trade_by_countries)

SERIES_IDS = {
    # =========================================================================
    # Census Money Supply Aggregates
    # =========================================================================
    'X0410': 'dataset_uscb.zip', 'X0414': 'dataset_uscb.zip', 'X0415': 'dataset_uscb.zip'
}
YEAR_BASE = 1915
df = stockpile_usa_hist(SERIES_IDS)
df.div(df.loc[YEAR_BASE, :]).mul(100).pipe(plot_uscb_money_stock)

plot_uscb_finance()