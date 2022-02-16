#%%
import matplotlib.pyplot as plt
from pandas import read_csv
import numpy as np

folder = 'runs2/'

data = read_csv(folder+'other_values.txt')
parameters = read_csv(folder+'parameters_table.txt')

# Convert to length
data['lengthscale_density_end_fit'] = data['lengthscale_density_end_fit']*0.008
experimental_summary = read_csv('../experimental_data/single_fits.csv')
experimental_summary['shrinking_speed_steady_state'] = experimental_summary['shrinking_speed_steady_state']/1000.
experimental_summary['accumulation_end_fit'] = experimental_summary['accumulation_end_fit'] / 13.
experimental_summary['lengthscale_density_end_fit'] = experimental_summary['tau']

#%%
for column in data:
    plt.figure()
    plt.ylabel(column)
    plt.xlabel('omega')
    plt.scatter(parameters['omega'],data[column],label='simulation results')
    plt.ylim(ymin=0)
    if column in experimental_summary:
        exp_value = float(experimental_summary[column])
        plt.axhline(y=exp_value,label='experimental value')
        plt.axvline(x=0.87,color='green')
        ax2 = plt.gca().twinx()
        ax2.set_ylabel('percentage deviation\nfrom experiment', color='magenta')
        yy = np.square((data[column] - exp_value)/exp_value)
        ax2.plot(parameters['omega'],yy,color='magenta',label='% deviation')
        # ax2.set_ylim(ymin=0)
        data[column+'_fitness'] = yy
    plt.legend()

plt.show()
# %% Calculate overall fitness
# We simply do the geometric mean
overall_fitness_sum = np.zeros_like(data['accumulation_end_fit'])
overall_fitness_geometric = np.ones_like(data['accumulation_end_fit'])
nb_coefficients = 0


for column in data:
    if column.endswith('_fitness'):
    # This one if we want to exclude the lengthscale from the model
    # if column.endswith('_fitness') and 'lengthscale_density_end_fit_fitness' != column:
        print(column)
        nb_coefficients+=1
        overall_fitness_sum+=data[column] 
        overall_fitness_geometric*=data[column]

overall_fitness_sum = overall_fitness_sum/nb_coefficients
overall_fitness_geometric = np.power(overall_fitness_geometric,1./nb_coefficients)

indexes_sorted = np.argsort(overall_fitness_geometric)

print([parameters.omega[i] for i in indexes_sorted])


plt.figure()
plt.scatter(parameters.omega,overall_fitness_sum)
plt.ylim(0,1)
plt.ylabel('arithmetic mean of errors')

ax2 = plt.gca().twinx()
ax2.scatter(parameters.omega,overall_fitness_geometric,color='magenta',label='% deviation')
ax2.set_ylabel('geometric mean of errors',c='magenta')
ax2.set_ylim(ymin=0)
plt.show()
