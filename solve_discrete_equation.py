# !/usr/bin/env python
"""
A script to evolve the discrete system for 25 seconds and record the speed at each time point in a text file.
First argument is the text file with the parameters
"""

import sys, os
import numpy as np
from simulation import Parameters
from equations import solveDiscrete


def main(parameter_file):
    print("running in " + os.getcwd())
    p = Parameters()
    p.read(parameter_file)
    t = np.linspace(0, 25, 100)
    solution = solveDiscrete(p, t, 400)
    speed = p.omega * (1 - solution[:, 0] * p.omega) * p.a
    np.savetxt("speed.txt",speed,delimiter=",")

# ------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        main(['.'])
    else:
        main(sys.argv[1])