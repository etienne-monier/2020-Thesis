#! /usr/bin/env python

import inpystem
import pyxport

import numpy as np
import scipy.io as sio

import matplotlib.pyplot as plt

import cv2

def myclip(A):
    return np.floor(255*((A-A.min())/(A.max()-A.min())))

if __name__ == '__main__':

    m_data = sio.loadmat('DataInfo.mat')
    eV = np.squeeze(m_data['eV'])

    s = inpystem.load_key('LR-Spim8', ndim=3)
    # s.plot()

    # Get spectra
    s1 = s.hsdata.data[16, 22, :]
    s2 = s.hsdata.data[39, 43, :]
    s3 = s.hsdata.data[30, 6, :]

    s1m = np.mean(s.hsdata.data[14:19, 20:25, :], axis=(0, 1))
    s2m = np.mean(s.hsdata.data[37:42, 41:46, :], axis=(0, 1))
    s3m = np.mean(s.hsdata.data[28:33, 4:9, :], axis=(0, 1))

    # save everything
    name = [f's{ind}' for ind in range(1, 4)] + [f's{ind}m' for ind in range(1, 4)]
    data = [eval(f's{ind}') for ind in range(1, 4)] + [eval(f's{ind}m') for ind in range(1, 4)]
    dico2 = dict(zip(name, data))
    dico = {'eV': eV, **dico2}
    pyxport.save_dat(dico, loc='data.dat')

    # Prepare image
    #
    im = inpystem.load_key('LR-Spim8', ndim=2).hsdata.data
    im = myclip(np.tile(im[:, :, np.newaxis], [1, 1, 3]))

    # Blue color in BGR
    colors = [(119, 158, 27), (2, 95, 217), (179, 112, 117)]

    im = cv2.rectangle(im, (20, 14), (24, 18), colors[0], 1)
    im = cv2.rectangle(im, (41, 37), (45, 41), colors[1], 1)
    im = cv2.rectangle(im, (4, 28), (8, 32), colors[2], 1)

    im[16, 22, :] = colors[0]
    im[39, 43, :] = colors[1]
    im[30, 6, :] = colors[2]

    im = np.swapaxes(im, 0, 1)

    cv2.imwrite('../loc-image.png', im)

    # Display with plt
    #
    fig, ax = plt.subplots(3, 1)
    ax[0].plot(s1)
    ax[0].plot(s2)
    ax[0].plot(s3)

    ax[1].plot(s1m)
    ax[1].plot(s2m)
    ax[1].plot(s3m)

    ax[2].matshow(im/255)
    plt.show()
