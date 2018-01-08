# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


import animals
import landscape

def test_animals():
    bulbasaur = animals.Herbivore()
    assert bulbasaur.age == 0
    bulbasaur.aging()
    w_before = bulbasaur.w
    bulbasaur.eating()
    assert bulbasaur.w > w_before
    assert bulbasaur.age == 1
    w_before = bulbasaur.w
    bulbasaur.weightloss()
    assert bulbasaur.w < w_before


