#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 13:14:17 2022

@author: alexander
"""

from setuptools import setup, find_packages


setup(
    name='thesis',
    version='0.9',
    packages=[
        'extract',
        'load',
        'plot',
        'prepare',
        'test',
        'toolkit',
    ],
    package_dir={
        '': '.',
        'extract': './extract',
        'load': './load',
        'plot': './plot',
        'prepare': './prepare',
        'test': './test',
        'toolkit': './toolkit',
    },
)
