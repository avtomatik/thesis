#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:26:36 2023

@author: green-machine

Project X. USA Census
"""

import itertools

from core.combine import (combine_uscb_employment_conflicts,
                          combine_uscb_trade_by_countries,
                          combine_uscb_unemployment_hours_worked)
from core.plot import (plot_uscb_employment_conflicts, plot_uscb_finance,
                       plot_uscb_gnp, plot_uscb_immigration,
                       plot_uscb_money_stock, plot_uscb_trade,
                       plot_uscb_trade_by_countries,
                       plot_uscb_trade_gold_silver,
                       plot_uscb_unemployment_hours_worked)
from core.stockpile import stockpile
from statcan.src.core.funcs import transform_sum
from uscb_capital import uscb_capital
from uscb_commodities import uscb_commodities
from uscb_farm_lands import uscb_farm_lands
from uscb_manufacturing import uscb_manufacturing
from uscb_metals import uscb_metals

# =============================================================================
# Census Manufacturing Indexes
# =============================================================================
uscb_manufacturing()

# =============================================================================
# Census Structures & Equipment
# =============================================================================
uscb_capital()

# =============================================================================
# Census Primary Metals & Railroad-Related Products Manufacturing Series
# =============================================================================
uscb_metals()

# =============================================================================
# Census Manufacturing Series
# =============================================================================
uscb_commodities()

# =============================================================================
# Census Immigration
# =============================================================================

SERIES_IDS = dict.fromkeys(
    map(
        lambda _: f'C{_:04n}', itertools.chain(
            range(91, 102),
            range(103, 110),
            range(111, 116),
            range(117, 120),
        )
    ),
    Dataset.USCB
)
stockpile(SERIES_IDS).pipe(
    transform_sum, name="C0089"
).pipe(plot_uscb_immigration)

# =============================================================================
# Census Employment Series
# =============================================================================
combine_uscb_unemployment_hours_worked().pipe(
    plot_uscb_unemployment_hours_worked
)

combine_uscb_employment_conflicts().pipe(plot_uscb_employment_conflicts)

# =============================================================================
# Census Gross National Product Series
# =============================================================================
SERIES_IDS = {
    # =========================================================================
    # Census Gross National Product Series
    # =========================================================================
    'F0003': Dataset.USCB, 'F0004': Dataset.USCB
}
df = stockpile(SERIES_IDS).truncate(before=1889)
df.div(df.iloc[0, :]).mul(100).pipe(plot_uscb_gnp)

uscb_farm_lands()

SERIES_IDS = {
    # =========================================================================
    # Census Foreign Trade Series
    # =========================================================================
    'U0001': Dataset.USCB, 'U0008': Dataset.USCB, 'U0015': Dataset.USCB
}
stockpile(SERIES_IDS).pipe(plot_uscb_trade)

SERIES_IDS = {
    # =========================================================================
    # Census Foreign Trade Series
    # =========================================================================
    'U0187': Dataset.USCB, 'U0188': Dataset.USCB, 'U0189': Dataset.USCB
}
stockpile(SERIES_IDS).pipe(plot_uscb_trade_gold_silver)

combine_uscb_trade_by_countries().pipe(plot_uscb_trade_by_countries)

SERIES_IDS = {
    # =========================================================================
    # Census Money Supply Aggregates
    # =========================================================================
    'X0410': Dataset.USCB, 'X0414': Dataset.USCB, 'X0415': Dataset.USCB
}
YEAR_BASE = 1915
df = stockpile(SERIES_IDS)
df.div(df.loc[YEAR_BASE, :]).mul(100).pipe(plot_uscb_money_stock)

plot_uscb_finance()
