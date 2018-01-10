# -*- coding: utf-8 -*-

import random
from math import exp as e

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


class Herbivore:

    param = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
            'a_half': 40.0, 'phi_age': 0.2, 'w_half': 10.0,
            'phi_weight': 0.1, 'mu': 0.25, 'lambda': 1.0,
            'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
            'omega': 0.4, 'F': 10.0, 'eta': 0.05}

    def __init__(self, weight=12):
        self.age = 0
        self.w = weight
        self.phi = None

    @classmethod
    def set_parameters(self, parameters=param):
        for parameter in parameters:
            self.param[parameter] = parameters[parameter]

    def aging(self):
        self.age += 1

    def fitness(self):
        self.phi = 1 / (1+e(self.param['phi_age']*(self.age - self.param['a_half'])))\
                   * 1 / (1+e(-self.param['phi_weight']*(self.w - self.param['w_half'])))
        return self.phi

    def weightloss(self):
        # weight reduced by mu/year
        self.w -= self.param['eta'] * self.w

    def movement(self):
        pass

    def death(self):
        p_death = self.param['omega'] * (1 - self.phi)
        return random.random() <= p_death

    def birth(self, animals_in_cell):
        p_of_birth = min([1, self.param['gamma']*self.phi*(animals_in_cell-1)])
        return random.random() <= p_of_birth

    def eating(self, available_fodder): # må vite hva som er i ruta (f), beta, F
        self.w += available_fodder * self.param['beta']



