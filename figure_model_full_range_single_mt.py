import seaborn as sns
import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt
import pandas

from figure_matplotlib_settings import matplotlib_settings, get_confidence_intervals, plot_confidence_interval

sns.set_style('ticks')
matplotlib_settings(plt)

data_intervals = pandas.read_csv('experimental_data2/processed_data/bootstrap_confidence_intervals.csv')


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
experimental_summary = experimental_summary[experimental_summary.condition == '1nM']
experimental_summary['condition'] = experimental_summary['condition'].apply(lambda x: 'Ase1 ' + x)
experimental_summary.fillna(0, inplace=True)

experimental_summary['shrinking_speed_steady_state'] = experimental_summary['shrinking_speed_steady_state'] / 1000.
experimental_summary['accumulation_end_fit'] = experimental_summary['accumulation_end_fit'] / 13.


model_3 = pandas.concat(
    [loadSimulationResults('parameter_scan2/runs_1nM_special_coop1'), loadSimulationResults('parameter_scan2/runs_1nM_special_coop2')],
    ignore_index=True
)
model_3 = model_3.drop_duplicates()
model_3 = model_3[model_3.cooperativity == 3]

models = [model_3]
names = ['Model 3']
chosen_vals = [0.84]
linestyles = [':']

# First plot

plt.figure()
handle = sns.scatterplot(
    data=experimental_summary,
    x='accumulation_end_fit',
    y='shrinking_speed_steady_state',
    hue='condition', clip_on=False
)

x_ci = get_confidence_intervals(data_intervals, '1nM', 'accumulation_end_fit') / 13.
y_ci = get_confidence_intervals(data_intervals, '1nM', 'shrinking_speed_steady_state') / 1000.

plot_confidence_interval(plt, experimental_summary.accumulation_end_fit, experimental_summary.shrinking_speed_steady_state, x_ci, y_ci)

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
# plt.savefig('figures_revision/speed_vs_accumulation.svg')

# Second plot
plt.figure()
handle = sns.scatterplot(
    data=experimental_summary,
    x='accumulation_timescale',
    y='shrinking_speed_steady_state',
    hue='condition', clip_on=False
)


x_ci = get_confidence_intervals(data_intervals, '1nM', 'accumulation_timescale')
y_ci = get_confidence_intervals(data_intervals, '1nM', 'shrinking_speed_steady_state') / 1000.
plot_confidence_interval(plt, experimental_summary.accumulation_timescale, experimental_summary.shrinking_speed_steady_state, x_ci, y_ci)

for model, name, ls, chosen_val in zip(models, names, linestyles, chosen_vals):
    sns.lineplot(x='accumulation_timescale', y='shrinking_speed_steady_state', data=model, ls=ls, color='black', label=name)
    d = model[model["omega"] == chosen_val]
    plt.scatter(d['accumulation_timescale'], d['shrinking_speed_steady_state'], c='k', s=20, marker='s')

plt.xlabel('Accumulation timescale (s)\n ')
plt.ylabel('depol. speed at\nsteady state (\u03BCm/s)')

plt.legend()
plt.ylim([0, .4])
plt.xlim([0, 20])
plt.tight_layout()
# plt.savefig('figures_revision/speed_vs_timescale.svg')


plt.show()
