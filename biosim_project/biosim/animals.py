# -*- coding: utf-8 -*-

import random
from math import exp as e

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


class Animal:
    """
    This class instantiates an animal
    """

    default_params = {'w_birth': None, 'sigma_birth': None, 'beta': None,
                      'a_half': None, 'phi_age': None, 'w_half': None,
                      'phi_weight': None, 'mu': None, 'lambda': None,
                      'gamma': None, 'zeta': None, 'xi': None, 'omega': None,
                      'F': None, 'eta': None, 'DeltaPhiMax': None}

    @classmethod
    def set_parameters(cls, new_params):
        """
        Set class parameters and checks if input is in the right format

        :type cls: Animal
        :param new_params: dict
            Legal keys: 'w_birth', 'sigma_birth', 'beta', 'a_half',
                        'phi_age', 'w_half', 'phi_weight', 'mu', 'lambda',
                        'gamma', 'zeta', 'xi', 'omega', 'F',
                        'eta', 'DeltaPhiMax'
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

                elif key in fractions and not (0 <= new_params[key] <= 1):
                    raise ValueError(str(key) + ' must have value from ' 
                                                '0 to 1.')

                else:
                    cls.default_params[key] = new_params[key]

    @classmethod
    def get_params(cls):
        """
        Get class parameters

        :return: dict
        """

        return cls.default_params

    def __init__(self, weight=default_params['w_birth'], age=0.0):
        """
        Creates the variables associated with the class
        """

        self.weight = random.normalvariate(
            weight, self.default_params['sigma_birth'])
        self.age = age
        self.phi = 1 / (1 + e(self.default_params['phi_age'] *
                              (self.age - self.default_params['a_half']))) \
            * 1 / (1 + e(-self.default_params['phi_weight'] *
                         (self.weight - self.default_params['w_half'])))

    def ages(self):
        """
        Animal ages by one cycle
        """

        self.age += 1

    def dies(self):
        """
        Decides if Animal dies

        :return: bool
        """

        p_death = self.default_params['omega'] * (1 - self.phi)
        return random.random() < p_death

    def fitness(self):
        """
        Calculates the fitness of the Animal

        :return: float
        """

        self.phi = 1 / (1 + e(self.default_params['phi_age'] *
                              (self.age - self.default_params['a_half']))) \
            * 1 / (1 + e(-self.default_params['phi_weight'] *
                         (self.weight - self.default_params['w_half'])))

        return self.phi

    def birth(self, n_animals):
        """
        Decides whether an Animal will give birth or not

        :param n_animals: int
        :return: bool
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
        Updates the weight, following an animal's weightloss during cycle
        """

        self.weight -= self.default_params['eta'] * self.weight

    @property
    def migrating(self):
        """
        Decides whether the animal is ready to migrate, or not

        :return: bool
        """
        return random.random() < self.default_params['mu'] * self.phi

    @property
    def is_herbivore(self):
        """
        Returns whether the animal is a Herbivore, or not

        :return: bool
        """

        return isinstance(self, Herbivore)

    @property
    def is_carnivore(self):
        """
        Returns whether the animal is a Carnivore, or not

        :return: bool
        """

        return isinstance(self, Carnivore)


class Herbivore(Animal):
    """
    Underclass of superclass Animal, Herbivore, with its default parameters.
    """

    default_params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                      'a_half': 40.0, 'phi_age': 0.2, 'w_half': 10.0,
                      'phi_weight': 0.1, 'mu': 0.25, 'lambda': 1.0,
                      'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                      'omega': 0.4, 'F': 10.0, 'eta': 0.05}

    def __init__(self, weight=None, age=0):
        """
        Creates the variables associated with the underclass
        """

        if weight is None:
            weight = self.default_params['w_birth']
        Animal.__init__(self, weight=weight, age=age)

    def eating(self, available_fodder):
        """
        Updates the weight of Herbivore after eating
        """

        self.weight += available_fodder * self.default_params['beta']

    def new_grassland(self, neighbours):
        """
        Decides where the migrating herbivore will migrate

        :param neighbours: list
        :return: list
        """
        props = [n.propensity(self, n.abundance_fodder_h) for n in neighbours]
        prob_list = [prop / sum(props) for prop in props]
        p = random.random()
        i = 0
        while p > sum(prob_list[0:i]):
            i += 1
        return neighbours[i - 1].new_pop[0]


class Carnivore(Animal):
    """
    Underclass of superclass Animal, Carnivore, with its default parameters.
    """

    default_params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                      'a_half': 60.0, 'phi_age': 0.4, 'w_half': 4.0,
                      'phi_weight': 0.4, 'mu': 0.4, 'lambda': 1.0,
                      'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
                      'omega': 0.9, 'F': 50.0,
                      'eta': 0.125, 'DeltaPhiMax': 10.0}

    def __init__(self, weight=None, age=0):
        """
        Creates the variables associated with the underclass
        """

        if weight is None:
            weight = self.default_params['w_birth']
        Animal.__init__(self, weight=weight, age=age)

    def prob_eating(self, herbivore):
        """
        Decides the probability of carnivore eating herbivore

        :param herbivore: object
        :return: float
        """

        delta_phi = self.phi - herbivore.phi
        delta_phi_max = self.default_params['DeltaPhiMax']

        if delta_phi <= 0.:
            return 0
        elif 0. < delta_phi < delta_phi_max:
            return delta_phi / delta_phi_max
        else:
            return 1

    def eating(self, herbs):
        """
        Updates the weight of carnivore after eating herbivore(s)
        Returns a list of surviving herbivores

        :param herbs: list
        :return: list
        """

        survivors = []
        eaten = 0

        for herb in herbs[::-1]:
            if eaten < self.default_params['F'] \
                    and random.random() < self.prob_eating(herb):
                self.weight += self.default_params['beta'] * herb.weight
                eaten += herb.weight

                self.phi = self.fitness()

            else:
                survivors.append(herb)

        return survivors

    def new_hunting_land(self, neighbours):
        """
        Decides where the migrating carnivore will migrate

        :param neighbours: list
        :return: list
        """
        props = [n.propensity(self, n.abundance_fodder_c) for n in neighbours]
        prob_list = [prop / sum(props) for prop in props]
        p = random.random()
        i = 0
        while p > sum(prob_list[0:i]):
            i += 1
        return neighbours[i - 1].new_pop[1]
