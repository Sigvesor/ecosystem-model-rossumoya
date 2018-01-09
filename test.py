# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


import animals
import landscape

def test_animals():
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


def test_jungle():
    landscape.Jungle.set_parameters({'f_max': 700})
    the_jungle = landscape.Jungle()
    assert the_jungle.f == 700
    assert the_jungle.eat_request(100) == 100
    assert the_jungle.eat_request(800) == 600
    assert the_jungle.eat_request(100) == 0
    the_jungle.regenerate()
    assert the_jungle.f == 700


def test_simulation():
    # should perform jungle_instance.eating_requeast(herbivore_instance.F)


