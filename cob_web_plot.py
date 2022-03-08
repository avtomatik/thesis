# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 22:55:41 2020

@author: Mastermind
"""

## Add Annotations
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
source_frame  =  pd.read_csv('dataset USA 0025PR.txt')
source_frame.iloc[:, 1]  =  source_frame.iloc[:, 1].div(source_frame.iloc[0, 1])
calculList  =  []
for i in range(1, 2*len(source_frame)):
    calculList.append(source_frame.iloc[i//2, 1])
calcul_frame  =  pd.Data_frame(calculList,  columns = ['calc'])
result_frame  =  pd.concat([calcul_frame,  calcul_frame.shift(-1)],  axis = 1,  sort = False).dropna()
xlin  =  np.linspace(source_frame.iloc[:, 1].min(),  source_frame.iloc[:, 1].max(),  100)
ylin  =  xlin
plt.figure()
plt.plot(result_frame.iloc[:, 0],  result_frame.iloc[:, 1],  label = 'Series',  lw = 0.5)
plt.plot(xlin,  ylin,  label = '$Y_{t} = Y_{1+t}$',  color = 'k',  lw = 0.5)
plt.xlabel('$Y_{t}$')
plt.ylabel('$Y_{1+t}$')
plt.title('Cobweb Plot')
plt.legend()
plt.grid(True)
os.chdir('C:\\Projects')
plt.savefig('plot.pdf')