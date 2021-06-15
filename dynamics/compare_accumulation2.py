from simulation import Parameters
from equations import solveDiscrete
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import curve_fit


p = Parameters()
p.read("double_mt.txt")

# Density on single mt:

single_dens = 0.031*8/13
print(single_dens)

plt.figure()


t = np.linspace(0,80,100)
solution = solveDiscrete(p,t,400)
accumulation = np.sum(solution-p.alpha,axis=1)
speed =p.v_s * (1-solution[:,0]*p.omega)

plt.plot(t, accumulation)

print(p.alpha)

# plt.plot(t,sol,linestyle="--")
plt.xlabel("Time (s)")
plt.ylabel("Accumulated molecules")

plt.figure()
plt.plot(t,speed)

plt.show()


