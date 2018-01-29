# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from .island import *
import pandas as pd
from .animals import *
import os
from subprocess import call
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

"""
This program will simulate the ecosystem of Rossumøya
"""


class BioSim:

    """
    This class instantiates an ecosystem simulation
    """

    version = '1.0'

    def __init__(self, island_map, ini_pop, seed):
        """
        Creates the variables associated with the class

        :param island_map: multi line string
        :param ini_pop: initial population in simulation
        :param seed: random seed
        """

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
                           columns=df_cols[2:4])
        empty_df = [[i+1, j+1, 0, 0] for j in range(n_cols)
                    for i in range(n_rows)]
        self.pop_by_cell = pd.DataFrame(data=empty_df, columns=df_cols)
        self.pop_by_cell.update(pop)
        self.ax_map = None
        self.ax_herb = None
        self.ax_carn = None
        self.ax_graph = None
        self.hax = None
        self.cax = None
        self.new_sim = False

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
        return {'Herbivores': herbs, 'Carnivores': carns}

    @property
    def years_passed(self):
        """
        Returns the number of years the BioSim instance has simulated

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

    def simulate(self, num_steps, vis_steps=1, img_steps=1):

        """
        Conducting the simulation, deciding number of cycles.

        :param num_steps: int
        :param vis_steps: int
        :param img_steps: int
        """

        self.new_sim = True
        for step in range(num_steps):
            sim_cyc = self.island.cycle()
            self.herb_list.append(sim_cyc[0])
            self.carn_list.append(sim_cyc[1])

            if self.year % vis_steps == 0:
                plt.ion()
                self.sim_plot()

            self.year += 1
            if self.year % img_steps == 0:
                plt.savefig('biosim_project/animation/biosim_' +
                            str(self.year).zfill(5) + '.png')

    def add_population(self, population=None):
        """
        Adds populations from a list of dictionaries
        The keys of the dictionaries have to be 'species', 'age' and 'weight'

        :param population: list
        """

        self.island.distribute_animals(population)

    def sim_plot(self):
        if self.new_sim:
            fig, ((self.ax_graph, self.ax_map), (self.ax_herb, self.ax_carn)) \
                = plt.subplots(2, 2)
            self.ax_map = plt.subplot2grid((3, 3), (2, 1))
            self.ax_herb = plt.subplot2grid((3, 3), (2, 0))
            self.ax_carn = plt.subplot2grid((3, 3), (2, 2))
            self.ax_graph = plt.subplot2grid((3, 3), (0, 0),
                                             colspan=3, rowspan=2)
            plt.tight_layout()
        self.heat_map()
        self.plot_map()
        self.plot_pop_density()
        if self.new_sim:
            fig.colorbar(self.hax, ax=self.ax_herb, orientation='horizontal',
                         ticks=[0, 100, 200], shrink=0.85)
            self.ax_herb.axes.get_xaxis().set_ticklabels([])
            self.ax_herb.axes.get_yaxis().set_ticklabels([])
            self.ax_carn.axes.get_xaxis().set_ticklabels([])
            self.ax_carn.axes.get_yaxis().set_ticklabels([])
            self.ax_map.axes.get_xaxis().set_ticklabels([])
            self.ax_map.axes.get_yaxis().set_ticklabels([])
            self.ax_map.axes.get_xaxis().set_ticks([])
            self.ax_map.axes.get_yaxis().set_ticks([])
            self.ax_herb.axes.get_xaxis().set_ticks([])
            self.ax_herb.axes.get_yaxis().set_ticks([])
            self.ax_carn.axes.get_xaxis().set_ticks([])
            self.ax_carn.axes.get_yaxis().set_ticks([])
            self.ax_graph.legend(["Herbivores", "Carnivores"], loc=2)
            fig.colorbar(self.cax, ax=self.ax_carn, ticks=[0, 100, 200],
                         orientation='horizontal', shrink=0.85)
            self.ax_graph.set_ylabel('number of animals')

        plt.pause(0.000001)
        self.new_sim = False

    def heat_map(self):
        """
        Returns a heat-map, describing population density and movements
        """
        pop_array_h = self.island.population_array()

        self.hax = self.ax_herb.imshow(pop_array_h, cmap='Greens',
                                       interpolation='nearest', vmin=0,
                                       vmax=200)
        self.ax_herb.set_title('Herbivore density')

        pop_array_c = self.island.population_array(False)
        self.cax = self.ax_carn.imshow(pop_array_c, cmap='Reds',
                                       interpolation='nearest', vmin=0,
                                       vmax=200)
        self.ax_carn.set_title('Carnivore density')

    def plot_pop_density(self):
        """
        Plots the population density for each
        """
        self.ax_graph.plot(range(len(self.herb_list)), self.herb_list, 'g-',
                           range(len(self.carn_list)), self.carn_list, 'r-')
        self.ax_graph.set_title('Total populations until year '+
                                str(self.years_passed + 1))


    def plot_map(self):
        rbg_value = {'D': (1., 1., 0.5),
                     'J': (0., 0.6, 0.),
                     'M': (0.5, 0.5, 0.5),
                     'O': (0., 0., 1.),
                     'S': (0.5, 1., 0.5)}
        rbg_map = [[rbg_value[x] for x in row] for row in self.island.map_str]
        self.ax_map.imshow(rbg_map)
        self.ax_map.set_title('Island map')
        #at = AnchoredText("Figure 1a",
        #                  prop=dict(size=8), frameon=True,
        #                  loc=1)
        #self.ax_map.add_artist(at)
        box = self.ax_map.get_position()
        #plt.figlegend(('Ocean', 'Desert'), (patches.Patch(color='b'), patches.Patch(color='g')), loc=1)
        desert_patch = mpatches.Patch(color=(1., 1., 0.5), label='Desert')
        jungle_patch = mpatches.Patch(color=(0., 0.6, 0.), label='Jungle')
        mountain_patch = mpatches.Patch(color=(0.5, 0.5, 0.5), label='Mountain')
        ocean_patch = mpatches.Patch(color=(0., 0., 1.), label='Ocean')
        savannah_patch = mpatches.Patch(color=(0.5, 1., 0.5), label='Savannah')

        self.ax_map.legend(handles=[ocean_patch, desert_patch, mountain_patch,
                            mountain_patch, jungle_patch,savannah_patch],
                            bbox_to_anchor=(1.5, 1), fontsize=6)

    def make_movie(self):

        #call('ffmpeg -i biosim_project/animation/biosim_%05d.png output.gif')

if __name__ == "__main__":

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

    ini_herbs = [{'loc': (10, 2),
                  'pop': [{'species': 'Herbivore', 'age': 5,
                           'weight': 20} for _ in range(150)]}]
    ini_carns = [{'loc': (20, 2),
                  'pop': [{'species': 'Carnivore', 'age': 5,
                           'weight': 20} for _ in range(40)]}]
    sim = BioSim(ini_pop=ini_herbs, island_map=kart, seed=12634)
    sim.simulate(100, 1, 1)
    sim.simulate(100)
    sim.add_population(ini_carns)
    sim.simulate(400)
