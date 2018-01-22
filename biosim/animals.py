# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

import random
from math import exp as e


class Animal:
    """Animal which eat, age, mate, loose weight and die with probabilities."""

    default_params = {'w_birth': None, 'sigma_birth': None, 'beta': None,
                      'a_half': None, 'phi_age': None, 'w_half': None,
                      'phi_weight': None, 'mu': None, 'lambda': None,
                      'gamma': None, 'zeta': None, 'xi': None, 'omega': None,
                      'F': None, 'eta': None, 'DeltaPhiMax': None}

    @classmethod
    def set_parameters(cls, new_params):
        """
        Set class parameters.

        Parameters
        ----------
        new_params : dict
            Legal keys: 'w_birth', 'sigma_birth', 'beta', 'a_half',
                        'phi_age', 'w_half', 'phi_weight', 'mu', 'lambda',
                        'gamma', 'zeta', 'xi', 'omega', 'F',
                        'eta', 'DeltaPhiMax'.

        Raises
        ------
        ValueError, KeyError
        """

        params = ('w_birth', 'sigma_birth', 'beta', 'a_half',
                  'phi_age', 'w_half', 'phi_weight', 'mu', 'lambda',
                  'gamma', 'zeta', 'xi', 'omega', 'F', 'eta', 'DeltaPhiMax')

        for key in new_params:
            if key not in params:
                raise KeyError('Invalid parameter name: ' + key)

            else:

                if not isinstance(new_params[key], (int, float)):
                    raise ValueError('Invalid type of inserted key value. ' +
                                     'Expected {}'.format
                                     (type(cls.default_params[key])))
                else:
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

    def __init__(self, weight=default_params['w_birth'], age=0.0):
        """Create Animal with age 0."""
        self.weight = random.normalvariate(
            weight, self.default_params['sigma_birth'])  # + 40
        self.age = age
        phi_exp = self.default_params['phi_age'] * \
                  (self.age - self.default_params['a_half'])
        self.phi = 1 / ((1 + e(phi_exp)) * (1 + e(- phi_exp)))

    def ages(self):
        """Animal ages by one cycle."""
        self.age += 1

    def dies(self):
        """
        Decide if Animal dies.

        Returns
        -------
        bool
            True if Animal dies.
        """

        p_death = self.default_params['omega'] * (1 - self.phi)
        return random.random() < p_death

    def fitness(self):
        """
        Calculates the fitness of the Animal.

        Returns
        -------
        float
            Between [0, 1]
        """
        phi_exp = self.default_params['phi_age'] * \
                  (self.age - self.default_params['a_half'])
        self.phi = 1 / ((1 + e(phi_exp)) * (1 + e(- phi_exp)))
        return self.phi

    def birth(self, n_animals):
        """
        Decide whether a Animal will give birth.

        Returns
        -------
        bool
            True if Animal gives birth.
        """
        if self.weight < self.default_params['zeta'] *\
                (self.default_params['w_birth'] +
                    self.default_params['sigma_birth']):
            p_of_birth = 0
        else:
            p_of_birth = min([1, self.default_params['gamma'] * self.phi *
                              (n_animals - 1)])

        reproduction_successful = random.random() <= p_of_birth
        return reproduction_successful

    def weightloss(self):
        """
        Updates the weight following a weightloss of an Animal in a cycle.
        """
        self.weight -= self.default_params['eta'] * self.weight


class Herbivore(Animal):  # test that will starve in desert

    default_params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                      'a_half': 40.0, 'phi_age': 0.2, 'w_half': 10.0,
                      'phi_weight': 0.1, 'mu': 0.25, 'lambda': 1.0,
                      'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                      'omega': 0.4, 'F': 10.0, 'eta': 0.05}

    def __init__(self, weight=None, age=0):
        """Create Animal with age 0."""
        if weight is None:
            weight = self.default_params['w_birth']
        Animal.__init__(self, weight=weight, age=age)

    def eating(self, available_fodder):
        """
        Updates the weight of Herbivore after eating.
        """

        self.weight += available_fodder * self.default_params['beta']


class Carnivore(Animal):    # test that will starve w/o herbs

    default_params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                      'a_half': 60.0, 'phi_age': 0.4, 'w_half': 4.0,
                      'phi_weight': 0.4, 'mu': 0.4, 'lambda': 1.0,
                      'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
                      'omega': 0.9, 'F': 50.0,
                      'eta': 0.125, 'DeltaPhiMax': 10.0}

    def __init__(self, weight=None, age=0):
        """Create Animal with age 0."""
        if weight is None:
            weight = self.default_params['w_birth']
        Animal.__init__(self, weight=weight, age=age)

    def eating(self, available_meat):
        """
        Updates the weight of Carnivore after eating.
        """

        self.weight += available_meat * self.default_params['beta']
