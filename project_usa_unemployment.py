#-*- coding: utf-8 -*-
"""
Created on Tue Sep 10 23:12:03 2019

@author: Mastermind
"""


os.chdir('/media/alexander/321B-6A94')
file_name = 'dataset_usa_census1975.zip'
semi_frame_a = fetch_census(file_name, 'D0086')
semi_frame_b = fetch_usa_bls_lnu('dataset_usa_bls-2017-07-06-ln.data.1.AllData')
result_frame = pd.concat([semi_frame_a, semi_frame_b], axis=1, sort=True)

result_frame.plot(title = 'US Unemployment, {}$-${}'.format(result_frame.index[0], result_frame.index[-1]), grid=True)
os.chdir('/media/alexander/321B-6A94')
plt.savefig('unemployment.pdf', format = 'pdf', dpi = 900)
# result_frame['fused'] = result_frame.mean(1)

# autocorrelation_plot(result_frame.iloc[:, 2])
# plt.grid(True)
# os.chdir('/media/alexander/321B-6A94')
# plt.savefig('unemployment.pdf', format = 'pdf', dpi = 900)

