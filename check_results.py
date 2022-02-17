
import sys, os
import numpy as np
from simulation import Parameters
import matplotlib.pyplot as plt
from analyse_results import timeScaleFitFunction, lengthScaleFitFunction

def main(folder):
    print("running in " + os.getcwd())
    
    # We read the parameters and the solution from the equation
    p = Parameters()
    p.read(os.path.join(folder,"config.txt"))
    solution = np.genfromtxt(os.path.join(folder,"solution.txt"),delimiter=',')
    speed = np.genfromtxt(os.path.join(folder,"speed.txt"),delimiter=',')
    accumulation = np.genfromtxt(os.path.join(folder,"ase1_accumulation.txt"),delimiter=',')

    # We read the single values
    with open(os.path.join(folder,'other_values.txt'),'r') as input:
        keys = input.readline().strip().split(',')
        values = [float(i) for i in input.readline().split(',')]
        value_dict = dict()
        for i in range(len(keys)):
            value_dict[keys[i]] = values[i]
    
    l = np.arange(0,400)
    decay_fit = lengthScaleFitFunction(l,value_dict['P0_end_fit'],value_dict['lengthscale_density_end_fit']) + p.alpha

    t = np.arange(0,200)
    accum_fit = timeScaleFitFunction(t,value_dict['accumulation_end_fit'],value_dict['accumulation_timescale'])

    plt.figure()
    plt.plot(accumulation,label='data')
    plt.plot(t,accum_fit,ls='--',label='fit')
    plt.ylabel("Accumulation (molecules)")
    plt.xlabel("Time (s)")
    
    plt.figure()
    for i in [0,1,3,9,21,48]:
        print(i)
        plt.plot(solution[i,:],label=f'time :{i}s')
    plt.plot(l,decay_fit,ls='--',label='fit')
    plt.ylabel("P(ocupied)")
    plt.xlabel("Lattice index")
    plt.ylim(ymin=0)
    plt.legend()

    plt.figure()
    plt.plot(t,speed)
    plt.scatter(0,)
    plt.ylabel("P(0)")
    plt.xlabel("t(s)")
    plt.show()

    

# ------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        main(["."])
    else:
        main(sys.argv[1])