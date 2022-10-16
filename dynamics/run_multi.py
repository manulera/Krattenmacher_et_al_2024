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
    mt_length = 700
    x = np.arange(0,mt_length*0.008,0.008)
    t = np.linspace(0,100,100)

    colorcoded = 'factor_isolated'
    colorcodedlabel = 'koff (isolated)/koff (overlap)'
    norm = matplotlib.colors.Normalize(vmin=0, vmax=130)

    p = Parameters()
    counter = 1
    for filename in os.listdir('./config/'):
        for var in [10, 50, 150]:
            # p.read('./config/' + os.listdir('./config/')[5])
            p.read('./config/' + filename)
            if p.D == 0.093 or p.kon > 0.06:
                continue
            N_shifted = 150
            p.factor_isolated = var
            p.alphas = p.kon / (p.koff * p.factor_isolated + p.kon)
            p.k_Ds = p.k_D * 10
            o = 350
            p.overlap_start = o
            p.beta = np.linspace(0.2, 0, num=N_shifted) if N_shifted > 0 else [0] #
            p.P_lose = 0.2
            # p.omega = 0 using P_lose=1-omega instead (is more intuitive for me)
            solution = solveDiscrete(p,t,mt_length)
            velocities = np.apply_along_axis(get_v, 1, solution[:, o:], p)
            v = velocities[:,0]
            accumulation = np.sum(solution[:, o:]-p.alpha,axis=1)
            onsingle = np.sum(solution[:, :o]-p.alphas,axis=1)
            y = solution[-1]-p.alpha
            y = y[o:]/y[o]
            d = x[np.where(y < 0.367879441)[0][0]]
            ye = np.exp(-x[:-o]/d)
            a = 1 - accumulation/accumulation[-1]
            belowe = np.where(a < 0.367879441)[0]
            t_const = t[belowe[0]] if belowe.size>0 else np.NaN
            print(counter, 'diff:', p.D, ' off from steady state:', (accumulation[-1]-accumulation[-2])/accumulation[-1], 
                'error in decay length:', np.max(y-ye))
            dat.append({'alpha':p.alpha, "alphas":p.alphas, 'N_shifted':N_shifted, 'beta_start':p.beta[0],'P_lose':p.P_lose, 'beta_step':p.beta[0]-p.beta[1], 
                        'factor_isolated':p.factor_isolated, 'omega':p.omega, 'D':p.D, 'kon':p.kon, 'koff':p.koff, 'decay_length':d, 't_const':t_const,
                        'v':v, 'v_shift':velocities[:,1], 'v_lose':velocities[:,2], 'p':p, "onsingle":onsingle, 'accumulation':accumulation, 'accumulation/onsingle':accumulation/onsingle, 'solution':solution, 
                        'string':str(counter) + " D=" + str(p.D) + "  alpha=" + str(p.alpha) + "  " + colorcoded + "=" + str(var)})
            counter += 1
    return dat, norm, colorcoded, colorcodedlabel, x, t, mt_length