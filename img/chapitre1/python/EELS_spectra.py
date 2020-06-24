#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import inpystem
import pyxport
import imageio
import matplotlib.pyplot as plt
import addpatch


if __name__ == '__main__':

    # Create output image and spectra
    spim = inpystem.load_example('HR-sample', ndim=3)
    haadf = inpystem.load_example('HR-sample', ndim=2)

    # Locations
    pixels = [(6, 25), (6, 38), (6, 69)]
    c = ['r', 'b', 'g']

    # Save spectra
    offset = spim.hsdata.axes_manager[2].offset
    scale = spim.hsdata.axes_manager[2].scale
    M = spim.hsdata.axes_manager[2].size
    dico = {'eV': offset + scale * np.arange(M),
            'loc1': spim.hsdata.data[pixels[0]],
            'loc2': spim.hsdata.data[pixels[1]],
            'loc3': spim.hsdata.data[pixels[2]]
            }
    pyxport.save_dat(dico, '../data/eels_spectra.dat')

    # Save images bor given bands.
    for band in [410, 1001, 1465]:
        pyxport.plot2im(
            spim.hsdata.data[:, :, band],
            loc='../eels_spectra_band_{}.png'.format(band),
            cmap='gray')
        print('Band #{}: {}eV'.format(band, offset + scale * band))

    # Save image
    file = 'eels_spectra_location.png'
    pyxport.plot2im(
        haadf.hsdata.data, file, cmap='gray')

    # Re-open image
    im = imageio.imread(file)

    # zoom_im = rect_patch(im, ulpix=(10, 5), lrpix=(30, 25))

    for cnt in range(3):
        # im = addpatch.pix_patch(im, pix=pixels[cnt], c=c[cnt])
        im = addpatch.rect_patch(
            im, ulpix=pixels[cnt],
            lrpix=(pixels[cnt][0] + 1, pixels[cnt][1] + 1), c=c[cnt])

    # Save result
    imageio.imwrite('../eels_spectra_haadf.png', im)

    # Plot result
    fig, ax = plt.subplots()
    ax.imshow(im)
    ax.axis('off')

    plt.show()
