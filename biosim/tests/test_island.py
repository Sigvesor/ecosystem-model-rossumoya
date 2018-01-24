# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

from biosim.island import *
import numpy


def test_island_instance():
    """
    Tests that an island is an instance of class Island.
    """

    island = Island()
    assert isinstance(island, Island)


def test_map_from_string():
    """
    Tests that a numpy.ndarray is generated when calling
    the map-generating method.
    """

    island = Island()
    island.map_from_string()
    assert isinstance(island.map, numpy.ndarray)


def test_distribute_animals():
    """
    Tests that the island is not empty after distributing animals on it.
    """

    island = Island()
    island.populated_island()
    assert island.total_island_population != (0, 0)


def test_random_landscapes():
    """
    Tests that a list is created from the numpy.ndarray map.
    """

    island = Island()
    island.map_from_string()
    assert isinstance(island.get_random_landscapes(), list)


def test_surrounding_landscapes():
    """
    Tests that the corner cell, which should be of type Ocean,
    don't have any valid neighbour cell for migration. Also tests
    if a Jungle cell with four adjacent Jungle cells has four valid
    neighbour cells for migration.
    """

    island = Island()
    island.map_from_string("""OOO
    OJO
    OOO""")
    assert len(island.get_surrounding_landscapes([0, 0])) == 0
    assert len(island.get_surrounding_landscapes([1, 1])) == 0
    island.map_from_string("""OOOOO
    OOJOO
    OJJJO
    OOJOO
    OOOOO""")
    assert len(island.get_surrounding_landscapes([2, 2])) == 4


def test_total_island_pop():
    """
    Given that the standard population in distribute animals method
    doesn't change; tests if returned correct integer amount of animals.
    """

    island = Island()
    island.map_from_string()
    island.distribute_animals()
    tot_tuple = island.total_island_population
    tot_tuple0 = tot_tuple[0]
    tot_tuple1 = tot_tuple[1]
    assert tot_tuple0 + tot_tuple1 == 190


def test_cycle():
    """
    Tests that cycle method returns a tuple.
    """

    island = Island()
    island.map_from_string()
    assert isinstance(island.cycle(), tuple)


def test_migration():
    """
    Tests that an animal actually migrates if it is ready to migrate.
    """

    Herbivore.set_parameters({'mu': 1})
    island = Island()
    island.map_from_string("""OOOOO
        OOOOO
        OJJOO
        OOOOO
        OOOOO""")

    ini_herbs = [{'loc': (3, 3),
                  'pop': [{'species': 'Herbivore', 'age': 5,
                           'weight': 20}]}]

    island.distribute_animals(ini_herbs)
    island.map[2, 2].pop_animals[0][0].phi = 1
    assert len(island.map[2, 2].pop_animals[0]) == 1
    island.migrate_island()
    assert len(island.map[2, 1].pop_animals[0]) == 1

