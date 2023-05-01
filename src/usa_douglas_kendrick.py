#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 03:34:11 2023

@author: green-machine

Subproject XII. USA Douglas & Kendrick
"""


from thesis.src.usa_douglas import usa_douglas
from thesis.src.usa_kendrick import usa_kendrick


def main():

    usa_douglas()

    # =========================================================================
    # {'KTA10S07': 'dataset_usa_kendrick.zip'}, {'KTA10S08': 'dataset_usa_kendrick.zip'} Not Working
    # =========================================================================
    usa_kendrick()


if __name__ == '__main__':
    main()
