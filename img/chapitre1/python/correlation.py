# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pyxport


def torad(angle):
    """Converts angle from degree to rad.
    """
    return angle * np.pi / 180


def draw_range(N, lim):
    """Draws uniformly N samples in the limits.
    """
    return (lim[1] - lim[0]) * np.random.random_sample(N) + lim[0]


if __name__ == '__main__':

    R = 10
    alim = [20, 80]
    blim = [20, 80]
    rlim = [0.9*R, 1.1*R]

    N = 1000
    lims = [alim, blim, rlim]

    a, b, r = (draw_range(N, lims[cnt]) for cnt in range(3))

    x = r * np.sin(torad(b)) * np.cos(torad(a))
    y = r * np.sin(torad(b)) * np.sin(torad(a))
    z = r * np.cos(torad(b))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax.set_xlim([0, R])
    ax.set_ylim([0, R])
    ax.set_zlim([0, R])

    plt.show()

    dico = {'x': x, 'y':y, 'z':z}
    pyxport.save_dat(dico, loc='manifold_corr.dat')
