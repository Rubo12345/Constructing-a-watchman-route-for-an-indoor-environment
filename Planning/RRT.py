# Standard Algorithm Implementation
# Sampling-based Algorithms RRT and RRT*

from ast import Break
import matplotlib.pyplot as plt
import numpy as np
from scipy import spatial
import math

# Class for each tree node
class Node:
    def __init__(self, row, col):
        self.row = row        # coordinate
        self.col = col        # coordinate
        self.parent = None    # parent node / edge
        self.cost = 0.0       # cost to parent / edge weight

# Class for RRT
class RRT:
    # Constructor
    def __init__(self, map_array, start, goal):
        self.map_array = map_array            # map array, 1->free, 0->obstacle
        self.size_row = map_array.shape[0]    # map size
        self.size_col = map_array.shape[1]    # map size

        self.start = Node(start[0], start[1]) # start node
        self.goal = Node(goal[0], goal[1])    # goal node
        self.vertices = []                    # list of nodes
        self.found = False                    # found flag     

    def init_map(self):
        '''Intialize the map before each search
        '''
        self.found = False
        self.vertices = []
        self.vertices.append(self.start)
   
    def dis(self, node1, node2):
        '''Calculate the euclidean distance between two nodes
        arguments:
            node1 - node 1
            node2 - node 2

        return:
            euclidean distance between two nodes
        '''
        return np.sqrt((node1.row-node2.row)**2 + (node1.col-node2.col)**2)
  
    def check_collision(self, node1, node2):
        '''Check if the path between two nodes collide with obstacles
        arguments:
            node1 - node 1
            node2 - node 2

        return:
            True if there are obstacles
            False if the new node is valid to be connected
        '''
        # Check obstacle between nodes
        # get all the points in between
        points_between = zip(np.linspace(node1.row, node2.row, dtype=int), 
                             np.linspace(node1.col, node2.col, dtype=int))
        # check if any of these are obstacles
        for point in points_between:
            if self.map_array[point[0]][point[1]] == 0:
                return True
        return False

    def get_new_point(self, goal_bias):
        '''Choose the goal or generate a random point
        arguments:
            goal_bias - the possibility of choosing the goal instead of a random point

        return:
            point - the new point
        '''
        # select goal
        if np.random.random() < goal_bias:
            point = [self.goal.row, self.goal.col]
        # or generate a random point
        else:
            point = [np.random.randint(0, self.size_row-1), np.random.randint(0, self.size_col-1)]
        return point
  
    def get_new_point_in_ellipsoid(self, goal_bias, c_best):
        '''Choose the goal or generate a random point in an ellipsoid
           defined by start, goal and current best length of path
        arguments:
            goal_bias - the possibility of choosing the goal instead of a random point
            c_best - the length of the current best path

        return:
            point - the new point
        '''
        # Select goal
        if np.random.random() < goal_bias:
            point = [self.goal.row, self.goal.col]
        
        #### TODO ####
        # Generate a random point in an ellipsoid
        else:
            pass
            # Compute the distance between start and goal - c_min
            c_min = RRT.dis(self, self.start, self.goal)
            # Calculate center of the ellipsoid - x_center
            x_center = (((self.start.row + self.goal.row)/2) , ((self.start.col + self.goal.col)/2))
            # Compute rotation matrix from ellipse to world frame - C       
            # M1 = 0
            # M2 = (self.goal.col - self.start.col)/(self.goal.row - self.start.row)
            ret = math.atan2(self.goal.col - self.start.col, self.goal.row - self.start.row)
            theta = round(ret, 4)
            C = [[math.cos(theta), -math.sin(theta)],[math.sin(theta), math.cos(theta)]]

            # Compute diagonal matrix - L
            r = [c_best / 2.0,
                 np.sqrt(c_best ** 2 - c_min ** 2) / 2.0]
            L =  np.diag(r)

            # Cast a sample from a unit ball - x_ball

            while True:
                x , y = np.random.uniform(-1, 1), np.random.uniform(-1, 1)
                if x ** 2 + y ** 2 < 1:
                   x_ball =  np.array([[x], [y]])
                   break 

            # Map ball sample to the ellipsoid - x_rand
            x_rand = np.dot(np.dot(C, L), x_ball) 
            point = ((x_rand[(0, 0)]) + x_center[0], (x_rand[(1, 0)]) + x_center[1])
        #### TODO END ####

        return point

    def get_nearest_node(self, point):
        '''Find the nearest node from the new point in self.vertices
        arguments:
            point - the new point

        return:
            the nearest node
        '''
        # Use kdtree to find the neighbors within neighbor size
        samples = [[v.row, v.col] for v in self.vertices]
        kdtree = spatial.cKDTree(samples)
        coord, ind = kdtree.query(point)
        return self.vertices[ind]
   
    def sample(self, goal_bias=0.05, c_best=0):
        '''Sample a random point in the area
        arguments:
            goal_bias - the possibility of choosing the goal instead of a random point
            c_best - the length of the current best path (For informed RRT)

        return:
            a new node if this node is valid and added, None if not.

        Generate a new point
        '''
        # Generate a new point

        #### TODO ####

        # new_point = self.get_new_point(goal_bias) #del this

        # Regular sampling if c_best <= 0
        # using self.get_new_point

        if c_best <= 0:
            new_point = self.get_new_point(goal_bias)
        else:
            new_point = self.get_new_point_in_ellipsoid(goal_bias, c_best)

        # Sampling in an ellipsoid if c_best is a positive value
        # using self.get_new_point_in_ellipsoid
        
        #### TODO END ####

        return new_point

    def extend(self, new_point, extend_dis=10):
        '''Extend a new node to the current tree structure
        arguments:
            new_point - the new sampled point in the map
            extend_dis - extension distance for each step

        return:
            a new node if this node is valid and added, None if not.

        Extend towards the new point and check feasibility.
        Create and add a new node if feasible.
        '''
        # Get nearest node
        nearest_node = self.get_nearest_node(new_point)

        # Calculate new node location
        slope = np.arctan2(new_point[1]-nearest_node.col, new_point[0]-nearest_node.row)
        new_row = nearest_node.row + extend_dis*np.cos(slope)
        new_col = nearest_node.col + extend_dis*np.sin(slope)
        new_node = Node(int(new_row), int(new_col))

        # Check boundary and collision
        if (0 <= new_row < self.size_row) and (0 <= new_col < self.size_col) and \
           not self.check_collision(nearest_node, new_node):
            # If pass, add the new node
            new_node.parent = nearest_node
            new_node.cost = extend_dis
            self.vertices.append(new_node)

            # Check if goal is close
            if not self.found:
                d = self.dis(new_node, self.goal)
                if d < extend_dis:
                    self.goal.cost = d
                    self.goal.parent = new_node
                    self.vertices.append(self.goal)
                    self.found = True

            return new_node
        else:
            return None

    def get_neighbors(self, new_node, neighbor_size):
        '''Get the neighbors that is within the neighbor distance from the node
        arguments:
            new_node - a new node
            neighbor_size - the neighbor distance

        return:
            neighbors - a list of neighbors that are within the neighbor distance 
        '''
        # Use kdtree to find the neighbors within neighbor size
        samples = [[v.row, v.col] for v in self.vertices]
        kdtree = spatial.cKDTree(samples)
        ind = kdtree.query_ball_point([new_node.row, new_node.col], neighbor_size)
        neighbors = [self.vertices[i] for i in ind]
        # Remove the new_node itself
        neighbors.remove(new_node)
        return neighbors

    def path_cost(self, start_node, end_node):
        '''Compute path cost starting from start node to end node
        arguments:
            start_node - path start node
            end_node - path end node

        return:
            cost - path cost
        '''
        cost = 0
        curr_node = end_node
        while start_node.row != curr_node.row or start_node.col != curr_node.col:
            # Keep tracing back until finding the start_node 
            # or no path exists
            parent = curr_node.parent
            if parent is None:
                print("Invalid Path")
                return 0
            cost += curr_node.cost
            curr_node = parent
        
        return cost

    def rewire(self, new_node, neighbors):
        '''Rewire the new node and all its neighbors
        arguments:
            new_node - the new node
            neighbors - a list of neighbors that are within the neighbor distance from the node

        Rewire the new node if connecting to a new neighbor node will give least cost.
        Rewire all the other neighbor nodes.
        '''
        # If no neighbors, skip
        if neighbors == []:
            return

        # Compute the distance from the new node to the neighbor nodes
        distances = [self.dis(new_node, node) for node in neighbors]

        # Rewire the new node
        # compute the least potential cost
        costs = [d + self.path_cost(self.start, neighbors[i]) for i, d in enumerate(distances)]
        indices = np.argsort(np.array(costs))
        # check collision and connect the best node to the new node
        for i in indices:
            if not self.check_collision(new_node, neighbors[i]):
                new_node.parent = neighbors[i]
                new_node.cost = distances[i]
                break

        # Rewire new_node's neighbors
        for i, node in enumerate(neighbors):
            # new cost
            new_cost = self.path_cost(self.start, new_node) + distances[i]
            # if new cost is lower
            # and there is no obstacles in between
            if self.path_cost(self.start, node) > new_cost and \
               not self.check_collision(node, new_node):
                node.parent = new_node
                node.cost = distances[i]
  
    def draw_map(self):
        '''Visualization of the result
        '''
        # Create empty map
        fig, ax = plt.subplots(1)
        img = 255 * np.dstack((self.map_array, self.map_array, self.map_array))
        ax.imshow(img)

        # Draw Trees or Sample points
        plt.figure(1)
        for node in self.vertices[1:-1]:
            plt.plot(node.col, node.row, markersize=1.5, marker='o', color='y')
            plt.plot([node.col, node.parent.col], [node.row, node.parent.row], color='y', linewidth=1.5)
        
        # Draw Final Path if found
        if self.found:
            cur = self.goal
            while cur.col != self.start.col or cur.row != self.start.row:
                plt.plot([cur.col, cur.parent.col], [cur.row, cur.parent.row], color='r',linewidth=2)
                cur = cur.parent
                plt.plot(cur.col, cur.row, markersize=3, marker='o', color='r')

        # Draw start and goal
        plt.plot(self.start.col, self.start.row, markersize=10, marker='o', color='r')
        plt.plot(self.goal.col, self.goal.row, markersize=10, marker='o', color='r')
        # show image
        # plt.show()
        
    def RRT(self, n_pts=1000):
        '''RRT main search function
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        In each step, extend a new node if possible, and check if reached the goal
        '''
        # Remove previous result
        self.init_map()
        # Start searching       
        for i in range(n_pts):
            # Extend a new node until all the points are sampled
            # or find the path
            new_point = self.sample(0.05, 0)
            new_node = self.extend(new_point, 10)
            if self.found:
                break

        # Output
        if self.found:
            steps = len(self.vertices) - 2
            length = self.path_cost(self.start, self.goal)
            print("It took %d nodes to find the current paths" %steps)
            print("The path length is %.2f" %length)
        if not self.found:
            print("No path found")
        
        # Draw result
        self.draw_map()

    def RRT_star(self, n_pts=1000, neighbor_size=20):
        '''RRT* search function
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points
            neighbor_size - the neighbor distance
        
        In each step, extend a new node if possible, and rewire the node and its neighbors
        '''
        # Remove previous result
        self.init_map()
        # Start searching       
        for i in range(n_pts):
            # Extend a new node
            new_point = self.sample(0.05, 0)
            new_node = self.extend(new_point, 10)
            # Rewire
            if new_node is not None:
                neighbors = self.get_neighbors(new_node, neighbor_size)
                self.rewire(new_node, neighbors)

        # Output
        if self.found:
            steps = len(self.vertices) - 2
            length = self.path_cost(self.start, self.goal)
            print("It took %d nodes to find the current path" %steps)
            print("The path length is %.2f" %length)
        else:
            print("No path found")

        # Draw result
        self.draw_map()

    def informed_RRT_star(self, n_pts=1000, neighbor_size=20):
        '''Informed RRT* search function
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points
            neighbor_size - the neighbor distance
        
        In each step, extend a new node if possible, and rewire the node and its neighbors
        Once a path is found, an ellipsoid will be defined to constrained the sampling area
        '''
        # Remove previous result
        self.init_map()
        # Start searching       
        for i in range(n_pts):

            #### TODO ####
            c_best = 0
            # Once a path is found, update the best length of path - c_best
            # using the function self.path_cost(self.start, self.goal)
            if self.found:
                c_best = self.path_cost(self.start, self.goal)
            #### TODO END ####

            # Extend a new node
            new_point = self.sample(0.05, c_best)
            new_node = self.extend(new_point, 10)
            # Rewire
            if new_node is not None:
                neighbors = self.get_neighbors(new_node, neighbor_size)
                self.rewire(new_node, neighbors)

        # Output
        if self.found:
            steps = len(self.vertices) - 2
            length = self.path_cost(self.start, self.goal)
            print("It took %d nodes to find the current path" %steps)
            print("The path length is %.2f" %length)
        else:
            print("No path found")

        # Draw result
        self.draw_map()
