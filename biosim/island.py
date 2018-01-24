# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

import numpy as np
from .landscape import *
import random


class Island:
    """An island population with several possible landscapes."""

    def __init__(self):
        """
        Parameters:
        ----------
        n_pops : int
            number of Herbivore populations
        """
        self.map_str = None
        self.map = None

    def cycle(self):
        """Adds one cycle to island population."""
        for row in self.map:
            for cell in row:

                cell.regenerate()
                cell.fitness_sort()
                cell.eat_request_herb()
                cell.eat_request_carn()
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

    def check_string_map(self, string_map):
        """
        Checks if the multi line string containing landscape distribution
        contains invalid landscape types.

        :param string_map: multi line string describing island.
        """
        landscape_error = ValueError('Wrong input for island map, \n'
                                     'D = Desert \nJ = Jungle \nM = Mountain \n'
                                     'O = Ocean \nS = Savannah\n')
        allowed_landscapes = ['D', 'J', 'M', 'O', 'S']
        for row in string_map:
            for cell in row:
                if cell not in allowed_landscapes:
                    raise landscape_error

        map_error = ValueError('The edges of the maps has to be Ocean only! \n')
        for end in [0, -1]:
            for cell in string_map[end]:
                if cell != 'O':
                    raise map_error
        for row in string_map[1:-1]:
            valid_ends = row.startswith('O') and row.endswith('O')
            if not valid_ends:
                raise map_error

        row_lengths = [len(row) for row in string_map]
        if max(row_lengths) != min(row_lengths):
            raise ValueError('Each row in map must be of the same length! \n')

    def map_str_manager(self, map_str=None):
        """
        Creates a numpy array map with landscape cells.

        :param map_str: multi line string describing island.
        :return: numpy array with landscape cells.
        """
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
        self.map_str = island_map.replace(" ", "").splitlines()

        self.check_string_map(string_map=self.map_str)
        return self.map_str

    def map_from_string(self, map_str=None):
        island_map = self.map_str_manager(map_str)
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
        """
        Puts Herbivores and Carnivores into their respective cells in map.

        :param ini_pop: list of dictionaries containing location/population.
        """

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
            map_row = dictionary['loc'][0]
            map_col = dictionary['loc'][1]

            if not 0 < map_row <= self.map.shape[0]:
                raise ValueError('x-coordinate out of bounds, '
                                 'relative to map, for loc: ' +
                                 str((map_row, map_col)))

            elif not 0 < map_col <= self.map.shape[1]:
                raise ValueError('y-coordinate out of bounds, '
                                 'relative to map, for loc: ' +
                                 str((map_row, map_col)))

            cell = self.map[(map_row - 1, map_col - 1)]

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
        """
        Creates a list of randomized landscapes from the numpy array map.

        :return: list of landscapes
        """

        array_list = self.map.tolist()
        land_list = [j for i in array_list for j in i]

        random.shuffle(land_list)

        return land_list

    def get_surrounding_landscapes(self, pos):
        """
        Collects a cell's neighbour cells, which are valid for migration.

        :param pos: cell coordinates for cell in numpy array map.
        :return: list of valid landscape objects, for migration.
        """

        possible_moves = []
        x, y = pos
        illegal = (Ocean, Mountain)
        if x + 1 < len(self.map):
            possible_moves.append(self.map[x + 1, y])
        if x - 1 >= 0:
            possible_moves.append(self.map[x - 1, y])
        if y + 1 < len(self.map[0]):
            possible_moves.append(self.map[x, y + 1])
        if y - 1 >= 0:
            possible_moves.append(self.map[x, y - 1])
        valid_moves = []
        for move in possible_moves:
            if not isinstance(move, illegal):
                valid_moves.append(move)
        return valid_moves

    def migrate_island(self):
        """Iterates through map and initiates migration for each landscape."""

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
        """
        Populates island with animals.

        :param map: map from multi line string, numpy array
        :param ini_pop: initial population of animals
        """

        self.map = self.map_from_string(map)
        self.distribute_animals(ini_pop)


    def population_array(self, herbivore=True):
        pop_array = np.zeros(self.map.shape)
        #if herbivore:
        #    species = pop_animals[#0]
        #else:
        #    species = pop_animals[0]
        for row in range(self.map.shape[1]):
            for cell in range(self.map.shape[0]):
                pop_array[cell, row] = len(self.map[cell, row].pop_animals[0])
        return pop_array



    @property
    def population_distribution(self):
        """
        Returns the population of herbivores and carnivores for each cell.

        Cells are listed row by row.

        :return: np.array([[herbivore, carnivore] for cell in row ...]
        """
        total_pop_herbs = []
        total_pop_carns = []

        for row in self.map:
            for cell in row:
                total_pop_herbs.append(len(cell.pop_animals[0]))
                total_pop_carns.append(len(cell.pop_animals[1]))
        return np.column_stack((total_pop_herbs, total_pop_carns))

    @property
    def total_island_population(self):
        """
        Calculates total population on island.

        :return: tuple containing total number of each animal on island.
        """
        pop = self.population_distribution
        herbs = [pop[i][0] for i in range(len(pop))]
        carns = [pop[i][1] for i in range(len(pop))]
        return (sum(herbs), sum(carns))
