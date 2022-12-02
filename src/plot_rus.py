# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:04:02 2019

@author: Alexander Mikhailov
"""


import os

from .plot import plot_grigoriev, plot_rus_is_lm
from .read import read_rus_grigoriev, read_rus_is_lm


def main():
    DIR = '/media/green-machine/KINGSTON'

    os.chdir(DIR)
    read_rus_is_lm().pipe(plot_rus_is_lm)
    read_rus_grigoriev().pipe(plot_grigoriev)


if __name__ == '__main__':
    main()
