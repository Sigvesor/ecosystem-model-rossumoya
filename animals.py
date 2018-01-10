# -*- coding: utf-8 -*-

import random
from math import exp as e

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

dft_herbivore = {}

class Herbivore:

    gamma = 0.2
    phi_age = 0.2
    phi_weight = 0.1
    a_half = 40
    w_half = 10
    omega = 0.4

    def __init__(self, weight=12, F=10, beta=0.9, eta=0.25):
        self.age = 0
        self.w = weight
        self.F = F
        self.beta = beta
        self.eta = eta
        self.phi = None


    def set_parameters(self, parameters=dft_herbivore):
        self.parameters = parameters

    def aging(self):
        self.age += 1

    def fitness(self):
        self.phi = 1 / (1+e(self.phi_age*(self.age - self.a_half))) * 1 / (1+e(-self.phi_weight*(self.w - self.w_half)))
        return self.phi

    def weightloss(self):
        # weight reduced by mu/year
        self.w -= self.eta * self.w

    def movement(self):
        pass

    def death(self):
        p_death = self.omega * (1 - self.phi)
        return random.random() <= p_death

    def birth(self, animals_in_cell):
        p_of_birth = min([1, self.gamma*self.phi*(animals_in_cell-1)])
        return random.random() <= p_of_birth

    def eating(self, available_fodder): # må vite hva som er i ruta (f), beta, F
        self.w += available_fodder * self.beta



