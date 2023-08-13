#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:16:06 2023

@author: green-machine

Project VIII. Complex
"""

from core.classes import Dataset
from core.combine import combine_cobb_douglas
from core.plot import plot_uscb_complex
from core.transform import transform_cobb_douglas

from thesis.src.core.backend import stockpile

# =============================================================================
# Project VIII. Complex
# =============================================================================

YEAR_BASE = 1899
df = combine_cobb_douglas().pipe(
    transform_cobb_douglas, year_base=YEAR_BASE
)[0].iloc[:, range(5)]

for column in df.columns:
    df.loc[:, [column]].pipe(plot_uscb_complex)

SERIES_IDS = [
    'D0004', 'D0130', 'F0003', 'F0004', 'P0110', 'U0001', 'U0008', 'X0414', 'X0415'
]

for series_id in SERIES_IDS:
    print(f'Processing {series_id}')
    stockpile(
        enlist_series_ids([series_id], Dataset.USCB)
    ).pipe(plot_uscb_complex)
