# A script to verify that the solutions coming from the numerical and the ODE evolution match

from equations import solveDiscrete,decayLength,numerical_prediction
from simulation import Parameters
import numpy as np
from matplotlib import pyplot as plt

for config in ["config_accum.txt","config_half.txt"]:
    p = Parameters()
    p.read(config)
    t = np.linspace(0, 300)
    ode_sol = solveDiscrete(p, t, 300)

    kd_sol, P0_sol = numerical_prediction(p)
    decay = decayLength(p,kd_sol)

    x = np.linspace(0,300)
    P = p.alpha + (P0_sol-p.alpha) * np.exp(-x/decay)
    print(P0_sol,ode_sol[-1,0])

    plt.figure()
    plt.plot(ode_sol[-1,:])
    plt.plot(x,P)

plt.show()
