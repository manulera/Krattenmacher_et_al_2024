#%%
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from simulation import Parameters

cmap = sns.color_palette("rocket", as_cmap=True)

folders = [
    'parameter_scan3/runs_6nM/scan/run0019',
    'parameter_scan3/runs_6nM/scan/run0145',
]
names = ['Model 1', 'Model 2']
linestyles = ['-','--',':']
plt.figure(figsize=[3,3])
for folder,name,ls in zip(folders,names,linestyles):
    speed = np.genfromtxt(f'{folder}/speed.txt',delimiter=',')    
    solution = np.genfromtxt(f'{folder}/solution.txt',delimiter=',')
    plt.plot(speed,ls=ls,label=name,c='k')
plt.xlim(0,100)
plt.ylim(ymin=0)
plt.ylabel('Shrinkage speed at \nsteady state (\u03BCm/s)')
plt.xlabel('Time (s)\n ')
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig('parameter_scan/plots_paper/dynamics.svg')

for folder, title in zip(folders,['model1','model2','model3']):
    # The maximum timepoint and max_length (in lattice sites)
    max_t = 50

    # We have to scale the kymograph, otherwise the svg is huge
    scale_image = 10

    solution = np.genfromtxt(f'{folder}/solution.txt',delimiter=',')
    solution = solution[0:max_t,:]
    nb_lattice_sites = solution.shape[1]

    speed = np.genfromtxt(f'{folder}/speed.txt',delimiter=',')
    speed = speed[0:max_t]/0.008

    # Figure of the profile
    l = np.arange(0,400,dtype=float)*0.008
    chosen_vals = [0,4,8,16,32,48]
    linestyles = ['-','--','-.',':','-','--','-.',':']
    plt.figure(figsize=[3,3])
    for chosen_val, ls in zip(chosen_vals, linestyles):
        plt.plot(l,solution[chosen_val,:],ls=ls,label=f't = {chosen_val} s', c= cmap(chosen_val/60.))
    plt.xlabel('Distance from plus end (\u03BCm)')
    plt.ylabel('Ase1 density (molecules/site)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'parameter_scan/plots_paper/{title}_density_profile.svg')
    
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

    plt.figure(figsize=[4,2.5])
    ax = sns.heatmap(kymograph, linewidth=0, cbar_kws = dict(use_gridspec=False,location="top"),vmin=0,vmax=0.5)
    ax.collections[0].colorbar.set_label("Ase1 per binding site", fontsize=12)
    ax.collections[0].colorbar.set_ticks([0,0.25,0.5])
    
    plt.yticks([])
    plt.xticks([])
    trans = ax.get_xaxis_transform()
    start_line = 0.1
    ax.plot([1/0.008/scale_image, 3/0.008/scale_image],[30,30], color="w", clip_on=False)
    ax.annotate('2 \u03BCm', xy=(2/0.008/scale_image, 29), ha="center", va="bottom", c='w', fontsize=12)

    ax.plot([1/0.008/scale_image,1/0.008/scale_image],[30,45], color="w", clip_on=False)
    ax.annotate('15 s', xy=(1/0.008/scale_image, 37.5), ha="right", va="center", rotation=90, c='w', fontsize=12)

    plt.savefig(f'figures_revision/{title}_simulated_kymograph.svg')

plt.show()