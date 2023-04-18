import seaborn as sns
import matplotlib.pyplot as plt
import pandas
from figure_matplotlib_settings import matplotlib_settings, get_confidence_intervals, plot_confidence_interval
from common_functions import load_simulation_results

plot_intervals = True

sns.set_style('ticks')
matplotlib_settings(plt)

args = [['1nM', 13], ['6nM', 13], ['antiparallel', 2], ['antiparallel', 3]]
# args = [['1nM', 13], ['6nM', 13]]
linestyles = [':', '-']
model_names = ['Model 1', 'Model 2']


for condition, protofilaments in args:

    # label for plots
    label = 'Antiparallel' if condition == 'antiparallel' else f'Single {condition}'

    # Experimental data
    fits2experiments = pandas.read_csv('experimental_data/processed_data/fits.csv')
    fits2experiments = fits2experiments[fits2experiments.condition == condition]

    # fits2experiments['condition'] = fits2experiments['condition'].apply(lambda x: 'Ase1 ' + x)
    fits2experiments.fillna(0, inplace=True)
    fits2experiments['shrinking_speed_steady_state'] = fits2experiments['shrinking_speed_steady_state'] / 1000.
    fits2experiments['shrinking_speed_steady_state_ci'] = fits2experiments['shrinking_speed_steady_state_ci'] / 1000.
    fits2experiments['accumulation_end_fit'] = fits2experiments['accumulation_end_fit'] / protofilaments

    # Confidence intervals
    data_intervals = pandas.read_csv('experimental_data/processed_data/bootstrap_confidence_intervals.csv')
    data_intervals.loc[data_intervals.magnitude == 'accumulation_end_fit', ['lower', 'upper']] = data_intervals.loc[data_intervals.magnitude == 'accumulation_end_fit', ['lower', 'upper']] / protofilaments

    if condition == '6nM':
        # model 1 and 2
        data = load_simulation_results(f'parameter_scan3/runs_6nM').drop_duplicates()
        model_1 = data[(data.cooperativity == 1) & (data.cooperativity_mode == 'protofilament')].copy()
        model_2 = data[(data.cooperativity == 3) & (data.cooperativity_mode == 'protofilament')].copy()
        model_3 = data[(data.cooperativity == 3) & (data.cooperativity_mode == 'mixed')].copy()

        models = [model_1, model_2]
        chosen_vals = [0.96, 0.9]

    elif condition == '1nM':
        data = load_simulation_results(f'parameter_scan3/runs_1nM').drop_duplicates()
        model_1 = data[(data.cooperativity == 1) & (data.cooperativity_mode == 'protofilament')].copy()
        model_2 = data[(data.cooperativity == 3) & (data.cooperativity_mode == 'protofilament')].copy()
        model_3 = data[(data.cooperativity == 4) & (data.cooperativity_mode == 'mixed')].copy()

        models = [model_1, model_2]
        chosen_vals = [0.96, 0.9]

    elif condition == 'antiparallel':
        data = load_simulation_results(f'parameter_scan3/runs_overlaps_{protofilaments}pf').drop_duplicates()
        model_1 = data[(data.cooperativity == 1) & (data.cooperativity_mode == 'protofilament')].copy()
        model_2 = data[(data.cooperativity == 3) & (data.cooperativity_mode == 'protofilament')].copy()
        model_3 = data[(data.cooperativity == 4) & (data.cooperativity_mode == 'mixed_antiparallel')].copy()

        models = [model_1, model_2]
        chosen_vals = [pandas.NA, pandas.NA]

    # When there is no accumulation timescale it can give aberrant results
    for model in models:
        model.loc[model.accumulation_timescale > 100, 'accumulation_timescale'] = 0
        model.loc[model.shrinking_speed_steady_state >= 0.39, 'accumulation_timescale'] = 0

    # Reformat the diffusion rate to use it as a category
    for model in models:
        model.D = model.D.apply(lambda x: ('%.2f' % x) + '\u03BCm$^2$/s')

    # First plot
    plt.figure()
    handle = sns.scatterplot(
        data=fits2experiments,
        x='accumulation_end_fit',
        y='shrinking_speed_steady_state',
        clip_on=False, label=label
    )

    x_ci = get_confidence_intervals(fits2experiments, data_intervals, condition, 'accumulation_end_fit')
    y_ci = get_confidence_intervals(fits2experiments, data_intervals, condition, 'shrinking_speed_steady_state')
    print(y_ci)

    plot_confidence_interval(plt, fits2experiments.accumulation_end_fit, fits2experiments.shrinking_speed_steady_state, x_ci, y_ci)

    for model, name, ls, chosen_val in zip(models, model_names, linestyles, chosen_vals):
        sns.lineplot(x='accumulation_end_fit', y='shrinking_speed_steady_state', data=model, ls=ls, color='black', label=name)
        d = model[model["omega"] == chosen_val]
        plt.scatter(d['accumulation_end_fit'], d['shrinking_speed_steady_state'], c='k', s=20, marker='s')
    plt.xlabel('Ase1 accumulation at\n steady state')
    plt.ylabel('Depol. speed at\nsteady state (\u03BCm/s)')

    plt.legend()
    if condition == 'antiparallel':
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles[:4], labels[:4])
    plt.ylim([0, .4])
    plt.xlim(xmin=0)
    plt.tight_layout()
    # plt.title(f'{condition} - {protofilaments} pfs')
    plt.savefig(f'figures_revision/{condition}_pf{protofilaments}_speed_vs_accumulation.svg')

    # Second plot
    plt.figure()
    handle = sns.scatterplot(
        data=fits2experiments,
        x='accumulation_end_fit',
        y='accumulation_timescale',
        clip_on=False, label=label
    )

    x_ci = get_confidence_intervals(fits2experiments, data_intervals, condition, 'accumulation_end_fit')
    y_ci = get_confidence_intervals(fits2experiments, data_intervals, condition, 'accumulation_timescale')
    plot_confidence_interval(plt, fits2experiments.accumulation_end_fit, fits2experiments.accumulation_timescale, x_ci, y_ci)

    for model, name, ls, chosen_val in zip(models, model_names, linestyles, chosen_vals):
        model.D = model.D.astype('str')
        sns.lineplot(x='accumulation_end_fit', y='accumulation_timescale', data=model, ls=ls, color='k', label=name)
        d = model[model["omega"] == chosen_val]
        plt.scatter(d['accumulation_end_fit'], d['accumulation_timescale'], c='k', s=20, marker='s')

    plt.xlabel('Ase1 accumulation at\n steady state')
    plt.ylabel('Accumulation\ntimescale (s)')


    plt.legend(loc='best')
    if condition == '6nM':
        plt.ylim([0, 40])
    elif condition == '1nM':
        plt.ylim([0, 15])
    elif protofilaments == 2:
        plt.ylim([0, 10])
    elif protofilaments == 3:
        plt.ylim([0, 25])

    plt.ylim([0, 40])

    plt.xlim(xmin=0)
    plt.tight_layout()
    # plt.title(f'{condition} - {protofilaments} pfs')
    plt.savefig(f'figures_revision/{condition}_pf{protofilaments}_speed_vs_timescale.svg')

plt.show()
