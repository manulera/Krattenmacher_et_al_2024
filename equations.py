import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve

def get_kd(P, p):
    cprodP = np.ones(len(p.beta))
    cprodP[1:] = np.cumprod(P[p.shifting[1:]]) 
    P_shifttoempty = p.beta * cprodP * (1 - P[p.shifting+1])
    P_shift = np.cumsum(P_shifttoempty[::-1])[::-1] # probability to shift, given P[0] (since we above set cprodP[0] = 1)
    if p.P_lose + p.omega + P_shift[0] > 1:
        raise Exception("P_lose + Omega + P_shift[0] > 1!")
    # kd = k0 * (1.-P[0]) + k0 * P[0] * (1.-omega) # without shifting
    k_free = p.depol_rate * (1.-P[0])
    k_shift = p.depol_rate * P[0] * P_shift[0]
    k_lose = p.depol_rate * P[0] * p.P_lose
    kd = k_free + k_shift + k_lose
    return P_shift, kd, k_shift, k_lose

def get_v(P, p):
    _, kd, k_shift, k_lose = get_kd(P, p)
    return np.stack((kd, k_shift, k_lose)) * p.a

def myODE(P, t,p):
    """
    Discrete differential equation dP/dt, with the special cases of P1 and PN, as shown in the paper
    """
    k0 = p.depol_rate
    kh = p.k_D/2
    kon = p.kon
    koff = p.koff

    P_shift, kd, _, _ = get_kd(P, p)

    # For all except position 1 and position N-1

    # dPN/dt as shown in the paper
    dP = np.zeros_like(P)
    dP[-1] = 0

    # dP1/dt as shown in the paper
    # diff_depo = kd * P[1] - k0 * P[0] * (1. - omega) # without shifting
    from_next = kd * P[1] - k0 * P[0] * P_shift[1] # Ase1 at spot 1 might shift
    lost = k0 * P[0] * p.P_lose
    dP[0] = kh * (P[1]-P[0]) - P[0] * koff + (1. - P[0]) * kon + from_next - lost

    # dPi/dt as shown in the paper

    # Pi (excluding 1 and N-1)
    Pi = P[1:-1]
    # Pi+1
    Pip1 = P[2:]
    # Pi-1
    Pim1 = P[:-2]

    s = p.shifting[1:] # we already took care of shifting for dP[0]
    dP[1:-1] = kh * (Pip1 + Pim1 - 2 * Pi) - Pi * koff + (1. - Pi) * kon + kd * (Pip1 - Pi)
    dP[s] += k0 * P[0] * P_shift[s]
    dP[s[:-1]] -= k0 * P[0] * P_shift[s[1:]] # Ase1 at next spot might shift

    return dP

def solveDiscrete(p,t,N):
    """
    Calculates the evolution of P with the differential equation myODE, starting from all the lattice sites
    equal to alpha (binding equilibrium)
    """
    P0 = np.zeros(N, dtype=float)
    P0[:] = p.alpha
    p.shifting = np.arange(len(p.beta))

    return odeint(myODE, P0, t, args=(p,))


def read_simulation():
    """
    Read the output files of the simulation
    :return: t (list of times of the snapshots), out (list of self.mt_array at the different stanpshots),
    depol_times (the times at which depolymerisation events occurred)
    """
    t = list()
    out = list()

    with open("output.txt") as ins:
        for line in ins:
            ls = line.split()
            t.append(float(ls[0]))
            out.append(np.array(ls[1:],dtype=int))
    with open("depol.txt") as ins:
        for line in ins:
            depol_times = np.array(line.split(),dtype=float)

    return t,out,depol_times

def numerical_prediction(p):
    """
    Solve the system of equations shown in the supplementary, we return P0 instead of rho0 (not normalised to alpha)
    :param p:
    :return:
    """
    k0 = p.depol_rate / (p.kon+p.koff)
    kh = p.k_D / 2. / (p.kon+p.koff)
    omega = p.omega
    alpha = p.alpha


    def eq2solve(rho0):
        kd = alpha*(rho0 * (1. - omega) * k0 + (1. / alpha - rho0) * k0)

        Pint = -2. * kh * (1 - rho0) / (kd + np.sqrt(kd * kd + 4. * kh))

        return kd - rho0 * (1. - omega) * k0 - Pint

    P0_sol = fsolve(eq2solve,20.)[0]*alpha
    kd_sol = k0*(1. - P0_sol) + k0*P0_sol*(1. - omega)

    return kd_sol,P0_sol

def decayLength(p, kd):
    """
    Calculate the decay length of the exponential from the parameters, in lattice sites
    :return:
    """
    kh = p.k_D / 2. / (p.kon + p.koff)
    return 2. * kh / (kd + np.sqrt(kd * kd + 4 * kh))

def decayLengthPhysical(p, v):
    """
    Calculate the decay length of the exponential from the parameters, in physical units
    :return:
    """
    return 2 * p.D / (v + np.sqrt(v * v + 4 * p.D * (p.koff + p.kon)))
