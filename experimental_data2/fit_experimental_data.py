import numpy as np
import pandas
from scipy.optimize import curve_fit


def accumulationFit(t, P, T):
    return P * (1 - np.exp(-t / T))


def velocityFit(t, P0, Pend, T):
    return P0 * np.exp(-t / T) + Pend


def get_fits(d, condition):
    # Fit the timescale to the non-normalised data
    sugg = [70, 20] if 'nM' in condition else [20, 30]

    logi = np.logical_not(np.isnan(d.number_of_ase1_exp))
    if sum(logi) < 3:
        return None
    try:
        params_accum, _ = curve_fit(accumulationFit, d.time[logi], d.number_of_ase1_exp[logi], sugg)
    except RuntimeError:
        return None

    # Fit the timescale to the velocity data (we exclude the first timepoints)
    sugg = [130, 110, 5] if 'nM' in condition else [200, 100, 5]
    logi = np.logical_not(np.isnan(d.velocity))
    logi = np.logical_and(logi, np.greater(d.timepoint, 2))
    if sum(logi) < 3:
        return None
    try:
        params_velocity, _ = curve_fit(velocityFit, d.time[logi], d.velocity[logi], sugg)
    except RuntimeError:
        return None
    # Tau should be approximately 200 nm
    row = {
        'condition': condition,
        'accumulation_end_fit': params_accum[0],
        'accumulation_timescale': params_accum[1],
        'velocity_decay_timescale': params_velocity[2],
        'v_s_fit': params_velocity[0] + params_velocity[1],
        'shrinking_speed_steady_state': params_velocity[1],

    }

    return row


data = pandas.read_csv('processed_data/experimental_data.csv')
output_data_list = list()
individual_fits_list = list()

for condition in pandas.unique(data.condition):
    data_condition = data[data.condition == condition]

    output_data_list.append(get_fits(data_condition, condition))
    for event_id in pandas.unique(data_condition.event_id):
        logi = data_condition.event_id == event_id
        # Do not do individual fits for very short traces
        if sum(logi) < 3:
            continue
        individual_fits_list.append(get_fits(data_condition[logi], condition))

out_data = pandas.DataFrame(output_data_list)
out_data.to_csv('processed_data/fits.csv', float_format='%.3E', index=False)

individual_fits_list = [f for f in individual_fits_list if f is not None]
individual_fits = pandas.DataFrame(individual_fits_list)
individual_fits.to_csv('processed_data/individual_fits.csv', float_format='%.3E', index=False)
