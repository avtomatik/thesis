#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:26:36 2023

@author: green-machine

Project X. USA Census
"""


from core.backend import stockpile
from core.combine import (combine_uscb_employment_conflicts,
                          combine_uscb_trade_by_countries,
                          combine_uscb_unemployment_hours_worked)
from core.plot import (plot_uscb_employment_conflicts, plot_uscb_finance,
                       plot_uscb_gnp, plot_uscb_money_stock, plot_uscb_trade,
                       plot_uscb_trade_by_countries,
                       plot_uscb_trade_gold_silver,
                       plot_uscb_unemployment_hours_worked)
from uscb_capital import uscb_capital
from uscb_commodities import uscb_commodities
from uscb_farm_lands import uscb_farm_lands
from uscb_manufacturing import uscb_manufacturing
from uscb_metals import uscb_metals

from thesis.src.uscb_immigration import uscb_immigration

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
uscb_immigration()

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
SERIES_IDS = [
    # =========================================================================
    # Census Gross National Product Series
    # =========================================================================
    'F0003', 'F0004'
]

SERIES_IDS = enlist_series_ids(SERIES_IDS, Dataset.USCB)

df = stockpile(SERIES_IDS).truncate(before=1889)
df.div(df.iloc[0, :]).mul(100).pipe(plot_uscb_gnp)

uscb_farm_lands()

SERIES_IDS = [
    # =========================================================================
    # Census Foreign Trade Series
    # =========================================================================
    'U0001', 'U0008', 'U0015'
]

SERIES_IDS = enlist_series_ids(SERIES_IDS, Dataset.USCB)

stockpile(SERIES_IDS).pipe(plot_uscb_trade)

SERIES_IDS = [
    # =========================================================================
    # Census Foreign Trade Series
    # =========================================================================
    'U0187', 'U0188', 'U0189'
]

SERIES_IDS = enlist_series_ids(SERIES_IDS, Dataset.USCB)

stockpile(SERIES_IDS).pipe(plot_uscb_trade_gold_silver)

combine_uscb_trade_by_countries().pipe(plot_uscb_trade_by_countries)

SERIES_IDS = [
    # =========================================================================
    # Census Money Supply Aggregates
    # =========================================================================
    'X0410', 'X0414', 'X0415'
]

SERIES_IDS = enlist_series_ids(SERIES_IDS, Dataset.USCB)

YEAR_BASE = 1915
df = stockpile(SERIES_IDS)
df.div(df.loc[YEAR_BASE, :]).mul(100).pipe(plot_uscb_money_stock)

plot_uscb_finance()
