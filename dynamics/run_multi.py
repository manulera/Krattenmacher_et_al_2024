import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.dirname(os.path.abspath(''))))

from simulation import Parameters
from equations import solveDiscrete, decayLengthPhysical, get_v

import os
def run_multiple():
    # Density on single mt:
    dat = []
    mt_length = 500
    x = np.arange(0,mt_length*0.008,0.008)
    t = np.linspace(0,100,100)

    beta_start = 0.5
    beta_step = 0.1

    colorcoded = 'delta'
    colorcodedlabel = 'delta'
    norm = matplotlib.colors.Normalize(vmin=0, vmax=0.25)

    p = Parameters()
    counter = 1
    for filename in os.listdir('./config/'):
        for var in [0, 0.05, 0.1, 0.15, 2]:
            # p.read('./config/' + os.listdir('./config/')[5])
            p.read('./config/' + filename)
            p.beta = [0,0]#np.arange(beta_start,0,-beta_step)
            p.P_lose = 0.5
            p.omega = 0
            p.gamma = var
            p.delta = var
            solution = solveDiscrete(p,t,mt_length)
            velocities = np.apply_along_axis(get_v, 1, solution, p)
            v = velocities[:,0]
            accumulation = np.sum(solution-p.alpha,axis=1)
            y = solution[-1]-p.alpha
            y = y/y[0]
            d = decayLengthPhysical(p, v[-1])
            ye = np.exp(-x/d)
            a = 1 - accumulation/accumulation[-1]
            belowe = np.where(a < 0.367879441)[0]
            t_const = t[belowe[0]] if belowe.size>0 else np.NaN
            print(counter, 'diff:', p.D, ' off from steady state:', (accumulation[-1]-accumulation[-2])/accumulation[-1], 
                'error in decay length:', np.max(y-ye))
            dat.append({'alpha':p.alpha, 'beta_start':beta_start, 'beta_step':beta_step, 'omega':p.omega, 'D':p.D, 'koff':p.koff, 'decay_length':d, 't_const':t_const, 'gamma': p.gamma, 'delta':p.delta,
                        'v':v, 'v_shift':velocities[:,1], 'v_lose':velocities[:,2], 'p':p, 'accumulation':accumulation, 'solution':solution, 
                        'string':str(counter) + " D=" + str(p.D) + "  alpha=" + str(p.alpha) + "  " + colorcoded + "=" + str(var)})
            counter += 1
    return dat, norm, colorcoded, colorcodedlabel