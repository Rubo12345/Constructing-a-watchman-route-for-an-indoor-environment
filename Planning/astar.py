from node import Node
from environment import *


def astar(grid, start, goal):
    '''

    Args:
        grid: grid
        start: starting point
        goal: goal point

    Returns: path length between points

    '''
    path = []
    node = []
    for i, row in enumerate(grid):
        col = []
        for j, val in enumerate(row):
            col.append(Node(i, j, val, 0))
        node.append(col)

    for i in range(len(node)):
        for j in range(len(node[i])):
            node[i][j].h = math.hypot(goal[0]-node[i][j].x, goal[1]-node[i][j].y)  # h value for each node

    seen = [[False for _ in range(len(node))]
            for _ in range(len(grid))]

    # initialize the start
    node[start[0]][start[1]].g = 0
    node[start[0]][start[1]].cost = node[start[0]][start[1]].g + node[start[0]][start[1]].h
    current_node = not_seen_min_cost(node, seen)
    seen[current_node.x][current_node.y] = True
    path_length = 0

    while current_node:
        # goal condition
        if current_node.x == goal[0] and current_node.y == goal[1]:

            path.append(goal)
            while path[-1] != start:
                path_length += distance(current_node, current_node.parent)
                path.append((current_node.parent.x, current_node.parent.y))
                current_node = current_node.parent
            path.reverse()
            break

        neighbor_locations = travel(current_node, grid, seen)
        for neighbor in neighbor_locations:
            # check f value
            if node[neighbor[0]][neighbor[1]].cost is None or \
                    node[neighbor[0]][neighbor[1]].cost > current_node.g + distance(current_node, node[neighbor[0]][neighbor[1]]) + node[neighbor[0]][neighbor[1]].h:
                node[neighbor[0]][neighbor[1]].g = current_node.g + distance(current_node, node[neighbor[0]][neighbor[1]])
                node[neighbor[0]][neighbor[1]].cost = node[neighbor[0]][neighbor[1]].g + node[neighbor[0]][
                    neighbor[1]].h
                node[neighbor[0]][neighbor[1]].parent = current_node
        current_node = not_seen_min_cost(node, seen)
        # if no path exists
        if current_node is None:
            break

        seen[current_node.x][current_node.y] = True  # won't visit this node again

    return path, path_length