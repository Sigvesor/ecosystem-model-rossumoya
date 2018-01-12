# -*- coding: utf-8 -*-

"""
This takes a list of numbers as input and
outputs a list containing the same numbers in increasing order
"""

__author__ = 'Filip Rotnes'
__email__ = 'firo@nmbu.no'


def animal_sort(number_list):
    bubble_sorted = list(number_list)
    comparisons = len(number_list)-1
    for j in range(len(number_list)-1):
        for i in range(comparisons):
            if bubble_sorted[i].phi > bubble_sorted[i+1].phi:
                bubble_sorted[i], bubble_sorted[i+1] = bubble_sorted[i + 1], \
                                                       bubble_sorted[i]
            else:
                bubble_sorted[i], bubble_sorted[i+1] = bubble_sorted[i], \
                                                       bubble_sorted[i + 1]
        comparisons -= 1
    return bubble_sorted
