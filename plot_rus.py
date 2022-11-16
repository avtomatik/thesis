# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:04:02 2019

@author: Mastermind
"""


import os

from plot.lib import plot_grigoriev, plot_is_lm


def main():
    DIR = '/media/green-machine/KINGSTON'

    os.chdir(DIR)
    plot_is_lm()
    plot_grigoriev()


if __name__ == '__main__':
    main()
