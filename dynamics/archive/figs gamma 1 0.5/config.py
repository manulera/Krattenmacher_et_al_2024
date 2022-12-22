import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.dirname(os.path.abspath(''))))

from simulation import Parameters
from equations import solveDiscrete, decayLengthPhysical, get_kd, get_v
from scipy.integrate import odeint
from scipy.optimize import curve_fit
import os
import plotly.express as px

# Density on single mt:
dat = []
mt_length = 500
x = np.arange(0,mt_length*0.008,0.008)
t = np.linspace(0,100,100)

beta = np.arange(0.8,0,-0.1)

p = Parameters()
counter = 1
for filename in os.listdir('./config/'):
    for gamma in [1, 0.5]:
        # p.read('./config/' + os.listdir('./config/')[5])
        p.read('./config/' + filename)
        p.beta = beta
        p.P_lose = 0.1
        p.omega = 0.1
        p.gamma = gamma
        p.delta = gamma
        solution = solveDiscrete(p,t,mt_length)
        velocities = np.apply_along_axis(get_v, 1, solution, p)
        v = velocities[:,0]
        accumulation = np.sum(solution-p.alpha,axis=1)
        y = solution[-1]-p.alpha
        y = y/y[0]
        d = decayLengthPhysical(p, v[-1])
        ye = np.exp(-x/d)
        a = 1 - accumulation/accumulation[-1]
        t_const = t[np.where(a < 0.367879441)[0][0]]
        print(counter, 'diff:', p.D, ' off from steady state:', (accumulation[-1]-accumulation[-2])/accumulation[-1], 
              'error in decay length:', np.max(y-ye))
        dat.append({'alpha':p.alpha, 'beta':p.beta, 'omega':p.omega, 'D':p.D, 'koff':p.koff, 'decay_length':d, 't_const':t_const, 'gamma': p.gamma, 'delta':p.delta,
                    'v':v, 'v_shift':velocities[:,1], 'v_lose':velocities[:,2], 'p':p, 'accumulation':accumulation, 'solution':solution})
        counter += 1

colorcoded = 'gamma'