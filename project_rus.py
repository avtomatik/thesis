# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:04:02 2019

@author: Mastermind
"""
def plot_is_lm():
    """Data Fetch"""
    source_frame  =  pd.read_csv('datasetRUSM1.zip')
    """Plotting"""
    plt.figure()
    plt.plot(source_frame.iloc[:, 1], source_frame.iloc[:, 2])
    plt.xlabel('Percentage')
    plt.ylabel('RUB,  Millions')
    plt.title('M1 Dependency on Prime Rate')
    plt.grid(True)
    plt.show()
def plot_grigoriev():
    source_frame  =  pd.read_csv('dataset RUS Grigoriev V-.csv')
    for s in source_frame.iloc[:, 2].sort_values().unique():
        current_frame  =  source_frame[source_frame.iloc[:, 2] == s]
        current_frame  =  current_frame[current_frame.columns[[3, 4]]]
        current_frame.set_index('period',  inplace=True)
        current_frame.sort_values('period',  inplace=True)
        current_frame.rename(columns = {'value':s},  inplace=True)
        current_frame.plot(grid = True)
import pandas as pd
import matplotlib.pyplot as plt
plot_is_lm()
plot_grigoriev()