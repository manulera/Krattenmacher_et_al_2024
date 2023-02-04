import pandas
import seaborn as sns
from matplotlib import pyplot as plt

data = pandas.read_csv('processed_data/individual_fits.csv')

mags = [
    'accumulation_end_fit',
    'accumulation_timescale',
    'velocity_decay_timescale',
    'v_s_fit',
    'shrinking_speed_steady_state']

for magnitude in mags:
    for condition in pandas.unique(data.condition):
        plt.figure(figsize=[4, 4])
        plt.hist(data.loc[data.condition == condition, magnitude])
        plt.title(f'{condition} - {magnitude}')


plt.show()
