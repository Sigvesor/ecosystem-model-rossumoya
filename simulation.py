# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from island import *
import matplotlib.pyplot as plt


class BioSim:
    """
    sim = BioSim(10)
    sim.sim.pops[0].f_max = 10
    plt.plot(sim.simulate(100))
    plt.show()
    """

    def __init__(self, ini_pop):
        self.ini_pop = ini_pop
        self.sim = Population(n_num_herbs=ini_pop)

    def simulate(self, num_steps):

        population_list = [self.ini_pop]

        for step in range(num_steps):
            population_list.append(self.sim.cycle())
        print(population_list)
        return population_list


if __name__ == "__main__":
    Jungle.set_params({'f_max': 2})

    sim = BioSim(2)
    sim.simulate(20)
    #sim.sim.pops[0].f_max = 2
    plt.plot(sim.simulate(10))
    #plt.show()