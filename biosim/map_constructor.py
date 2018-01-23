# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

import matplotlib.pyplot as plt
from island import *
class MapConstructor:

    rgb_value = {'D': (1., 1., 0.5),
                 'J': (0., 0.6, 0.),
                 'M': (0.5, 0.5, 0.5),
                 'O': (0., 0., 1.),
                 'S': (0.5, 1., 0.5)}

    def __init__(self):
        self.map = None

    def Island_Map(self, map):
        self.map = Island().map_str_manager(map)
        rgb_map = [[rgb_value[x] for x in row] for row in map.splitlines()]
        fig = plt.figure()
        axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        axim.imshow(rgb_map, interpolation='nearest')



#map = """OOO
#OSO
#OOO"""
#
#
#rgb_value = {'D': (1.,1.,0.5),
#             'J': (0.,0.6,0.),
#             'M': (0.5,0.5,0.5),
#             'O': (0.,0.,1.),
#             'S': (0.5,1.,0.5)}
#
#rgb_map = [[rgb_value[x] for x in row] for row in map.splitlines()]
#
#fig = plt.figure()
#
#axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
#
#axim.imshow(rgb_map, interpolation='nearest')


if __name__ == '__main__':
    map = """OOO
OSO
OOO"""
    constructor = MapConstructor()
    constructor.Island_Map(map)

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

    rgb_map = [[rgb_value[x] for x in row] for row in standard_map.splitlines()]
    fig = plt.figure()
    axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
    axim.imshow(rgb_map, interpolation='nearest')
