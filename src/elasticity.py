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

SERIES_IDS = {
    'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
}
plot_elasticity(*stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(transform_elasticity))

SERIES_IDS = {
    'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
}
stockpile_usa_bea(SERIES_IDS).dropna(axis=0).pipe(plot_growth_elasticity)
