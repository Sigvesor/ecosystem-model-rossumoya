# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

import numpy as np

from biosim.landscape import *


class Island:
    """A population with many jungles"""

    def __init__(self):
        """
        Parameters:
        ----------
        n_pops : int
            number of Herbivore populations
        """
        self.map = None

    def cycle(self):
        """Update all populations by one cycle."""
        for row in self.map:
            for cell in row:

                cell.regenerate()
                cell.fitness_sort()
                cell.eat_request()
                cell.update_fitness()
                cell.reproduction()

        self.migrate_island()

        for row in self.map:
            for cell in row:

                cell.aging()
                cell.weightloss()
                cell.update_fitness()
                cell.death()

        return self.total_island_population

    def map_from_string(self, map_str=None):

        standard_map = """OOOOOOOOOOOOOOOOOOOOO
        OOOOOOOOSMMMMJJJJJJJO
        OSSSSSJJJJMMJJJJJJJOO
        OSSSSSSSSSMMJJJJJJOOO
        OSSSSSJJJJJJJJJJJJOOO
        OSSSSSJJJDDJJJSJJJOOO
        OSSJJJJJDDDJJJSSSSOOO
        OOSSSSJJJDDJJJSOOOOOO
        OSSSJJJJJDDJJJJJJJOOO
        OSSSSJJJJDDJJJJOOOOOO
        OOSSSSJJJJJJJJOOOOOOO
        OOOSSSSJJJJJJJOOOOOOO
        OOOOOOOOOOOOOOOOOOOOO"""
        if not map_str:
            island_map = standard_map
        else:
            island_map = map_str
        island_map = island_map.replace(" ", "").splitlines()
        self.map = np.empty(
            (len(island_map), len(island_map[0])), dtype=object)
        for x, line in enumerate(island_map):
            for y, cell in enumerate(line):
                if cell == 'O':
                    self.map[x, y] = Ocean()
                elif cell == 'J':
                    self.map[x, y] = Jungle()
                elif cell == 'S':
                    self.map[x, y] = Savannah()
                elif cell == 'D':
                    self.map[x, y] = Desert()
                elif cell == 'M':
                    self.map[x, y] = Mountain()
        return self.map

    def distribute_animals(self, ini_pop=None):

        ini_herbs = [{'loc': (10, 10),
                      'pop': [{'species': 'Herbivore', 'age': 5,
                               'weight': 20} for _ in range(150)]}]
        ini_carns = [{'loc': (10, 10),
                      'pop': [{'species': 'Carnivore', 'age': 5,
                               'weight': 20} for _ in range(40)]}]
        standard_pop = ini_herbs + ini_carns

        if not ini_pop:
            population = standard_pop
        else:
            population = ini_pop
        for dictionary in population:
            cell = self.map[dictionary['loc']]

            if isinstance(cell, (Mountain, Ocean)):
                raise ValueError('Animals can not be placed in ' +
                                 str(type(cell)) + '. Permitted landscapes: ' 
                                                   'Jungle, Savannah'
                                                   ' and Desert.')
            for animal in dictionary['pop']:
                age, weight = animal['age'], animal['weight']
                if not isinstance(age, int) or age < 0 or weight < 0:
                    raise ValueError('Violated one of two conditions:\n' 
                                     '1. Animal age has to be a non-negative' 
                                     ' integer.\n2. Animal weight has to be' 
                                     ' a non-negative number(float).')
            cell.populate_cell(dictionary['pop'])

    def get_random_landscapes(self):

        array_list = self.map.tolist()
        land_list = [j for i in array_list for j in i]

        random.shuffle(land_list)

        return land_list

    def get_surrounding_landscapes(self, pos):

        valid_moves = []
        x, y = pos

        if x + 1 < len(self.map):
            valid_moves.append(self.map[x + 1, y])
        if x - 1 >= 0:
            valid_moves.append(self.map[x - 1, y])
        if y + 1 < len(self.map[0]):
            valid_moves.append(self.map[x, y + 1])
        if y - 1 >= 0:
            valid_moves.append(self.map[x, y - 1])
        return valid_moves

    def migrate_island(self):

        land_list = self.get_random_landscapes()

        for land in land_list:
            coords = np.where(self.map == land)
            x = coords[0][0]
            y = coords[1][0]
            self.map[x, y].migrate(
                self.get_surrounding_landscapes([x, y]))

        for land in land_list:
            coords = np.where(self.map == land)
            x = coords[0][0]
            y = coords[1][0]
            self.map[x, y].pop_animals = self.map[x, y].new_pop
            self.map[x, y].new_pop = [[], []]

    def populated_island(self, map=None, ini_pop=None):

        self.map = self.map_from_string(map)
        self.distribute_animals(ini_pop)

    @property
    def total_island_population(self):

        total_pop_herbs = []
        total_pop_carns = []

        for row in self.map:
            for cell in row:

                total_pop_herbs.append(len(cell.pop_animals[0]))
                total_pop_carns.append(len(cell.pop_animals[1]))

        total_pop = (sum(total_pop_herbs), sum(total_pop_carns))

        return total_pop
