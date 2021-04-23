# !/usr/bin/env python
from simulation import Simulation

import sys

def main(args):
    for arg in args:
        s = Simulation()
        s.run(arg)


# ------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == 'help':
        main(['.'])
    else:
        main(sys.argv[1:])