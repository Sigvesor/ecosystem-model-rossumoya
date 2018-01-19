# -*- coding: utf-8 -*-

__author__ = 'Sigve Sorensen', 'Filip Rotnes'
__email__ = 'sigvsore@nmbu.no', 'firo@nmbu.no'

import matplotlib.pyplot as plt

map = """OOO
OSO
OOO"""


rgb_value = {'D': (1.,1.,0.5),
             'J': (0.,0.6,0.),
             'M': (0.5,0.5,0.5),
             'O': (0.,0.,1.),
             'S': (0.5,1.,0.5)}

rgb_map = [[rgb_value[x] for x in row] for row in map.splitlines()]

fig = plt.figure()

axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h

axim.imshow(rgb_map, interpolation='nearest')


if __name__ == '__main__':
    map = """OOO
    OSO
    OOO"""
