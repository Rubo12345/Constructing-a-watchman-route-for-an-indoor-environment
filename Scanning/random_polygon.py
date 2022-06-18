import numpy as np

# only done for testing, these polygons
# are not realistic
# but can be used to test how the Travelling salesman problem works
def draw_polygon(ax, n, lim_x, lim_y):
    '''

    Args:
        ax: matplot ax
        n: number of edges of polygon
        lim_x: x limit of grid
        lim_y: y limit of grid

    Returns: random polygon

    '''

    x = np.random.randint(0, lim_x, n)
    y = np.random.randint(0, lim_y, n)

    # computing the (or a) 'center point' of the polygon
    center_point = [np.sum(x)/n, np.sum(y)/n]

    angles = np.arctan2(x-center_point[0],y-center_point[1])

    # sorting the points:
    sort_tups = sorted([(i, j, k) for i, j, k in zip(x, y, angles)], key=lambda t: t[2])

    # making sure that there are no duplicates:
    if len(sort_tups) != len(set(sort_tups)):
        raise Exception('two equal coordinates -- exiting')

    x, y, angles = zip(*sort_tups)
    x = list(x)
    y = list(y)

    # appending first coordinate values to lists:
    x.append(x[0])
    y.append(y[0])

    ax.plot(x, y, label='{}'.format(n))
    poly = list(zip(x, y))
    return poly