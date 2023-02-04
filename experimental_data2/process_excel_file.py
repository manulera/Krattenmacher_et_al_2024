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

data.rename(columns={
    'event id': 'event_id',
    'MT id': 'mt_id',
    'time (s)': 'time',
    'velocity (nm/s)': 'velocity',
    'equilibrium density (1/nm)': 'equilibrium_density',
    'number of Ase1 molecules at tip fitted with gaussian (1)': 'number_of_ase1_gauss',
    'number of Ase1 molecules at tip fitted with exponential (1)': 'number_of_ase1_exp',
    'lengthscale of exponential decay (nm)': 'decay_lengthscale',
    'condition': 'condition',
}

)

data.to_csv('experimental_data.csv', index=False)
