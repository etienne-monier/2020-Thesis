#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import scipy.interpolate as spint
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import Delaunay, delaunay_plot_2d, Voronoi, voronoi_plot_2d


def interpolate(points, values, method='nearest'):

    d = np.loadtxt('points_2.txt')
    n_p = 100

    # Interpolation is performed.
    nn_interpolated_values = spint.griddata(
        points*n_p, values, d, method=method)

    return nn_interpolated_values, d


if __name__ == '__main__':

    # Get points
    np.random.seed(0)
    N = 10
    points = np.random.rand(N, 2)
    values = np.random.rand(N)

    # Interpolation
    int_values, d = interpolate(points, values, 'nearest')
    n_p = 100

    im = np.zeros((n_p, n_p))
    for x in range(n_p):
        for y in range(n_p):
            if [x, y] in d.tolist():
                im[y, x] = int_values[d.tolist().index([x, y])]
            else:
                im[y, x] = np.nan

    fig, ax = plt.subplots()
    ax.matshow(im)

    ax.set_aspect('equal')
    plt.show()

    # Save text
    txt = ''
    for x in range(n_p):
        for y in range(n_p):
            if not np.isnan(im[y, x]):
                txt += '({}, {}, {:.4f}) '.format(x, y, im[y, x])
            else:
                txt += '({}, {}, inf) '.format(y, x)
        txt += '\n\n'

    with open('test/tmp.dat', 'w') as file:
        file.write(txt)

    # Save text for points
    txt = ''
    for n in range(N):
        txt += '({:.2f}, {:.2f}, {:.4f}) '.format(points[n, 0]*n_p, points[n, 1]*n_p, values[n])

    with open('test/tmp2.dat', 'w') as file:
        file.write(txt)
