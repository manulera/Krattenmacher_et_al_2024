from simulation import Parameters
from equations import solveDiscrete
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import curve_fit


def expo(x,r,y0):
    return np.exp(x*r)



p = Parameters()
p.read("config.txt")

def dynamicsODE(P,t,p):
    k0 = p.depol_rate
    kh = p.k_D / 2
    omega = p.omega
    kd = k0 * (1. - P) + k0 * P * (1. - omega)

    return p.alpha*kd - (P-p.alpha)*kh

def solveDynamics(p, t):

    P0 = p.alpha

    return odeint(dynamicsODE, P0, t, args=(p,))


for kon in [0.01]:
    p.kon = kon
    p.derivated()
    t = np.linspace(0,2,1000000)
    solution = solveDiscrete(p,t,400)


    # fit_sol = curve_fit(expo, t, solution[:,0])

    # plt.plot(t,solution[:,0]/solution[0,0])
    # plt.plot(t, 4*(1-np.gradient(solution[:, 0]) / np.gradient(solution[:, 0])[0]))

    plt.figure()
    # plt.plot(t, (speed)/speed[0])
    # grad_speed = np.gradient(speed)
    # plt.plot(t, (grad_speed-grad_speed[0])/grad_speed[0]/3)
    # plt.figure()
    # plt.plot(t,solution[:,0])
    # print(t[0])
    # plt.plot(t,(solution[-1,0]-p.alpha)*(1-np.exp(-0.3*t))+ p.alpha,linestyle='--')
    # plt.plot(t,np.gradient(solution[:,0]))

    plt.plot(t,np.gradient(solution[:,0])/(t[1]-t[0]))
    plt.axhline(p.depol_rate*(1-p.alpha)*p.alpha)


    # plt.plot(t,solveDynamics(p,t),linestyle="--")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (um /s)")

plt.show()


