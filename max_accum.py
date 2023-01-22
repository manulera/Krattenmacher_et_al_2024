import numpy as np
from matplotlib import pyplot as plt

D = np.linspace(0, 0.1)
v = 0.1
ku = 0.01
alpha = 0.53/0.008

plt.figure()

for ku in [0.01, 0.1]:
    lamb = 2*D/(v + np.sqrt(v**2 + 4*D*ku))
    max_density = 1/0.008
    accum = lamb * (max_density - alpha)
    plt.plot(D, accum, label='ku = ' + str(ku))

plt.axhline(y=20, label='Target')
plt.ylabel('Accumulation')
plt.xlabel('D (um2/s)')
plt.legend()

plt.show()
