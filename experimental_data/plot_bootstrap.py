import pandas
from matplotlib import pyplot as plt
import numpy as np
import os

bootstrap_data = pandas.read_csv('processed_data/bootstrap_fits.csv')
whole_experiment_fits = pandas.read_csv('processed_data/fits.csv')

things2plot = [
    'accumulation_end_fit',
    'accumulation_timescale',
    'velocity_decay_timescale',
    'v_s_fit',
    'shrinking_speed_steady_state',
]

# Directory to store histograms with plots (not in git)
if not os.path.isdir('./plots/bootstrap'):
    os.makedirs('./plots/bootstrap')

output_data_list = list()

for condition in pandas.unique(bootstrap_data.condition):
    bootstrap_data_condition = bootstrap_data[bootstrap_data.condition == condition]
    for column in things2plot:
        plt.figure()
        x = bootstrap_data_condition[column]
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
            'whole_experiment_fit': whole_experiment_fits.loc[whole_experiment_fits.condition == condition, column].iloc[0],
            'lower': np.percentile(x, 2.5),
            'upper': np.percentile(x, 97.5)
        }
        output_data_list.append(this_dict)

output_data = pandas.DataFrame(output_data_list)
output_data.to_csv('processed_data/bootstrap_confidence_intervals.csv', index=False)

# plt.show()
