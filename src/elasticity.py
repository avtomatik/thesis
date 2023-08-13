#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:09:50 2023

@author: green-machine

Project VI. Elasticity
"""

from core.plot import plot_elasticity, plot_growth_elasticity
from core.transform import transform_elasticity

from thesis.src.core.backend import stockpile

SERIES_IDS = ['A191RX', 'A191RC', 'A032RC']
SERIES_IDS = enlist_series_ids(SERIES_IDS, URL.NIPA)
plot_elasticity(
    *stockpile(SERIES_IDS).dropna(axis=0).pipe(transform_elasticity)
)

SERIES_IDS = [SeriesID('A032RC', URL.NIPA)]
stockpile(SERIES_IDS).dropna(axis=0).pipe(plot_growth_elasticity)
