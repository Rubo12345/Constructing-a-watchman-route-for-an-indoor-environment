import math
from shapely.geometry import Point
import copy

def grid(limx, limy, polygon):
    '''

    Args:
        limx: x limit of the grid, equivalent to the largest x coordinate of polygon
        limy: y limit of the grid, equivalent to the largest x coordinate of polygon
        polygon: The polygon

    Returns: grid with 0 and 1 depending if point is inside or outside the polygon

    '''
    grid = []
    if limx > limy:
        limy = limx
    else:
        limx = limy # sometimes dimension error, debug later, only changes the grid to square

    for i in range(0, limx+1):
        row = []
        for j in range(0, limy+1):
            if polygon.contains(Point(i, j)):
                row.append(1)
            else:
                row.append(0)
        grid.append(row)
    return grid



def valid(x, y, grid, visited):
    '''

    Args:
        x: x coordinate of node to be visited
        y: y coodinate of node to be visited
        grid: the grid
        visited: see if the node has already been visited

    Returns: True or False depending on validity

    '''
    if (x >= 0 and y >= 0) and (x < len(grid) and y < len(grid[0])):
        if grid[x][y] == 1 and visited[x][y] is False:
            return True
    return False

def collision_check(p1, p2, polygon):
    n = 10  # number of segments
    p = copy.deepcopy(p1)
    for i in range(n):
        p[0] = p[0] + (p2[0] - p1[0]) / n
        p[1] = p[1] + (p2[1] - p1[1]) / n
        if not polygon.contains(Point(p[0], p[1])):
            return False
    return True

def travel(node, grid, visited, polygon):
    '''

    Args:
        node: The current node
        grid: the grid
        visited: 2d visited array checking if node has already been visited

    Returns: List of points to where the current node can travel

    '''

    possible_travel = []
    if valid(node.x, node.y+1, grid, visited) and collision_check([node.x, node.y], [node.x, node.y+1], polygon):
        possible_travel.append([node.x, node.y+1])

    if valid(node.x+1, node.y, grid, visited) and collision_check([node.x, node.y], [node.x+1, node.y], polygon):
        possible_travel.append([node.x+1, node.y])

    if valid(node.x, node.y-1, grid, visited) and collision_check([node.x, node.y], [node.x, node.y-1], polygon):
        possible_travel.append([node.x, node.y-1])

    if valid(node.x-1, node.y, grid, visited) and collision_check([node.x, node.y], [node.x-1, node.y], polygon):
        possible_travel.append([node.x-1, node.y])

    if valid(node.x-1, node.y-1, grid, visited) and collision_check([node.x, node.y], [node.x-1, node.y-1], polygon):
        possible_travel.append([node.x-1, node.y-1])

    if valid(node.x+1, node.y-1, grid, visited) and collision_check([node.x, node.y], [node.x+1, node.y-1], polygon):
        possible_travel.append([node.x+1, node.y-1])

    if valid(node.x-1, node.y+1, grid, visited) and collision_check([node.x, node.y], [node.x-1, node.y+1], polygon):
        possible_travel.append([node.x-1, node.y+1])

    if valid(node.x+1, node.y+1, grid, visited) and collision_check([node.x, node.y], [node.x+1, node.y+1], polygon):
        possible_travel.append([node.x+1, node.y+1])
    return possible_travel  # returns all possible node locations that you can travel to


def not_seen_min_cost(node, seen):
    '''

    Args:
        node: Current node
        seen: 2d list if the node has been visited

    Returns: the node with minimum f value

    '''
    min_node = None  # initialize min node
    for i in range(len(node)):
        for j in range(len(node[i])):
            if seen[i][j] or node[i][j].cost is None:  # if true
                continue
            if min_node is None:  # updating node
                min_node = node[i][j]
            elif min_node.cost > node[i][j].cost:  # cost
                min_node = node[i][j]
            elif min_node.cost == node[i][j].cost:
                if min_node.h > node[i][j].h:  # comparing h when cost is same
                    min_node = node[i][j]

    return min_node

def distance(start, end):
    '''

    Args:
        start: starting point
        end: ending point

    Returns: eucledian distance

    '''
    distance = math.hypot(abs(end.x-start.x), abs(end.y - start.y))
    return distance

