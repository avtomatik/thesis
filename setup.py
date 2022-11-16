#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 13:14:17 2022

@author: alexander
"""

from setuptools import find_packages, setup

setup(
    name='thesis',
    version='0.9.2',
    description='08.00.13 Mathematical and Instrumental Methods of Economics',
    author='Alexander Mikhailov',
    author_email='alexander.mikhailoff@gmail.com',
    url='https://github.com/avtomatik/thesis/',
    packages=[
        'collect',
        'read',
        'pull',
        'plot',
        'push',
        'test',
        'toolkit',
    ],
    package_dir={
        '': '.',
        'collect': './collect',
        'read': './read',
        'pull': './pull',
        'plot': './plot',
        'push': './push',
        'test': './test',
        'toolkit': './toolkit',
    },
)
