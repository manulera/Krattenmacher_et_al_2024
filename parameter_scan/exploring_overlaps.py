# %% Load the different data
import seaborn as sns
from pandas import read_csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
sns.set_style('ticks')


def loadSimulationResults(folder):
    data = read_csv(folder+'/other_values.txt')
    parameters = read_csv(folder+'/parameters_table.txt')
    data["omega"] = parameters["omega"]
    data["equilibrium_density"] = parameters["equilibrium_density"].astype(float)
    not_fit = data["accumulation_timescale"] == 1.0
    data["accumulation_timescale"][not_fit] = 0
    data['cooperativity'] = parameters['cooperativity'].astype(int)
    data['D'] = parameters['D'].astype(float)
    data['folder'] = folder
    return data


model = loadSimulationResults('runs_overlaps_2')

plt.figure()

# Find closest to velocity observed
for d_value in pd.unique(model.D):
    logi = model.D == d_value
    this_data = model[logi].copy()
    diff_with_observed = this_data['shrinking_speed_steady_state'] - 0.1
    x = this_data.loc[diff_with_observed.idxmin()]
    print(x.folder)
    plt.scatter(x['D'], x['P0_end_fit'] + x['equilibrium_density'])

    # sns.lineplot(x='accumulation_end_fit', y='shrinking_speed_steady_state',
    #              data=model[logi], label=f'{d_value}')





plt.show()
