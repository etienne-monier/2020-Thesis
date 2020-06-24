#!/usr/bin/env python

import numpy as np

for meth in ['3s', 's2n']:
    for cnt in range(1, 4):
        
        arr = np.loadtxt(f'{meth}-data-{cnt}.dat', skiprows=1)

        for cnt2 in range(1, 4):
            arr[:, cnt2] = (-1) * 10 * np.log10(arr[:, cnt2])

        np.savetxt(f'{meth}-data-{cnt}-snr.dat', arr,
                   header='SNR Mean Sup Low', fmt='%.10f', comments='')
