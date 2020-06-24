#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from sklearn import decomposition
from sklearn.feature_extraction.image import extract_patches_2d

import cv2

import numpy as np
import inpystem
import pyxport


def get_10_pos(A, shape, p, Nr=10):

    pos_mat = []
    m, n = shape
    lim = 12
    A -= A.min()

    x_pos = []
    y_pos = []

    for ind in (range(A.shape[-1])):
        print(f'Comp #{ind}')
        tmp = []

        mat = A[:, ind]

        for cnt in range(Nr):
            print(f'point #{cnt}')
            pos_0 = np.argmax(mat)
            pos = (pos_0 % (n-p), pos_0 // (n-p))

            while np.any(np.logical_and(
                    np.isin(x_pos, np.arange(pos[0]-lim, pos[0]+lim)),
                    np.isin(y_pos, np.arange(pos[1]-lim, pos[1]+lim))
                    )):

                mat[pos_0] = 0
                pos_0 = np.argmax(mat)
                pos = (pos_0 % (n-p), pos_0 // (n-p))

            pos_tuple = pos
            x_pos.append(pos_tuple[0])
            y_pos.append(pos_tuple[1])

            tmp.append(pos_tuple)
            mat[pos_0] = 0

        pos_mat.append(tmp)

    return pos_mat


def myclip(A):
    return np.floor(255*((A-A.min())/(A.max()-A.min())))


if __name__ == '__main__':

    # Load data
    spim = inpystem.load_key('HR-Spim4-2-ali', ndim=2)
    im = spim.hsdata.data

    # Reshape data
    p = 10
    X = extract_patches_2d(im, (p, p)).reshape((-1, p**2))

    # Learn Dico
    n_components = 3
    op = decomposition.MiniBatchDictionaryLearning(
        n_components=n_components, alpha=0.8, transform_algorithm='lasso_cd',
        n_iter=100, batch_size=3, positive_code=True)
    X_out = op.fit_transform(X)

    # Dico
    D = op.components_.reshape(n_components, p, p)

    # Save dico
    c = ['red', 'green', 'blue']
    for cnt in range(n_components):
        cv2.imwrite(f'../dico_{c[cnt]}.png', myclip(D[cnt, :, :]))

    # Display dico
    fig, ax = plt.subplots(1, n_components)
    for ind in range(n_components):
        ax[ind].matshow(D[ind, :, :])

    # Save image with interest regions
    Nr = 5
    pos = get_10_pos(X_out, im.shape, p, Nr)
    color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    img = myclip(np.tile(im[:, :, np.newaxis], [1, 1, 3]))

    for cnt in range(n_components):
        for cnt_2 in range(Nr):
            c_pos = pos[cnt][cnt_2]
            c_pos_2 = (c_pos[0] + p, c_pos[1] + p)
            img = cv2.rectangle(img, (int(c_pos[0]), int(c_pos[1])),
                                (int(c_pos_2[0]), int(c_pos_2[1])), color[cnt], 1)

    # Display image
    fig, ax = plt.subplots()
    ax.matshow(img/255)

    cv2.imwrite(f'../search.png', myclip(img))


    plt.show()


