import numpy as np
import random
import os

# We define some constants

DIFFUSION = 0
DEPOLIMERIZATION = 1
DIFFUSION_EDGE = 2
ATTACHMENT = 3
DETACHMENT = 4
NB_RATES = 5

def timeToNextEvent(rate):
    """
    Calculate Gillespie time until next event given a certain rate, taking into account
    that if the rate is zero it should return infinity
    :param rate: the rate of a process
    :return: the time of next event
    """
    if rate:
        return -np.log(random.random()) / rate
    else:
        # If we divide by zero
        return np.inf

class Parameters:

    def __init__(self):
        """
        Initialization of an empty parameter object
        """
        # All units are in um, s,

        # Simulation ====================================================

        # Time at which the simulation will stop
        self.t_max = None

        # Time interval at which the simulation takes snapshots
        self.t_snap = None


        # Microtubules ================================================================

        # Lattice size (by default should be microtubule lattice, 0.008)
        self.a = 0.

        # Velocity of shrinkage of the MT in absence of Ase1
        self.v_s = 0.

        # Probability of preventing depolymerization if Ase1 is there (Set to zero by default)
        self.omega = 0.

        # Ase1 ========================================================================
        # Diffusion rate of Ase1 (by default should be around 0.1)
        self.D = 0.

        # Binding rate of Ase1 per lattice site
        self.kon = 0.

        # Unbinding rate of Ase1
        self.koff = 0.

        # Initial conditions ==========================================================

        # This could be in a different object, but for now we can treat it as a parameter:

        # Simulated length of the microtubule
        self.L_init = 0.

        # Boolean that indicates whether binding equilibrium is imposed in the simulation prior to start
        self.do_equilibration = False

        # Derivatedd quantities
        self.depol_rate = 0.
        self.k_D = 0.
        self.alpha =0.

    def derivated(self):
        """
        Calculate some quantities from input parameters
        :return:
        """

        # Rate of monomer unbinding given a certain speed.
        self.depol_rate = self.v_s / self.a

        # Rate at which Ase1 steps, multiplied by 2 because in can diffuse to either side
        self.k_D = self.D / self.a / self.a * 2.

        # The expected probability of a site being occupied just by binding/unbinding
        self.alpha = self.kon / (self.koff + self.kon)

    def read(self,config_file):
        """
        Read parameters from a config file of the structure parameter_name parameter_value, use # as comments
        :param config_file: the file
        :return:
        """

        with open(config_file,"r") as ins:
            for line in ins:
                if len(line.strip()) and line[0]!="#":
                    ls = line.split("=")
                    ls[0] = ls[0].strip()

                    if ls[0]=="a":
                        self.a = float(ls[1])

                    elif ls[0] == "v_s":
                        self.v_s = float(ls[1])

                    elif ls[0] == "omega":
                        self.omega = float(ls[1])

                    elif ls[0] == "D":
                        self.D = float(ls[1])

                    elif ls[0] == "kon":
                        self.kon = float(ls[1])

                    elif ls[0] == "koff":
                        self.koff = float(ls[1])

                    elif ls[0] == "L_init":
                        self.L_init = float(ls[1])

                    elif ls[0] == "do_equilibration":
                        self.do_equilibration = bool(ls[1])

                    elif ls[0] == "t_max":
                        self.t_max = float(ls[1])

                    elif ls[0] == "t_snap":
                        self.t_snap = float(ls[1])

                    else:
                        raise ValueError("Unkwon parameter: " + ls[0])

        if self.t_snap is None or self.t_max is None:

            raise ValueError("Set t_snap and t_max")

        # Calculate the derivated quantities
        self.derivated()


    def __str__(self):
        """
        Convert the parameters into a readable string (like the input file)
        :return:
        """
        out = ""
        out+="a = %f\n" % self.a
        out += "v_s = %f\n" % self.v_s
        out += "omega = %f\n" % self.omega
        out += "D = %f\n" % self.D
        out += "kon = %f\n" % self.kon
        out += "koff = %f\n" % self.koff
        out += "L_init = %f\n" % self.L_init
        out += "do_equilibration = %u\n" % self.do_equilibration
        out += "t_max = %f\n" % self.t_max
        out += "t_snap = %f\n" % self.t_snap

    def print_for_file(self):
        """
        Print the parameters as a csv with column names
        :return:
        """
        out = ""
        out+="a|v_s|omega|D|kon|koff|L_init|do_equilibration|t_max|t_snap\n"

        extra = [self.a,self.v_s,self.omega,self.D,self.kon,self.koff,self.L_init,self.do_equilibration,self.t_max,self.t_snap]
        extra = map(str,extra)

        out+= "|".join(extra)+"\n"

        return out

class Simulation:
    """
    A class to run the simulation
    """

    def __init__(self):
        # Plus end is zero
        self.mt_array = np.array([0],dtype=int)
        self.t = 0.

        # Keeps track of when depolimerization events happenned
        self.depol_events = list()

        # Store the different rates in order of the frequency of happening
        # (rate_diffusion,rate_depol,rate_diffEdge,rate_attachment,rate_detachment,)
        self.rates = np.zeros(NB_RATES)
        self.cum_rates = np.zeros(NB_RATES)

        # The are updated after there is binding, unbinding, or an Ase1 diffuses
        # out of the system at site N.
        self.total_sites = 0
        self.bound_ase1 = 0
        self.empty_sites = 0

    # Surpringsingly is faster than numpys cumsum (this was a limiting step)
    def my_cumsum(self):
        self.cum_rates[0] = self.rates[0]
        self.cum_rates[1] = self.cum_rates[0]+self.rates[1]
        self.cum_rates[2] = self.cum_rates[1]+self.rates[2]
        self.cum_rates[3] = self.cum_rates[2]+self.rates[3]
        self.cum_rates[4] = self.cum_rates[3]+self.rates[4]

    def resetRates(self,p):
        # Re-set the rates
        self.total_sites = self.mt_array.size
        self.bound_ase1 = np.count_nonzero(self.mt_array)
        self.empty_sites = self.total_sites - self.bound_ase1

        self.rates[ATTACHMENT] = self.empty_sites * p.kon
        self.rates[DETACHMENT] = self.bound_ase1 * p.koff
        self.rates[DIFFUSION] = self.bound_ase1 * p.k_D
        # this is equal to depol_rate if the position 0 is empty, and depol_rate * (1-omega) otherwise
        self.rates[DEPOLIMERIZATION] = p.depol_rate * (1 - self.mt_array[0] * p.omega)
        self.rates[DIFFUSION_EDGE] = p.alpha * p.k_D / 2.

        self.my_cumsum()


        # self.cum_rates = np.cumsum(self.rates)

    def populate(self,p):
        """
        Initialize the simulation providing initial conditions in p
        :param p:
        :type p:Parameters
        """

        # An array that represents the lattice of the microtubule.
        # False if nothing is bound, True if Ase1 is bound. Plus end is at zero
        self.mt_array = np.zeros(int(p.L_init/p.a),dtype=int)

        # Simulation time
        self.t = 0.

        # Reach binding equilibrium
        if p.do_equilibration:
            self.equilibrate(p)

        self.resetRates(p)

    def equilibrate(self,p):
        """
        Reach binding equilibrium with solution, before starting the simulation
        :return:
        """
        # Number of lattice sites
        mt_sites = self.mt_array.size
        expected_bound = int(mt_sites*p.alpha)

        # Get a set of random positions in the microtubule where Ase1 is bound
        self.mt_array[0:expected_bound] = True
        np.random.shuffle(self.mt_array)

    def decideEvent(self):
        """
        Returns the index of the next event, as defined by the constants in CAPs
        on the top of this file, by using the Gillespie method
        :return:
        """
        randn = random.random()*self.cum_rates[-1]

        # We know that most often it will be a diffusion event, so we check first
        if randn<self.cum_rates[0]:
            return 0
        i=1
        while i <NB_RATES:
            if randn < self.cum_rates[i]:
                return i
            i+=1

    def nextEvent(self,p):
        """
        Decide which event will occur next (diffusion, binding, unbinding, or depolimerization of the microtubule)
        """

        which_event = self.decideEvent()
        event_tau = timeToNextEvent(self.cum_rates[-1])

        if which_event==DIFFUSION:
            if self.eventDiffusion(p)==2:
                self.resetRates(p)

        elif which_event==DEPOLIMERIZATION:
            if self.eventDepol(p):
                self.resetRates(p)
                self.depol_events.append(self.t + event_tau)

        elif which_event == DIFFUSION_EDGE:
            if self.eventDiffusionEdge(p):
                self.resetRates(p)

        elif which_event == ATTACHMENT:
            self.eventAttachment(p)
            self.resetRates(p)

        elif which_event == DETACHMENT:
            self.eventDetachment(p)
            self.resetRates(p)

        return event_tau

    def changeRatesGain(self,p):
        # Unused, could be used to change the rates when a molecule is added. In reality since most of events
        # by far are diffusion events, does not really make a difference

        self.rates[DETACHMENT] += p.koff
        self.cum_rates[DETACHMENT:] += p.koff
        self.rates[ATTACHMENT] -= p.kon
        self.cum_rates[ATTACHMENT] -= p.kon
        self.rates[DIFFUSION] += p.k_D
        self.cum_rates[DIFFUSION] += p.k_D
        return

    def changeRatesLoss(self, p):
        # Unused, could be used to change the rates when a molecule is lost. In reality since most of events
        # by far are diffusion events, does not really make a difference
        self.rates[DETACHMENT] -= p.koff
        self.cum_rates[DETACHMENT:] -= p.koff
        self.rates[ATTACHMENT] += p.kon
        self.cum_rates[ATTACHMENT] += p.kon
        self.rates[DIFFUSION] -= p.k_D
        self.cum_rates[DIFFUSION] -= p.k_D
        return

    def eventAttachment(self,p):
        """
        Do an attachment event at a random position
        :return: returns 1 always
        """
        # Get the indexes of unoccupied sites in the lattice
        empty_positions = np.where(self.mt_array == 0)[0]

        # Attach at a random position
        # chosen_i = np.random.randint(empty_positions.size)
        # This is faster
        chosen_i = int(random.random()*empty_positions.size)
        chosen = empty_positions[chosen_i]

        self.mt_array[chosen] = True

        return 1

    def eventDetachment(self,p):
        """
        Detach randomly one of the bound Ase1 molecules
        :return: returns 1 always
        """
        # Get the indexes of the occupied sites in the lattice
        bound_positions = np.where(self.mt_array == True)[0]

        # Detach a random molecule
        # chosen_i = np.random.randint(bound_positions.size)
        chosen_i = int(random.random() * bound_positions.size)
        chosen = bound_positions[chosen_i]

        self.mt_array[chosen] = False

        return 1


    def eventDiffusion(self,p):
        """
        Perform a diffusion step in a random direction for a random Ase1 molecule. If the position it is trying to move
        to is either occupied or at the plus end of the microtubule, do not do anything, and
        return zero, since no event happenned
        :return: 2 if the molecules diffuses out of the system at site N, 1 if event happens, 0 otherwise.
        The rates of the system only need to be recalculated if the return is 2
        """

        # Get the indexes of the occupied sites in the lattice
        bound_positions = np.where(self.mt_array == True)[0]

        # Select the molecule that will move
        # chosen_i = np.random.randint(bound_positions.size)
        chosen_i = int(random.random() * bound_positions.size)

        chosen = bound_positions[chosen_i]

        # Fifty percent of probability of one side or the other
        move_plus_end = random.random()>0.5

        if move_plus_end:
            new_position = chosen + 1
        else:
            new_position = chosen - 1

        # Plus end edge is reached

        if new_position==-1:
            # We could add something here to make it fall off or something like that
            # We return zero because this event didnt happen
            return 0

        elif new_position==self.mt_array.size:
            # The special case of exchange with the body of the microtubule, where the probability of a site being
            # occupied is alpha. Therefore we test the probability alpha to decide whether the molecule exits the system
            # at the minus end
            if p.alpha>random.random():
                return 0
            else:
                # The molecule goes to the 'bath'
                self.mt_array[chosen] = 0
                # Here we return 2 to know that we have to reset the rates due to the loss of the molecule
                return 2

        # The site we try to move to is occupied
        elif self.mt_array[new_position]:

            # We return zero because this event didnt happen
            return 0

        # The site is available, perform the step and return 1
        else:

            self.mt_array[chosen]=0
            self.mt_array[new_position]=1
            return 1

    def eventDiffusionEdge(self,p):
        """
        A molecule enters the system at position N from the microtubule body, if the site N is empty
        :return: 1 if the event happens, 0 otherwise
        """
        if not self.mt_array[-1]:
            self.mt_array[-1]=1
            return 1
        else:
            return 0

    def eventDepol(self,p):
        """
        The first site of the lattice is lost due to depolymerisation, and the incoming site N has a
        probability alpha of being occupied
        :return: 1 always
        """
        # We shift the array, and the last position we give it a probability of alpha to be occupied
        self.mt_array[:-1] = self.mt_array[1:]
        self.mt_array[-1] = p.alpha>random.random()

        return 1

    def write(self,output_file):
        """
        Print a string to the output file containing the time of the simulation, plus the values in the array self.mt_array
        :return:
        """
        with open(output_file,"a") as out:

            out.write(str(self.t) + " ")
            array_string = list(np.array(self.mt_array,dtype=str))
            out.write(" ".join(array_string))
            out.write("\n")

    def writeDepol(self,output_file):
        """
        Write a file with the times at which depolymerisation events occured (stored in the property depol_events of the
        simulation)
        :return:
        """
        with open(output_file, "w") as out:
            out_list = map(str,self.depol_events)
            out.write(" ".join(out_list))


    def run(self,sim_dir):
        """
        Run the simulation in sim_dir until the time is bigger than `t_max`, save a snapshot of the simulation,
        every `t_snap` seconds. It expects the file sim_dir/config.txt to exist
        """

        # Read parameters from config file
        p = Parameters()

        if not os.path.isfile(os.path.join(sim_dir,"config.txt")):
            raise FileNotFoundError("No config.txt file found in %s" % sim_dir)

        p.read(os.path.join(sim_dir,"config.txt"))
        output_file = os.path.join(sim_dir,"output.txt")
        depol_file = os.path.join(sim_dir, "depol.txt")

        # Create the empty file
        with open(output_file, "w") as f:
            f.write("")

        # Calculate derivated quantities of the parameters
        p.derivated()

        self.populate(p)

        # Calculate events until reaching time zero
        self.write(output_file)


        next_snap = p.t_snap
        while self.t < p.t_max:

            # Proceed to next event, and get the time until the next event
            dt = self.nextEvent(p)
            self.t = self.t + dt

            # If time is higher than next_snap, save a snapshot of the simulation in a list
            if self.t>next_snap:
                self.write(output_file)
                next_snap+=p.t_snap

        # Write the depolym file
        self.writeDepol(depol_file)

        return 0