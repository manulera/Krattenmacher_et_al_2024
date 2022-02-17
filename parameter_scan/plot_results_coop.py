#%%
import matplotlib.pyplot as plt
from pandas import read_csv
import numpy as np
from matplotlib import cm
import glob
import os

folders = glob.glob('./run*/')

for folder in folders:
    plot_folder = os.path.join(folder,'plots')
    if not os.path.isdir(plot_folder):
        os.mkdir(plot_folder)
# %% Extract the data
    data = read_csv(folder+'other_values.txt')
    parameters = read_csv(folder+'parameters_table.txt')

    # Convert to length
    data['lengthscale_density_end_fit'] = data['lengthscale_density_end_fit']*0.008
    experimental_summary = read_csv('../experimental_data/single_fits.csv')
    experimental_summary['shrinking_speed_steady_state'] = experimental_summary['shrinking_speed_steady_state']/1000.
    experimental_summary['accumulation_end_fit'] = experimental_summary['accumulation_end_fit'] / 13.
    experimental_summary['lengthscale_density_end_fit'] = experimental_summary['tau']
    data['omega'] = parameters['omega']
    data['cooperativity'] = parameters['cooperativity']
    cmap = cm.get_cmap('viridis')

    for column in experimental_summary:
        print(column,float(experimental_summary[column]))

    # Add accumulation normalised by the equilibrium amount
    data['accumulation_norm_end_fit'] = data['accumulation_end_fit']
    data['accumulation_norm_timescale'] = data['accumulation_timescale']
    experimental_summary['accumulation_norm_end_fit'] *= float(data['equilibrium_density'][0])


    # Calculate fitness
    overall_fitness_sum = np.zeros_like(data['accumulation_end_fit'])
    overall_fitness_geometric = np.ones_like(data['accumulation_end_fit'])
    nb_coefficients = 0
    for column in data:
        if column in experimental_summary and column != 'lengthscale_density_end_fit' and column != 'velocity_decay_timescale':

            nb_coefficients+=1
            # ((observed-expected)/expected)^2
            expected = float(experimental_summary[column])
            data[column+'_fitness'] = np.square((data[column] - expected)/expected)
            overall_fitness_sum+=data[column+'_fitness']
            overall_fitness_geometric*=data[column+'_fitness']

    overall_fitness_sum = overall_fitness_sum/nb_coefficients
    overall_fitness_geometric = np.power(overall_fitness_geometric,1./nb_coefficients)

    data['overall_fitness_sum'] = overall_fitness_sum
    data['overall_fitness_geometric'] = overall_fitness_geometric

#%% Plot fitness

    data.plot.scatter('omega','overall_fitness_sum',c=data['cooperativity'],cmap=cmap,sharex=False)    
    if np.min(data['omega'])>0.5:
        plt.ylim([0,0.5])
    plt.ylim([0,2])
    plt.savefig(os.path.join(plot_folder,'fitness_sum.svg'))
    data.plot.scatter('omega','overall_fitness_geometric',c=data['cooperativity'],cmap=cmap,sharex=False)    
    if np.min(data['omega'])>0.5:
        plt.ylim([0,0.5])
    plt.savefig(os.path.join(plot_folder,'fitness_geometric.svg'))


#%% Plot the rest

    colors = ['blue','magenta','green','orange']
    print(np.unique(data['cooperativity']))
    for column in data:
        if 'fitness' not in column:
            data.plot.scatter('omega',column,c=data['cooperativity'],cmap=cmap,sharex=False)    
            if column in experimental_summary:
                exp_value = float(experimental_summary[column])
                plt.axhline(y=exp_value,label='experimental value')

            plt.ylim(ymin=0)
            plt.savefig(os.path.join(plot_folder,column+'.svg'))

#%% Don't show the figures if not running ipython
plt.close('all')

