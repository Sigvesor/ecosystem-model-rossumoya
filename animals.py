# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

import random
from math import exp as e


class Herbivore:
    """Herbiwars which mate, multiply and die with fixed probabilities."""

    default_params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                      'a_half': 40.0, 'phi_age': 0.2, 'w_half': 10.0,
                      'phi_weight': 0.1, 'mu': 0.25, 'lambda': 1.0,
                      'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                      'omega': 0.4, 'F': 10.0, 'eta': 0.05}

    @classmethod
    def set_params(cls, new_params):
        """
        Set class parameters.

        Parameters
        ----------
        new_params : dict
            Legal keys: 'w_birth', 'sigma_birth', 'beta', 'a_half',
                        'phi_age', 'w_half', 'phi_weight', 'mu', 'lambda',
                        'gamma', 'zeta', 'xi', 'omega', 'F', 'eta'

        Raises
        ------
        ValueError, KeyError
        """

        params = ('w_birth', 'sigma_birth', 'beta', 'a_half',
                  'phi_age', 'w_half', 'phi_weight', 'mu', 'lambda',
                  'gamma', 'zeta', 'xi', 'omega', 'F', 'eta')

        for key in new_params:
            if key not in params:
                raise KeyError('Invalid parameter name: ' + key)

            if key in params:
            #    if not type(default_params[key]):
            #        raise ValueError('Invalid type of inserted key value')
#
                cls.default_params[key] = new_params[key]

    @classmethod
    def get_params(cls):
        """
        Get class parameters.

        Returns
        -------
        dict
            Dictionary with class parameters.
        """

        return cls.default_params

    def __init__(self, weight=8.0, age=0.0):
        """Create Herbivore with age 0."""
        self.weight = weight
        self.age = age
        self.phi = None

    def ages(self):
        """Herbivoar ages by one cycle."""
        self.age += 1

    def dies(self):
        """
        Decide if Herbivore dies.

        Returns
        -------
        bool
            True if Herbivore dies.
        """

        p_death = self.default_params['omega'] * (1 - self.phi)
        return random.random() < p_death

    def fitness(self):
        """
        Calculates the fitness of the Herbivoar.

        Returns
        -------
        float
            Between [0, 1]
        """
        self.phi = 1 / (1+e(self.default_params['phi_age']*(self.age - self.default_params['a_half'])))\
            * 1 / (1+e(-self.default_params['phi_weight']*(self.weight - self.default_params['w_half'])))
        return self.phi

    def birth(self, pop_herbs):
        """
        Decide whether a Herbivore will give birth.

        Returns
        -------
        bool
            True if Herbivore gives birth.
        """

        p_of_birth = min([1, self.default_params['gamma'] * self.phi * (pop_herbs - 1)])
        return random.random() <= p_of_birth

    def eating(self, available_fodder):
        """
        Updates the weight of Herbivore after eating.
        """

        self.weight += available_fodder * self.default_params['beta']

    def weightloss(self):
        """
        Updates the weight following weightloss of Herbivore in a cycle.
        """
        self.weight -= self.default_params['eta'] * self.weight




