import pandas

isolated_6nm = pandas.read_excel('Data Figure 3D 3E S3A S3B S4D.xlsx', sheet_name='isolated 6nM')
isolated_1nm = pandas.read_excel('Data Figure 3D 3E S3A S3B S4D.xlsx', sheet_name='isolated 1nM')
antiparallel = pandas.read_excel('Data Figure 3D 3E S3A S3B S4D.xlsx', sheet_name='antiparallel')
parallel = pandas.read_excel('Data Figure 3D 3E S3A S3B S4D.xlsx', sheet_name='parallel')

# Remove 1nM outliers
isolated_1nm = isolated_1nm[~isolated_1nm['experiment id'].isin([20, 21])].copy()
isolated_1nm.drop(columns='experiment id', inplace=True)

isolated_1nm['condition'] = '1nM'
isolated_6nm['condition'] = '6nM'
antiparallel['condition'] = 'antiparallel'
parallel['condition'] = 'parallel'

data = pandas.concat([isolated_1nm, isolated_6nm, antiparallel, parallel])

data.loc[:, 'event id'] = data.apply(lambda r: r['condition'] + '_' + str(r['event id']), axis=1)

data.rename(inplace=True, columns={
    'event id': 'event_id',
    'MT id': 'mt_id',
    'time (s)': 'time',
    'velocity (nm/s)': 'velocity',
    'equilibrium density (1/nm)': 'equilibrium_density',
    'number of Ase1 molecules at tip fitted with gaussian (1)': 'number_of_ase1_gauss',
    'number of Ase1 molecules at tip fitted with exponential (1)': 'number_of_ase1_exp',
    'lengthscale of exponential decay (nm)': 'decay_lengthscale',
    'condition': 'condition',
})

# Scale the Ase1 signal with new calibration
data['equilibrium_density'] = data['equilibrium_density'] * 2.74
data['number_of_ase1_gauss'] = data['number_of_ase1_gauss'] * 2.74
data['number_of_ase1_exp'] = data['number_of_ase1_exp'] * 2.74

# We add extra columns with integers to indicate the timepoint per event
# and the nb of event within the condition.

timepoint = 0
event_nb = 0

data['timepoint'] = 0
data['event_nb'] = 0

for condition in pandas.unique(data.condition):
    logi = data.condition == condition
    for i, event_id in enumerate(pandas.unique(data[logi].event_id)):
        logi2 = data.event_id == event_id
        data.loc[logi & logi2, 'event_nb'] = i

for event_id in pandas.unique(data.event_id):
    logi = data.event_id == event_id
    data.loc[logi, 'timepoint'] = list(range(sum(logi)))

data.to_csv('processed_data/experimental_data.csv', index=False)
