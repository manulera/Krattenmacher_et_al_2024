

from equations import solveDiscrete,decayLength,numerical_prediction
from simulation import Parameters
import numpy as np
from matplotlib import pyplot as plt

for config in ["config_accum.txt"]:
    p = Parameters()
    p.read(config)

    plt.figure()
    p0_model = list()
    D_all=np.linspace(0,0.1)
    for D in D_all:
        p.D = D
        p.derivated()
        kd_sol, P0_sol = numerical_prediction(p)
        # t = np.linspace(0, 300)
        # ode_sol = solveDiscrete(p, t, 300)
        plt.scatter(D,P0_sol)
        # plt.scatter(D, ode_sol[-1,0],marker='d')

        p0_model.append((p.depol_rate)/(p.k_D+p.depol_rate))
    plt.plot(D_all,p0_model)

plt.show()
