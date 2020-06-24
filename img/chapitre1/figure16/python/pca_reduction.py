import inpystem
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pyxport


if __name__ == '__main__':

    # Import data
    #
    s = inpystem.load_key('HR-Spim4-2-ali', ndim=3)
    data = s.hsdata.data

    # shapes
    m, n, l = data.shape
    Y = data.reshape((m*n, l)).T

    # Centered data.
    Ym = Y - np.tile(Y.mean(axis=1)[:, np.newaxis], [1, m*n])
    # Reduced data.
    Yr = Ym / np.tile(Y.std(axis=1)[:, np.newaxis], [1, m*n])

    ev = s.hsdata.axes_manager[2].offset + \
        np.arange(l) * s.hsdata.axes_manager[2].scale

    # Compute variance and save it
    #

    std_Y = Y.std(axis=1)

    dico = {'eV': ev, 'std': std_Y, 'mean': Y.mean(axis=1)}
    pyxport.save_dat(dico, loc='data_variance.dat')

    # Study with centered data
    #
    Ncomp = 5

    # Apply pca
    pca = PCA(n_components=Ncomp)
    pca.fit(Ym.T)

    H_m = pca.components_.T
    ratios_m = pca.explained_variance_ratio_

    # Study with reduced data
    #
    # Apply pca
    pca = PCA(n_components=Ncomp)
    pca.fit(Yr.T)

    H_r = pca.components_.T
    ratios_r = pca.explained_variance_ratio_

    # Display everything
    #

    fig, ax = plt.subplots(Ncomp, 1)

    for ind in range(Ncomp):
        ax[ind].plot(H_m[:, ind])
        ax[ind].plot(H_r[:, ind])

    # Save spectra
    dico = {'eV': ev}
    for ind in range(Ncomp):
        dico[f'Hm{ind}'] = H_m[:, ind]
        dico[f'Hr{ind}'] = H_r[:, ind]
    pyxport.save_dat(dico, loc='components.dat')

    print(f'centered data: {ratios_m}\nreduced data: {ratios_r}')
