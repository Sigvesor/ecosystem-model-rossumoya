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

def jungle_constructor():
    pass

def Bio_Sim():
    island_map = Jungle()
