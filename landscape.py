# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from animals import Herbivore


class Jungle:
    """A jungle containing Herbivoars"""

    f_max = 800.0

    default_params = {'f_max': f_max}

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

        self.f_max = Jungle.default_params['f_max']
        self.f = self.f_max
        self.pop_herbs = [Herbivore() for _ in range(num_herbs)]

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
            return [Herbivore() for herb in pop if herb.birth(len(pop))]

        self.pop_herbs.extend(newborns(self.pop_herbs))

    def weightloss(self):
        for herb in self.pop_herbs:
            herb.weightloss()

    def fitness_sort(self):
        for herb in self.pop_herbs:
            herb.fitness()

        asc = False
        while not asc:
            asc = True
            for herb in range(len(self.pop_herbs) - 1):
                if self.pop_herbs[herb].phi < self.pop_herbs[herb + 1].phi:
                    self.pop_herbs[herb], self.pop_herbs[herb + 1] = self.pop_herbs[herb + 1], self.pop_herbs[herb]
                    asc = False
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

    def regenerate(self):
        self.f = self.f_max