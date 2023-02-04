import seaborn as sns
import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt
import pandas as pd

from figure_matplotlib_settings import matplotlib_settings

sns.set_style('ticks')
matplotlib_settings(plt)


def loadSimulationResults(folder):
    data = read_csv(folder + '/other_values.txt')
    parameters = read_csv(folder + '/parameters_table.txt')
    data["omega"] = parameters["omega"]

    not_fit = data["accumulation_timescale"] == 1.0
    data["accumulation_timescale"][not_fit] = 0
    data['cooperativity'] = parameters['cooperativity'].astype(int)
    return data


# Experimental data
experimental_summary = read_csv('experimental_data2/processed_data/fits.csv')
experimental_summary = experimental_summary[experimental_summary.condition.str.contains('nM')]
experimental_summary['condition'] = experimental_summary['condition'].apply(lambda x: 'Ase1 ' + x)
experimental_summary.fillna(0, inplace=True)

experimental_summary['shrinking_speed_steady_state'] = experimental_summary['shrinking_speed_steady_state'] / 1000.
experimental_summary['accumulation_end_fit'] = experimental_summary['accumulation_end_fit'] / 13.

# model 1 and 2

model_1n2 = pd.concat(
    [loadSimulationResults('parameter_scan/runs_coop1'), loadSimulationResults('parameter_scan/runs_coop2')],
    ignore_index=True
)

# Remove repeated rows
model_1n2 = model_1n2.drop_duplicates()

model_1 = model_1n2[model_1n2.cooperativity == 1]
model_2 = model_1n2[model_1n2.cooperativity == 4]

model_3 = pd.concat(
    [loadSimulationResults('parameter_scan/runs_special_coop1'), loadSimulationResults('parameter_scan/runs_special_coop2')],
    ignore_index=True
)
model_3 = model_3.drop_duplicates()
model_3 = model_3[model_3.cooperativity == 3]

models = [model_1, model_2, model_3]
names = ['Model 1', 'Model 2', 'Model 3']
chosen_vals = [1, 0.90, 0.84]
linestyles = ['-', '--', ':']

# First plot

plt.figure()
handle = sns.scatterplot(
    data=experimental_summary,
    x='accumulation_end_fit',
    y='shrinking_speed_steady_state',
    hue='condition', clip_on=False
)

for model, name, ls, chosen_val in zip(models, names, linestyles, chosen_vals):
    sns.lineplot(x='accumulation_end_fit', y='shrinking_speed_steady_state', data=model, ls=ls, color='black', label=name)
    d = model[model["omega"] == chosen_val]
    plt.scatter(d['accumulation_end_fit'], d['shrinking_speed_steady_state'], c='k', s=20, marker='s')
plt.xlabel('Ase1 accumulation at\n steady state')
plt.ylabel('depol. speed at\nsteady state (\u03BCm/s)')

plt.legend()
plt.ylim([0, .4])
plt.xlim(xmin=0)
plt.tight_layout()
plt.savefig('figures_revision/speed_vs_accumulation.svg')

# Second plot
plt.figure()
handle = sns.scatterplot(
    data=experimental_summary,
    x='accumulation_timescale',
    y='shrinking_speed_steady_state',
    hue='condition', clip_on=False
)


for model, name, ls, chosen_val in zip(models, names, linestyles, chosen_vals):
    sns.lineplot(x='accumulation_timescale', y='shrinking_speed_steady_state', data=model, ls=ls, color='black', label=name)
    d = model[model["omega"] == chosen_val]
    plt.scatter(d['accumulation_timescale'], d['shrinking_speed_steady_state'], c='k', s=20, marker='s')

plt.xlabel('Accumulation timescale (s)\n ')
plt.ylabel('depol. speed at\nsteady state (\u03BCm/s)')

plt.legend()
plt.ylim([0, .4])
plt.xlim(xmin=0)
plt.tight_layout()
plt.savefig('figures_revision/speed_vs_timescale.svg')


# plt.show()
