from environment import *
from node import Node


def search(grid, start, goal, poly):
    '''

    Args:
        grid: grid
        start: starting point
        goal: goal point
        poly: polygon

    Returns: path length using dijkstra

    '''
    path = []
    node = []
    path_length = 0

    # print(f'this is {start}, {goal}')
    # created nodes
    for i, row in enumerate(grid):
        col = []
        for j, val in enumerate(row):
            col.append(Node(i, j, val, 0))
        node.append(col)
    # 2d array to keep track of visited/seen
    seen = [[False for _ in range(len(node))]
            for _ in range(len(grid))]

    # initialize starting node
    node[start[0]][start[1]].cost = 0
    current_node = not_seen_min_cost(node, seen)
    # print(current_node.x, current_node.y)
    seen[current_node.x][current_node.y] = True

    while current_node:
        # goal condition
        if current_node.x == goal[0] and current_node.y == goal[1]:
            path.append(goal)
            # print(current_node.x, current_node.y)
            while path[-1] != start:
                path_length += distance(current_node, current_node.parent)
                path.append((current_node.parent.x, current_node.parent.y))
                current_node = current_node.parent
            path.reverse()
            break

        neighbor_locations = travel(current_node, grid, seen)
        for neighbor in neighbor_locations:

            # relax condition
            if node[neighbor[0]][neighbor[1]].cost is None or node[neighbor[0]][
                neighbor[1]].cost > current_node.cost + distance(current_node, node[neighbor[0]][neighbor[1]]):
                node[neighbor[0]][neighbor[1]].cost = current_node.cost + distance(current_node, node[neighbor[0]][neighbor[1]])
                node[neighbor[0]][neighbor[1]].parent = current_node

        current_node = not_seen_min_cost(node, seen)  # get current node with min cost
        if current_node is None:  # if no path exists
            break
        seen[current_node.x][current_node.y] = True  # won't visit this element again

    return path, path_length