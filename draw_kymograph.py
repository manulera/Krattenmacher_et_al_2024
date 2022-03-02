import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from simulation import Parameters

folder = 'parameter_scan/runs2/scan/run0030'
# The maximum timepoint and max_length (in lattice sites)
max_t = 50

# We have to scale the kymograph, otherwise the svg is huge
scale_image = 5

solution = np.genfromtxt(f'{folder}/solution.txt',delimiter=',')
solution = solution[0:max_t,:]
nb_lattice_sites = solution.shape[1]

speed = np.genfromtxt(f'{folder}/speed.txt',delimiter=',')
speed = speed[0:max_t]/0.008


p = Parameters()
p.read(f'{folder}/config.txt')

# Now we calculate the position of the plus end in time:
dt = 1
position = np.cumsum(speed*dt)
position = position - position[0]
t = np.arange(0,max_t)

position_int = np.array(position,dtype=int) 
kymograph_space_width = np.max(position_int) + nb_lattice_sites + 100

kymograph = np.zeros([max_t,kymograph_space_width])

for i in range(max_t):
    start = position_int[i]
    end = start + nb_lattice_sites
    kymograph[i,start:end] = solution[i,:]
    kymograph[i,end:] = p.alpha

kymograph = kymograph[:,::scale_image]

plt.figure(figsize=[4,2])
ax = sns.heatmap(kymograph, linewidth=0, cbar_kws = dict(use_gridspec=False,location="left"))
ax.collections[0].colorbar.set_label("Ase1 density\n(molecules/site)")
plt.yticks([])
plt.xticks([])
trans = ax.get_xaxis_transform()
ax.plot([0,2/0.008/scale_image],[1.01,1.01], color="k", transform=trans, clip_on=False)
ax.annotate('2 \u03BCm', xy=(1/0.008/scale_image, 1.02), xycoords=trans, ha="center", va="bottom")

trans = ax.get_yaxis_transform()
ax.plot([-.01,-.01],[0,15], color="k", transform=trans, clip_on=False)
ax.annotate('15 s', xy=(-.02, 7.5), xycoords=trans, ha="right", va="center", rotation=90)

plt.savefig('simulated_kymograph.svg')
plt.show()