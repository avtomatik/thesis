# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 20:45:44 2019

@author: Mastermind
"""


def plot_growth_elasticity(source_frame):
    '''Growth Elasticity Plotting
    source_frame.iloc[:, 0]: Period,
    source_frame.iloc[:, 1]: Series
    '''
    result_list = []  # Create List Results
    for i in range(source_frame.shape[0]-3):
        '''
        `period`: Period, Centered
        `value_a`: Value, Centered
        `value_b`: Value, Growth Rate
        `value_c`: Value, Elasticity
        '''
        result_list.append({'period': (source_frame.iloc[1 + i, 0] + source_frame.iloc[2 + i, 0])/2,
                            'value_a': (source_frame.iloc[1 + i, 1] + source_frame.iloc[2 + i, 1])/2,
                            'value_b': (source_frame.iloc[2 + i, 1]-source_frame.iloc[i, 1])/(source_frame.iloc[i, 1] + source_frame.iloc[1 + i, 1]),
                            'value_c': (source_frame.iloc[2 + i, 1] + source_frame.iloc[3 + i, 1]-source_frame.iloc[i, 1]-source_frame.iloc[1 + i, 1])/(source_frame.iloc[i, 1] + source_frame.iloc[1 + i, 1] + source_frame.iloc[2 + i, 1] + source_frame.iloc[3 + i, 1])})
    result_frame = pd.DataFrame(result_list)  # Convert List to Dataframe

    result_frame = result_frame.set_index('Period')
    plt.figure()
    result_frame.iloc[:, 1].plot(label='Growth Rate')
    result_frame.iloc[:, 2].plot(label='Elasticity Rate')
    plt.title('Growth & Elasticity Rates')
    plt.xlabel('Period')
    plt.ylabel('Index')
    plt.grid(True)
    plt.legend()
    plt.show()


file_name = 'dataset_usa_census1949.zip'
source_frame = fetch_census(file_name, 'J0014', False)
plot_growth_elasticity(source_frame)
plot_rmf(source_frame)
