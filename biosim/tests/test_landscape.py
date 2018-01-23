# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from biosim.landscape import *


def test_jungle():
    """
    Tests that a jungle is an instance of Jungle.
    Also tests if updating parameters works correctly.
    """
    jungle = Jungle()
    assert isinstance(jungle, Jungle)
    assert jungle.default_params['f_max'] == 800.0
    Jungle.set_parameters({'f_max': 200})
    jungle = Jungle()
    assert jungle.default_params['f_max'] == 200.0


def test_savannah():
    """
    Tests that a jungle is an instance of Jungle.
    Also tests if updating parameters works correctly.
    """
    savannah = Savannah()
    assert isinstance(savannah, Savannah)
    assert savannah.default_params['f_max'] == 300.0
    Savannah.set_parameters({'f_max': 200})
    savannah = Savannah()
    assert savannah.default_params['f_max'] == 200.0


def test_desert():
    """
    Tests that a desert is an instance of Desert.
    Also tests if there's no food in desert.
    """

    desert = Desert()
    assert isinstance(desert, Desert)
    assert desert.default_params['f_max'] == 0


def test_num_herbs():
    """Tests that it counts number of Herbivore in landscape."""

    land = Landscape()
    land.pop_animals[0].append(Herbivore())
    assert land.num_herbs == 1


def test_num_carns():
    """Tests that it counts number of Carnivore in landscape."""

    land = Landscape()
    land.pop_animals[1].append(Carnivore())
    assert land.num_carns == 1


def test_fitness_sort():
    """Tests that it sorts fitness correctly, descending."""
    jungle = Jungle()
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[1].append(Carnivore())
    jungle.pop_animals[1].append(Carnivore())
    jungle.pop_animals[1].append(Carnivore())

    jungle.fitness_sort()

    phi1 = jungle.pop_animals[0][0].phi
    phi2 = jungle.pop_animals[0][1].phi
    phi3 = jungle.pop_animals[0][2].phi
    phi4 = jungle.pop_animals[1][0].phi
    phi5 = jungle.pop_animals[1][1].phi
    phi6 = jungle.pop_animals[1][2].phi

    assert phi1 > phi2
    assert phi2 > phi3
    assert phi4 > phi5
    assert phi5 > phi6


def test_eat_request_herb():
    """Tests if Herbivore eat in landscape"""

    jungle = Jungle()
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    w0 = jungle.sum_herb_mass
    jungle.eat_request_herb()
    w1 = jungle.sum_herb_mass
    assert w1 > w0


def test_eat_requests_carn():
    """Tests if Carnivore eat in landscape"""

    Carnivore.set_parameters({'w_birth': 500, 'DeltaPhiMax': 0.0000000001})
    jungle = Jungle()
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[1].append(Carnivore())
    jungle.fitness_sort()

    carn = jungle.pop_animals[1][0]
    w0 = carn.weight
    weight_herb = jungle.sum_herb_mass
    jungle.eat_request_carn()
    assert len(jungle.pop_animals[0]) == 0
    assert carn.weight == w0 + (weight_herb * carn.default_params['beta'])













#def test_reproduction():
#    Landscape.set_parameters({'f_max'} )
#    land = Landscape()
#
#
#
#
#
#def test_reproduction():
#    the_jungle = Jungle(100, 10)
#    for herb in the_jungle.pop_animals[0]:
#        herb.weight = 100.0
#    for carn in the_jungle.pop_animals[1]:
#        carn.weight = 100.0
#    the_jungle.reproduction()
#    assert len(the_jungle.pop_animals[0]) > 100
#    assert len(the_jungle.pop_animals[1]) > 10
#
#
#def test_aging():
#    the_jungle = Jungle(1, 1)
#    a0h = the_jungle.pop_animals[0][0].age
#    a0c = the_jungle.pop_animals[1][0].age
#    the_jungle.aging()
#    assert the_jungle.pop_animals[0][0].age - a0h == 1
#    assert the_jungle.pop_animals[1][0].age - a0c == 1
#
#
#def test_weightloss():
#    the_jungle = Jungle(1, 1)
#    w0_herb = the_jungle.pop_animals[0][0].weight
#    w0_carn = the_jungle.pop_animals[1][0].weight
#
#    the_jungle.pop_animals[0][0].weightloss()
#    the_jungle.pop_animals[1][0].weightloss()
#
#    assert w0_herb > the_jungle.pop_animals[0][0].weight
#    assert w0_carn > the_jungle.pop_animals[1][0].weight
#
#
#def test_death():
#    the_jungle = Jungle(1000, 100)
#    the_jungle.death()
#    assert len(the_jungle.pop_animals[0]) < 1000 and len(the_jungle.pop_animals[1]) < 100
#
#
#def test_regenerate_jungle():
#    the_jungle = Jungle(1)
#    f0 = the_jungle.f
#    the_jungle.eat_request()
#    f1 = the_jungle.f
#    assert f1 < f0
#    the_jungle.regenerate()
#    assert the_jungle.f == the_jungle.default_params['f_max']
#
#
#def test_regenerate_savannah():
#    Savannah.set_params({'f_max': 300})
#    the_savannah = Savannah(1)
#    f0 = the_savannah.f
#    the_savannah.eat_request()
#    f1 = the_savannah.f
#    assert f1 < f0
#    the_savannah.f = 0
#    the_savannah.regenerate()
#    assert the_savannah.f < the_savannah.default_params['f_max']
#
#
#def test_eat_request():
#    the_jungle = Jungle(100, 10)
#    w0_herb = sum([herb.weight for herb in the_jungle.pop_animals[0]])/len(the_jungle.pop_animals[0])
#    w0_carn = sum([carn.weight for carn in the_jungle.pop_animals[1]])
#    the_jungle.eat_request()
#    assert sum([herb.weight for herb in the_jungle.pop_animals[0]])/len(the_jungle.pop_animals[0]) > w0_herb
#    assert sum([carn.weight for carn in the_jungle.pop_animals[1]]) > w0_carn
#
#def test_migration()
#    kart = """OOOO
#    OJJO
#    OOOO"""
#   population = [Herbivore() for i in range(100)]
#    sim = BioSim(island_map=kart, ini_pop=population, seed=1234)
#    sim.island.map[]