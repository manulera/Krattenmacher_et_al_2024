import pandas
import numpy as np
from fit_experimental_data import get_fits

data = pandas.read_csv('processed_data/experimental_data.csv')
repetitions = 1000

output_data_list = list()

for condition in pandas.unique(data.condition):
    data_condition = data[data.condition == condition]
    unique_ids = pandas.unique(data_condition.event_id)
    nb_events = unique_ids.shape[0]

    for i in range(repetitions):
        picked_ids = np.random.choice(unique_ids, nb_events)
        logi = data_condition.event_id.isin(picked_ids)
        this_dict = get_fits(data_condition[logi], condition)
        this_dict['picked_ids'] = ','.join(picked_ids)
        output_data_list.append(this_dict)

    out_data = pandas.DataFrame(output_data_list)
    out_data.to_csv('processed_data/bootstrap_fits.csv', float_format='%.3E', index=False)
