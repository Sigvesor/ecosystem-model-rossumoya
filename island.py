# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from landscape import *
import numpy as np

standard_map = """OOO
OJO
OOO"""


class Island:
    """A population with many jungles"""

    def __init__(self):
                 # island_map=standard_map, ini_pop=standard_pop):
                 #n_pops=1, n_num_herbs=10, n_num_carns=2):
        """
        Parameters:
        ----------
        n_pops : int
            number of Herbivore populations
        """
        self.map = np.array(None)


        #self.pops = [Jungle(n_num_herbs, n_num_carns) for _ in range(n_pops)]

    def cycle(self):
        """Update all populations by one cycle."""
        for pop in self.pops:
            pop.fitness_sort()
            pop.eat_request()
            pop.update_fitness()
            pop.reproduction()
            pop.aging()
            pop.weightloss()
            pop.update_fitness()
            pop.death()
            pop.regenerate()

            return (len(pop.pop_animals[0]),len(pop.pop_animals[1]))


    def map_from_string(self, map_str=None):
        standard_map = """OOOOOOOOOOOOOOOOOOOOO
        OOOOOOOOSMMMMJJJJJJJO
        OSSSSSJJJJMMJJJJJJJOO
        OSSSSSSSSSMMJJJJJJOOO
        OSSSSSJJJJJJJJJJJJOOO
        OSSSSSJJJDDJJJSJJJOOO
        OSSJJJJJDDDJJJSSSSOOO
        OOSSSSJJJDDJJJSOOOOOO
        OSSSJJJJJDDJJJJJJJOOO
        OSSSSJJJJDDJJJJOOOOOO
        OOSSSSJJJJJJJJOOOOOOO
        OOOSSSSJJJJJJJOOOOOOO
        OOOOOOOOOOOOOOOOOOOOO"""
        if not map_str:
            map = standard_map
        else:
            map = map_str
        map = map.replace(" ","").splitlines()
        island_map = np.empty((len(map[0]),len(map)), dtype=object)
        for index, line in enumerate(map):
            for idx, cell in enumerate(line):
                if cell == 'O':
                    island_map[idx,index] = Ocean()
                elif cell == 'J':
                    island_map[idx, index] = Jungle()
                elif cell == 'S':
                    island_map[idx, index] = Savannah()
                elif cell == 'D':
                    island_map[idx, index] = Desert()
                elif cell == 'M':
                    island_map[idx, index] = Mountain()


        return island_map

    def distribute_animals(self, ini_pop=None):
        standard_pop = [{'loc': (1, 1), 'pop':
            [{'species': 'Herbivore', 'age': 5, 'weight': 30}]},
                        {'loc': (1, 1), 'pop':
                            [{'species': 'Carnivore', 'age': 5, 'weight': 30}]}]
        if not ini_pop:
            population = standard_pop
        else:
            population = ini_pop
        for dictionary in population:
            self.map[dictionary['loc']].populate_cell(population['pop'])

    def populated_island(self, map=None, ini_pop=None):
        self.map = self.map_from_string(map)
        self.distribute_animals(ini_pop)