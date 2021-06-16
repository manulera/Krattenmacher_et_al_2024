# Scanning parameters and running simulations

Have a look at the bash script `run_scan.sh`.

The script will generate multiple parameter files, put them in directories, and run
the script `solve_discrete_equation.py` in each of them.

I included two python files that we typically use for this (`collect.py` and `scan.py`). I would not recommend going
through the code, but I think the calls in `run_scan.sh` are self-explaining.

Finally, before running simulations again, always delete the `scan` directory.