# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

##import pytest
##
##from ..simulation import *
##
##
##@pytest.fixture(autouse=True)
##def simulation_environment():
##    island_map = """OOO
##    OJO
##    OOO"""
##    ini_pop = [{'loc':(1,1),
##                   'pop': [{'species': 'Herbivore', 'age': 4, 'weight': 15}
##                           for i in range(10)]}]
##    sim = island_map,ini_pop,1234
##    return island_map, ini_pop

#def test_init():
#    sim = BioSim([{'species': 'Herbivore', 'age': 4, 'weight': 15}])
#    assert len(sim.herbs) == 1
#    assert type(sim.herbs[0]) == animals.Herbivore

#def test_environment():
#   island_map = """OOO
#       OJO
#       OOO"""
#   ini_pop = [{'loc': (1, 1),
#               'pop': [{'species': 'Herbivore', 'age': 4, 'weight': 15}
#                       for i in range(10)]}]
#   cell = BioSim(island_map, ini_pop, 1234).island.map[(1,1)]
#   assert type(cell) == Jungle

##def test_simulate():
#    island_map = """OOO
#        OJO
#        OOO"""
#    ini_pop = [{'loc': (1, 1),
#                'pop': [{'species': 'Herbivore', 'age': 4, 'weight': 15}
#                        for i in range(10)]}]
#    short_sim = BioSim(island_map, ini_pop, 1234).simulate(5)
#    assert type(short_sim) == list
#    assert type(short_sim[0]) == list
#    assert type(short_sim[0][0]) == list
#

#map_construction():
#
#e map constructed correctly?
#mber of elements correct?
#e island framed by ocean?
#the type of each element correspond to the input?
#rn:
#
#ert type(island_map) == pd.core.frame.DataFrame
#


#animal_placement():
#
#e right number ##of animals created?

#rn:
#
#


#def test_eating():
#    """
#    the animal is eating if fodder in cell. the fodder of the cell is reduced,
#    weight of animal increased.
#    """
#    sim = BioSim([{'species': 'Herbivore', 'age': 4, 'weight': 15}])
#    w0 = sim.herbs[0].w
#    f0 = sim.map.f
#    sim.herbs[0].eating(sim.map.eat_request(sim.herbs[0].param['F']))
#    w1 = sim.herbs[0].w
#    f1 =# sim.map.f
#    assert w1 > w0
#    assert f0 - f1 == 10
#    sim.map.f = 8
#    sim.herbs[0].eating(sim.map.eat_request(sim.herbs[0].param['F']))
#    assert sim.map.f == 0
#    assert sim.map.eat_request(sim.herbs[0].param['F']) == 0


#def test_eating_order():
#    """
#    are the animals getting ordered so that the fittest get to feed
#    and the unfit starve?
#    :return:
#    """
#    pass
#
#
#def test_population_growth():
#    """
#    is the population growing in an resource rich environment?
#    give rich environment and count number of individuals
#    :return:
#    """
#    pass
#
#
#def test_population_decline():
#    """ test that the population declines as a result of death due to
#    limited resources, and that the list of animals declines"""
#    pass
#
#