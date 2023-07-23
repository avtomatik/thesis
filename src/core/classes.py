#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 19:22:22 2023

@author: green-machine
"""

from enum import Enum
from pathlib import Path
from typing import Any


class Token(str, Enum):

    def __new__(cls, value: str, usecols: range):
        obj = str.__new__(cls)
        obj._value_ = value
        obj.usecols = usecols
        return obj

    DOUGLAS = 'dataset_douglas.zip', range(4, 7)
    USA_BROWN = 'dataset_usa_brown.zip', range(5, 8)
    USA_COBB_DOUGLAS = 'dataset_usa_cobb-douglas.zip', range(5, 8)
    USA_KENDRICK = 'dataset_usa_kendrick.zip', range(4, 7)
    USA_MC_CONNELL = 'dataset_usa_mc_connell_brue.zip', range(1, 4)
    USCB = 'dataset_uscb.zip', range(9, 12)

    def get_kwargs(self) -> dict[str, Any]:

        NAMES = ['series_id', 'period', 'value']

        return {
            'filepath_or_buffer': Path(__file__).parent.parent.parent.joinpath('data').joinpath(self.value),
            'header': 0,
            'names': NAMES,
            'index_col': 1,
            'skiprows': (0, 4)[self.value == 'dataset_usa_brown.zip'],
            'usecols': self.usecols,
        }
