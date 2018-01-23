# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

import random
from math import exp as e
from landscape import *


class Animal:
    """
    Animal which eat, age, reproduce,
    migrate and die with probabilities.
    """

    default_params = {'w_birth': None, 'sigma_birth': None, 'beta': None,
                      'a_half': None, 'phi_age': None, 'w_half': None,
                      'phi_weight': None, 'mu': None, 'lambda': None,
                      'gamma': None, 'zeta': None, 'xi': None, 'omega': None,
                      'F': None, 'eta': None, 'DeltaPhiMax': None}

    @classmethod
    def set_parameters(cls, new_params):
        """
        Set class parameters. Checks if input is in the right format.

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

        tuples = ('w_birth', 'w_half', 'a_half', 'gamma',
                  'zeta', 'xi', 'F', 'DeltaPhiMax')

        fractions = ('beta', 'eta', 'sigma_birth', 'phi_age', 'phi_weight',
                     'mu', 'lambda', 'omega')

        for key in new_params:
            if key not in tuples and key not in fractions:
                raise KeyError('Invalid parameter name: ' + key)

            else:

                if not isinstance(new_params[key], (int, float)):
                    raise ValueError('Invalid type of inserted key value. ' 
                                     'Expected {}'.format
                                     (type(cls.default_params[key])))

                elif key in tuples and new_params[key] < 0:
                    raise ValueError(str(key) + ' must have positive value.')

                elif key in fractions and not (0 < new_params[key] < 1):
                    raise ValueError(str(key) + ' must have value from ' 
                                                '0 to 1.')

                else:
                    cls.default_params[key] = new_params[key]

    @classmethod
    def get_params(cls):
        """
        Get class parameters.
        :return: Dict, with class parameters.
        """

        return cls.default_params

    def __init__(self, weight=default_params['w_birth'], age=0.0):
        """Create Animal with age 0 and birth weight."""

        self.weight = random.normalvariate(
            weight, self.default_params['sigma_birth'])  # + 40
        self.age = age
        #phi_exp = self.default_params['phi_age'] * \
        #          (self.age - self.default_params['a_half'])
        #self.phi = (1 / 1 + e(phi_exp)) * (1 / (1 + e(- phi_exp)))
        self.phi = 1 / (1 + e(self.default_params['phi_age'] *
                              (self.age - self.default_params['a_half']))) \
            * 1 / (1 + e(-self.default_params['phi_weight'] *
                         (self.weight - self.default_params['w_half'])))

    def ages(self):
        """Animal ages by one cycle."""

        self.age += 1

    def dies(self):
        """
        Decide if Animal dies.
        :return: Bool, True if Animal dies.
        """

        p_death = self.default_params['omega'] * (1 - self.phi)
        return random.random() < p_death

    def fitness(self):
        """
        Calculates the fitness of the Animal.
        :return: Float, between [0, 1]
        """

        #phi_exp = self.default_params['phi_age'] * \
        #          (self.age - self.default_params['a_half'])
        #self.phi = (1 / (1 + e(phi_exp))) * (1 /  (1 + e(- phi_exp)))
        self.phi = 1 / (1 + e(self.default_params['phi_age'] *
                              (self.age - self.default_params['a_half']))) \
            * 1 / (1 + e(-self.default_params['phi_weight'] *
                         (self.weight - self.default_params['w_half'])))

        return self.phi

    def birth(self, n_animals):
        """
        Decides whether an Animal will give birth.
        :param n_animals: Total number of that species, in that landscape.
        :return: Bool, True if animal gives birth.
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
        Updates the weight, following a weight loss,
        of an Animal in a cycle.
        """

        self.weight -= self.default_params['eta'] * self.weight

    @property
    def migrating(self):
        return random.random() < self.default_params['mu'] * self.phi

    @property
    def is_herbivore(self):
        return isinstance(self, Herbivore)

    @property
    def is_carnivore(self):
        return isinstance(self, Carnivore)

    #def moving_propensity(self, epsilon):
    #    illegal = (Mountain, Ocean)
    #    if isinstance(self, illegal):
    #        return 0
    #    else:
    #        return e(animal.default_params['lambda'] * epsilon)
    #def new_habitat(self, neighbours):
#
#
#
    #    if isinstance(self, Herbivore):
    #        prop_list = [self.moving_propensity(
    #                        animal=self,
    #                        epsilon=neighbour.abundance_fodder_herb
    #                        ) for neighbour in neighbours]
    #    elif isinstance(self, Carnivore):
    #        prop_list = [self.moving_propensity(
    #                        animal=self,
    #                        epsilon=neighbour.abundance_fodder_carn
    #                        ) for neighbour in neighbours]


class Herbivore(Animal):  # test that will starve in desert
    """
    Herbivore. Underclass of superclass Animal,
    with its default parameters.
    """

    default_params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                      'a_half': 40.0, 'phi_age': 0.2, 'w_half': 10.0,
                      'phi_weight': 0.1, 'mu': 0.25, 'lambda': 1.0,
                      'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                      'omega': 0.4, 'F': 10.0, 'eta': 0.05}

    def __init__(self, weight=None, age=0):
        """Creates a Herbivore with age 0."""

        if weight is None:
            weight = self.default_params['w_birth']
        Animal.__init__(self, weight=weight, age=age)

    def eating(self, available_fodder):
        """Updates the weight of Herbivore after eating."""

        self.weight += available_fodder * self.default_params['beta']

    def new_grassland(self, neighbours):
        props = [n.propensity(self, n.abundance_fodder_c) for n in neighbours]
        prob_list = [prop / sum(props) for prop in props]
        p = random.random()
        i = 0
        while p > sum(prob_list[0:i]):
            i += 1
        return neighbours[i - 1].new_pop[0]


class Carnivore(Animal):    # test that will starve w/o herbs
    """
    Carnivore. Underclass of superclass Animal,
    with its default parameters.
    """

    default_params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                      'a_half': 60.0, 'phi_age': 0.4, 'w_half': 4.0,
                      'phi_weight': 0.4, 'mu': 0.4, 'lambda': 1.0,
                      'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
                      'omega': 0.9, 'F': 50.0,
                      'eta': 0.125, 'DeltaPhiMax': 10.0}

    def __init__(self, weight=None, age=0):
        """Creates a Carnivore with age 0."""

        if weight is None:
            weight = self.default_params['w_birth']
        Animal.__init__(self, weight=weight, age=age)

    def eating(self, available_meat):
        """Updates the weight of Carnivore after eating."""

        self.weight += available_meat * self.default_params['beta']

    def new_huntingground(self, neighbours):
        props = [n.propensity(self, n.abundance_fodder_c) for n in neighbours] # [neighbours[i].propensity(self, epsilons[i]) for i in range(len(epsilons))]
        prob_list = [prop / sum(props) for prop in props]
        p = random.random()
        i = 0
        while p > sum(prob_list[0:i]):
            i += 1
        return neighbours[i - 1].new_pop[1]