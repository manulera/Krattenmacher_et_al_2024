import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.dirname(os.path.abspath(''))))

from simulation import Parameters
from equations import solveDiscrete
from scipy.integrate import odeint
from scipy.optimize import curve_fit
import os

# Density on single mt:
plt.figure(figsize=(10,10))

for filename in os.listdir('./config/'):
    p = Parameters()
    p.read('./config/' + filename)
    t = np.linspace(0,30,100)
    solution = solveDiscrete(p,t,400)
    accumulation = np.sum(solution-p.alpha,axis=1)
    speed =p.v_s * (1-solution[:,0]*p.omega)
    # plt.plot(t, accumulation, label=str(p.alpha) + '' + str(p.omega))
    # plt.plot(np.arange(0,400*0.008,0.008), (solution[-1,:].T - p.alpha), label=str(p.alpha) + ' ' + str(p.omega))
    plt.plot(t,speed, label=str(p.alpha) + '' + str(p.omega))
    

# plt.ylabel("Accumulated molecules")
plt.xlabel("Time (s)")
plt.ylabel("Depolymerization speed (um/s)")
# plt.ylabel("Accumulated molecules")
# plt.xlabel("Coverage (s)")
# plt.xlabel("Distance from tip (um)")

legend = plt.legend(loc='upper right', shadow=False, fontsize='x-large')
plt.show()
