import pandas
import numpy as np

data = pandas.read_csv('processed_data/experimental_data.csv')

data = data[(data['condition'] == 'antiparallel') & (data['time']> 10.)].copy()

print(np.nanmedian(data['number_of_ase1_gauss']))
print(np.nanmedian(data['number_of_ase1_exp']))