#!/usr/bin/env python

import numpy as np
import numpy.linalg as lin


def EigenEstimate(l):
    
    # Get data dimension
    M = l.size

    # Initial data ----------------------
    #
    # The initial data consists in a table
    #
    # +-----+-----+-----+---------+
    # | l_0 | l_1 | ... | l_{M-1} |
    # +-----+-----+-----+---------+
    # | a_0 | a_1 | ... | a_{M-1} |
    # +-----+-----+-----+---------+
    # where l (resp. a) are lattent variables (resp. denominator of Stein
    # estimator).

    # Stein estimator
    table = np.stack((l, np.zeros(l.size)), axis=0)

    for col in range(M):

        # That's an (M, )-array filled with 1 but at col position.
        ncol = np.logical_not(np.in1d(range(M), col))

        table[1, col] = 1 + (1 / M) * np.sum(
            (l[col] + l[ncol]) / (l[col] - l[ncol])
            )
    
    for cnt in range(M):
        print(f"{table[0, cnt]:.2f}&\t{table[1, cnt]:.2f}\\\\")
    # Procedure 1st step ----------------------
    #
    # Here, the goal is to make all a_i positive.
    #
    # 1. Start at the right of the table and search to the left until the
    #    first pair (l_j, a_j) with negative a_j is reached.
    # 2. Pool this pair with the pair imediately on the left of it,
    #    replacing them with the pair (l_j + l_{j-1}, a_j + a_{j-1}), to
    #    form a list which is on pair shorter.
    # 3. Repeat 1 and 2 until all a_j are positive.
    #
    # We will denote here M1 the length of the modified table.
    #
    # The back_pos variable is a list of lists. Its length will be M1 at the
    # end of this step. back_pos[j1] for j1 smaller than M1 will be all the
    # columns of the initial table that were used to create the column j1
    # of the new table.

    back_pos = [[i] for i in range(M)]

    while (np.any(table[1, :] < 0)):  # there are <0 alphai

        # Initial cursor position in the table.
        cpos = table.shape[1] - 1

        # Searching the position of the negative a_i.
        while (table[1, cpos] > 0):
            cpos = cpos - 1

        # The sum of the two pairs.
        sum_pairs = np.sum(table[:, cpos-1:cpos+1], axis=1)[:, np.newaxis]

        # Depending of the cases, the arrays to stack are different.
        if cpos == table.shape[1] - 1:  # That's the last pair.
            hstack_ar = (table[:, :cpos-1], sum_pairs)

        elif cpos == 1:  # That's the first pair
            hstack_ar = (sum_pairs, table[:, cpos+1:])

        else:  # The cursor is in the middle of table.
            hstack_ar = (table[:, :cpos-1], sum_pairs, table[:, cpos+1:])

        # Create new table
        table = np.hstack(hstack_ar)

        # Modify index list.
        back_pos[cpos-1].extend(back_pos[cpos])
        del back_pos[cpos]

    # Procedure 2nd step ----------------------
    #
    # Here, the goal is to re-order the ratios l_j/a_j so that they are
    # decreasing.
    #
    # To that end, a row will be added to table, which is the ratio of the
    # first and the second lines.
    #
    # A pair (l_j, a_j) is called violating pair if the ratio l_j/a_j is not
    # larger than l_{j+1}/a_{j+1}.
    #
    # 1. Start at the bottom of the list found in Step 1 and proceed to the
    #    left until the first violating pair, say (l_j, a_j), is reached.
    # 2. Pool this violating pair with the pair immediately on the right by
    #    replacing these two pairs and their ratios with the pair
    #    (l_j+l_{j+1}, a_j+a_{j+1}) and its ratio
    #    (l_j+l_{j+1})/(a_j+a_{j+1}), forming a new list shorter by one pair.
    # 3. Start at the pair imediately at the right (or the replacing pair
    #    itself if that's the last one) and proceed to the left until a
    #    violating pair is found, then repeat 2.
    # 4. Repeat 3 until all ratios l_j/a_j are in decreasing order.
    #
    # In this step, the back_pos variable will be modified in a similar way
    # as for Step 1.

    table = np.vstack((table, table[0, :] / table[1, :]))

    # Current position
    cpos = table.shape[1] - 2

    # If cpos get to -1, it means that no pair is violating.
    while cpos >= 0:

        while table[2, cpos+1] < table[2, cpos] and cpos >= 0:
            cpos = cpos - 1

        if cpos >= 0:
            # A violating pair was found.

            # The pairs are summed.
            sum_pairs = np.sum(table[:, cpos:cpos+2], axis=1)[:, np.newaxis]
            sum_pairs[2] = sum_pairs[0] / sum_pairs[1]

            # Depending of the cases, the arrays to stack are different.
            if cpos == table.shape[1] - 2:  # That's the before last pair.
                hstack_ar = (table[:, :cpos], sum_pairs)

            elif cpos == 0:  # That's the first pair
                hstack_ar = (sum_pairs, table[:, cpos+2:])

            else:  # The cursor is in the middle of table.
                hstack_ar = (table[:, :cpos], sum_pairs, table[:, cpos+2:])

            # Create new table
            table = np.hstack(hstack_ar)

            # Modify index list.
            back_pos[cpos].extend(back_pos[cpos+1])
            del back_pos[cpos+1]

            # Move the cursor to the left if cpos is at the extreme right.
            if cpos == table.shape[1] - 1:
                cpos = table.shape[1] - 2

    # Procedure 3nd step ----------------------
    #
    # Each ratio in the final table was obtained by pooling a block of one
    # or more consecutive pairs in the original list. To obtain Stein's
    # modified estimates, we assign this ratio to all pairs of the block.

    # Stein estimate output.
    sl = np.zeros(M)

    for cnt in range(table.shape[1]):
        sl[back_pos[cnt]] = table[2, cnt] * np.ones(len(back_pos[cnt]))

    # Sigma and dimension estimation ----------------------
    #

    # A threasholding is applied to avoid zero estimates.
    sl[sl < 1e-12] = 1e-12

    # Noise standard deviation is estimated to be the last Stein estimate.
    sig = np.sqrt(sl[-1])

    # The signal dimension is estimated to be the first positin such that sl
    # is equal to sig.
    D = min(back_pos[-1])

    return (sl, sig, D)



if __name__ == '__main__':

    # Construct Wishart realisation
    p, n = 10, 10
    np.random.seed(2)
    X = np.random.randn(n, p)
    S = X @ X.T

    # Catch eigs
    w, V = lin.eig(S)

    # Sort it
    d = np.sort(w)[::-1]
    print(d)
    EigenEstimate(d)
