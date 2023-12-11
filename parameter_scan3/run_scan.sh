#!/usr/bin/env bash

# Delete old data if it exists
rm $1/scan/run*/*.txt
rmdir $1/scan/run*
rm $1/scan/.DS_Store
rmdir $1/scan

# Make directory to put the files
mkdir $1/scan

# Create the files for the template
python ./preconfig.py $1/config.txt.tpl $1/scan

# Move the files in to directories and rename them (see the result):
python ./collect.py $1/scan/run%04i/config.txt $1/scan/config????.txt

## Call the python executable in each of the files (jobs is if you want to run in parallel, change N to the number of processes)
# Note that this is the relative path of solve_discrete_equation.py with respect to the scan/run????/ directory
python ./scan.py 'python ../../../../solve_discrete_equation.py' jobs=8 $1/scan/run*
