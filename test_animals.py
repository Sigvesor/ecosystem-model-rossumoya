# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


from animals import *


def test_biocycle_herbivore():
    herbivore = Herbivore()
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
    carnivore = Carnivore()
    assert carnivore.age == 0
    carnivore.ages()
    w0 = carnivore.weight
    carnivore.eating(100)
    assert carnivore.weight > w0
    assert carnivore.age == 1
    w0 = carnivore.weight
    carnivore.weightloss()
    assert carnivore.weight < w0


def test_fitness():
    anim = Animal()
    anim.fitness()
    fit1 = anim.phi
    assert 0 <= fit1 <= 1
    anim.ages()
    anim.fitness()
    fit2 = anim.phi
    assert fit1 > fit2
    anim.weightloss()
    anim.fitness()
    fit3 = anim.phi
    assert fit2 > fit3


def test_birth():
    Animal.set_params({'zeta': 0.0})
    anim = Animal()
    anim.fitness()
    assert not anim.birth(1)
    assert anim.birth(10000000)


def test_death():
    anim = Animal()
    anim.default_params['omega'] = 1
    anim.phi = 0
    assert anim.dies()
    anim.phi = 1
    assert not anim.dies()



