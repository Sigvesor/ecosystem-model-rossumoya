# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

import pandas as pd
from landscape import *
from animals import *
"""
plan:

make map
make animals and place
for _ in nrounds:
    1. order by fitness
    2. for animal:
            sim_eat(animal)
            update phi
    3. mate and add new animals
    4. if animal.phi !=  None:
        ageing()
        weightloss()
        death()
    update phi
    regenerate fodder
"""

class BioSim:

    def __init__(self, ini_pop):

        """
        sim = BioSim([{'species':'Herbivore'}, {'species':'Carnivore'}])
        sim.herbs
        :param ini_pop:
        """

        island_map = Jungle()
 #       for individual in ini_pop:

        self.herbs = [Herbivore(weight=ini_pop[n]['weight'],
                                age=ini_pop[n]['age']) for
                                n in range(len(ini_pop))
                        if ini_pop[n]['species'] == 'Herbivore']



    def simulate(self): #, num_steps=100, vis_steps=1, img_steps=2000):
        pass

    def add_population(self): # , population):
        pass
