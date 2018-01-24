# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from ..landscape import *


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


def test_update_fitness():
    """
    Tests if fitness is being updated for animals in the landscape.
    """

    jungle = Jungle()
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[1].append(Carnivore())
    f0_herb = jungle.pop_animals[0][0].phi
    f0_carn = jungle.pop_animals[1][0].phi
    jungle.weightloss()
    jungle.update_fitness()
    f1_herb = jungle.pop_animals[0][0].phi
    f1_carn = jungle.pop_animals[1][0].phi
    assert f0_herb > f1_herb
    assert f0_carn > f1_carn


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
    jungle.pop_animals[1].append(Carnivore())
    jungle.fitness_sort()

    w0 = jungle.pop_animals[1][0].weight
    jungle.eat_request_carn()
    w1 = jungle.pop_animals[1][0].weight
    assert len(jungle.pop_animals[0]) == 0
    assert w0 < w1


def test_death():
    """
    Tests if animals die when they should.
    """

    Herbivore.set_parameters({'omega': 1})
    Carnivore.set_parameters({'omega': 1})
    jungle = Jungle()
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[1].append(Carnivore())
    jungle.pop_animals[0][0].phi = 0
    jungle.pop_animals[1][0].phi = 0
    jungle.death()
    assert len(jungle.pop_animals[0]) == 0
    assert len(jungle.pop_animals[1]) == 0


def test_weightloss():
    """
    Tests if an animal looses weight following a weight loss.
    """

    jungle = Jungle()
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[1].append(Carnivore())
    w0_herb = jungle.pop_animals[0][0].weight
    w0_carn = jungle.pop_animals[1][0].weight
    jungle.weightloss()
    w1_herb = jungle.pop_animals[0][0].weight
    w1_carn = jungle.pop_animals[1][0].weight
    assert w0_herb > w1_herb
    assert w0_carn > w1_carn


def test_reproduction_herb():
    """
    Tests if reproduction works and new animals are being born, when the
    chance of birth are guaranteed. Same method for testing carnivores.
    """

    Herbivore.set_parameters({'zeta': 0})
    jungle = Jungle()
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[0][0].default_params['gamma'] = 1
    jungle.pop_animals[0][1].default_params['gamma'] = 1
    jungle.pop_animals[0][0].phi = 1
    jungle.pop_animals[0][1].phi = 1
    n0 = len(jungle.pop_animals[0])
    jungle.reproduction()
    n1 = len(jungle.pop_animals[0])
    assert n1 > n0


def test_aging():
    """
    Tests if animals in the landscape ages.
    """
    jungle = Jungle()
    jungle.pop_animals[0].append(Herbivore())
    jungle.pop_animals[1].append(Carnivore())
    jungle.aging()
    assert jungle.pop_animals[0][0].age == 1
    assert jungle.pop_animals[1][0].age == 1


def test_regenerate():
    """
    Tests if Jungle- and Savannah landscapes regenerate fodder.
    """
    jungle = Jungle()
    savannah = Savannah()
    desert = Desert()
    mountain = Mountain()
    ocean = Ocean()

    desert.f = 0
    jungle.f = 0
    savannah.f = 0
    ocean.f = 0
    mountain.f = 0

    jungle.regenerate()
    savannah.regenerate()
    desert.regenerate()
    mountain.regenerate()
    ocean.regenerate()

    assert jungle.f > 0
    assert savannah.f > 0
    assert desert.f == 0
    assert mountain.f == 0
    assert ocean.f == 0


#def test_abundance_fodder_herb():
#    """
#    Tests that the abundance of fodder in
#    Jungle > Savannah > Desert == Ocean == Mountain, when new instance.
#    """
#
#    desert = Desert()
#    jungle = Jungle()
#    savannah = Savannah()
#    ocean = Ocean()
#    mountain = Mountain()
#
#    assert jungle.abundance_fodder_h > savannah.abundance_fodder_h
#    assert savannah.abundance_fodder_h > desert.abundance_fodder_h
#    assert desert.abundance_fodder_h == ocean.abundance_fodder_h
#    assert ocean.abundance_fodder_h == mountain.abundance_fodder_h


def test_abundance_fodder_carn():
    """
    Tests that the abundance of food for Carnivores is bigger
    in a landscape with more Herbivores.
    """

    jungle1 = Jungle()
    jungle2 = Jungle()

    jungle1.pop_animals[0].append(Herbivore())
    jungle1.pop_animals[0].append(Herbivore())
    jungle2.pop_animals[0].append(Herbivore())

    assert jungle1.abundance_fodder_c > jungle2.abundance_fodder_c


#def test_pro#pensity():

    


