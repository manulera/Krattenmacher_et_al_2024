## Preconfig -------------------
# n = 0

cooperativity = [[ [1,2,3,4] ]]
cooperativity_mode = protofilament

# Lattice size
a = 0.008
# Velocity of shrinkage of the MT in absence of Ase1 (From table)
v_s = 0.3
# Probability of preventing depolymerization if Ase1 is there
omega = [[ [i/20. for i in range(1,21)] ]]

# Ase1 ========================================================================
# Diffusion rate of Ase1
D = 0.09

# Binding rate of Ase1 per lattice site
# From the data in Fig. S2B
kon = 0.001

# Unbinding rate of Ase1 - We scan this parameter
koff = 0.016

## Initial conditions --------------------------------------------------

# Length of the microtubule at the start
L_init = 4
do_equilibration = True

t_max = 100
t_snap = 1