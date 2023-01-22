## Preconfig -------------------
# n = 0

cooperativity = 1
cooperativity_mode = protofilament

# Lattice size
a = 0.008
# Velocity of shrinkage of the MT in absence of Ase1 (From table)
v_s = 0.3
# Probability of preventing depolymerization if Ase1 is there
omega = [[ [i/20. for i in range(0,21)] ]]

# Ase1 ========================================================================
# Diffusion rate of Ase1
D = [[ [i/1000 for i in range(10,52,3)] ]]

# Binding rate of Ase1 per lattice site
# See model parameter table
kon = 0.001

# Unbinding rate of Ase1 - # See model parameter table
koff = 0.0009

## Initial conditions --------------------------------------------------

# Length of the microtubule at the start
L_init = 4
do_equilibration = True

t_max = 100
t_snap = 1