import seaborn as sns
from pandas import read_csv
import matplotlib.pyplot as plt
import pandas
from figure_matplotlib_settings import matplotlib_settings, get_confidence_intervals, plot_confidence_interval

plot_intervals = True

sns.set_style('ticks')
matplotlib_settings(plt)
condition = 'antiparallel'
protofilaments = 3


def loadSimulationResults(folder):
    data = read_csv(folder + '/other_values.txt')
    parameters = read_csv(folder + '/parameters_table.txt')
    data["omega"] = parameters["omega"]

    not_fit = data["accumulation_timescale"] == 1.0
    data["accumulation_timescale"][not_fit] = 0
    data['cooperativity'] = parameters['cooperativity'].astype(int)
    data['D'] = parameters['D'].astype(float)
    return data


# Experimental data
fits2experiments = read_csv('experimental_data2/processed_data/fits.csv')
fits2experiments = fits2experiments[fits2experiments.condition == condition]
# fits2experiments['condition'] = fits2experiments['condition'].apply(lambda x: 'Ase1 ' + x)
fits2experiments.fillna(0, inplace=True)
fits2experiments['shrinking_speed_steady_state'] = fits2experiments['shrinking_speed_steady_state'] / 1000.
fits2experiments['shrinking_speed_steady_state_ci'] = fits2experiments['shrinking_speed_steady_state_ci'] / 1000.
fits2experiments['accumulation_end_fit'] = fits2experiments['accumulation_end_fit'] / protofilaments

# Confidence intervals
data_intervals = pandas.read_csv('experimental_data2/processed_data/bootstrap_confidence_intervals.csv')
data_intervals.loc[data_intervals.magnitude == 'accumulation_end_fit', ['lower', 'upper']] = data_intervals.loc[data_intervals.magnitude == 'accumulation_end_fit', ['lower', 'upper']] / protofilaments

if condition == '6nM':
    # model 1 and 2
    model_1n2 = pandas.concat(
        [loadSimulationResults('parameter_scan2/runs_coop1'), loadSimulationResults('parameter_scan2/runs_coop2')],
        ignore_index=True
    )
    # Remove repeated rows
    model_1n2 = model_1n2.drop_duplicates()
    model_1 = model_1n2[model_1n2.cooperativity == 1].copy()
    model_2 = model_1n2[model_1n2.cooperativity == 4].copy()
    model_3 = pandas.concat(
        [loadSimulationResults('parameter_scan2/runs_special_coop1'), loadSimulationResults('parameter_scan2/runs_special_coop2')],
        ignore_index=True
    )
    model_3 = model_3.drop_duplicates()
    model_3 = model_3[model_3.cooperativity == 3]

    models = [model_1, model_2, model_3]
    names = ['Model 1', 'Model 2', 'Model 3']
    chosen_vals = [1, 0.90, 0.84]
    linestyles = ['-', '--', ':']

elif condition == '1nM':
    model_3 = pandas.concat(
        [loadSimulationResults('parameter_scan2/runs_1nM_special_coop1'), loadSimulationResults('parameter_scan2/runs_1nM_special_coop2')],
        ignore_index=True
    )
    model_3 = model_3.drop_duplicates()
    model_3 = model_3[model_3.cooperativity == 3].copy()

    models = [model_3]
    names = ['Model 3']
    chosen_vals = [0.84]
    linestyles = [':']

elif condition == 'antiparallel':
    model_3 = pandas.concat(
        [loadSimulationResults(f'parameter_scan2/runs_overlap_coop1_{protofilaments}pf')],
        ignore_index=True
    )
    model_3 = model_3.drop_duplicates()
    model_3 = model_3[model_3.cooperativity == 3]

    models = [model_3]
    names = ['Model 3']
    chosen_vals = [0.84]
    linestyles = [':']

# When there is no accumulation timescale it can give aberrant results
for model in models:
    model.loc[model.accumulation_timescale > 1000, 'accumulation_timescale'] = 0


# First plot
plt.figure()
handle = sns.scatterplot(
    data=fits2experiments,
    x='accumulation_end_fit',
    y='shrinking_speed_steady_state',
    hue='condition', clip_on=False
)

x_ci = get_confidence_intervals(fits2experiments, data_intervals, condition, 'accumulation_end_fit')
y_ci = get_confidence_intervals(fits2experiments, data_intervals, condition, 'shrinking_speed_steady_state')
print(y_ci)

plot_confidence_interval(plt, fits2experiments.accumulation_end_fit, fits2experiments.shrinking_speed_steady_state, x_ci, y_ci)

for model, name, ls, chosen_val in zip(models, names, linestyles, chosen_vals):
    model.D = model.D.astype('str')
    sns.lineplot(x='accumulation_end_fit', y='shrinking_speed_steady_state', data=model, ls=ls, hue='D')
    # sns.lineplot(x='accumulation_end_fit', y='shrinking_speed_steady_state', data=model, ls=ls, color='black', label=name)
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
    data=fits2experiments,
    x='accumulation_timescale',
    y='shrinking_speed_steady_state',
    hue='condition', clip_on=False
)

x_ci = get_confidence_intervals(fits2experiments, data_intervals, condition, 'accumulation_timescale')
y_ci = get_confidence_intervals(fits2experiments, data_intervals, condition, 'shrinking_speed_steady_state')
plot_confidence_interval(plt, fits2experiments.accumulation_timescale, fits2experiments.shrinking_speed_steady_state, x_ci, y_ci)

for model, name, ls, chosen_val in zip(models, names, linestyles, chosen_vals):
    model.D = model.D.astype('str')
    sns.lineplot(x='accumulation_timescale', y='shrinking_speed_steady_state', data=model, ls=ls, hue='D')
    d = model[model["omega"] == chosen_val]
    plt.scatter(d['accumulation_timescale'], d['shrinking_speed_steady_state'], c='k', s=20, marker='s')

plt.xlabel('Accumulation timescale (s)\n ')
plt.ylabel('depol. speed at\nsteady state (\u03BCm/s)')

plt.legend()
plt.ylim([0, .4])
plt.tight_layout()
plt.xlim(xmin=0)
plt.savefig('figures_revision/speed_vs_timescale.svg')


plt.show()
