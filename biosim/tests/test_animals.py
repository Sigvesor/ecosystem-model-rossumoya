# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


from biosim.animals import *


def test_biocycle_herbivore():
    """
    Tests that an instance of Herbivore is a Herbivore, starts with
    age 0, ages correctly, eats and puts on weight, and loose weight
    following a weight loss.
    """

    herbivore = Herbivore()
    assert isinstance(herbivore, Herbivore)
    assert herbivore.age == 0
    herbivore.ages()
    w0 = herbivore.weight
    herbivore.eating(100)
    assert herbivore.weight > w0
    assert herbivore.age == 1
    w0 = herbivore.weight
    herbivore.weightloss()
    assert herbivore.weight < w0


def test_biocycle_carnivore():
    """
    Tests that an instance of Carnivore is a Carnivore, starts with
    age 0, ages correctly, eats and puts on weight, and loose weight
    following a weight loss.
    """

    carnivore = Carnivore()
    assert isinstance(carnivore, Carnivore)
    assert carnivore.age == 0
    carnivore.ages()
    w0 = carnivore.weight
    carnivore.eating(100)
    assert carnivore.weight > w0
    assert carnivore.age == 1
    w0 = carnivore.weight
    carnivore.weightloss()
    assert carnivore.weight < w0


def test_fitness_herb():
    """Tests that the fitness of an instance of Herbivore works correctly"""

    herb = Herbivore()
    herb.fitness()
    fit1 = herb.phi
    assert 0 <= fit1 <= 1
    herb.ages()
    herb.fitness()
    fit2 = herb.phi
    assert fit2 < fit1
    herb.weightloss()
    herb.fitness()
    fit3 = herb.phi
    assert fit2 > fit3


def test_fitness_carn():
    """Tests that the fitness of an instance of Herbivore works correctly"""

    carn = Herbivore()
    carn.fitness()
    fit1 = carn.phi
    assert 0 <= fit1 <= 1
    carn.ages()
    carn.fitness()
    fit2 = carn.phi
    assert fit2 < fit1
    carn.weightloss()
    carn.fitness()
    fit3 = carn.phi
    assert fit2 > fit3


def test_birth_herb():
    """
    Tests that the Herbivore will give birth when it shall,
    and not give birth when it shouldn't.
    """

    Herbivore.set_parameters({'zeta': 0.0})
    herb = Herbivore()
    herb.fitness()
    assert not herb.birth(1)
    assert herb.birth(100000)


def test_birth_carn():
    """
    Tests that the Carnivore will give birth when it should,
    and not give birth when it shouldn't.
    """

    Carnivore.set_parameters({'zeta': 0.0})
    carn = Carnivore()
    carn.fitness()
    assert not carn.birth(1)
    assert carn.birth(100000)


def test_death_carn():
    """
    Tests that Carnivore will die when probability of death is 100%,
    and that it will not die when the probability of death is 0%.
    """

    carn = Carnivore()
    carn.default_params['omega'] = 1
    carn.phi = 0
    assert carn.dies()
    carn.phi = 1
    assert not carn.dies()


def test_death_herb():
    """
    Tests that Carnivore will die when probability of death is 100%,
    and that it will not die when the probability of death is 0%.
    """

    herb = Herbivore()
    herb.default_params['omega'] = 1
    herb.phi = 0
    assert herb.dies()
    herb.phi = 1
    assert not herb.dies()



