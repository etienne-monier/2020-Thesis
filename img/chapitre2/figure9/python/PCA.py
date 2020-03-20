#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import inpystem
import pyxport


if __name__ == '__main__':

    # Load full data
    spim = inpystem.load_key('HR-Spim4-2-ali', ndim=3)

    # Perform PCA
    pca_op = inpystem.tools.PCA.PcaHandler(spim.hsdata.data, PCA_th='max')

    # Build eV array
    offset = spim.hsdata.axes_manager[2].offset
    scale = spim.hsdata.axes_manager[2].scale
    # Number of bands
    B = spim.hsdata.data.shape[-1]
    eV = offset + np.arange(B) * scale

    # Mean spectrum
    Ym = np.squeeze(pca_op.Ym[0, 0, :])

    # Get spectrum components
    N = 6
    H = pca_op.H[:, :N]

    # Save everything
    dico = {'eV': eV, 'mean': Ym,
            'd': pca_op.InfoOut['d'], 'xd': np.arange(B) + 1}

    for ind in range(6):
        dico['comp{}'.format(ind)] = H[:, ind]

    pyxport.save_dat(dico, loc='data/pca_spectra.dat')

    # Save image
    for cnt in range(6):
        pyxport.plot2im(
            np.squeeze(pca_op.Y_PCA[:, :, cnt]),
            'PCA_map_{}.png'.format(cnt), cmap='gray')
