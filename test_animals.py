# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


import animals

def test_year():
    herbivore = animals.Herbivore()
    assert herbivore.age == 0
    herbivore.aging()
    w_before = herbivore.w
    herbivore.eating(100)
    assert herbivore.w > w_before
    assert herbivore.age == 1
    w_before = herbivore.w
    herbivore.weightloss()
    assert herbivore.w < w_before

def test_fitness():
    herbivore = animals.Herbivore()
    herbivore.fitness()
    fit1 = herbivore.phi
    assert 0 <= fit1 <= 1
    herbivore.aging()
    herbivore.fitness()
    fit2 = herbivore.phi
    assert fit1 > fit2
    herbivore.weightloss()
    herbivore.fitness()
    fit3 = herbivore.phi
    assert fit2 > fit3

def test_birth():
    herbivore = animals.Herbivore()
    herbivore.fitness()
    assert not herbivore.birth(1)
    assert herbivore.birth(100000)

def test_death():
    herbivore = animals.Herbivore()
    herbivore.omega = 1
    herbivore.phi = 0
    assert herbivore.death()
    herbivore.phi = 1
    assert not herbivore.death()
