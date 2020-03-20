#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import inpystem
import pyxport


if __name__ == '__main__':

    # Create output image and spectra
    spim = inpystem.load_key('HR-Spim4-2-ali', ndim=3)

    # Get eV
    offset = spim.hsdata.axes_manager[2].offset
    scale = spim.hsdata.axes_manager[2].scale
    B = spim.hsdata.data.shape[-1]
    eV = offset + np.arange(B) * scale

    # Spectrum
    dico = {'eV': eV, 'spec': np.squeeze(spim.hsdata.data[42, 17, :])}
    pyxport.save_dat(dico, loc='naive_spectrum.dat')

    s = spim.hsdata
    s.remove_background(zero_fill=False, display=True)
    
    pyxport.plot2im(s.data[:, :, 1000:1004].sum(2),
                    loc='regression.png', cmap='gray')

    # s2 = s.remove_background(signal_range=(698, 945), zero_fill=False)
