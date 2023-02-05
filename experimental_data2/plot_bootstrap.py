import pandas
from matplotlib import pyplot as plt
import numpy as np


data = pandas.read_csv('processed_data/bootstrap_fits.csv')

things2plot = [
    'accumulation_end_fit',
    'accumulation_timescale',
    'velocity_decay_timescale',
    'v_s_fit',
    'shrinking_speed_steady_state',
]

output_data_list = list()

for condition in pandas.unique(data.condition):
    data_condition = data[data.condition == condition]
    for column in things2plot:
        plt.figure()
        x = data_condition[column]
        x = x[x > 0].copy()
        bins = np.linspace(np.percentile(x, 2), np.percentile(x, 98))
        plt.hist(x, bins)
        plt.xlabel(column)
        plt.axvline(np.percentile(x, 2.5), c='red')
        plt.axvline(np.percentile(x, 97.5), c='red')
        plt.title(f'{condition}\n{bins[0]} - {bins[-1]}')
        plt.savefig(f'./plots/bootstrap/{condition}_{column}.svg')

        this_dict = {
            'condition': condition,
            'magnitude': column,
            'lower': np.percentile(x, 2.5),
            'upper': np.percentile(x, 97.5)
        }
        output_data_list.append(this_dict)

output_data = pandas.DataFrame(output_data_list)
output_data.to_csv('processed_data/bootstrap_confidence_intervals.csv', index=False)

plt.show()
