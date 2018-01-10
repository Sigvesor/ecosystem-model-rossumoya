# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from simulation import *
import animals

def test_init():
    sim = BioSim([{'species':'Herbivore', 'age':4,'weight':15}])
    assert len(sim.herbs) == 1
    assert type(sim.herbs[0]) == animals.Herbivore

def test_simulation():
    pass

def test_map_construction():
    """
    is the map constructed correctly?
    is number of elements correct?
    is the island framed by ocean?
    does the type of each element correspond to the input?
    :return:
    """
    # assert type(island_map) == pd.core.frame.DataFrame
    pass

def test_animal_placement():
    """
    is the right number of animals created?

    :return:
    """
    pass

def test_eating():
    """
    the animal is eating if fodder in cell. the fodder of the cell is reduced,
    weight of animal increased.
    """
    pass

def test_eating_order():
    """
    are the animals getting ordered so that the fittest get to feed
    and the unfit starve?
    :return:
    """
    pass

def test_population_growth():
    """
    is the population growing in an resource rich environment?
    give rich environment and count number of individuals
    :return:
    """
    pass

def test_population_decline():
    """ test that the population declines as a result of death due to
    limited resources, and that the list of animals declines"""
    pass
