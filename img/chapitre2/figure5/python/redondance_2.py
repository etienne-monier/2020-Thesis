#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn import decomposition
from sklearn.feature_extraction.image import extract_patches_2d

import cv2

import numpy as np
import inpystem


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
    n_components = 6
    op = decomposition.MiniBatchDictionaryLearning(
        n_components=n_components, alpha=0.8, transform_algorithm='lasso_cd',
        n_iter=100, batch_size=3, positive_code=True)
    X_out = op.fit_transform(X)

    # Dico
    D = op.components_.reshape(n_components, p, p)

    # Save dico
    for cnt in range(n_components):
        cv2.imwrite(f'../dico_{cnt}.png', myclip(D[cnt, :, :]))
