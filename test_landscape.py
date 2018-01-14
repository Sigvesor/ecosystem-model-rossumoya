# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from landscape import *
"""
PLAN for integrating savannah (and dessert):
- parameters have to be defined for each class (maybe params for dessert as default?)
- savannah's regenerate function differs from jungle
- dessert has f = 0, and does not regenerate

"""

def test_jungle():
    Jungle.set_params({'f_max': 12})
    the_jungle = Jungle(1)
    w0 = the_jungle.pop_herbs[0].weight
    assert the_jungle.f == 12
    the_jungle.eat_request()
    assert the_jungle.pop_herbs[0].weight - w0 == the_jungle.pop_herbs[0].default_params['beta'] * 10
    the_jungle.eat_request()
    assert the_jungle.pop_herbs[0].weight - w0 == the_jungle.pop_herbs[0].default_params['beta'] * 12
    the_jungle.eat_request()
    assert the_jungle.pop_herbs[0].weight - w0 == the_jungle.pop_herbs[0].default_params['beta'] * 12
    the_jungle.regenerate()
    assert the_jungle.f == 12

def test_savannah():
    Savannah.set_params({'f_max': 12})
    the_savannah = Savannah(1)
    assert type(the_savannah) == Savannah
    w0 = the_savannah.pop_herbs[0].weight
    assert the_savannah.f == 12
    the_savannah.eat_request()
    assert the_savannah.pop_herbs[0].weight - w0 == the_savannah.pop_herbs[0].default_params['beta'] * 10
    the_savannah.eat_request()
    assert the_savannah.pop_herbs[0].weight - w0 == the_savannah.pop_herbs[0].default_params['beta'] * 12
    the_savannah.eat_request()
    assert the_savannah.pop_herbs[0].weight - w0 == the_savannah.pop_herbs[0].default_params['beta'] * 12
    the_savannah.regenerate()
    #assert the_savannah.f == 12


#def test_set_params():
#  #  Landscape.set_params({'f_max': 120})
#    assert Jungle.f_max == Savannah.f_max
#    Jungle.set_params({'f_max': 100})
#    assert Jungle.f_max < Savannah.f_max


def test_reproduction():
    the_jungle = Jungle(1000)
    the_jungle.reproduction()
    assert len(the_jungle.pop_herbs) > 1000


def test_aging():
    the_jungle = Jungle(1)
    a0 = the_jungle.pop_herbs[0].age
    the_jungle.aging()
    assert the_jungle.pop_herbs[0].age - a0 == 1


def test_weightloss():
    the_jungle = Jungle(2)
    the_jungle.pop_herbs[0].weightloss()
    assert the_jungle.pop_herbs[0].weight < the_jungle.pop_herbs[1].weight


def test_death():
    the_jungle = Jungle(1000)
    the_jungle.death()
    assert len(the_jungle.pop_herbs) < 1000


def test_regenerate():
    the_jungle = Jungle(1)
    f0 = the_jungle.f
    the_jungle.eat_request()
    f1 = the_jungle.f
    assert f1 < f0
    the_jungle.regenerate()
    assert the_jungle.f == the_jungle.default_params['f_max']