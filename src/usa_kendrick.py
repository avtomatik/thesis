#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 19:00:30 2023

@author: green-machine
"""

import os

from core.constants import TITLES_KENDRICK, YLABELS_KENDRICK
from core.plot import plot_douglas

if __name__ == '__main__':
    # =========================================================================
    # Kendrick Macroeconomic Series
    # =========================================================================

    PATH_SRC = '/home/green-machine/data_science/data/interim'

    ARCHIVE_NAME = 'dataset_usa_kendrick.zip'

    os.chdir(PATH_SRC)

    plot_douglas(ARCHIVE_NAME, TITLES_KENDRICK, YLABELS_KENDRICK, 'description', 'K')

