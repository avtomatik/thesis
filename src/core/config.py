#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  7 20:06:28 2025

@author: alexandermikhailov
"""

from pathlib import Path

DIR = "/home/green-machine/data_science/"

BASE_DIR = Path(DIR)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"

DATA_INTERIM_DIR = DATA_DIR / "interim"
