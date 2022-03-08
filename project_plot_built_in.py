def fetch_world_bank(source,  string):
    source_frame  =  pd.read_csv(source)
    source_frame  =  source_frame[source_frame.columns[[1, 0, 2]]]
    source_frame  =  source_frame[source_frame.iloc[:, 0] == string]
    source_frame  =  source_frame[source_frame.columns[[1, 2]]]
    if source  ==  'CHN_TUR_GDP.zip':
        source_frame.rename(columns = {'Series Name: GDP (current US$)':'Value'}, 
                            inplace=True)
    else:
        source_frame.columns  =  source_frame.columns.str.title()
    source_frame  =  source_frame.set_index('Period')
    source_frame.reset_index(level = 0,  inplace=True)
    return source_frame


def plot_built_in(module):
    source_frame  =  pd.read_csv('datasetAutocorrelation.txt')
    source_frame  =  source_frame[source_frame.columns[[1, 0, 2]]]
    series  =  source_frame.iloc[:, 0].sort_values().unique()
    del source_frame
    for i in range(len(series)):
        current  =  fetch_world_bank('datasetAutocorrelation.txt',  series[i])
        plt.figure(1+i)
        module(current.iloc[:, 1])
        plt.grid(True)
        del current
    del series
    source_frame  =  pd.read_csv('CHN_TUR_GDP.zip')
    source_frame  =  source_frame[source_frame.columns[[1, 0, 2]]]
    series  =  source_frame.iloc[:, 0].sort_values().unique()
    del source_frame
    for i in range(len(series)):
        current  =  fetch_world_bank('CHN_TUR_GDP.zip',  series[i])
        plt.figure(5+i)
        module(current.iloc[:, 1])
        plt.grid(True)
        del current
    del series
    plt.show()


'''Project:
Correlogram,  Pandas;
Bootstrap Plot,  Pandas;
Lag Plot,  Pandas'''
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import autocorrelation_plot
from pandas.plotting import bootstrap_plot
from pandas.plotting import lag_plot
plot_built_in(autocorrelation_plot)
plot_built_in(bootstrap_plot)
plot_built_in(lag_plot)