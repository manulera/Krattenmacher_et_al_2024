#%%
from pandas import read_csv
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
sns.set_style('ticks')


for f in ['single','AP']:
    data = read_csv(f'experimental_data/{f}_bootstrap_fits.csv')

    for column in data:
        plt.figure()
        x = data[column]
        bins = np.linspace(np.percentile(x,2),np.percentile(x,98))
        plt.hist(x,bins)
        plt.xlabel(column)
        plt.axvline(np.percentile(x,2.5),c='red')
        plt.axvline(np.percentile(x,97.5),c='red')
        plt.title(f'{bins[0]} - {bins[-1]}')
        plt.savefig(f'experimental_data/bootstrap_plots/{f}/{column}.svg')
        
    
plt.show()