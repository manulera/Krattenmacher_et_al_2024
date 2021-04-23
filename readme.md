# Krattenmacher et al. 2021

## Running the python code

### Setting up the python environment

To reproduce the simulations, analysis and plots used in the paper, you need to have `pipenv` installed to manage the python dependencies. See the [documentation](https://pypi.org/project/pipenv/) to install it, but essentially you can do:

```
pip install pipenv
```

Once you have `pipenv` installed, you can install the project dependencies by going to the project folder (where `Pipfile.lock` file is) and running:

```
pipenv install
```

Then, to run any of the scripts you can activate a shell with the python environment you just created by calling:

```
pipenv shell
```

The installed packages are `numpy`, `scipy`, `matplotlib`.

To create the configuration files for the simulation, you will also need the python script `preconfig`, that you can download:

```
git clone https://github.com/nedelec/preconfig
```

Then copy the file `preconfig` to the main folder, in bash:

```
cp preconfig/preconfig ./preconfig.py
```
You should be ready to run all the scripts now

### Reproducing the simulations

Each set of simulations is described by a file called `config.txt.tpl`, which contains the parameters of all the simulations that will be run in that folder. To understand how each individual configuration file is produced from this, see [preconfig documentation](https://github.com/nedelec/preconfig).

