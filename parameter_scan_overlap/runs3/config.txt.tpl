## Preconfig -------------------
# n = 0

cooperativity = [[[1,2,3]]]
cooperativity_mode = protofilament
# Lattice size
a = 0.008
# Velocity of shrinkage of the MT in absence of Ase1 (From table)
v_s = 0.3
# Probability of preventing depolymerization if Ase1 is there
omega = 0.84

# Ase1 ========================================================================
# Diffusion rate of Ase1
D = 0.009

# Binding rate of Ase1 per lattice site
# If alpha = 0.5, koff = kon
[[k = list(np.logspace(-4,-1,25))]]
kon = [[k]]

# Unbinding rate of Ase1 - We scan this parameter
koff = [[k]]

## Initial conditions --------------------------------------------------

# Length of the microtubule at the start
L_init = 4
do_equilibration = True

t_max = 100
t_snap = 1