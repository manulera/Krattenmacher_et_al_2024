# %% Load the different data
import seaborn as sns
from pandas import read_csv
import matplotlib.pyplot as plt
import pandas as pd
sns.set_style('ticks')


def loadSimulationResults(folder):
    data = read_csv(folder+'/other_values.txt')
    parameters = read_csv(folder+'/parameters_table.txt')
    data["omega"] = parameters["omega"]

    not_fit = data["accumulation_timescale"] == 1.0
    data["accumulation_timescale"][not_fit] = 0
    data['cooperativity'] = parameters['cooperativity'].astype(int)
    data['D'] = parameters['D'].astype(float)
    data['tip_off'] = parameters['tip_off'].astype(float)
    return data


# Experimental data
experimental_summary = read_csv('../experimental_data/AP_fits.csv')
experimental_summary['shrinking_speed_steady_state'] = experimental_summary['shrinking_speed_steady_state'] / \
    1000.
# We don't divide for overlaps
experimental_summary['accumulation_end_fit'] = experimental_summary['accumulation_end_fit']

# model 1 and 2

model = loadSimulationResults('runs_overlaps_2')


# First plot

for tip_value in pd.unique(model.tip_off):
    logi1 = model.tip_off == tip_value
    plt.figure()
    plt.title(f'{tip_value}')
    for d_value in pd.unique(model.D):
        logi = (model.D == d_value) & logi1
        sns.lineplot(x='accumulation_end_fit', y='shrinking_speed_steady_state',
                    data=model[logi], label=f'{d_value}')
    plt.scatter(
    20,
    0.1,
    label='Experiment'
    )
    plt.ylim([0,0.3])
    plt.xlim([0,20])

plt.xlabel('Ase1 accumulation at steady state\n(per protofilament)')
plt.ylabel('Shrinkage speed at \nsteady state (\u03BCm/s)')

plt.legend()
plt.tight_layout()


# Second plot
plt.figure(figsize=[3, 3])
plt.scatter(
    10,
    0.1,
    label='Experiment'
)
for d_value in pd.unique(model.D):
    logi = model.D == d_value
    sns.lineplot(x='accumulation_timescale', y='shrinking_speed_steady_state',
                 data=model[logi], label=f'{d_value}')

plt.xlabel('Accumulation timescale (s)\n ')
plt.ylabel('Shrinkage speed at \nsteady state (\u03BCm/s)')

plt.legend()
plt.ylim(ymin=0)
plt.xlim([0, 20])
plt.tight_layout()


plt.show()
