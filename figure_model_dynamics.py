import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas
from figure_matplotlib_settings import matplotlib_settings

matplotlib_settings(plt)


def reorder_legend(order):
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='upper right')


def mean_conf_interval(data):
    sem = np.nanstd(data) / np.sqrt(np.size(data))
    return 1.96 * sem


def aveline(x_in, y_in, bins):
    interv = bins[1] - bins[0]
    x_out = list()
    y_out = list()
    conf_int_out = list()
    for i in bins[1:]:
        log = np.less_equal(x_in, i)
        y_out.append(np.nanmean(y_in[log]))
        x_out.append(i - interv / 2)
        conf_int_out.append(mean_conf_interval(y_in[log]))
        x_in = x_in[np.logical_not(log)]
        y_in = y_in[np.logical_not(log)]

    return np.array(x_out), np.array(y_out), np.array(conf_int_out)


cmap = sns.color_palette("rocket", as_cmap=True)

folders = [
    'parameter_scan/runs_coop1/scan/run0020',
    'parameter_scan/runs_coop2/scan/run0113',
    'parameter_scan/runs_special_coop2/scan/run0076'
]

_, accum_figure = plt.subplots(figsize=[3.75, 3])
_, velocity_figure = plt.subplots(figsize=[3.75, 3])

data = pandas.read_csv('experimental_data2/processed_data/experimental_data.csv')

data_condition = data[data.condition == '6nM']
data_condition.velocity = data_condition.velocity / 1000.

accum_figure.scatter(data_condition.time, data_condition.number_of_ase1_exp / 13., 10, c=sns.color_palette()[0], alpha=0.3)
velocity_figure.scatter(data_condition.time, data_condition.velocity, 10, color=sns.color_palette()[0], alpha=0.3)

xx, yy, err = aveline(data_condition.time, data_condition.number_of_ase1_exp / 13., np.linspace(0, 50, 6))
xx = np.insert(xx, 0, 0)
yy = np.insert(yy, 0, 0)
err = np.insert(err, 0, 0)
accum_figure.errorbar(xx, yy, err, lw=2, color=sns.color_palette()[0], ecolor='black', capsize=5, label='Ase1 6nM')

xx, yy, err = aveline(data_condition.time[data_condition.timepoint > 2], data_condition.velocity[data_condition.timepoint > 2], np.linspace(0, 50, 6))
velocity_figure.errorbar(xx, yy, err, lw=2, c=sns.color_palette()[0], capsize=5, ecolor='black', label='Ase1 6nM')


names = ['Model 1', 'Model 2', 'Model 3']
linestyles = ['-', '--', ':']
for folder, name, ls in zip(folders, names, linestyles):
    speed = np.genfromtxt(f'{folder}/speed.txt', delimiter=',')
    accumulation = np.genfromtxt(f'{folder}/ase1_accumulation.txt', delimiter=',')
    accum_figure.plot(accumulation, ls=ls, label=name, c='k')
    velocity_figure.plot(speed, ls=ls, label=name, c='k')

plt.sca(accum_figure)

plt.xlabel('time (s)')
plt.ylabel('Ase1 accumulation')
plt.xlim([0, 60])
plt.ylim([0, 20])
plt.tight_layout()
plt.legend(loc='upper right')
# reorder_legend([0, 4, 1, 2, 3])
plt.savefig('figures_revision/accumulation_dynamics.svg')

plt.sca(velocity_figure)
plt.xlabel('time (s)')
plt.ylabel('depol. speed (μm/s)')
plt.xlim([0, 60])
plt.ylim([0, .4])
plt.tight_layout()
plt.legend(loc='upper right')
# reorder_legend([0, 4, 1, 2, 3])
plt.savefig('figures_revision/speed_dynamics.svg')

# plt.show()
