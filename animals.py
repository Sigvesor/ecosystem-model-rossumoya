# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


class Herbivore:
    def __init__(self, weight=10, F = 10, beta = 0.9, eta = 0.25):
        self.age = 0
        self.w = weight
        self.F = F
        self.beta = beta
        self.eta = eta

    def set_parameters(self, parameter):
        pass

    def aging(self):
        self.age += 1

    def weightloss(self):
        # weight reduced by mu/year
        self.w -= self.eta * self.w

    def movement(self):
        pass

    def death(self):
        pass

    def birth(self):
        pass

    def eating(self): # må vite hva som er i ruta (f), beta, F
        self.w += self.F * self.beta



