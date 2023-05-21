#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:14:01 2023

@author: green-machine

Subproject VII. Lash-Up Spline
"""

from thesis.src.lib.combine import combine_cobb_douglas
from thesis.src.lib.tools import (lash_up_spline_ea, lash_up_spline_eb,
                                  lash_up_spline_la, lash_up_spline_lb,
                                  lash_up_spline_lls, run_lash_up_spline)
from thesis.src.lib.transform import transform_cobb_douglas

# =============================================================================
# Subproject VII. Lash-Up Spline
# =============================================================================
# =============================================================================
# Lash-Up Splines
# =============================================================================
# =============================================================================
# Fixed Assets Turnover
# =============================================================================
YEAR_BASE = 1899
df = combine_cobb_douglas().pipe(
    transform_cobb_douglas, year_base=YEAR_BASE
)[0].iloc[:, [6]]
# =============================================================================
# Option 1
# =============================================================================
df.pipe(run_lash_up_spline, kernel=lash_up_spline_lls)
# =============================================================================
# Option 2.1.1
# =============================================================================
df.pipe(run_lash_up_spline, kernel=lash_up_spline_ea)
# =============================================================================
# Option 2.1.2
# =============================================================================
df.pipe(run_lash_up_spline, kernel=lash_up_spline_eb)
# =============================================================================
# Option 2.2.1
# =============================================================================
df.pipe(run_lash_up_spline, kernel=lash_up_spline_la)
# =============================================================================
# Option 2.2.2
# =============================================================================
df.pipe(run_lash_up_spline, kernel=lash_up_spline_lb)
