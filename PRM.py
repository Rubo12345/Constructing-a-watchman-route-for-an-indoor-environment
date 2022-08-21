# Standard Algorithm Implementation
# Sampling-based Algorithms PRM

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from scipy import spatial

# Class for PRM
class PRM:
    # Constructor
    def __init__(self, map_array):
        self.map_array = map_array            # map array, 1->free, 0->obstacle
        self.size_row = map_array.shape[0]    # map size
        self.size_col = map_array.shape[1]    # map size

        self.samples = []                     # list of sampled points
        self.graph = nx.Graph()               # constructed graph
        self.path = []                        # list of nodes of the found path

    def check_collision(self, p1, p2):
        '''Check if the path between two points collide with obstacles
        arguments:
            p1 - point 1, [row, col]
            p2 - point 2, [row, col]

        return:
            True if there are obstacles between two points
        '''
        ### YOUR CODE HERE ###
        parts = 20
        points = list(zip(np.linspace(p1[0], p2[0], parts+1),
               np.linspace(p1[1], p2[1], parts+1)))
        cc = []
        for i in range(len(points)):
            if self.map_array[int(points[i][0])][int(points[i][1])] == 0:
                cc.append(0)
            else:
                cc.append(1)
        if 0 in cc:
            return True
        else:
            return False
        
    def dis(self, point1, point2):
        '''Calculate the euclidean distance between two points
        arguments:
            p1 - point 1, [row, col]
            p2 - point 2, [row, col]

        return:
            euclidean distance between two points
        '''
        ### YOUR CODE HERE ###
        d = np.math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
        return d

    def uniform_sample(self, n_pts):
        '''Use uniform sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()
        
        ### YOUR CODE HERE ###
        for i in range(self.size_row):
            for j in range(self.size_col):
                if (i % 10 == 0) and (j % 10 == 0):
                    if self.map_array[i][j] == 1:
                        self.samples.append((i,j))
                    else:
                        continue
                else:
                    continue
        self.samples.append((0, 0))

    def random_sample(self, n_pts):
        '''Use random sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()

        ### YOUR CODE HERE ###
        r_sample = list(zip((np.random.randint(self.size_row, size=n_pts)),
                    (np.random.randint(self.size_col, size=n_pts))))
        
        for i in range(len(r_sample)):
            if  self.map_array[r_sample[i][0]][r_sample[i][1]] == 1:
                self.samples.append((r_sample[i][0],r_sample[i][1]))
        self.samples.append((0, 0))

    def gaussian_sample(self, n_pts):
        '''Use gaussian sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()

        ### YOUR CODE HERE ###  
        for i in range(n_pts):
            q1_sample = list(zip((np.random.randint(0,self.size_row, 1)),
                     (np.random.randint(0,self.size_col, 1))))
            q1_sample = q1_sample[0]
            cov = [[200 , 0],[0, 200]]
            q2 = np.random.multivariate_normal(q1_sample, cov)
            q2_sample = [int(q2[0]), int(q2[1])]
            if ((q2_sample[0] >= self.size_row or q2_sample[0] < 0) or (q2_sample[1] >= self.size_col or q2_sample[0] < 0)):
                continue
            elif ((self.map_array[q2_sample[0]][q2_sample[1]]) == (self.map_array[q1_sample[0]][q1_sample[1]])):
                continue
            elif (self.map_array[q2_sample[0]][q2_sample[1]] == 1):
                if q2_sample not in self.samples:
                    self.samples.append(q2_sample)
            elif (self.map_array[q1_sample[0]][q1_sample[1]] == 1):
                if q1_sample not in self.samples:
                    self.samples.append(q1_sample) 
               
        self.samples.append((0, 0))

    def bridge_sample(self, n_pts):
        '''Use bridge sampling and store valid points
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points

        check collision and append valide points to self.samples
        as [(row1, col1), (row2, col2), (row3, col3) ...]
        '''
        # Initialize graph
        self.graph.clear()

        ### YOUR CODE HERE ###
        for i in range(n_pts):
            q1_sample = list(zip((np.random.randint(0,self.size_row, 1)),
                     (np.random.randint(0,self.size_col, 1))))
            q1_sample = q1_sample[0]
            if  (self.map_array[q1_sample[0]][q1_sample[1]] == 0):
                cov = [[300 , 0],[0, 300]]
                q2 = np.random.multivariate_normal(q1_sample, cov)
                q2_sample = [int(q2[0]), int(q2[1])]
                if ((q2_sample[0] >= self.size_row or q2_sample[0] < 0) or (q2_sample[1] >= self.size_col or q2_sample[0] < 0)):
                    continue
                elif (self.map_array[q2_sample[0]][q2_sample[1]] == 0):
                    MP = ((q2_sample[0] + q1_sample[0])/2,(q2_sample[1] + q1_sample[1])/2)
                    if (self.map_array[int(MP[0])][int(MP[1])] == 1):
                        self.samples.append(MP) 
        self.samples.append((0, 0))

    def draw_map(self):
        '''Visualization of the result
        '''
        # Create empty map
        fig, ax = plt.subplots()
        img = 255 * np.dstack((self.map_array, self.map_array, self.map_array))
        ax.imshow(img)

        # Draw graph
        # get node position (swap coordinates)
        node_pos = np.array(self.samples)[:, [1, 0]]
        pos = dict( zip( range( len(self.samples) ), node_pos) )
        pos['start'] = (self.samples[-2][1], self.samples[-2][0])
        pos['goal'] = (self.samples[-1][1], self.samples[-1][0])
        
        plt.figure(1)
        # draw constructed graph
        nx.draw(self.graph, pos, node_size=3, node_color='y', edge_color='y' ,ax=ax)

        # If found a path
        if self.path:
            # add temporary start and goal edge to the path
            final_path_edge = list(zip(self.path[:-1], self.path[1:]))
            nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=self.path, node_size=8, node_color='r')
            nx.draw_networkx_edges(self.graph, pos=pos, edgelist=final_path_edge, width=2, edge_color='r')

        # draw start and goal
        nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=['start'], node_size=50,  node_color='r')
        nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=['goal'], node_size=50,  node_color='r')

        # show image
        plt.axis('on')
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        # plt.show()

    def sample(self, n_pts=1000, sampling_method="uniform"):
        '''Construct a graph for PRM
        arguments:
            n_pts - number of points try to sample, 
                    not the number of final sampled points
            sampling_method - name of the chosen sampling method

        Sample points, connect, and add nodes and edges to self.graph
        '''
        # Initialize before sampling
        self.samples = []
        self.graph.clear()
        self.path = []

        # Sample methods
        if sampling_method == "uniform":
            self.uniform_sample(n_pts)
        elif sampling_method == "random":
            self.random_sample(n_pts)
        elif sampling_method == "gaussian":
            self.gaussian_sample(n_pts)
        elif sampling_method == "bridge":
            self.bridge_sample(n_pts)

        ### YOUR CODE HERE ###

        # Find the pairs of points that need to be connected
        # and compute their distance/weight.
        # Store them as
        # pairs = [(p_id0, p_id1, weight_01), (p_id0, p_id2, weight_02), 
        #          (p_id1, p_id2, weight_12) ...]
        
        pairs = []
        r = 20
        kdtree = spatial.KDTree(self.samples)
        qp = list(kdtree.query_pairs(r))
        for i in range(len(qp)):
            d = PRM.dis(self, self.samples[qp[i][0]], self.samples[qp[i][1]])
            if PRM.check_collision(self, self.samples[qp[i][0]], self.samples[qp[i][1]]) == False:
                pairs.append((qp[i][0],qp[i][1],d))

        # Use sampled points and pairs of points to build a graph.
        # To add nodes to the graph, use
        # self.graph.add_nodes_from([p_id0, p_id1, p_id2 ...])
        # To add weighted edges to the graph, use
        # self.graph.add_weighted_edges_from([(p_id0, p_id1, weight_01), 
        #                                     (p_id0, p_id2, weight_02), 
        #                                     (p_id1, p_id2, weight_12) ...])
        # 'p_id' here is an integer, representing the order of 
        # current point in self.samples
        # For example, for self.samples = [(1, 2), (3, 4), (5, 6)],
        # p_id for (1, 2) is 0 and p_id for (3, 4) is 1.
        n = []
        for i in range(len(self.samples)):
            n.append(i)
        self.graph.add_nodes_from(n)
        self.graph.add_weighted_edges_from(pairs)

        # Print constructed graph information
        n_nodes = self.graph.number_of_nodes()
        n_edges = self.graph.number_of_edges()
        print("The constructed graph has %d nodes and %d edges" %(n_nodes, n_edges))

    def search(self, start, goal):
        '''Search for a path in graph given start and goal location
        arguments:
            start - start point coordinate [row, col]
            goal - goal point coordinate [row, col]

        Temporary add start and goal node, edges of them and their nearest neighbors
        to graph for self.graph to search for a path.
        '''
        # Clear previous path
        self.path = []

        # Temporarily add start and goal to the graph
        self.samples.append(start)
        self.samples.append(goal)
        # start and goal id will be 'start' and 'goal' instead of some integer
        self.graph.add_nodes_from(['start', 'goal'])

        ### YOUR CODE HERE ###

        # Find the pairs of points that need to be connected
        # and compute their distance/weight.
        # You could store them as
        # start_pairs = [(start_id, p_id0, weight_s0), (start_id, p_id1, weight_s1), 
        #                (start_id, p_id2, weight_s2) ...]
        start_pairs = []
        goal_pairs = []

        start_id = self.samples.index(start)
        goal_id = self.samples.index(goal)

        r = 120
        kdtree = spatial.KDTree(self.samples)
        qps = list(kdtree.query_pairs(r))
        for i in range(len(qps)):
            if PRM.check_collision(self, self.samples[qps[i][0]], self.samples[qps[i][1]]) == False:
                if  qps[i][0] == start_id:
                    d = PRM.dis(self, start, self.samples[qps[i][1]])
                    start_pairs.append(('start',qps[i][1],d))
                elif  qps[i][1] == start_id:
                    d = PRM.dis(self, start, self.samples[qps[i][0]])
                    start_pairs.append((qps[i][0],'start',d))

        for i in range(len(qps)):
            if PRM.check_collision(self, self.samples[qps[i][0]], self.samples[qps[i][1]]) == False:
                if  qps[i][0] == goal_id:
                    d = PRM.dis(self, start, self.samples[qps[i][1]])
                    goal_pairs.append(('goal',qps[i][1],d))
                elif  qps[i][1] == goal_id:
                    d = PRM.dis(self, start, self.samples[qps[i][0]])
                    goal_pairs.append((qps[i][0],'goal',d))

        # Add the edge to graph
        self.graph.add_weighted_edges_from(start_pairs)
        self.graph.add_weighted_edges_from(goal_pairs)
        
        # Seach using Dijkstra
        try:
            self.path = nx.algorithms.shortest_paths.weighted.dijkstra_path(self.graph, 'start', 'goal')
            path_length = nx.algorithms.shortest_paths.weighted.dijkstra_path_length(self.graph, 'start', 'goal')
            print("The path length is %.2f" %path_length)
        except nx.exception.NetworkXNoPath:
            print("No path found")
        
        # Draw result
        self.draw_map()

        # Remove start and goal node and their edges
        self.samples.pop(-1)
        self.samples.pop(-1)
        self.graph.remove_nodes_from(['start', 'goal'])
        self.graph.remove_edges_from(start_pairs)
        self.graph.remove_edges_from(goal_pairs)
       