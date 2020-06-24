#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import scipy.interpolate as spint
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import Delaunay, delaunay_plot_2d, Voronoi, voronoi_plot_2d


def interpolate(points, values, n_p, method='nearest'):

    X, Y = np.mgrid[0:n_p, 0:n_p]

    # Interpolation is performed.
    nn_interpolated_values = spint.griddata(
        points*n_p, values, (Y, X), method=method)

    return nn_interpolated_values.reshape((n_p, n_p)), X, Y


if __name__ == '__main__':

    # Get points
    np.random.seed(0)
    N = 10
    points = np.random.rand(N, 2)
    values = np.random.rand(N)

    # Interpolation
    n_p = 100
    int_values, X, Y = interpolate(points, values, n_p, 'cubic')

    fig, ax = plt.subplots()
    ax.matshow(int_values)
    ax.scatter(points[:, 0]*n_p, points[:, 1]*n_p, c='red')

    ax.set_aspect('equal')
    plt.show()

    # Save text
    txt = ''
    for x in range(n_p):
        for y in range(n_p):
            if not np.isnan(int_values[x, y]):
                txt += '({}, {}, {:.4f}) '.format(Y[x, y], X[x, y], int_values[x, y])
            else:
                txt += '({}, {}, inf) '.format(Y[x, y], X[x, y])
        txt += '\n\n'

    with open('test/tmp.dat', 'w') as file:
        file.write(txt)

    # Save text for points
    txt = ''
    for n in range(N):
        txt += '({:.2f}, {:.2f}, {:.4f}) '.format(points[n, 0]*n_p, points[n, 1]*n_p, values[n])

    with open('test/tmp2.dat', 'w') as file:
        file.write(txt)


    # Dlaunay tri
    # tri = Delaunay(points)


    # with open('tmp.tikz', 'w') as file:

    #     # Delaunay tri
    #     style_d = 'draw=black, thick'
    #     simp = tri.simplices
    #     x, y = tri.points.T
    #     for cnt in range(simp.shape[0]):
    #         ind0, ind1, ind2 = list(simp[cnt, :])
    #         file.write(
    #             "\t\\path [{}] (axis cs:{}, {}) -- \n\t\t(axis cs:{}, {}) -- \n\t\t(axis cs:{}, {}) -- cycle;\n".format(
    #                 style_d,
    #                 x[ind0]*n_p, y[ind0]*n_p, x[ind1]*n_p, y[ind1]*n_p, x[ind2]*n_p, y[ind2]*n_p))


    #     file.write('\t\\end{axis}\n\\end{tikzpicture}')

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # ax.scatter(points[:, 0]*n_p, points[:, 1]*n_p, values, c='red')
    # plt.show()
