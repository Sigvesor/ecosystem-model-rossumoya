# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from math import exp as e
from animals import *


class Landscape:
    """Landscape containing Herbivores and/or Carnivores."""

    default_params = {'f_max': 0}

    @classmethod
    def set_parameters(cls, new_params=default_params):
        """
        Set class parameters.j

        Parameters
        -------
        new_params : dict
            Legal keys: 'f_max'

        Raises
        -------
        ValueError, KeyError
        """

        for key in new_params:
            if key not in 'f_max':
                raise KeyError('Invalid parameter name: ' + key)

            if key in new_params:
                cls.default_params[key] = new_params[key]

    @classmethod
    def get_params(cls):
        """
        Get class parameters.
        :return: dict
            class parameters.
        """

        return {'f_max': cls.default_params['f_max']}

    def __init__(self):  # , num_herbs=0, num_carns=0):
        """Creates an instance of Landscape"""

        self.f = self.default_params['f_max']
        self.pop_animals = [[], []]
        self.new_pop = [[], []]

    def populate_cell(self, population=None):
        """
        :param population: list
            list of dictionaries with animal parameters.
        """
        for animal in population:

            if isinstance(animal, Herbivore):
                self.pop_animals[0].append(Herbivore(weight=animal['weight'],
                                                     age=animal['age']))
            elif isinstance(animal, Carnivore):
                self.pop_animals[1].append(Carnivore(weight=animal['weight'],
                                                     age=animal['age']))

    @property
    def num_herbs(self):
        """Return number of Herbivore in landscape."""

        return len(self.pop_animals[0])

    @property
    def num_carns(self):
        """Return number of Carnivore in landscape."""

        return len(self.pop_animals[1])

    @property
    def sum_herb_mass(self):
        """Return the sum of Herbivore weights in the landscape."""

        return sum([herb.weight for herb in self.pop_animals[0]])

    def aging(self):
        """Age all animals in landscape with one cycle."""

        for species in self.pop_animals:
            for animal in species:
                animal.ages()

    def death(self):
        """Removes dying animals."""

        def survivors(pop):
            return [animal for animal in pop if not animal.dies()]

        self.pop_animals[0] = survivors(self.pop_animals[0])
        self.pop_animals[1] = survivors(self.pop_animals[1])

    def reproduction(self):
        """For each Animal reproducing, add one new."""

        for species in self.pop_animals:
            newborn_animals = []
            for animal in species:
                if animal.birth(len(species)):
                    animal.weight -= animal.default_params['w_birth'] * \
                        animal.default_params['xi']
                    if isinstance(animal, Herbivore):
                        newborn_animals.append(Herbivore())
                    elif isinstance(animal, Carnivore):
                        newborn_animals.append(Carnivore())
            species.extend(newborn_animals)

    def weightloss(self):
        """
        Updates the weight of all animals,
        following a yearly weight loss.
        """

        for species in self.pop_animals:
            for animal in species:
                animal.weightloss()

    def update_fitness(self):
        """Updates fitness for all animals."""

        for species in self.pop_animals:
            for animal in species:
                animal.fitness()

    def fitness_sort(self):
        """Sorts animals in landscape by their fitness."""

        desc = False
        for species in self.pop_animals:
            while not desc:
                desc = True
                for animal in range(len(species) - 1):
                    if species[animal].phi < species[animal + 1].phi:
                        species[animal], species[animal + 1] = \
                            species[animal + 1], species[animal]
                        desc = False

    def eat_request(self):
        """
        Herbivores and Carnivores eats in the landscape, in order of fitness.
        The least fit herbivores gets eaten first.
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

        for carn in self.pop_animals[1]:
            request = carn.default_params['F']
            w_0 = carn.weight
            i = 1
            while carn.weight - w_0 < request and i < len(self.pop_animals[0]):
                herb = self.pop_animals[0][len(self.pop_animals) - i]
                if carn.phi <= herb.phi:
                    p = 0
                elif 0 < carn.phi - herb.phi < \
                        carn.default_params['DeltaPhiMax']:
                    p = (carn.phi - herb.phi) / \
                        carn.default_params['DeltaPhiMax']
                else:
                    p = 1

                if random.random() < p:
                    carn.eating(herb.weight)
                    self.pop_animals[0].pop(len(self.pop_animals) - i)
                    carn.fitness()
                else:
                    i += 1

    def regenerate(self):
        """If possible, regenerates fodder in the landscape."""
        if self.f != self.default_params['f_max']:
            if isinstance(self, Jungle):
                self.f = self.default_params['f_max']
            elif isinstance(self, Savannah):
                self.f += self.default_params['alpha'] * \
                    (self.default_params['f_max'] - self.f)

    @property
    def abundance_fodder_herb(self):
        """
        Landscape property: Abundance of fodder, for herbivores.
        :return: float
            Abundance of fodder
        """
        return self.f / ((self.num_herbs + 1) * Herbivore.default_params['F'])

    @property
    def abundance_fodder_carn(self):
        """
        Landscape property: Abundance of fodder, for carnivores.
        :return: float
            Abundance of meat.
        """

        return self.sum_herb_mass / \
            ((self.num_carns + 1) * Carnivore.default_params['F'])

    def moving_propensity(self, animal, epsilon):
        """
        Calculates the animal's propensity to migrate.
        :param animal: animal ready to migrate
        :param epsilon: abundance of fodder/meat
        :return: float
            Moving propensity

        """
        if isinstance(self, (Ocean, Mountain)):
            return 0
        else:
            return e(animal.default_params['lambda'] * epsilon)

    def migrate(self, neighbours):
        """
        Migrates animals in landscape.
        :param neighbours: list of valid landscapes for migration
        """

        for species in self.pop_animals:
            for animal in species:
                if random.random() < animal.default_params['mu'] * animal.phi:
                    if isinstance(animal, Herbivore):
                        prop_list = [self.moving_propensity(
                            animal=animal,
                            epsilon=neighbour.abundance_fodder_herb
                        ) for neighbour in neighbours]
                    elif isinstance(animal, Carnivore):
                        prop_list = [self.moving_propensity(
                            animal=animal,
                            epsilon=neighbour.abundance_fodder_carn
                        ) for neighbour in neighbours]
                    #if sum(prop_list) == 0:
                    #    break
                    prob_list = [prop / sum(prop_list) for prop in prop_list]
                    p = random.random()
                    i = 0
                    p_sum = 0
                    while p > p_sum:
                        p_sum += prob_list[i]
                        i += 1
                    destination = neighbours[i - 1]

                    if isinstance(animal, Herbivore):
                        destination.new_pop[0].append(animal)
                    elif isinstance(animal, Carnivore):
                        destination.new_pop[1].append(animal)

                else:
                    if isinstance(animal, Herbivore):
                        self.new_pop[0].append(animal)
                    elif isinstance(animal, Carnivore):
                        self.new_pop[1].append(animal)

        self.pop_animals = [[], []]


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
