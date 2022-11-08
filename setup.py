#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 13:14:17 2022

@author: alexander
"""

from setuptools import find_packages, setup

setup(
    name='thesis',
    version='0.9.1',
    packages=[
        'collect',
        'extract',
        'plot',
        'push',
        'test',
        'toolkit',
    ],
    package_dir={
        '': '.',
        'collect': './collect',
        'extract': './extract',
        'plot': './plot',
        'push': './push',
        'test': './test',
        'toolkit': './toolkit',
    },
)
