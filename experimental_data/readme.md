## Preparing experimental data

The data from experiments is in the file `Data Figure 3D 3E S3A S3B S4D.xlsx`. To analyse the data:

```bash
# Reformat the data from spreadsheet, applies a 2.47x correction to the Ase1 density / accumulation
# Creates processed_data/experimental_data.csv
python process_excel_file.py

# Fit experimental data (see below)
# Creates processed_data/fits.csv
# Creates processed_data/individual_fits.csv (unused)
python fit_experimental_data.py

# Do bootstrap on the data to have confidence intervals for fitting parameters (1000 repetitions, sample with replacement of N, where N is the number of events per condition)
# Creates processed_data/bootstrap_fits.csv
python do_bootstrap.py

# Summarise and plot bootstrap data:
# Creates processed_data/bootstrap_confidence_intervals.csv
python plot_bootsrap.py

# Plot the data and fits (to see how they look)
python plot_experimental_data.py

# Calculate the kon of Ase1 in different conditions, assuming different number of protofilaments
# The values on equilibrium_densities.tsv equilibrium_density column come from the experimental data
# in ase1_densities.xlsx
# Runs on the file equilibrium_densities.tsv and updates it.
python get_kon.py
```

### Fits:

The following fitted parameters are used to fit with the model:

* accumulation_end_fit: `P` in a fit to `P * (1 - np.exp(-t / T))` of `number_of_ase1_exp` vs. time.
* accumulation_timescale: `T` in a fit to `P * (1 - np.exp(-t / T))` of `number_of_ase1_exp` vs. time.
* shrinking_speed_steady_state: mean of the shrinking speed after twenty seconds of shrinkage.
* The confidence intervals come from bootstrapping the data and are summarised in `processed_data/bootstrap_fits.csv`

