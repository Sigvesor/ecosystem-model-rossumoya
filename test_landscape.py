# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

def test_jungle():
    landscape.Jungle.set_parameters({'f_max': 700})
    the_jungle = landscape.Jungle()
    assert the_jungle.f == 700
    assert the_jungle.eat_request(100) == 100
    assert the_jungle.eat_request(800) == 600
    assert the_jungle.eat_request(100) == 0
    the_jungle.regenerate()
    assert the_jungle.f == 700