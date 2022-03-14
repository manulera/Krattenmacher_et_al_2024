# Krattenmacher et al. 2022

## Setting up the python environment

To reproduce the simulations, analysis and plots used in the paper, you need to have `pipenv` installed to manage the python dependencies. See the [documentation](https://pypi.org/project/pipenv/) to install it, but essentially you can do:

```
pip install pipenv
```

Once you have `pipenv` installed, you can install the project dependencies by going to the project folder (where `Pipfile.lock` file is) and running:

```
pipenv install
```

For this to work, you either need to have python 3.9 installed in your computer, or have a python environment manager that can download the version specified in the `Pipfile` file. I normally use `pyenv` ([link](https://github.com/pyenv/pyenv#installation)).

Then, to run any of the scripts you can activate a shell with the python environment you just created by calling:

```
pipenv shell
```

To create the configuration files for the simulation, you will also need the python script `preconfig`, that is already included with minor changes. The repository can be found [here](https://github.com/nedelec/preconfig).

## Analysing experimental data

To reproduce the analysis, move to `experimental_data`.

1. The raw data is the folders `time_*` (received from collaborators). By running `reformat_data.py`, you collect all the data and put it in the files `data_AP.csv` and `data_single.csv`, corresponding to antiparallel and single microtubules.
2. To fit the experimental data to the equations mentioned in the main text, call `fit_experimental_data.py`. This will generate `AP_fits.csv` and `single_fits.csv`.
3. You can also call `experimental_data_bootstrap.py` and `plot_bootstrap_data.py` for a bootstrap analysis.
4. You can plot the experimental data calling `plot_experimental_data.py` (this uses the fitted data to plot).

## Solving the equations of the different models

The script that evolves the discrete equation is `solve_discrete_equation.py`. See the script, as well as the python file `equations.py`. Note the function `scaleVelocity`, which is used to calculate the shrinkage speed depending on the model.

To reproduce the analysis, move to `parameter_scan`.

1. Each folder named `runs_*` before running the scripts only contains one file `config.txt.tpl`: a template configuration file that contains a set of parameters to be scanned. See `preconfig`, mentioned above. You can read the `config.txt.tpl` file, variables are self-explaining. The folders that were used for the paper:
    * `runs_coop?`: Model 1 and Model 2
    * `runs_special_coop?`: Model 3
2. See the bash script `run_scan.sh` which:
    * Can be run calling `run_scan.sh runs_coop1` (or whatever). Does not take multiple arguments.
    * Removes the old solutions, if they exist.
    * Generates new configuration files with all combinations of parameters, and puts them in folders named `scan/run????`.
    * Runs `solve_discrete_equation.py` in each of those folders.
3. See the bash script `run_analysis.sh` which:
    * Calls `analyse_results` in each folder `scan/run????`.
    * Collects the results and parameters of simulations in `other_values.txt` and `parameters_table.txt`.
4. To reproduce the figures of the paper, call `figure_francois.py`. There are other graphs to be plotted, see the other python scripts.

Finally, once you have ran `run_scan.sh` in all folders, to reproduce the kymograph and supplementary figure, go to the main folder and run `draw_kymograph.py`.

## Simulation

There is a 1-D simulation (see `sim.py`) to show that the mean field approach is valid. In other words, that the discrete equation reproduces the simulation results. In the end we did not use it in the paper, but it is well documented in the file and here we provide a brief description.

## Simulation Program

The program is in the file `simulation.py`. It contains the code that can be imported into other python scripts to run the simulation in them.

It contains three things:

### timeToNextEvent

This is just a function to calculate a stochastic time until the next event using Gillespie algorithm. If a process has a certain rate, we can sample the probability distribution of time until that event with random numbers, using `log(r)/rate`, where `r` is a random number, and `rate` is the rate of the process. If many objects have the same rate, then we multiply the rate by the number of objects, to get the time where a random one of them will undergo the event.

### Parameters

This is a python class used to store the parameters of the simulation and the initial conditions. It has several fields. All units expressed in um and s, see the file for what they are.

### Simulation

The simulation class.

### The simulation algorithm

> **_NOTE:_** Some of the variable/method names mentioned here might have changed, but the essence of the simulation is the same.

You can have a look at the code in `simulation.py`, in the class `Simulation`.
Essentially works like this:

When you call the method `sim.run(p,t_max,t_snap)` -method is a "class function"-, the program iteratively calls the method `nextEvent`, which calculates the next event that will happen, and when, it does the following:

1. Calculates the rates of binding (`empty_sites*p.kon`), unbinding (`bound_ase1 * p.koff`), diffusion (`bound_ase1 * p.k_D`), and depolymerization (`p.depol_rate`).
2. From the rates it calculates the time to the next event of each kind, using the function `timeToNextEvent`, described above.
3. The smallest time is the event that will happen next, then a function is called that executes the event.

The events:

1. Unbinding: One of the mt_array sites that was `True` is made `False` at random.
2. Binding: One of the mt_array sites that was `False` is made `True` at random.
3. Diffusion: One of the mt_array sites that is `True` is chosen at random. Then we chose a direction at random (step towards plus end or minus end), and then check if the position we try to move is open. If the site is empty, we move Ase1 to that position. If the site is occupied, the event does not happen. If the site is outside the microtubule (either at the minus or plus end), the event does not happen.
4. Depolimerization: If there is no Ase1 in the last position `self.mt_array[-1]==0`, the last position of `mt_array` is removed. If Ase1 is there, we test a random number against the probability `p.P_no_depol>random.random()`. If this is `True`, then no event happens. Otherwise, the last position of `mt_array` is removed. If it is false, no event happens.

In the cases where events do not happen, the function returns 0, and not the time calculated, since the event did not happen. 

This function is called recursively until the simulation time is bigger than `t_max`. Also, every `t_snap` seconds, a snapshot of the simulation is added to a list, that is then the output of `Simulation.run`.


