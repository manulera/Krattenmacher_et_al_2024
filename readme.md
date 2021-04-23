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

Then copy the file `preconfig.py` to the main folder, in bash:

```
cp 
```


###