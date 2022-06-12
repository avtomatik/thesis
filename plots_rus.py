# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:04:02 2019

@author: Mastermind
"""


import os
from plot.lib import plot_is_lm
from plot.lib import plot_grigoriev


def main():
    FOLDER = '/media/alexander/321B-6A94'
    os.chdir(FOLDER)
    plot_is_lm()
    plot_grigoriev()


if __name__ == '__main__':
    main()
