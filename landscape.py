# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


class Landscape(object):

    def __init__(self, x_val, y_val):
        self.x_val = x_val
        self.y_val = y_val


class Ocean(Landscape):


class Mountains(Landscape):


class Jungle(Landscape):
    def __init__(self, f_max=800.0):
        self.f = f_max


class Savannah(Landscape):
    def __init__(self, f_max=300.0):
        self.f = f_max
