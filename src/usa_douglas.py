#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 23:30:39 2023

@author: green-machine
"""

import os

from core.classes import Dataset
from core.config import DATA_DIR
from core.constants import TITLES_DOUGLAS, YLABELS_DOUGLAS
from core.plot import plot_douglas

if __name__ == "__main__":
    # =========================================================================
    # Douglas European Demographics & Growth of US Capital
    # =========================================================================

    os.chdir(DATA_DIR)

    plot_douglas(
        Dataset.DOUGLAS, TITLES_DOUGLAS, YLABELS_DOUGLAS, "series", "D"
    )
