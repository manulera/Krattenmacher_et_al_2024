"""Contains the values that are selected as best fit to the data"""

import pandas

omega_single_model1 = 0.95
omega_single_model2 = 0.9

cooperativity_single_model1 = 1
cooperativity_single_model2 = 3

parameters_1nM = pandas.read_csv('parameter_scan3/runs_1nM/parameters_table.txt', delimiter=',')
parameters_6nM = pandas.read_csv('parameter_scan3/runs_6nM/parameters_table.txt', delimiter=',')


folder_dynamics_1nM_model1 = parameters_1nM.loc[(parameters_1nM.cooperativity == cooperativity_single_model1) &
                                     (parameters_1nM.cooperativity_mode == 'protofilament') &
                                     (parameters_1nM.omega == omega_single_model1), ['run_folder']].iloc[0, 0]


folder_dynamics_6nM_model1 = parameters_6nM.loc[(parameters_6nM.cooperativity == cooperativity_single_model1) &
                                     (parameters_6nM.cooperativity_mode == 'protofilament') &
                                     (parameters_6nM.omega == omega_single_model1), ['run_folder']].iloc[0, 0]

folder_dynamics_1nM_model2 = parameters_1nM.loc[(parameters_1nM.cooperativity == cooperativity_single_model2) &
                                     (parameters_1nM.cooperativity_mode == 'protofilament') &
                                     (parameters_1nM.omega == omega_single_model2), ['run_folder']].iloc[0, 0]


folder_dynamics_6nM_model2 = parameters_6nM.loc[(parameters_6nM.cooperativity == cooperativity_single_model2) &
                                     (parameters_6nM.cooperativity_mode == 'protofilament') &
                                     (parameters_6nM.omega == omega_single_model2), ['run_folder']].iloc[0, 0]

folder_dynamics_1nM_model2 = 'parameter_scan3/' + folder_dynamics_1nM_model2
folder_dynamics_6nM_model2 = 'parameter_scan3/' + folder_dynamics_6nM_model2
folder_dynamics_1nM_model1 = 'parameter_scan3/' + folder_dynamics_1nM_model1
folder_dynamics_6nM_model1 = 'parameter_scan3/' + folder_dynamics_6nM_model1
