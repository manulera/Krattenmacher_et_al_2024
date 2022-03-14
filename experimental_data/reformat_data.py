# %%
import numpy as np
import os
from pandas import DataFrame

# %% Read the data

for f in ["single","AP"]:
    outdict = dict()
    for dir in os.listdir('.'):
        if not os.path.isdir('./'+dir) or not dir.startswith('time_'):
            continue
        
        key = dir[8:]
        data = np.genfromtxt(f'./{dir}/{f}.csv',delimiter=',',skip_header=1)
        outdict[key] = data[:,1]
        
    # These are always the same, so we take from the last one
    outdict['t'] = data[:,0]
    outdict['event'] = data[:,2]
    outdict['trace'] = np.empty_like(outdict['event'])
    outdict['trace_count'] = np.empty_like(outdict['event'])
    outdict['timepoint'] = np.empty_like(outdict['event'])

    indexes_start = list(np.where(outdict['t'] == 0)[0])
    indexes_start.append(data.shape[0])
    event_count = 0
    current_event = 1
    for j in range(len(indexes_start)-1):
        
        start = indexes_start[j]
        end = indexes_start[j+1]
        outdict['trace'][start:end] = j
        if current_event == outdict['event'][start]:
            event_count+=1
        else:
            current_event = outdict['event'][start]
            event_count = 1
        outdict['trace_count'][start:end] = event_count
        outdict['timepoint'][start:end] = range(end-start)

    df = DataFrame.from_dict(outdict)
    print(df)
    df.to_csv('./data_'+f+'.csv')

