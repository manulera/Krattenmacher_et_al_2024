# %%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from pandas import read_csv

# %% Extra functions

cmap = get_cmap('Spectral')

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
which_folder = 'single'
df = read_csv(f'experimental_data/data_{which_folder}.csv')
fits = read_csv(f'experimental_data/{which_folder}_fits.csv')

# %% Some plots showing that the first or second does not really matter

plt.figure()
max_trace_count = np.max(df.trace_count)-1
for trace in np.unique(df['trace']):
    logi = df['trace']==trace
    this_df = df[logi]
    plt.plot(this_df.t,this_df.number_of_Ase1,c=getColorFromId(this_df.trace_count.iat[0],max_trace_count))

plt.ylabel("number of Ase1")
plt.xlabel("time")


# %% Colouring by event
plt.figure()
N = np.max(df.event)-1
for trace in np.unique(df['trace']):
    logi = df['trace']==trace
    this_df = df[logi]
    plt.plot(this_df.t,this_df.number_of_Ase1,c=getColorFromId(this_df.event.iat[0],N))

# Binned data
xx,yy=aveline(df.t,df.number_of_Ase1,range(0,60,5))
plt.scatter(xx,yy,c='black',zorder=1000)
plt.ylabel("number of Ase1")
plt.xlabel("time")

plt.figure()
N = np.max(df.event)-1
for trace in np.unique(df['trace']):
    logi = df['trace']==trace
    this_df = df[logi]
    plt.plot(this_df.t,this_df.number_of_Ase1_norm,c=getColorFromId(this_df.event.iat[0],N))

# Binned data
xx,yy=aveline(df.t,df.number_of_Ase1_norm,range(0,60,5))
plt.scatter(xx,yy,c='black',zorder=1000)

# Fits
t = np.linspace(0,200)
P = float(fits.accumulation_norm_end_fit)
T = float(fits.accumulation_norm_timescale)
y_fit = accumulationFit(t,P,T)

plt.plot(t,y_fit,c='black',lw=3)


plt.ylabel("number of Ase1 norm")
plt.xlabel("time")

#%%
plt.figure()
N = np.max(df.event)-1
timepoint_cut = 2
for trace in np.unique(df['trace']):
    logi = np.logical_and(df['trace']==trace,df['timepoint']>timepoint_cut)
    if not np.any(logi):
        continue
    this_df = df[logi]
    plt.plot(this_df.t,this_df.velocity,c=getColorFromId(this_df.event.iat[0],N))
logi = df['timepoint']>timepoint_cut
xx,yy=aveline(df.t[logi],df.velocity[logi],range(0,60,5))
plt.scatter(xx,yy,c='black',zorder=1000)
print(np.min(df.t[logi]))
# Fits
t = np.linspace(7.5,200)
T = float(fits.velocity_T)
v_s_fit = float(fits.v_s_fit)
shrinking_speed_steady_state = float(fits.shrinking_speed_steady_state)
print(v_s_fit,shrinking_speed_steady_state,T)
y_fit = velocityFit(t,v_s_fit,shrinking_speed_steady_state,T)
y_fit2 = velocityFit(t,130,110,15)
plt.plot(t,y_fit,c='black',lw=3)
plt.plot(t,y_fit2,c='gray',lw=3)

plt.ylabel("Velocity")
plt.xlabel("time")



# %% Plot median speed with the median intensity

plt.figure()

N = np.max(df.event)-1
for trace in np.unique(df['trace']):
    logi = df['trace']==trace
    this_df = df[logi]
    x = np.nanmean(this_df.number_of_Ase1)
    y = np.nanmean(this_df.velocity)
    plt.scatter(x,y)



# %% Plot median speed with duration (discard that longer ones make the speed lower)

plt.figure()

N = np.max(df.event)-1
for trace in np.unique(df['trace']):
    logi = df['trace']==trace
    this_df = df[logi]
    x = this_df.shape[0]
    y = np.nanmean(this_df.velocity)
    plt.scatter(x,y)
plt.xlim(xmin=0)
plt.ylim(ymin=0)


# %% Plot the tau
plt.figure()
N = np.max(df.event)-1
for trace in np.unique(df['trace']):
    logi = df['trace']==trace
    this_df = df[logi]
    plt.plot(this_df.t,this_df.tau,c=getColorFromId(this_df.event.iat[0],N))

xx,yy=aveline(df.t,df.tau,range(0,60,5))
plt.scatter(xx,yy,c='black',zorder=1000)

plt.ylabel("tau")
plt.xlabel("time")

plt.show()
