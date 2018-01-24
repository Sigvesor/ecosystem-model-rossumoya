# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import random
from .island import *
import pandas as pd
import numpy as np
from math import exp as e
__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'


class BioSim:

    def __init__(self, island_map, ini_pop, seed):
        random.seed(seed)
        self.year = 0
        self.ini_pop = ini_pop
        self.island = Island()
        self.island.populated_island(island_map, ini_pop)
        n_rows, n_cols = len(self.island.map_str), len(self.island.map[0])
        self.herb_list = [self.island.total_island_population[0]]
        self.carn_list = [self.island.total_island_population[1]]
        df_cols = ['x', 'y', 'Herbivores', 'Carnivores']
        pop = pd.DataFrame(self.island.population_distribution,
                           columns= df_cols[2:4])
        empty_df = [[i+1, j+1, 0, 0] for j in range(n_cols)
                    for i in range(n_rows)]
        self.pop_by_cell = pd.DataFrame(data= empty_df, columns=df_cols)
        self.pop_by_cell.update(pop)

    @property
    def population_by_cell(self):
        """
        Returns a DataFrame containing the number of each species per cell
        Columns: 'x', 'y', 'Herbivores', 'Carnivores'
        :return: pandas.DataFrame
        """
        pop = pd.DataFrame(self.island.population_distribution,
                           columns=['Herbivores', 'Carnivores'])
        self.pop_by_cell.update(pop)
        return self.pop_by_cell

    @property
    def population_by_species(self):
        """
        Returns a dictionary containing the number of animals for each species.
        :return: dict
        """
        herbs = self.herb_list[-1]
        carns = self.carn_list[-1]
        return {'Herbivores': herbs,'Carnivores': carns}

    @property
    def years_passed(self):
        """
        Returns the number of years the BioSim instance has simulated.
        :return: int
        """
        return self.year

    @property
    def total_animals(self):
        """
        Returns the total number of animals
        :return: int
        """
        return self.herb_list[-1] + self.carn_list[-1]

    def simulate(self, num_steps, vis_steps=1, img_steps=None):

        for step in range(num_steps):
            sim_cyc = self.island.cycle()
            self.herb_list.append(sim_cyc[0])
            self.carn_list.append(sim_cyc[1])

            if self.year % vis_steps == 0:
                plt.ion()
                self.sim_plot()
            self.year += 1
            plt.pause(0.000001)
        # print(herb_list)
        # print(carn_list)
        #fig = plt.figure()

        # return [herb_list, carn_list]

    def add_population(self, population=None):
        """
        Adds populations from a list of dictionaries.

        The keys of the dictionaries have to be 'species', 'age' and 'weight'
        :param population: list
        """
        self.island.distribute_animals(population)

    def sim_plot(self):
        #plt.ion()
        year0 = self.years_passed < 1
        print(self.years_passed)
        if year0:
            fig = plt.figure()
            self.ax_herb = fig.add_subplot(223)
            plt.title('Herbivore density')
            self.ax_carn = fig.add_subplot(224)
        self.heat_map()
        if year0:
            self.ax_map = fig.add_subplot(222)
        self.plot_map()
        if year0:
            self.ax_graph = fig.add_subplot(221)
        self.plot_pop_density()
        plt.title(str(self.years_passed))
        #plt.pause(0.0001)

    def heat_map(self):
        pop_array_h = self.island.population_array()
        self.ax_herb.imshow(pop_array_h, cmap='Greens', interpolation='nearest')

        pop_array_c = self.island.population_array(False)
        self.ax_carn.imshow(pop_array_c, cmap='Reds', interpolation='nearest')
        plt.title('Carnivore density')

    def plot_pop_density(self):
        self.ax_graph.plot(range(len(self.herb_list)), self.herb_list, 'r-',
                       range(len(self.carn_list)), self.carn_list, 'b-')
        plt.title('Total populations per year')

    def plot_map(self):
        rbg_value = {'D': (1., 1., 0.5),
                     'J': (0., 0.6, 0.),
                     'M': (0.5, 0.5, 0.5),
                     'O': (0., 0., 1.),
                     'S': (0.5, 1., 0.5)}
        rbg_map = [[rbg_value[x] for x in row] for row in self.island.map_str]
        self.ax_map.imshow(rbg_map)
        plt.title('Island map')



if __name__ == "__main__":
    import timeit

    t0 = timeit.default_timer()

    kart = """OOOOOOOOOOOOOOOOOOOOO
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

    ini_herbs = [{'loc': (2, 20),
                  'pop': [{'species': 'Herbivore', 'age': 5,
                           'weight': 20} for _ in range(150)]}]
    ini_carns = [{'loc': (2, 20),
                  'pop': [{'species': 'Carnivore', 'age': 5,
                           'weight': 20} for _ in range(40)]}]
    sim = BioSim(ini_pop=ini_herbs, island_map=kart, seed=12634)

    sim.simulate(100, vis_steps=5)
    sim.add_population(ini_carns)
    sim.simulate(400)
    sim.sim_plot()
    print(timeit.default_timer() - t0)
