# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from landscape import *
from animals import *
import numpy as np

class Island:
    """A population with many jungles"""

    def __init__(self):
                 # island_map=standard_map, ini_pop=standard_pop):
                 #n_pops=1, n_num_herbs=10, n_num_carns=2):
        """
        Parameters:
        ----------
        n_pops : int
            number of Herbivore populations
        """
        self.map = None


        #self.pops = [Jungle(n_num_herbs, n_num_carns) for _ in range(n_pops)]

    def cycle(self):
        """Update all populations by one cycle."""
        for row in self.map:
            for cell in row:
                cell.fitness_sort()
                cell.eat_request()
                cell.update_fitness()
                cell.reproduction()
                cell.aging()
                cell.weightloss()
                cell.update_fitness()
                cell.death()
                cell.regenerate()

        #for pop in self.pops:


            return (len(cell.pop_animals[0]),len(cell.pop_animals[1]))

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
        island_map = island_map.replace(" ","").splitlines()
        self.map = np.empty((len(island_map),len(island_map[0])), dtype=object)
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
        standard_pop = [{'loc': (1, 1), 'pop':
            [{'species': 'Herbivore', 'age': 5, 'weight': 30}]},
                        {'loc': (1, 1), 'pop':
                            [{'species': 'Carnivore', 'age': 5, 'weight': 30}]}]
        if not ini_pop:
            population = standard_pop
        else:
            population = ini_pop
        for dictionary in population:
            self.map[dictionary['loc']].populate_cell(dictionary['pop'])

    def get_random_landscapes(self):

        array_list = self.map.tolist()
        land_list = [j for i in array_list for j in i]

        random.shuffle(land_list)

        return land_list

    def get_surrounding_landscapes(self, pos):

        valid_moves = []
        x, y = pos

        if x + 1 < len(self.map):
            valid_moves.append(self.map[x+1, y])
        if x - 1 >= 0:
            valid_moves.append(self.map[x-1, y])
        if y + 1 < len(self.map[0]):
            valid_moves.append(self.map[x, y+1])
        if y - 1 >= 0:
            valid_moves.append(self.map[x, y - 1])
        return valid_moves

    def migrate_island(self):

        land_list = self.get_random_landscapes()

        for land in land_list:
            coords = np.where(self.map == land)
            self.map[coords[0][0], coords[1][0]].migrate(self.get_surrounding_landscapes([coords[0][0], coords[1][0]]))

        for land in land_list:
            coords = np.where(self.map == land)
            self.map[coords[0][0], coords[1][0]].pop_animals = self.map[coords[0][0], coords[1][0]].new_pop
            self.map[coords[0][0], coords[1][0]].new_pop = [[], []]

    def populated_island(self, map=None, ini_pop=None):

        self.map = self.map_from_string(map)
        self.distribute_animals(ini_pop)