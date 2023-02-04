import numpy as np
import matplotlib.pyplot as plt
import pandas
import seaborn as sns


def accumulationFit(t, P, T):
    return P * (1 - np.exp(-t / T))


def velocityFit(t, P0, Pend, T):
    return P0 * np.exp(-t / T) + Pend


cmap = sns.color_palette("rocket", as_cmap=True)

data = pandas.read_csv('processed_data/experimental_data.csv')
fits = pandas.read_csv('processed_data/fits.csv')

things2plot = [
    'velocity',
    'equilibrium_density',
    'number_of_ase1_gauss',
    'number_of_ase1_exp',
    'decay_lengthscale',
]


for condition in ['6nM']:
    data_condition = data[data.condition == condition]
    fits_condition = fits[fits.condition == condition].iloc[0].to_dict()
    # For plotting the model
    t = np.linspace(0, np.max(data_condition.time))
    accumulation_fit = accumulationFit(t, fits_condition['accumulation_end_fit'], fits_condition['accumulation_timescale'])

    v0 = fits_condition['v_s_fit'] - fits_condition['shrinking_speed_steady_state']
    velocity_fit = velocityFit(t, v0, fits_condition['shrinking_speed_steady_state'], fits_condition['velocity_decay_timescale'])

    def accumulationFit(t, P, T):
        return P * (1 - np.exp(-t / T))

    def velocityFit(t, P0, Pend, T):
        return P0 * np.exp(-t / T) + Pend

    for magnitude in things2plot:
        plt.figure(figsize=[4, 4])
        plt.title(condition)
        for event in np.unique(data_condition['event_id']):
            logi = data_condition['event_id'] == event
            this_df = data_condition[logi]
            color = cmap(list(this_df.event_nb)[0] / np.max(data_condition.event_nb) * 0.8)
            plt.plot(this_df.time, this_df[magnitude], c=color)

        if magnitude == 'velocity':
            plt.plot(t, velocity_fit, color='black', lw=3)
        if magnitude == 'number_of_ase1_exp':
            plt.plot(t, accumulation_fit, color='black', lw=3)

        plt.xlabel('time')
        plt.ylabel(magnitude)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0)
        plt.tight_layout()
        plt.savefig(f'plots/{condition}_time_vs_{magnitude}.svg')

plt.show()
