from simulation import Parameters
from equations import solveDiscrete
import numpy as np
import matplotlib.pyplot as plt

plt.figure()
p = Parameters()
p.read("config.txt")

def term_values(p,P):
    k0 = p.depol_rate
    kh = p.k_D / 2
    kon = p.kon
    koff = p.koff
    omega = p.omega



    kd = k0 * (1. - P[:,0]) + k0 * P[:,0] * (1. - omega)


    diff = -kh * (P[:,1] - P[:,0])
    bind = (1. - P[:,0]) * kon
    unbind = P[:,0] * koff
    flux= kd * P[:,1] - k0 * P[:,0] * (1. - omega)
    fluxin = kd * P[:, 1]
    fluxout = k0 * P[:, 0] * (1. - omega)
    # dP1/dt as shown in the paper
    return diff,bind,unbind,flux,fluxin,fluxout


# for D in np.arange(0.01,0.1,0.01):
#     p.D = D
#     p.derivated()
#     t = np.linspace(0,40,100)
#     solution = solveDiscrete(p,t,400)
#
#     speed =p.omega * (1-solution[:,0]*p.omega)*p.a
#
#     # plt.plot(t,speed)
#     plt.plot(t,solution[:,0]/solution[-1,0])
#
#     plt.xlabel("Time (s)")
#     plt.ylabel("Velocity (um /s)")

t = np.linspace(0,40,100)
solution = solveDiscrete(p,t,400)

diff,bind,unbind,flux,fluxin,fluxout = term_values(p,solution)

speed =p.omega * (1-solution[:,0]*p.omega)*p.a

# plt.plot(t,speed)
plt.plot(t,diff,label="diff")
plt.plot(t,bind,label="bind")
plt.plot(t,unbind,label="unbind")
plt.plot(t,flux,label='flux')
plt.plot(t,fluxin,label='fluxin')
plt.plot(t,fluxout,label='fluxout')

plt.xlabel("Time (s)")
plt.ylabel("Velocity (um /s)")

plt.legend()


plt.show()


