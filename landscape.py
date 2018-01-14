# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from animals import Herbivore

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

    def __init__(self, num_herbs):
        """
        Parameters#
        ----------
        num_herbs : int
            number of Herbivores in the jungle.
        """

        self.f = self.default_params['f_max']
        self.pop_herbs = [Herbivore() for _ in range(num_herbs)]
        #self.pop_carns = [Carnivore() for _ in range(num_carns)]

    def get_num_herbs(self):
        """Return number of Herbivores in Jungle"""

        return len(self.pop_herbs)

    def aging(self):
        """Age all Herbivores in Jungle by one cycle."""

        for herb in self.pop_herbs:
            herb.ages()

    def death(self):
        """Remove dying Herbivores."""

        def survivors(pop):
            return [herb for herb in pop if not herb.dies()]

        self.pop_herbs = survivors(self.pop_herbs)

    def reproduction(self):
        """For each Herbivore reproducing, add one new."""

        def newborns(pop):
            babies = []
            for herb in pop:
                if herb.birth(len(pop)):
                    herb.weight -= 8 # her burde vi koble til vekta til barnet..
                    babies.append(Herbivore())
                return babies
            # return [Herbivore() for herb in pop if herb.birth(len(pop))]

        self.pop_herbs.extend(newborns(self.pop_herbs))

    def weightloss(self):
        for herb in self.pop_herbs:
            herb.weightloss()

    def update_fitness(self):
        for herb in self.pop_herbs:
            herb.fitness()

    def fitness_sort(self):
        desc = False
        while not desc:
            desc = True
            for herb in range(len(self.pop_herbs) - 1):
                if self.pop_herbs[herb].phi < self.pop_herbs[herb + 1].phi:
                    self.pop_herbs[herb], self.pop_herbs[herb + 1] = self.pop_herbs[herb + 1], self.pop_herbs[herb]
                    desc = False
        return self.pop_herbs

    def eat_request(self):
        for herb in self.pop_herbs:
            request = herb.default_params['F']
            if request <= self.f:
                self.f -= request
            else:
                request = self.f
                self.f = 0
            herb.eating(request)
            herb.fitness()

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















# class Savannah