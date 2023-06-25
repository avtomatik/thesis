# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 22:29:22 2020

Thesis Project

@author: Alexander Mikhailov
"""


import cobb_douglas_can
import cobb_douglas_complex
import elasticity
import usa_bea
import usa_bea_approximation
import usa_capital
import usa_complex
import usa_mc_connell
import uscb_manufacturing_complex

import lash_up_spline
import uscb
from thesis.src.usa_douglas import usa_douglas
from thesis.src.usa_kendrick import usa_kendrick


def main():

    usa_bea_approximation()

    usa_mc_connell()

    usa_capital()

    cobb_douglas_complex()

    cobb_douglas_can()

    elasticity()

    lash_up_spline()

    usa_complex()

    # =========================================================================
    # Project IX. USA BEA
    # =========================================================================
    usa_bea()
    # =========================================================================
    # Project X. USA Census
    # =========================================================================
    uscb()
    # =========================================================================
    # Project XI. USA Census J14
    # =========================================================================
    uscb_manufacturing_complex()
    # =========================================================================
    # Project XII. USA Douglas & Kendrick
    # =========================================================================
    usa_douglas()

    usa_kendrick()


if __name__ == '__main__':
    main()
