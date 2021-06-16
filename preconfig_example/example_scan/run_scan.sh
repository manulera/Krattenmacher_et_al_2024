#!/usr/bin/env bash

# Make directory to put the files
mkdir scan

# Create the files for the template
python ../preconfig.py single_mt.txt.tpl scan

# Move the files in to directories and rename them (see the result):
python ../collect.py ./scan/run%04i/single_mt.txt ./scan/single_mt????.txt

## Call the python executable in each of the files (nproc is if you want to run in parallel, change N to the number of processes)
# Note that this is the relative path of solve_discrete_equation.py with respect to the scan/run????/ directory
python ../scan.py 'python ../../../../solve_discrete_equation.py single_mt.txt' nproc=1 ./scan/run*


