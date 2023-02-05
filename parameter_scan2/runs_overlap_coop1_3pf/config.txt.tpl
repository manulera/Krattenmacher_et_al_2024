## Preconfig -------------------
# n = 0

cooperativity = [[ [1, 3] ]]
cooperativity_mode = protofilament

# Lattice size
a = 0.008
# Velocity of shrinkage of the MT in absence of Ase1 (From table)
v_s = 0.3
# Probability of preventing depolymerization if Ase1 is there
omega = [[ [i/20. for i in range(0,21)] ]]

# Ase1 ========================================================================
# Diffusion rate of Ase1
D = [[ [0.01, 0.02, 0.04] ]]

# Binding rate of Ase1 per lattice site
# See model parameter table
kon = 0.0035

# Unbinding rate of Ase1 - # See model parameter table
koff = 0.016

## Initial conditions --------------------------------------------------

# Length of the microtubule at the start
L_init = 4
do_equilibration = True

t_max = 100
t_snap = 1