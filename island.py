# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from landscape import Jungle


class Population:
    """A population with many jungles"""

    def __init__(self, n_pops=1, n_num_herbs=10):
        """
        Parameters:
        ----------
        n_pops : int
            number of Herbivore populations
        """

        self.pops = [Jungle(n_num_herbs) for _ in range(n_pops)]

    def cycle(self):
        """Update all populations by one cycle."""

        for pop in self.pops:

            pop.fitness_sort()
            pop.eat_request()
            pop.reproduction()
            pop.aging()
            pop.weightloss()
            pop.death()
            pop.regenerate()

            return len(pop.pop_herbs)




