from simulation import Parameters
from equations import solveDiscrete
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import curve_fit


plt.figure()
p = Parameters()
p.read("config.txt")




t = np.linspace(0,25,100)
solution = solveDiscrete(p,t,400)

speed =p.omega * (1-solution[:,0]*p.omega)*p.a

# fit_sol = curve_fit(expo, t, solution[:,0])

# plt.plot(t,solution[:,0]/solution[0,0])
# plt.plot(t, 4*(1-np.gradient(solution[:, 0]) / np.gradient(solution[:, 0])[0]))

plt.figure()

plt.plot((solution[::10,:].T - p.alpha)/(solution[::10,0]-p.alpha))


plt.show()


