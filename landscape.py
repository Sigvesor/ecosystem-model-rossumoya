# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from animals import *


# class Landscape
class Landscape:
    """A jungle containing Herbivoars"""

    #f_max = 0

    default_params = {'f_max': 0}

    @classmethod
    def set_params(cls, new_params=default_params):

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
        Get class parameters

        Returns
        -------
        dict
            Dictionary with class parameters.
        """

        return {'f_max': cls.default_params['f_max']}

    def __init__(self, num_herbs=0, num_carns=0):
        """
        Parameters#
        ----------
        num_herbs : int
            number of Herbivores in the jungle.
        """
        self.f = self.default_params['f_max']
        self.pop_herbs = [Herbivore() for _ in range(num_herbs)]
        self.pop_carns = [Carnivore() for _ in range(num_carns)]
        self.pop_animals = [self.pop_herbs, self.pop_carns]

    def get_num_herbs(self):
        """Return number of animals in landscape"""

        return len(self.pop_herbs)

    def get_num_carns(self):
        """Return number of Carnivores in landscape"""

        return len(self.pop_carns)

    def aging(self):
        """Age all animals in Jungle by one cycle."""

        for herb in self.pop_herbs:
            herb.ages()

        for carn in self.pop_carns:
            carn.ages()

    def death(self):
        """Remove dying Herbivores and Carnivores."""

        def survivors(pop):
            return [animal for animal in pop if not animal.dies()]

        self.pop_herbs = survivors(self.pop_herbs)
        self.pop_carns = survivors(self.pop_carns)

    def reproduction(self):
        """For each Herbivore reproducing, add one new."""

        def newborns(pop):
            babies = []

            for animal in pop:
                if animal.birth(len(pop)):
                    animal.weight -= animal.default_params['w_birth'] * animal.default_params['xi']
                    if type(animal) == Herbivore:
                        babies.append(Herbivore())
                    elif type(animal) == Carnivore:
                        babies.append(Carnivore())
                return babies

        try:
            self.pop_carns.extend(newborns(self.pop_carns))
            self.pop_herbs.extend(newborns(self.pop_herbs))
        except Exception:
            pass

    def weightloss(self):
        for species in self.pop_animals:
            for animal in species:
                animal.weightloss()

        #for herb in self.pop_herbs:
        #    herb.weightloss()
        #
        #for carn in self.pop_carns:
        #    carn.weightloss()#

    def update_fitness(self):
        for species in self.pop_animals:
            for animal in species:
                animal.fitness()

        #for herb in self.pop_herbs:
        #    herb.fitness()
        #
        #for carn in self.pop_carns:
        #    carn.fitness()

    def fitness_sort(self):
        desc = False
        for species in self.pop_animals:
            while not desc:
                desc = True
                for animal in range(len(species) - 1):
                    if species[animal].phi < species[animal + 1].phi:
                        species[animal], species[animal + 1] = species[animal + 1], species[animal]
                        desc = False

    def eat_request(self):
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
            i = 0
            herb_yard = []
            while carn.weight - w_0 < request:
                herb = self.pop_animals[0][i]
                if carn.phi <= herb:
                    p = 0
                elif 0 < carn.phi - herb.phi < carn.default_params['DeltaPhiMax']:
                    p = (carn.phi - herb.phi) / carn.default_params['DeltaPhiMax']
                else:
                    p = 1
                if random.random() < p:
                    carn.weight += carn.default_params['beta'] * herb.weight
                    herb_yard.append(i)
                i += 1
            [self.pop_animals[0].pop(pos) for pos in herb_yard]


    def regenerate(self):
        if self.f != self.default_params['f_max']:
            if type(self) == Jungle:
                self.f = self.default_params['f_max']
            elif type(self) == Savannah:
                self.f += self.default_params['alpha'] * (self.default_params['f_max'] - self.f)


class Jungle(Landscape):

    default_params = {'f_max': 800.0}

    #f_max = default_params['f_max']


class Savannah(Landscape):

    default_params = {'f_max': 300.0, 'alpha': 0.3}

    #f_max = default_params['f_max']
    #alpha = default_params['alpha']


class Desert(Landscape):

    default_params = {'f_max': 0.0}
















# class Savannah