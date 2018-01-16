# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from landscape import *


class Population:
    """A population with many jungles"""

    def __init__(self, n_pops=1, n_num_herbs=10, n_num_carns=2):
        """
        Parameters:
        ----------
        n_pops : int
            number of Herbivore populations
        """



        self.pops = [Jungle(n_num_herbs, n_num_carns) for _ in range(n_pops)]

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




