## Preconfig -------------------
# n = 0

# Lattice size
a = 0.008
# Velocity of shrinkage of the MT in absence of Ase1 (From your presentation)
v_s = [[0.3]]
# Probability of preventing depolymerization if Ase1 is there
omega = [[[0.6, 0.8, 0.9]]]

# Ase1 ========================================================================
# Diffusion rate of Ase1
[[x = [0.093, 0.04515]]]
D = [[x]]
# Unbinding rate of Ase1
koff = [[x / 5.8125]]

# Binding rate of Ase1 per lattice site
kon = [[0.0002, 0.001, 0.002, 0.006, 0.01, 0.02, 0.06, 0.1, 0.2, 0.6]]

## Initial conditions --------------------------------------------------

# Length of the microtubule at the start
L_init = 4
do_equilibration = True

t_max = 100
t_snap = 1
