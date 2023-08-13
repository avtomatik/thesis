#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 19:22:22 2023

@author: green-machine
"""

import io
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Union

import requests


class Dataset(str, Enum):

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
            'skiprows': (0, 4)[self.name in ['USA_BROWN']],
            'usecols': self.usecols,
        }


class URL(Enum):
    FIAS = 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    NIPA = 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'

    def get_kwargs(self) -> dict[str, Any]:

        NAMES = ['series_ids', 'period', 'value']

        kwargs = {
            'header': 0,
            'names': NAMES,
            'index_col': 1,
            'thousands': ','
        }
        if requests.head(self.value).status_code == 200:
            kwargs['filepath_or_buffer'] = io.BytesIO(
                requests.get(self.value).content
            )
        else:
            kwargs['filepath_or_buffer'] = self.value.split('/')[-1]
        return kwargs


@dataclass(frozen=True, eq=True)
class SeriesID:
    series_id: str
    source: Union[Dataset, URL]
