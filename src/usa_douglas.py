#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 23:30:39 2023

@author: green-machine
"""

import os

from core.constants import TITLES_DOUGLAS, YLABELS_DOUGLAS
from core.plot import plot_douglas

if __name__ == '__main__':
    # =========================================================================
    # Douglas European Demographics & Growth of US Capital
    # =========================================================================

    PATH_SRC = '/home/green-machine/data_science/data/interim'

    os.chdir(PATH_SRC)

    plot_douglas(
        Dataset.DOUGLAS,
        TITLES_DOUGLAS,
        YLABELS_DOUGLAS,
        'series',
        'D'
    )
