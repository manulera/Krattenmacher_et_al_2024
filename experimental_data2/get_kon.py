import pandas

# This is experimentally measured
koff = 0.016
data = pandas.read_csv('equilibrium_densities.tsv', sep='\t', na_filter=False)


def get_kon(row):
    probability_bound = row['equilibrium_density'] * 8 / row['protofilaments']
    return koff / (1. / probability_bound - 1.)


def get_alpha(row):
    return row['equilibrium_density'] * 8 / row['protofilaments']


data['kon'] = data.apply(get_kon, axis=1)
data['alpha'] = data.apply(get_alpha, axis=1)
data.to_csv('equilibrium_densities.tsv', sep='\t', index=False, float_format='%.5f')
