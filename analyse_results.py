
"""
A script to calculate derived quantities from the solution of the discrete equation.
    - Shrinking speed of microtubules in time.
    - Accumulation of ase1 in time.
    - Single values:
        - Shrinking speed at steady state (last time point)
        - Equilibrium density at the body of the microtubule (from the parameters of the simulation)
        - Lengthscale (L) of the exponential decay along the microtubule length (l),
          from an exponential fit to P * exp(-l/L)
        - Timescale (T) of the accumulation of ase1 in time (t), from a fit to P * (1-exp(-t/T))
"""

import sys
import os
import numpy as np
from simulation import Parameters
from equations import scaleVelocity
from scipy.optimize import curve_fit


def timeScaleFitFunction(t, P, T):
    return P * (1 - np.exp(-t / T))


def lengthScaleFitFunction(l, P, L):
    return P * np.exp(-l / L)


def velocityFit(t, P0, Pend, T):
    return P0 * np.exp(-t / T) + Pend


def main(folder):

    # We read the parameters and the solution from the equation
    p = Parameters()
    p.read(os.path.join(folder, "config.txt"))
    solution = np.genfromtxt(os.path.join(
        folder, "solution.txt"), delimiter=',')
    t = np.arange(0, 200, 1)

    # Better to do this in a loop than to duplicate the code on how to calculate the speed
    speed = np.zeros_like(t, dtype=float)
    for i in range(len(speed)):
        speed[i] = p.v_s * scaleVelocity(solution[i, :],
                                         p.omega, p.cooperativity, p.cooperativity_mode)
    np.savetxt(os.path.join(folder, "speed.txt"), speed, delimiter=",")

    # We also calculate its decay
    fit, _ = curve_fit(velocityFit, t, speed, [
                       speed[0] - speed[-1], speed[-1], 1])
    _, _, velocity_decay_timescale = tuple(fit)

    # We calculate and export the accumulated ase1 (over the equilibrium value, alpha)
    accum = solution - p.alpha
    accum = np.sum(accum, axis=1)
    np.savetxt(os.path.join(folder, "ase1_accumulation.txt"),
               accum, delimiter=",")

    # We export a csv with the single values
    fit, _ = curve_fit(timeScaleFitFunction, t, accum, [accum[-1], 1])
    timescale_P, timescale_T = tuple(fit)

    l = np.arange(0, 400)
    fit, _ = curve_fit(lengthScaleFitFunction, l,
                       solution[-1, :] - p.alpha, [accum[-1], 20])
    lengthscale_P, lengthscale_L = tuple(fit)

    with open(os.path.join(folder, "other_values.txt"), "w") as out:
        out.write("shrinking_speed_steady_state,velocity_decay_timescale,equilibrium_density,P0_end_fit,lengthscale_density_end_fit,accumulation_end_fit,accumulation_timescale\n")
        out.write(
            f'{speed[-1]},{velocity_decay_timescale},{p.alpha},{lengthscale_P},{lengthscale_L},{timescale_P},{timescale_T}\n')

    with open(os.path.join(folder, "parameters_table.txt"), "w") as out:
        out.write(
            f'omega,cooperativity,kon,v_s,D,tip_off,cooperativity_mode\n{p.omega},{p.cooperativity},{p.kon},{p.v_s},{p.D},{p.tip_off},{p.cooperativity_mode}\n')


# ------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        main(".")
    else:
        main(sys.argv[1])
