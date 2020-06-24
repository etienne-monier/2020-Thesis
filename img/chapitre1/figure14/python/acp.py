#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pyxport


def return_dico(X, h):
    dico = {'x1': X[0, :], 'x2': X[1, :]}

    h = h/np.linalg.norm(h)

    p = np.squeeze(h[np.newaxis, :] @ X)
    dico['p'] = p

    P = X.shape[1]
    dico['py'] = np.zeros(P)
    dico['pyy'] = np.ones(P)
    dico['pyyy'] = 2*np.ones(P)
    dico['pyyyy'] = 3*np.ones(P)

    return dico


if __name__ == '__main__':

    P, M = 100, 2
    np.random.seed(0)

    H = np.random.randn(M, P)
    H[1, :] = 0.3*H[1, :]

    t = (H[0, :] + H[1, :], H[0, :] - H[1, :])
    X = np.vstack((u[np.newaxis, :] for u in t))

    # good case
    h = np.array([1, 0.5])
    dico = return_dico(X, h)
    pyxport.save_dat(dico, 'data.dat')

    # worst case
    h = np.array([1, -1])
    dico = return_dico(X, h)
    pyxport.save_dat(dico, 'worst_data.dat')

    # better case
    h = np.array([1, 10])
    dico = return_dico(X, h)
    pyxport.save_dat(dico, 'better_data.dat')

    # best case
    h = np.array([1, 1])
    dico = return_dico(X, h)
    pyxport.save_dat(dico, 'best_data.dat')

    fig, ax = plt.subplots()
    ax.scatter(X[0, :], X[1, :])
    plt.show()

    # Approximations
    h = h/np.linalg.norm(h)
    Y1 = h[:, np.newaxis] @ h[np.newaxis, :] @ X
    Res = X - Y1

    h2 = np.array([1, -1])
    h2 = h2/np.linalg.norm(h2)

    s1 = np.squeeze(h[np.newaxis, :] @ X)
    s2 = np.squeeze(h2[np.newaxis, :] @ Res)

    dico2 = {'y1': Y1[0, :], 'y2': Y1[1, :],
             'res1': Res[0, :], 'res2': Res[1, :],
             's1': s1, 's2': s2}
    pyxport.save_dat(dico2, 'approximations.dat')
