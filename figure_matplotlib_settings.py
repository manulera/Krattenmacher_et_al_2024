import numpy as np


def matplotlib_settings(plt):
    plt.rcParams['legend.frameon'] = False
    plt.rcParams['font.size'] = 12
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.figsize'] = [3, 3]


def get_confidence_intervals(fits2experiments, bootstrap_data, condition, magnitude):

    vals = bootstrap_data.loc[(bootstrap_data.condition == condition) & (bootstrap_data.magnitude == magnitude), ['lower', 'upper']].iloc[0].values
    return np.array(vals).reshape(2, 1)


def plot_confidence_interval(plt, x_value, y_value, x_ci, y_ci, *args):
    x_ci_plot = np.abs(x_ci - np.array(x_value))
    y_ci_plot = np.abs(y_ci - np.array(y_value))

    return plt.errorbar(x_value, y_value, xerr=x_ci_plot, yerr=y_ci_plot, capsize=3,)

def reorder_legend(plt, order):
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order], loc='upper right')