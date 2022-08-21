from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
import Shrink_Polygon_Watchman_Route
from Shrink_Polygon_AGP_With_Holes import return_values
from astar import *
from dijkstra import *
from TSP_search import *
from genetic_tsp import genetic_search
import argparse

def get_min(polygon):
    '''

    Args:
        polygon: The polygon, with and without holes

    Returns: min x and y coordinate of the polygon to help set the grid

    '''
    min_x = 0
    min_y = 0

    for (x, y) in polygon:
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y

    return min_x, min_y


def get_limits(polygon):
    '''

    Args:
        polygon: The polygon with or without holes

    Returns: The max x and y coordinate of the polygon to help setup the grid

    '''
    lim_x, lim_y = 0, 0

    for x, y in polygon:
        if x > lim_x:
            lim_x = x
        if y > lim_y:
            lim_y = y

    return lim_x, lim_y

def translate_holes(holes, min_x, min_y):
    '''

    Args:
        holes: The holes in the polygon
        min_x: min_x of the holes
        min_y: min_y of the holes

    Returns: Translate the polygon to help setup the grid in 0-max limit

    '''
    np = []
    for i in holes:
        new_poly = []
        for (x, y) in i:
            new_poly.append((x+abs(min_x), y+abs(min_y)))
        np.append(new_poly)
    return np


def translate_poly(polygon, min_x, min_y):
    '''

    Args:
        polygon: Polygon without holes
        min_x: min x of the polygon
        min_y: min y of the polygon

    Returns: translated polygon to help setup the grid

    '''
    new_poly = []
    for (x, y) in polygon:
        new_poly.append((x+abs(min_x), y+abs(min_y)))
    return new_poly


def plot(back_track, P, flag, holes=[]):
    '''

    Args:
        back_track: Paths pf all the points
        P: Polygon for collision check

    Returns: None

    '''
    for i in back_track:
        if len(i) == 1:
            continue
        point_list = [pair for pair in itertools.pairwise(i)]
        for j in range(len(point_list)):
            x_values = [point_list[j][0][0], point_list[j][1][0]]
            y_values = [point_list[j][0][1], point_list[j][1][1]]
            plt.plot(x_values, y_values, c='grey')

    x, y = zip(*P)
    plt.plot(x, y)
    plt.scatter(guard_x, guard_y, c='blue')
    if not flag:
        for h in holes:
            h.append(h[0])
            xh, yh = zip(*h)
            plt.plot(xh, yh)
    # plt.scatter(guard_x, guard_y, c="red")
    plt.show()

def dfs(point, polygon):
    '''

    Args:
        point: The point of scan locaation, sometimes on the edge of the polygon or just outside, will cause error
        polygon: polygon

    Returns: point inside the polygon

    '''
    if polygon.contains(Point(point[0]+1, point[1])):
        return (point[0]+1, point[1])
    if polygon.contains(Point(point[0]-1, point[1])):
        return (point[0]-1, point[1])
    if polygon.contains(Point(point[0], point[1]+1)):
        return (point[0], point[1]+1)
    if polygon.contains(Point(point[0], point[1]-1)):
        return (point[0], point[1]-1)

if __name__ == '__main__':

    fig, ax = plt.subplots()
    guard_x, guard_y, watchman_route_pts = [], [], []
    parser = argparse.ArgumentParser(description='Watchman Route')
    parser.add_argument('--holes', '-ho', help='Enter flag for polygon with or without holes', action=argparse.BooleanOptionalAction, required=True)
    args = parser.parse_args()
    print(args.holes)
    flag = args.holes  # for polygon with holes keep false
    if flag:
        guards, old_p = Shrink_Polygon_Watchman_Route.shrink()
        mx, my = get_min(old_p)
    else:
        guards, old_p, h = return_values()
        mx, my = get_min(old_p)
        holes = translate_holes(h, mx, my)
    # get the guards
    Guards = translate_poly(guards, mx, my)
    P = translate_poly(old_p, mx, my)
    lim_x, lim_y = get_limits(P)
    final_guards = tuple(tuple(map(int, tup)) for tup in Guards)
    # convert polygon into shapely polygon
    if flag:
        polygon = Polygon(P)
    else:
        polygon = Polygon(P, holes=holes)

    grid = grid(lim_x, lim_y, polygon) # setup the grid
    for i in final_guards:
        if polygon.contains(Point(i)):
            guard_x.append(int(i[0])), guard_y.append(int(i[1]))
            watchman_route_pts.append(i)
        else:
            watchman_route_pts.append(dfs(i, polygon))
    print(f"Number of guards: {len(watchman_route_pts)}")
    back_track, paths, back_track_track = [], [], []
    s = time.time()

    for i in range(len(watchman_route_pts)):
        path_length_for_one_pt = []
        path_for_specific_point = []
        for j in range(len(watchman_route_pts)):
            # path, path_length = search(grid, watchman_route_pts[i], watchman_route_pts[j], polygon)
            path, path_length = astar(grid, watchman_route_pts[i], watchman_route_pts[j], polygon)

            path_length_for_one_pt.append(path_length)
            back_track.append(path)
            path_for_specific_point.append(path)
        back_track_track.append(path_for_specific_point)
        paths.append(path_length_for_one_pt)

    # sometimes one path is shown as 0 for some reason, debug properly but this fixes it, same thing  essentially
    for i in range(len(paths)):
        for j in range(len(paths[i])):
            if i != j and paths[i][j] == 0:
                paths[i][j] = paths[j][i]

    print(f'This the adj matrix for path lengths')
    print()
    for p in paths:
        print(p)
    print()

    genetic_search(paths)
    print(f'The path length from brute force {brute_force(paths)}')
    print('----------------------------------')
    pl, final_path, t = held_karp(paths)
    print(f'This is the order of traversal {final_path}')
    print(f'The path length for held-karp {pl}')
    print('----------------------------------')

    if not flag:
        plot(back_track, P, flag, holes)
    else:
        plot(back_track, P, flag)

    x, y = zip(*P)
    plt.figure()
    plt.plot(x, y)
    # plot the holes
    if not flag:
        for h in holes:
            h.append(h[0])
            xh, yh = zip(*h)
            plt.plot(xh, yh)

    plt.scatter(guard_x, guard_y, s=0.3, c='blue')
    final_arrange = []
    final_path.append(0)
    for i in range(len(final_path)-1):
        final_arrange.append(back_track_track[final_path[i]][final_path[i+1]])

    final_pairs = [[j for j in itertools.pairwise(final_pair)] for final_pair in final_arrange]
    for j in final_pairs:
        for i in range(len(j)):
            if i == len(j)-1:
                x_values = [j[i][0][0], j[i][1][0]]
                y_values = [j[i][0][1], j[i][1][1]]
                plt.arrow(x_values[0], y_values[0], x_values[1] - x_values[0], y_values[1] - y_values[0],
                          head_width=1, width=0.7, ec='black')
            else:
                x_values = [j[i][0][0], j[i][1][0]]
                y_values = [j[i][0][1], j[i][1][1]]
                plt.arrow(x_values[0], y_values[0], x_values[1]-x_values[0], y_values[1]-y_values[0], ec='red')
    plt.show()
