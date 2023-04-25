# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:04:02 2019

@author: Alexander Mikhailov
"""


import os

from thesis.src.lib.plot import plot_rus_grigoriev, plot_rus_is_lm
from thesis.src.lib.read import read_rus_grigoriev, read_rus_is_lm


def main(path_src: str = '/media/green-machine/KINGSTON') -> None:

    os.chdir(path_src)
    read_rus_is_lm().pipe(plot_rus_is_lm)
    read_rus_grigoriev().pipe(plot_rus_grigoriev)


if __name__ == '__main__':
    main()
