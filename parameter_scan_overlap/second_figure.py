#%% Load the different data
import seaborn as sns
import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt
import pandas as pd
sns.set_style('ticks')

def loadSimulationResults(folder):
    data = read_csv(folder+'/other_values.txt')
    parameters = read_csv(folder+'/parameters_table.txt')
    data["v_s"] = parameters["v_s"]
    
    not_fit = data["accumulation_timescale"]==1.0
    data["accumulation_timescale"][not_fit] = 0
    data['cooperativity'] = parameters['cooperativity'].astype(int)
    return data

# Experimental data
experimental_summary = read_csv('../experimental_data/AP_fits.csv')
experimental_summary['shrinking_speed_steady_state'] = experimental_summary['shrinking_speed_steady_state']/1000.

# Here we don't divide because the accumulation is mostly in the overlap
experimental_summary['accumulation_end_fit'] = experimental_summary['accumulation_end_fit'] / 12.


model_3 = loadSimulationResults('runs2')

models = [model_3]
names = ['Model 3, N=3, $\Omega$=0.84']
chosen_vals = [1,0.90, 0.84]
linestyles = [':']

plt.figure(figsize=[3,3])
plt.scatter(
    experimental_summary['accumulation_end_fit'],
    0.1,
    label='Experiment'
)
for model, name, ls, chosen_val in zip(models,names,linestyles,chosen_vals):
    sns.lineplot(x='accumulation_end_fit',y='shrinking_speed_steady_state',data=model,ls=ls,hue='cooperativity', label=name,sort=False)
    d = model[model["v_s"]==chosen_val]
    plt.scatter(d['accumulation_end_fit'],d['shrinking_speed_steady_state'],c='k',s=20,marker='s')
plt.xlabel('Ase1 accumulation at steady state\n(per protofilament)')
plt.ylabel('Shrinkage speed at \nsteady state (\u03BCm/s)')

plt.legend()
plt.ylim([0,0.3])
plt.xlim(xmin=0)
plt.tight_layout()
plt.savefig('plots_paper/speed_vs_accumulation_2.svg')

# Second plot
plt.figure(figsize=[3,3])
plt.scatter(
    experimental_summary['accumulation_timescale'],
    0.1,
    label='Experiment'
)
for model, name, ls, chosen_val in zip(models,names,linestyles,chosen_vals):
    sns.lineplot(x='accumulation_timescale',y='shrinking_speed_steady_state',data=model,ls=ls,hue='cooperativity', label=name,sort=False)
    d = model[model["v_s"]==chosen_val]
    plt.scatter(d['accumulation_timescale'],d['shrinking_speed_steady_state'],c='k',s=20,marker='s')

plt.xlabel('Accumulation timescale (s)\n ')
plt.ylabel('Shrinkage speed at \nsteady state (\u03BCm/s)')

plt.legend()
plt.ylim([0,0.3])
plt.xlim(xmin=0)
plt.tight_layout()
plt.savefig('plots_paper/speed_vs_timescale_2.svg')



plt.show()