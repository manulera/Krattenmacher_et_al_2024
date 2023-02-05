from pandas import read_csv
import numpy as np

def load_simulation_results(folder):
    data = read_csv(folder + '/other_values.txt')
    parameters = read_csv(folder + '/parameters_table.txt')
    data["omega"] = parameters["omega"]

    not_fit = data["accumulation_timescale"] == 1.0
    data["accumulation_timescale"][not_fit] = 0
    data['cooperativity'] = parameters['cooperativity'].astype(int)
    data['D'] = parameters['D'].astype(float)
    return data


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
