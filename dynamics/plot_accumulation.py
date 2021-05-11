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

def dynamicsODE(N,t,p):
    k0 = p.depol_rate
    kh = p.k_D / 2
    omega = p.omega


    return p.alpha*k0 - N*(p.kon+p.koff)

def solveDynamics(p, t):



    return odeint(dynamicsODE, 0, t, args=(p,))

plt.figure()
for kon in [0.01,0.02,0.04,0.08]:
    p.kon = kon
    p.D = 0.01
    p.derivated()
    t = np.linspace(0,20,100)
    solution = solveDiscrete(p,t,400)
    accumulation = np.sum(solution-p.alpha,axis=1)


    plt.plot(t, accumulation/accumulation[-1])
    # plt.plot(t, solution[:,0] / solution[-1,0])

    def fun2fit(t,p):
        return accumulation[-1] * (1 - np.exp(p * t))

    pars=curve_fit(fun2fit, t, accumulation, 0.3)
    print(pars)
    plt.plot(t, fun2fit(t,pars[0][0]) /accumulation[-1], linestyle='--')
    # plt.plot(t,p.depol_rate*p.alpha*t)
    # grad_speed = np.gradient(speed)
    # plt.plot(t, (grad_speed-grad_speed[0])/grad_speed[0]/3)
    # plt.figure()
    # plt.plot(t,solution[:,0])
    # print(t[0])
    #
    # plt.plot(t,np.gradient(solution[:,0]))



    sol=solveDynamics(p,t)
    # plt.plot(t,sol,linestyle="--")
    plt.xlabel("Time (s)")
    plt.ylabel("Accumulated molecules")

plt.show()


