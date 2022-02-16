#%%
import numpy as np
from pandas import read_csv, DataFrame
from scipy.optimize import minimize


def accumulationFit(t,P,T):
    return  P * (1 - np.exp(-t / T))

def velocityFit(t,P0,Pend,T):
    return  P0 * np.exp(-t / T) + Pend
    
def least_squares_fitting(f,x,y,sugg):

    def weightFun(args):
        return np.sum(np.square(f(x,*args) - y))
    
    return minimize(weightFun,sugg)


for f in ['single','AP']:
    df = read_csv(f'experimental_data/data_{f}.csv')

    # Fit the timescale to the normalised data
    logi = np.logical_not(np.isnan(df.number_of_Ase1_norm))
    res = least_squares_fitting(accumulationFit,df.t[logi],df.number_of_Ase1_norm[logi],[700,20])
    params_accum_norm = res.x
    
    # Fit the timescale to the non-normalised data
    logi = np.logical_not(np.isnan(df.number_of_Ase1))
    res = least_squares_fitting(accumulationFit,df.t[logi],df.number_of_Ase1[logi],[70,20])
    params_accum = res.x
    
    # Fit the timescale to the velocity data (we exclude the first timepoints)
    logi = np.logical_not(np.isnan(df.velocity))
    logi = np.logical_and(logi,np.greater(df.timepoint,2))
    res = least_squares_fitting(velocityFit,df.t[logi],df.velocity[logi],[130,110,50])
    params_velocity = res.x
    
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

    
