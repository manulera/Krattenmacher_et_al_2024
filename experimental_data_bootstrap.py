#%%
import numpy as np
from pandas import read_csv, DataFrame
from fit_experimental_data import accumulationFit, velocityFit, least_squares_fitting

value_dict = {
        'accumulation_end_fit': list(),
        'accumulation_timescale': list(),
        'velocity_decay_timescale': list(),
        'v_s_fit': list(),
        'shrinking_speed_steady_state': list(),
}

for f in ['single','AP']:
    all_df = read_csv(f'experimental_data/data_{f}.csv')
    # The ids of unique shrinkage events
    unique_ids = np.unique(all_df.trace)
    # The number of events we pick each time
    pick_nb = int(unique_ids.shape[0]/2)
    
    for i in range(1000):
        print(i)
        picked_ids = np.random.choice(unique_ids,pick_nb)
        logi = all_df.trace.isin(picked_ids)
        df = all_df[logi]
        
        # Fit the timescale to the non-normalised data
        logi = np.logical_not(np.isnan(df.number_of_Ase1))
        res = least_squares_fitting(accumulationFit,df.t[logi],df.number_of_Ase1[logi],[70,20])
        params_accum = res.x
        
        # Fit the timescale to the velocity data (we exclude the first timepoints)
        logi = np.logical_not(np.isnan(df.velocity))
        logi = np.logical_and(logi,np.greater(df.timepoint,2))
        res = least_squares_fitting(velocityFit,df.t[logi],df.velocity[logi],[130,110,50])
        params_velocity = res.x
        
        value_dict['accumulation_end_fit'].append(params_accum[0])
        value_dict['accumulation_timescale'].append(params_accum[1])
        value_dict['velocity_decay_timescale'].append(params_velocity[2])
        value_dict['v_s_fit'].append(params_velocity[0]+params_velocity[1])
        value_dict['shrinking_speed_steady_state'].append(params_velocity[1])
    

    results = DataFrame.from_dict(value_dict)
    results.to_csv(f'experimental_data/{f}_bootstrap_fits.csv')
    

    
