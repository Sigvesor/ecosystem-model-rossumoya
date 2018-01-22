# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


import matplotlib.pyplot as plt
#from biosim.landscape import *

from biosim.island import *


class BioSim:

    def __init__(self, island_map, ini_pop, seed):
        random.seed(seed)
        self.ini_pop = ini_pop
        self.island = Island()
        self.island.populated_island(island_map, ini_pop)
        self.herb_list = [self.island.total_island_population[0]]
        self.carn_list = [self.island.total_island_population[1]]

    def simulate(self, num_steps, vis_steps=None, img_steps=None):

        for step in range(num_steps):
            sim_cyc = self.island.cycle()
            self.herb_list.append(sim_cyc[0])
            self.carn_list.append(sim_cyc[1])
        # print(herb_list)
        # print(carn_list)
        #fig = plt.figure()
        plt.plot(range(len(self.herb_list)), self.herb_list, 'r-',
                 range(len(self.carn_list)), self.carn_list, 'b-')
        plt.show()

        # return [herb_list, carn_list]

    def add_population(self, population=None):
        self.island.distribute_animals(population)

    def sim_plot(self):
        pass


if __name__ == "__main__":
    import timeit

    t0 = timeit.default_timer()

    kart = """OOOOOOOOOOOOOOOOOOOOO
        OOOOOOOOSMMMMJJJJJJJO
        OSSSSSJJJJMMJJJJJJJOO
        OSSSSSSSSSMMJJJJJJOOO
        OSSSSSJJJJJJJJJJJJOOO
        OSSSSSJJJDDJJJSJJJOOO
        OSSJJJJJDDDJJJSSSSOOO
        OOSSSSJJJDDJJJSOOOOOO
        OSSSJJJJJDDJJJJJJJOOO
        OSSSSJJJJDDJJJJOOOOOO
        OOOSSSSJJJJJJJOOOOOOO
        OOOOOOOOOOOOOOOOOOOOO"""

    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore', 'age': 5,
                           'weight': 20} for _ in range(150)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore', 'age': 5,
                           'weight': 20} for _ in range(40)]}]
    sim = BioSim(ini_pop=ini_herbs, island_map=kart, seed=12634)
    sim.simulate(10)
    sim.add_population(ini_carns)
    sim.simulate(10)
    print(timeit.default_timer() - t0)
    # plt.show()
