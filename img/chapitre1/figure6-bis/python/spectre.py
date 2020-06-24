# -*- coding: utf-8 -*-

import hyperspy.api as hs

import numpy as np
import matplotlib.pyplot as plt

from scipy.special import erf

import pyxport


def normalize(x):
    return x/x.max()


def seuil(mu, sig, ampl, ratio=0.2):

    gauss = normalize(np.exp(-(ev-mu)**2/(2*sig**2)))
    cdf = 0.5*(1+erf((ev-mu)/(sig*np.sqrt(2))))

    return ampl * normalize(gauss + ratio * cdf)


if __name__ == '__main__':

    # Fond décroissant
    ev = np.arange(400, 1e3)
    s = 5e5/ev

    # Seuils
    s1 = seuil(500, 5, 300)
    s2 = seuil(700, 3, 200)
    s3 = seuil(800, 2, 100)

    # Débuts
    T1 = np.argmax(ev == 500 - 5 * 3)
    T2 = np.argmax(ev == 700 - 3 * 3)
    T3 = np.argmax(ev == 800 - 2 * 3)
    sl1 = slice(T1, None)
    sl2 = slice(T2, None)
    sl3 = slice(T3, None)

    # Dico to save
    pyxport.save_dat({'ev': ev, 'fond': s, 'sig': s+s1+s2+s3},
                     loc='full.dat')

    pyxport.save_dat({'ev': ev[sl1], 'sig': (s+s1)[sl1]},
                     loc='cseuil1.dat')
    pyxport.save_dat({'ev': ev[sl2], 'sig': (s+s1+s2)[sl2]},
                     loc='cseuil2.dat')
    pyxport.save_dat({'ev': ev[sl3], 'sig': (s+s1+s2+s3)[sl3]},
                     loc='cseuil3.dat')

    pyxport.save_dat({'ev': ev[sl1], 'sig': s1[sl1]},
                     loc='seuil1.dat')
    pyxport.save_dat({'ev': ev[sl2], 'sig': s2[sl2]},
                     loc='seuil2.dat')
    pyxport.save_dat({'ev': ev[sl3], 'sig': s3[sl3]},
                     loc='seuil3.dat')

    # fig, ax = plt.subplots()
    # ax.plot(ev, s, ev[sl1], s[sl1] + s1[sl1])

    # plt.show()
