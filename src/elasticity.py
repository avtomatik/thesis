#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:09:50 2023

@author: green-machine

Project VI. Elasticity
"""

from core.plot import plot_elasticity, plot_growth_elasticity
from core.stockpile import stockpile_usa_bea
from core.transform import transform_elasticity

URL_NIPA_DATA_A = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
SERIES_IDS = {
    'A191RX': URL_NIPA_DATA_A,
    'A191RC': URL_NIPA_DATA_A,
    'A032RC': URL_NIPA_DATA_A
}
plot_elasticity(*stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(transform_elasticity))

SERIES_IDS = {
    'A032RC': URL_NIPA_DATA_A
}
stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(plot_growth_elasticity)
