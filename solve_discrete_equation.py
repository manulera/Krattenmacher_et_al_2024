# !/usr/bin/env python
"""
A script to evolve the discrete system for 50 seconds and record the speed at each time point in a text file.
First argument is the text file with the parameters
"""

import sys, os
import numpy as np
from simulation import Parameters
from equations import solveDiscrete


def main(folder):
    print("running in " + os.getcwd())
    p = Parameters()
    p.read(os.path.join(folder,'config.txt'))
    
    # Here we use a dt of 1./4 seconds
    t = np.linspace(0, 200, 800)
    solution = solveDiscrete(p, t, 400)
    
    # In the solution we export, the dt is 1 second
    solution = solution[::4,:]
    np.savetxt(os.path.join(folder,"solution.txt"),solution,delimiter=",")
    

# ------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        main('.')
    else:
        main(sys.argv[1])