import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, delaunay_plot_2d, Voronoi, voronoi_plot_2d


def Voronoi_repr(vor):

    center = vor.points.mean(axis=0)
    ptp_bound = vor.points.ptp(axis=0)

    finite_segments = []
    infinite_segments = []
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            finite_segments.append(vor.vertices[simplex])
        else:
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            if (vor.furthest_site):
                direction = -direction
            far_point = vor.vertices[i] + direction * ptp_bound.max()

            infinite_segments.append([vor.vertices[i], far_point])

    return finite_segments, infinite_segments


def get_circumscribed_circle(x1, y1, x2, y2, x3, y3):
    A = np.array([[x3-x1, y3-y1], [x3-x2, y3-y2]])
    Y = np.array([(x3**2 + y3**2 - x1**2 - y1**2), (x3**2+y3**2 - x2**2-y2**2)])
    if np.linalg.det(A) == 0:
        return False
    Ainv = np.linalg.inv(A)
    X = 0.5*np.dot(Ainv, Y)
    x, y = X[0], X[1]
    r = np.sqrt((x-x1)**2+(y-y1)**2)
    return x, y, r


if __name__ == '__main__':
    # Get points
    np.random.seed(0)
    N = 10  # 5
    points = np.random.rand(N, 2)

    # Compute voronoi cells
    vor = Voronoi(points)

    # Dlaunay tri
    tri = Delaunay(points)

    # Create file
    with open('Voronoi.tikz', 'w') as file:

        file.write(r"""\begin{tikzpicture}

    \begin{axis}[
        xmin=0, xmax=1,
        ymin=0, ymax=1,
        xtick=\empty, ytick=\empty,
        ]
    """)

        # Iterate over path
        file.write('\n\n% Voronoi Cells.\n\n')

        style_v = 'draw=red, thick'
        finite, infinite = Voronoi_repr(vor)
        for cnt in range(len(finite)):
            file.write(
                "\t\\path [{}] (axis cs:{}, {}) -- \n\t\t(axis cs:{}, {});\n".format(
                    style_v,
                    finite[cnt][0, 0], finite[cnt][0, 1],
                    finite[cnt][1, 0], finite[cnt][1, 1]))
        for cnt in range(len(infinite)):
            file.write(
                "\t\\path [{}] (axis cs:{}, {}) -- (axis cs:{}, {});\n".format(
                    style_v,
                    infinite[cnt][0][0], infinite[cnt][0][1],
                    infinite[cnt][1][0], infinite[cnt][1][1]))

        file.write('\n\n% Delaunay triangulation.\n\n')

        # Delaunay tri
        style_d = 'draw=black, thick'
        simp = tri.simplices
        x, y = tri.points.T
        for cnt in range(simp.shape[0]):
            ind0, ind1, ind2 = list(simp[cnt, :])
            file.write(
                "\t\\path [{}] (axis cs:{}, {}) -- \n\t\t(axis cs:{}, {}) -- \n\t\t(axis cs:{}, {}) -- cycle;\n".format(
                    style_d,
                    x[ind0], y[ind0], x[ind1], y[ind1], x[ind2], y[ind2]))

        # Draw sampl. points
        file.write('\n\n% Samp. points.\n\n')

        file.write("\t\\addplot+[only marks] coordinates{\n")
        for cnt in range(N):
            file.write("\t\t({}, {})\n".format(points[cnt, 0], points[cnt, 1]))
        file.write('\t};\n\n')

        file.write('\t\\end{axis}\n\\end{tikzpicture}')

    # Create file # 2
    #
    #
    with open('Delaunay.tikz', 'w') as file:

        file.write(r"""\begin{tikzpicture}

    \begin{axis}[
        width=7cm, height=7cm,
        xmin=0, xmax=1,
        ymin=0, ymax=1,
        xtick=\empty, ytick=\empty,
        hide axis,
        ]
    """)

        # Circles
        file.write('\n\n% Circles.\n\n')

        style_d = 'draw=gray, opacity=0.5, thick'
        simp = tri.simplices
        x, y = tri.points.T
        for cnt in range(simp.shape[0]):

            # Get locations
            ind0, ind1, ind2 = list(simp[cnt, :])
            x0, y0, x1, y1, x2, y2 = x[ind0], y[ind0], x[ind1], y[ind1], x[ind2], y[ind2]
            xc, yc, radius = get_circumscribed_circle(x0, y0, x1, y1, x2, y2)

            file.write(
                "\t\\draw [{}] (axis cs:{}, {}) circle [radius={}];\n".format(
                    style_d, xc, yc, radius))

        # Delaunay triangulation
        file.write('\n\n% Delaunay triangulation.\n\n')

        # Delaunay tri
        style_d = 'draw=black, thick'
        simp = tri.simplices
        x, y = tri.points.T
        for cnt in range(simp.shape[0]):
            ind0, ind1, ind2 = list(simp[cnt, :])
            file.write(
                "\t\\path [{}] (axis cs:{}, {}) -- \n\t\t(axis cs:{}, {}) -- \n\t\t(axis cs:{}, {}) -- cycle;\n".format(
                    style_d,
                    x[ind0], y[ind0], x[ind1], y[ind1], x[ind2], y[ind2]))

        # Draw sampl. points
        file.write('\n\n% Samp. points.\n\n')

        file.write("\t\\addplot+[only marks] coordinates{\n")
        for cnt in range(N):
            file.write("\t\t({}, {})\n".format(points[cnt, 0], points[cnt, 1]))
        file.write('\t};\n\n')

        file.write('\t\\end{axis}\n\\end{tikzpicture}')





    #fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=2)
    # delaunay_plot_2d(tri)
    # plt.show()
