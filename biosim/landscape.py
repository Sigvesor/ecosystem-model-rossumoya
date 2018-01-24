# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from math import exp as e
from animals import *
import random


class Landscape:
    """
    This class instantiates a landscape
    """

    default_params = {'f_max': 0}

    @classmethod
    def set_parameters(cls, new_params=default_params):
        """
        Sets class parameters from dictionary

        :param new_params: dict
        :raises: ValueError, KeyError
        """

        for key in new_params:
            if key not in 'f_max':
                raise KeyError('Invalid parameter name: ' + key)

            if key in new_params:
                cls.default_params[key] = new_params[key]

    @classmethod
    def get_params(cls):
        """
        Get dictionary of class parameters

        :type cls: Landscape
        :return: dict
        """

        return {'f_max': cls.default_params['f_max']}

    def __init__(self):
        """
        Creates the variables associated with the class
        """

        self.f = self.default_params['f_max']
        self.pop_animals = [[], []]
        self.new_pop = [[], []]

    def populate_cell(self, population=None):
        """
        Populates the cell with respective animals

        :param population: dict
        """

        for animal in population:

            if animal['species'] == 'Herbivore':
                self.pop_animals[0].append(Herbivore(weight=animal['weight'],
                                                     age=animal['age']))
            elif animal['species'] == 'Carnivore':
                self.pop_animals[1].append(Carnivore(weight=animal['weight'],
                                                     age=animal['age']))

    @property
    def num_herbs(self):
        """
        Return number of Herbivore in landscape
        """

        return len(self.pop_animals[0])

    @property
    def num_carns(self):
        """
        Return number of Carnivore in landscape
        """

        return len(self.pop_animals[1])

    @property
    def sum_herb_mass(self):
        """
        Return the sum of Herbivore weights in the landscape
        """

        return sum([herb.weight for herb in self.pop_animals[0]])

    def aging(self):
        """
        Age all animals in landscape with one cycle
        """

        for species in self.pop_animals:
            for animal in species:
                animal.ages()

    def death(self):
        """
        Removes dying animals
        """

        def survivors(pop):
            return [animal for animal in pop if not animal.dies()]

        self.pop_animals[0] = survivors(self.pop_animals[0])
        self.pop_animals[1] = survivors(self.pop_animals[1])

    def reproduction(self):
        """
        For each Animal reproducing, adds one newborn
        """

        for species in self.pop_animals:
            newborn_animals = []
            for animal in species:
                if animal.birth(len(species)):
                    if isinstance(animal, Herbivore):
                        newborn_animals.append(Herbivore())
                    elif isinstance(animal, Carnivore):
                        newborn_animals.append(Carnivore())
                    animal.weight -= newborn_animals[-1].weight * \
                        animal.default_params['xi']
            species.extend(newborn_animals)

    def weightloss(self):
        """
        Updates the weight of all animals, following a cycle weightloss
        """

        for species in self.pop_animals:
            for animal in species:
                animal.weightloss()

    def update_fitness(self):
        """
        Updates fitness for all animals
        """

        for species in self.pop_animals:
            for animal in species:
                animal.fitness()

    def fitness_sort(self):
        """
        Sorts animals in landscape by their respective fitness
        """

        for species in self.pop_animals:
            desc = False
            while not desc:
                desc = True
                for animal in range(len(species) - 1):
                    if species[animal].phi < species[animal + 1].phi:
                        species[animal], species[animal + 1] = \
                            species[animal + 1], species[animal]
                        desc = False

    def eat_request_herb(self):

        """
        Herbivores eat in the landscape, in order of fitness
        The fittest eats first
        """

        for herb in self.pop_animals[0]:
            request = herb.default_params['F']
            if request <= self.f:
                self.f -= request
            else:
                request = self.f
                self.f = 0
            herb.eating(request)
            herb.fitness()

    def eat_request_carn(self):
        """
        Carnivores eat in the landscape, in order of fitness
        The least fit Herbivore gets eaten first
        """

        carns = self.pop_animals[1]

        for carn in carns:
            self.pop_animals[0] = carn.eating(self.pop_animals[0])

    def regenerate(self):
        """
        Regenerates fodder in the landscape, if possible
        """

        if self.f != self.default_params['f_max']:
            if isinstance(self, Jungle):
                self.f = self.default_params['f_max']
            elif isinstance(self, Savannah):
                self.f += self.default_params['alpha'] * \
                    (self.default_params['f_max'] - self.f)

    @property
    def abundance_fodder_h(self):
        """
        Abundance of fodder, in the landscape, for herbivores

        :return: float
        """

        return self.f / ((self.num_herbs + 1) * Herbivore.default_params['F'])

    @property
    def abundance_fodder_c(self):
        """
        Abundance of fodder, in the landscape, for carnivores

        :return: float
        """
        return self.sum_herb_mass / \
            ((self.num_carns + 1) * Carnivore.default_params['F'])

    def propensity(self, animal, epsilon):
        """
        Calculates the animal's propensity to migrate

        :param animal: object
        :param epsilon: float (abundance of food)
        :return: float (moving propensity)
        """

        if isinstance(self, (Ocean, Mountain)):
            return 0
        else:
            return e(animal.default_params['lambda'] * epsilon) # kan være funk i animal..

    def migrate(self, neighbours):
        """
        Migrates animals in landscape

        :param neighbours: list (valid neighbours)
        """

        for species in self.pop_animals:
            for animal in species:
                if animal.migrating and animal.is_herbivore:
                    animal.new_grassland(neighbours).append(animal)
                elif animal.migrating and animal.is_carnivore:
                    animal.new_hunting_land(neighbours).append(animal)
                else:                                                           # hvis dyret ikke skal gå
                    if animal.is_herbivore:
                        self.new_pop[0].append(animal)
                    elif animal.is_carnivore:
                        self.new_pop[1].append(animal)
        self.pop_animals = [[], []]                                             # alle dyr skal være i en new_pop i cella eller en nabo; tøm pop_animals


class Jungle(Landscape):
    """Jungle. Underclass of superclass Landscape."""

    default_params = {'f_max': 800.0}


class Savannah(Landscape):
    """Savannah. Underclass of superclass Landscape."""

    default_params = {'f_max': 300.0, 'alpha': 0.3}


class Desert(Landscape):
    """Desert. Underclass of superclass Landscape."""

    default_params = {'f_max': 0.0}


class Ocean(Landscape):
    """Ocean. Underclass of superclass Landscape."""

    default_params = {'f_max': 0.0}


class Mountain(Landscape):
    """Mountain. Underclass of superclass Landscape."""

    default_params = {'f_max': 0.0}
