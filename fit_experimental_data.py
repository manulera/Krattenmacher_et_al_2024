#%%
import numpy as np
from pandas import read_csv, DataFrame
from scipy.optimize import minimize, curve_fit


def accumulationFit(t,P,T):
    return  P * (1 - np.exp(-t / T))

def velocityFit(t,P0,Pend,T):
    return  P0 * np.exp(-t / T) + Pend


for f in ['single','AP']:
    df = read_csv(f'experimental_data/data_{f}.csv')

    sugg = {
        'single': [700,20],
        'AP': [200,30]
    }

    # Fit the timescale to the normalised data
    logi = np.logical_not(np.isnan(df.number_of_Ase1_norm))
    params_accum_norm,_ = curve_fit(accumulationFit,df.t[logi],df.number_of_Ase1_norm[logi],sugg[f])
    
    # Fit the timescale to the non-normalised data
    sugg = {
        'single': [70,20],
        'AP': [20,30]
    }
    logi = np.logical_not(np.isnan(df.number_of_Ase1))
    params_accum,_ = curve_fit(accumulationFit,df.t[logi],df.number_of_Ase1[logi],sugg[f])

    
    # Fit the timescale to the velocity data (we exclude the first timepoints)
    sugg = {
        'single': [130,110,50],
        'AP': [200,100,20]
    }
    logi = np.logical_not(np.isnan(df.velocity))
    logi = np.logical_and(logi,np.greater(df.timepoint,2))
    params_velocity,_ = curve_fit(velocityFit,df.t[logi],df.velocity[logi],sugg[f])
    
    # Tau should be approximately 200 nm
    value_dict = {
        'accumulation_norm_end_fit': params_accum_norm[0],
        'accumulation_norm_timescale': params_accum_norm[1],
        'accumulation_end_fit': params_accum[0],
        'accumulation_timescale': params_accum[1],
        'velocity_decay_timescale': params_velocity[2],
        'v_s_fit': params_velocity[0]+params_velocity[1],
        'shrinking_speed_steady_state': params_velocity[1],
        'tau': 0.2
    }

    values = list()
    for key in value_dict:
        values.append('%.3E' % value_dict[key])

    with open(f'experimental_data/{f}_fits.csv','w') as out:
        out.write(",".join(list(value_dict.keys()))+"\n")
        out.write(",".join(values)+"\n")

    
