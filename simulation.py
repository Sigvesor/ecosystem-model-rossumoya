# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from landscape import *
from animals import *
from island import *
import matplotlib.pyplot as plt
import timeit


class BioSim:

    def __init__(self, island_map, ini_pop, seed):
        random.seed(seed)
        self.ini_pop = ini_pop
        self.island = Island()
        self.island.populated_island(island_map, ini_pop)

    def simulate(self, num_steps, vis_steps=None, img_steps=None):

        herb_list = [self.ini_pop]
        carn_list = [2]

        for step in range(num_steps):
            sim_cyc = self.island.cycle()
            herb_list.append(sim_cyc[0])
            carn_list.append(sim_cyc[1])
        print(herb_list)
        print(carn_list)
        return [herb_list, carn_list]


if __name__ == "__main__":
    #Savannah.set_params({'f_max': 300})
    t0 = timeit.default_timer()

    #Carnivore.set_params({'})
    sim = BioSim(100)
    #[sim.sim.pops[0].pop_animals[0][i].weight = 40 for i in range(len(sim.sim.pops[0].pop_animals[0]))]
    #sim.simulate(15)
    #sim.sim.pops[0].f_max = 2
    #sim.simulate(100)
    #plt.hist([sim.sim.pops[0].pop_animals[0][i].weight for i in range(len(sim.sim.pops[0].pop_animals[0]))])
    simulation = sim.simulate(300)
    plt.plot(range(301), simulation[0], 'r--', range(301), simulation[1], 'b-')
    #plt.hist([sim.sim.pops[0].pop_herbs[i].age for i in range(len(sim.sim.pops[0].pop_herbs))])
    print(timeit.default_timer() - t0)
    plt.show()
