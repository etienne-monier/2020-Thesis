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

    t1 = (H[0, :] + H[1, :], H[0, :] - H[1, :])
    t2 = (H[0, :] + 0.3*H[1, :], H[0, :] - 0.3*H[1, :])
    t3 = (H[0, :] + 0.1*H[1, :], H[0, :] - 0.1*H[1, :])

    for cnt, t in enumerate([t1, t2, t3]):

        X = np.vstack((u[np.newaxis, :] for u in t))

        h = np.array([1, 1])
        h = h/np.linalg.norm(h)
        
        Y1 = h[:, np.newaxis] @ h[np.newaxis, :] @ X
        
        dico = {'x1': X[0, :], 'x2': X[1, :], 'y1': Y1[0, :], 'y2': Y1[1, :]}
        pyxport.save_dat(dico, f'approximations_{cnt}.dat')

