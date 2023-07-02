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

    ARCHIVE_NAME = 'dataset_douglas.zip'

    os.chdir(PATH_SRC)

    plot_douglas(ARCHIVE_NAME, TITLES_DOUGLAS, YLABELS_DOUGLAS, 'series', 'D')
