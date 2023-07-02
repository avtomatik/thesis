#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:18:46 2023

@author: green-machine

Project IX. USA BEA
"""


from core.combine import (combine_usa_d, combine_usa_e, combine_usa_investment,
                          combine_usa_investment_manufacturing,
                          combine_usa_kurenkov,
                          combine_usa_manufacturing_money)
from core.plot import (plot_d, plot_e, plot_investment,
                       plot_investment_manufacturing, plot_manufacturing_money,
                       plot_usa_kurenkov)
from core.read import read_temporary
from core.transform import (transform_d, transform_e, transform_investment,
                            transform_investment_manufacturing)

# =============================================================================
# Project: Initial Version Dated: 05 October 2012
# =============================================================================
combine_usa_investment_manufacturing().pipe(
    transform_investment_manufacturing
).pipe(
    plot_investment_manufacturing
)

# =============================================================================
# Project: Initial Version Dated: 23 November 2012
# =============================================================================
combine_usa_investment().pipe(transform_investment).pipe(plot_investment)

# =============================================================================
# Project: Initial Version Dated: 16 June 2013
# =============================================================================
combine_usa_manufacturing_money().pipe(
    transform_investment
).pipe(
    plot_manufacturing_money
)

# =============================================================================
# Project: Initial Version Dated: 15 June 2015
# =============================================================================
plot_d(*combine_usa_d().pipe(transform_d))

# =============================================================================
# Project: Initial Version Dated: 17 February 2013
# =============================================================================
for df in combine_usa_e().pipe(transform_e):
    df.pipe(plot_e)

# =============================================================================
# Project: BEA Data Compared with Kurenkov Yu.V. Data
# =============================================================================
FILE_NAME = 'dataset_usa_reference_ru_kurenkov_yu_v.csv'
COLUMNS_TO_TEST = [
    ['A191RX', 'AIPMA_SA_IX'],
    ['bea_labor_mfg'],
    ['k1n31gd1es00'],
    ['CAPUTL.B50001.A']
]

df_control = read_temporary(FILE_NAME)
df_test = combine_usa_kurenkov()

plot_usa_kurenkov(df_control, df_test, COLUMNS_TO_TEST)
