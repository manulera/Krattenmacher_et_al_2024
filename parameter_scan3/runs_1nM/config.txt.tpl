## Preconfig -------------------
# n = 0

cooperativity_mode = [[ ["protofilament", "mixed"] ]]
cooperativity = [[ [1,2,3,4] ]]

# Lattice size
a = [[parameters.lattice_size]]
# Velocity of shrinkage of the MT in absence of Ase1 (From table)
v_s = [[parameters.shrinkage_velocity_no_ase1]]

# Probability of preventing depolymerization if Ase1 is there
omega = [[ [i/20. for i in range(0,21)] + [i/100. for i in range(70,101)] ]]

# Ase1 ========================================================================
# Diffusion rate of Ase1
D = [[parameters.ase1_diffusion_single_mt]]

# Binding rate of Ase1 per lattice site
# See model parameter table
kon = [[parameters.kon_single_mt_1nM]]

# Unbinding rate of Ase1 - # See model parameter table
koff = [[parameters.ase1_koff]]

## Initial conditions --------------------------------------------------

# Length of the microtubule at the start
L_init = 4
do_equilibration = True

t_max = 100
t_snap = 1