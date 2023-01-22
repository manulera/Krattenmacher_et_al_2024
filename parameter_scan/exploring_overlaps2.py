import numpy as np
from matplotlib import pyplot as plt

data = np.genfromtxt(f'runs_overlaps_2/scan/run0282/solution.txt',delimiter=',')

plt.figure()
plt.plot(data[-1,:])
plt.show()

