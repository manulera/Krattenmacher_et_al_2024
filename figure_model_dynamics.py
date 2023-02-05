import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas
from figure_matplotlib_settings import matplotlib_settings
from common_functions import aveline

matplotlib_settings(plt)

args = [['1nM', 13], ['6nM', 13], ['antiparallel', 2], ['antiparallel', 3]]

for condition, protofilaments in args:

    cmap = sns.color_palette("rocket", as_cmap=True)

    if condition == '6nM':
        continue
        folders = [
            'parameter_scan2/runs_coop1/scan/run0020',
            'parameter_scan2/runs_coop2/scan/run0113',
            'parameter_scan2/runs_special_coop2/scan/run0076'
        ]
        names = ['Model 1', 'Model 2', 'Model 3']
        linestyles = [':', '--', '-']

    elif condition == '1nM':
        folders = [
            'parameter_scan2/runs_1nM_special_coop2/scan/run0076',
        ]
        names = ['Model 3']
        linestyles = ['-']

    else:
        continue

    _, accum_figure = plt.subplots(figsize=[3.75, 3])
    _, velocity_figure = plt.subplots(figsize=[3.75, 3])

    data = pandas.read_csv('experimental_data2/processed_data/experimental_data.csv')

    data_condition = data[data.condition == condition]
    data_condition.loc[:, 'velocity'] = data_condition.loc[:, 'velocity'] / 1000.

    accum_figure.scatter(data_condition.time, data_condition.number_of_ase1_exp / protofilaments, 10, c=sns.color_palette()[0], alpha=0.3)
    velocity_figure.scatter(data_condition.time, data_condition.velocity, 10, color=sns.color_palette()[0], alpha=0.3)

    xx, yy, err = aveline(data_condition.time, data_condition.number_of_ase1_exp / protofilaments, np.linspace(0, 50, 6))
    xx = np.insert(xx, 0, 0)
    yy = np.insert(yy, 0, 0)
    err = np.insert(err, 0, 0)
    accum_figure.errorbar(xx, yy, err, lw=2, color=sns.color_palette()[0], ecolor='black', capsize=5, label='Ase1 6nM')

    xx, yy, err = aveline(data_condition.time[data_condition.timepoint > 2], data_condition.velocity[data_condition.timepoint > 2], np.linspace(0, 50, 6))
    velocity_figure.errorbar(xx, yy, err, lw=2, c=sns.color_palette()[0], capsize=5, ecolor='black', label='Ase1 6nM')

    for folder, name, ls in zip(folders, names, linestyles):
        speed = np.genfromtxt(f'{folder}/speed.txt', delimiter=',')
        accumulation = np.genfromtxt(f'{folder}/ase1_accumulation.txt', delimiter=',')
        accum_figure.plot(accumulation, ls=ls, label=name, c='k')
        velocity_figure.plot(speed, ls=ls, label=name, c='k')

    plt.sca(accum_figure)

    plt.xlabel('time (s)')
    plt.ylabel('Ase1 accumulation')
    plt.xlim([0, 60])
    plt.ylim(ymin=0)
    plt.tight_layout()
    plt.legend(loc='upper right')
    plt.savefig(f'figures_revision/{condition}_pf{protofilaments}_accumulation_dynamics.svg')

    plt.sca(velocity_figure)
    plt.xlabel('time (s)')
    plt.ylabel('depol. speed (μm/s)')
    plt.xlim([0, 60])
    plt.ylim([0, .4])
    plt.tight_layout()
    plt.legend(loc='upper right')
    plt.savefig(f'figures_revision/{condition}_pf{protofilaments}_speed_dynamics.svg')

plt.show()
