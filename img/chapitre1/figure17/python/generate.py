import numpy as np
import math
import pyxport


if __name__ == '__main__':

    # Triangle réduit
    #
    c = 0.5
    triangle = (1/3) * np.array([[1+2*c, 1-c, 1-c],
                                 [1-c, 1+2*c, 1-c],
                                 [1-c, 1-c, 1+2*c]])

    for ind in range(3):
        print('({:.3f}, {:.3f}, {:.3f})'.format(
            triangle[ind, 0], triangle[ind, 1], triangle[ind, 2]))

    # Rotation matrix
    #
    u = np.array([1, 1, 1])
    u = u/np.linalg.norm(u)

    theta = 0  # 360/3
    theta_r = theta*math.pi/180
    co, si = math.cos(theta_r), math.sin(theta_r)

    R = np.array([[u[0]**2*(1-co) + co, u[0]*u[1]*(1-co) - u[2]*si, u[0]*u[2]*(1-co) + u[1]*si],
                  [0,                   u[1]**2*(1-co) + co,        u[1]*u[2]*(1-co) - u[0]*si],
                  [0,                   0,                          u[2]**2*(1-co) + co]])
    R[1, 0] = R[0, 1]
    R[2, 0] = R[0, 2]
    R[2, 1] = R[1, 2]

    triangle_2 = np.transpose(R.dot(triangle.T))

    print('\n')
    for ind in range(3):
        print('({:.3f}, {:.3f}, {:.3f})'.format(
            triangle_2[ind, 0], triangle_2[ind, 1], triangle_2[ind, 2]))

    # Construction des échantillons 
    #
    P = 1000
    A = np.random.random((3, P))
    A = A / np.tile(A.sum(0)[np.newaxis, :], [3, 1])

    points = triangle.T @ A

    dico = {'x_0': points[0, :], 'x_1': points[1, :], 'f(x)': points[2, :]}
    pyxport.save_dat(dico, 'rand.dat')

