#!/usr/bin/env python

import numpy as np

arr = np.loadtxt('s2n-hyper.dat', skiprows=1)
arr[:, 2] = (-1) * 10 * arr[:, 2]

np.savetxt('s2n-hyper-snr.dat', arr, header='x   y   c', fmt='%.10f')
