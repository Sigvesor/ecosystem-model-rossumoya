# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from biosim.island import Population


def test_cycle():
    sim = Population()
    assert type(sim.cycle()) == int
