import numpy as np
from hdm_actr.hrr import HRR
from math import ceil
from scipy.stats import expon


class TimeVector():
    """
    Creates a time context vector of functions T to represent a time step, see
    (Brown 2000). It picks oscillator functions and then draws from them for
    each learning context vector element T_i. Has methods to return T(t) - time
    context vector — at each time step so we can start at the beginning and
    step through time to see if an item matches the time context.
    """

    def __init__(self, O_n=15, T_n=16*20, scale=10e-5, osc_avg=5.125, seed=None):
        """
        Creates functions for oscillators and time context vector

        :param O_n: (int) number of oscillators
        :param T_n: number of elements in learning context vector
        :param scale: multiplied by t  so oscillators appropriately fit time
            scale
        """
        
        self.T_n = T_n
        # random number generator, can be seeded for reproducibility
        rng = np.random.default_rng(seed)
        # pick oscillator parameters
        # frequency param theta
        theta = rng.normal(0.0, 1.0, O_n)
        theta *= scale
        theta *= [2**i for i in range(O_n)]
        
        # re-sort oscillators by theta size
        theta = np.sort(theta)
       
        # offset param phi, from 0 to oscillator period
        periods = np.divide(np.pi, theta,
                            out=np.zeros_like(theta), where=theta!=0)
        phi = rng.uniform(0, abs(periods))
        # alternate btwn sin and cos, the latter of which we convert to sin
        # with cos(x) = sin(x + pi/2) 
        trig_fns = np.array([0.0, np.pi/2])
        oscillator_fns = np.tile(trig_fns, ceil(O_n / len(trig_fns)))[:O_n]
        phi += oscillator_fns
        # print(theta, phi)
        # pick from oscillators, saving parameters
        #
        # combine theta and phi
        osc_params = np.vstack([theta, phi]).T
        # draw 4 of them for each learning context vector element probability
        # distribution for oscillators roughly following Brown 2000 figure 6
        osc_pmf = (expon.cdf(np.arange(1, O_n+1), scale=osc_avg) 
                   - expon.cdf(np.arange(0, O_n), scale=osc_avg) 
                   + (1 - expon.cdf(O_n, scale=osc_avg))/O_n)
        print(osc_pmf)
        draws = rng.choice(osc_params, size=4*T_n, p=osc_pmf)

        # sort so the first oscillator in each element gets the largest per oscillators,
        # as per Brown 2000 Fig 6 so more stable
        draws = draws[np.argsort(abs(draws[:,0]))]
        # print(draws.shape)
        # print(draws)
        # split by 4 so we get params for each 1...4 oscillators per element
        draws = np.vsplit(draws, 4)
        self.context_thetas = [grp[:,0] for grp in draws] 
        self.context_phis = [grp[:,1] for grp in draws] 
        # generate offsets to randomly pick sin/cos for each oscillator in each
        # context element
        context_offsets = rng.choice(trig_fns, 4*T_n)
        self.context_offsets = np.split(context_offsets, 4)

    
    # return time context vector at current timestep
    def eval(self, t):
        T = np.ones(self.T_n, dtype=np.float64)
        for j in range(4):
            T *= np.sin(self.context_offsets[j] 
                        + np.sin(self.context_phis[j]
                                 + t * self.context_thetas[j]))
        # normalize
        T /= np.linalg.norm(T)
        return T


# t = TimeVector(t)