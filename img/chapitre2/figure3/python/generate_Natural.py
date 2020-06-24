import numpy as np
from scipy.spatial import Voronoi


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


if __name__ == '__main__':
    # Get points
    np.random.seed(0)
    N = 10  # 5
    points = np.random.rand(N, 2)

    # Compute voronoi cells
    vor = Voronoi(points, incremental=True)
    finite, infinite = Voronoi_repr(vor)

    vor.add_points(np.array([[0.25, 0.25]]))
    finite2, infinite2 = Voronoi_repr(vor)

    # Create file
    with open('Voronoi_Natural.tikz', 'w') as file:

        file.write(r"""\begin{tikzpicture}

    \begin{axis}[
        xmin=0, xmax=1,
        ymin=0, ymax=1,
        xtick=\empty, ytick=\empty,
        ]
    """)

        # Iterate over path
        file.write('\n\n% Voronoi Cells before.\n\n')

        style_v = 'draw=red, thick'
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

        # Iterate over path
        file.write('\n\n% Voronoi Cells before.\n\n')

        style_v = 'draw=gray, thick, opacity=0.5'
        for cnt in range(len(finite2)):
            file.write(
                "\t\\path [{}] (axis cs:{}, {}) -- \n\t\t(axis cs:{}, {});\n".format(
                    style_v,
                    finite2[cnt][0, 0], finite2[cnt][0, 1],
                    finite2[cnt][1, 0], finite2[cnt][1, 1]))
        for cnt in range(len(infinite2)):
            file.write(
                "\t\\path [{}] (axis cs:{}, {}) -- (axis cs:{}, {});\n".format(
                    style_v,
                    infinite2[cnt][0][0], infinite2[cnt][0][1],
                    infinite2[cnt][1][0], infinite2[cnt][1][1]))

        # Draw sampl. points
        file.write('\n\n% Samp. points.\n\n')

        file.write("\t\\addplot+[only marks] coordinates{\n")
        for cnt in range(N):
            file.write("\t\t({}, {})\n".format(points[cnt, 0], points[cnt, 1]))
        file.write('\t};\n\n')

        file.write('\t\\end{axis}\n\\end{tikzpicture}')

