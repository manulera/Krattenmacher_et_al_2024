# %%
import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
import seaborn as sns
# %% Extra functions

cmap = sns.color_palette("rocket", as_cmap=True)

def getColorFromId(id,N):
    # if id == 1:
    #     return 'red'
    # else:
    #     return 'blue'
    return cmap((id-1)/N)

def aveline(x_in,y_in,bins):
    interv = bins[1]-bins[0]
    x_out = list()
    y_out = list()
    for i in bins[1:]:
        log = np.less_equal(x_in,i)
        y_out.append(np.nanmean(y_in[log]))
        x_out.append(i-interv/2)
        x_in = x_in[np.logical_not(log)]
        y_in = y_in[np.logical_not(log)]

    return x_out,y_out


def accumulationFit(t,P,T):
    return  P * (1 - np.exp(-t / T))

def velocityFit(t,P0,Pend,T):
    return  P0 * np.exp(-t / T) + Pend

# %% Load the data
# Single or AP

for which_folder in ['AP','single']:

    df = read_csv(f'./data_{which_folder}.csv')
    fits = read_csv(f'./{which_folder}_fits.csv')

    # %% Colouring by event

    plt.figure(figsize=[4,4])
    N = np.max(df.event)-1
    for trace in np.unique(df['trace']):
        logi = df['trace']==trace
        this_df = df[logi]
        plt.plot(this_df.t,this_df.number_of_Ase1_norm,c=getColorFromId(this_df.event.iat[0],N))

    # Binned data
    xx,yy=aveline(df.t,df.number_of_Ase1_norm,range(0,60,5))
    plt.scatter(xx,yy,c='black',zorder=1000,label='binned')

    # Fits
    t = np.linspace(0,50)
    P = float(fits.accumulation_norm_end_fit)
    T = float(fits.accumulation_norm_timescale)
    y_fit = accumulationFit(t,P,T)

    plt.plot(t,y_fit,c='black',lw=3,label='fit')


    plt.ylabel("number of Ase1 norm")
    plt.xlabel("time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'./{which_folder}_accumulation_norm.svg')

    plt.figure(figsize=[4,4])
    N = np.max(df.event)-1
    for trace in np.unique(df['trace']):
        logi = df['trace']==trace
        this_df = df[logi]
        plt.plot(this_df.t,this_df.number_of_Ase1,c=getColorFromId(this_df.event.iat[0],N))

    # Binned data
    xx,yy=aveline(df.t,df.number_of_Ase1,range(0,60,5))
    plt.scatter(xx,yy,c='black',zorder=1000,label='binned')

    # Fits
    t = np.linspace(0,50)
    P = float(fits.accumulation_end_fit)
    T = float(fits.accumulation_timescale)
    y_fit = accumulationFit(t,P,T)
    plt.plot(t,y_fit,c='black',lw=3,label='fit')

    plt.ylabel("Ase1 accumulation")
    plt.xlabel("Time (s)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'./{which_folder}_accumulation.svg')

    plt.figure(figsize=[4,4])
    N = np.max(df.event)-1
    timepoint_cut = 2
    for trace in np.unique(df['trace']):
        logi = np.logical_and(df['trace']==trace,df['timepoint']>timepoint_cut)
        if not np.any(logi):
            continue
        this_df = df[logi]
        plt.plot(this_df.t,this_df.velocity/1000.,c=getColorFromId(this_df.event.iat[0],N))
    logi = df['timepoint']>timepoint_cut
    xx,yy=aveline(df.t[logi],df.velocity[logi],range(0,60,5))
    plt.scatter(xx,np.array(yy)/1000.,c='black',zorder=1000,label='binned')
    print(np.min(df.t[logi]))
    # Fits
    t = np.linspace(7.5,50)
    T = float(fits.velocity_decay_timescale)
    v_s_fit = float(fits.v_s_fit)
    shrinking_speed_steady_state = float(fits.shrinking_speed_steady_state)
    print(v_s_fit,shrinking_speed_steady_state,T)
    y_fit = velocityFit(t,v_s_fit,shrinking_speed_steady_state,T)
    plt.plot(t,y_fit/1000.,c='black',lw=3,label='fit')

    plt.ylabel("Velocity (\u03BCm/s)")
    plt.xlabel("Time (s)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'./{which_folder}_speed.svg')





plt.show()
