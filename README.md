# RBE550Project

## Motion Planning Group Project
### Shreyas Kanjalkar, [Rutwik Bonde](https://github.com/Rubo12345)
Before you run the code, to make sure you have all the requirements met do:

```pip install -r requirements.txt```

## Problem Statement: 
Try to find the Watchman Route, when the area of map is given, by using the optimal positions of static guards.

## Approach

For a given "realistic" polygon with or without holes, first find the ideal static guard locations by using the 
geometry of the polygon. In this case, we check the visibility of the edges of the polygon for each vertex and 
choose the vertex which has the highest visibility, and keep on recursively repeating this process
till all the edges of the polygon are guarded. Here our guards are considered *Omnipotent* meaning they have 
360 degree vision and no limit on how far they can look. There are also certain constraints where if the guard 
can see < 10 degrees of the edge, then it is not considered to be guarded by that particular guard. Given the positions
of these guards, if the watchman were to visit all these guard locations at least once then it would mean that the
watchman has guarded all the edges of the polygon and thus successfully completed a watchman route. 

### Art Gallery Problem - Scan Locations:
Art Gallery Problem is a problem to determine the minimum number of scan locations that are required or are sufficient to cover or see every point in the interior of an indoor environment. An indoor environment can be viewed as a polygon with or without holes with a total of n vertices; and scanners as points in the polygon, or on the vertex of the polygon. or on the edge of the polygon. Any point P in the polygon is said to be visible from a scanner G if the line segment joining P and G does not intersect the exterior of the polygon. 

#### Proposed Algorithm to solve the Art Gallery Problem:
  1) Create a polygon
  2) Find a vertex(Vi) in the polygon which scans maximum no. of edges of the polygon
  3) Now search for edges that remain unscanned by the previous vertex (Vi)
  4) Find another vertex (Vj) on the polygon which scans maximum of the remaining unscanned edges.
  5) Continue step 3 and 4 until all th edges are scans
  
  The figure below gives an idea of how the algorithm works:
  
  ![Proposed Algorithm Flow](https://user-images.githubusercontent.com/79450753/166077173-88e61091-e632-4abb-84a0-ed738710028f.png)

Run the following python code to get the solution for Art Gallery Problem:
- The Shrink_Polygon_AGP.py gives the output as a list of co-ordinates of the scan locations (on the vertices of the polygon)

  `Shrink_Polygon_AGP.py`
- The Final_Voronoi_New_and_Short.py gives the output as a list of co-ordinates of the scan locations (on the vertices of the voronoi diagram of the polygon)

  `Final_Voronoi_New_and_Short.py`
  
  (The detailed instructions for the above codes are given in code itself)
 
AGP for polygon with holes

`Shrink_Polygon_AGP_With_Holes.py`

![Polygon_with_Holes](https://user-images.githubusercontent.com/79450753/166182110-bc99b7c7-0f69-4a1e-964e-d50f7978eab5.png)

More details on AGP: [Art Gallery Problem](https://github.com/Rubo12345/Computational-Geometry-Research-on-the-Art-Gallery-Problem-AGP)

### Travelling Salesman Problem - Watchman Route:
Watchman Route is considered a Travelling Salesman Problem, which is defined as Given a list of cities and the distances
between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the 
origin city?". In our case the cities are replaced with guard locations. In normal TSP, you get the path distance between two
cities directly by connecting them in a straight line. However, for our case, the points are constrained in the polygon
and subsequently subjected to discretization. In order to connect the points, we used Dijkstra and A* search algorithm 
by setting heuristic as eucledian distance between the points. Here we have to consider if a point is inside the polygon 
or not before exploring those points.

After we get the adjacency matrix of path lengths for each guard, we use them as input for the three algorithms we have 
tried to implement: 
1. Brute Force
2. Held-Karp Algorithm
3. Genetic Algorithm

To run the code, please type in 

`python search.py --holes`

to run the code without holes and

`python serach.py --no-holes`

This will print the path length for each Algorithm and the time it took for that algorithm, and the order of traversal.

  The figure below gives an idea of how the TSP works:
  ![TSP_Path](https://user-images.githubusercontent.com/79450753/166120028-24daafd8-d80e-4687-9a23-b80037624b10.png)

  TSP for polygon with holes:
  ![HOLES_TSP_PATH](https://github.com/zen1405/Watchman-Route-Optimal/blob/main/Polygon%20with%20holes%20example.PNG)

Even though we say the route is "Optimal", it is optimal only in the contrained discretized grid. If we keep on discretizing
the grid even finer, we will get a better result but we can never escape the curse of discretization. Perhaps, one better
approach could be to try to directly connect the scan locations in a straight line and when we encounter an obstacle, in 
this case would  be the polygon boundary or holes within the polygon, we can switch to A* or Dijkstra algorithm to find the
path. Some mix of Global and Local planner perhaps.

Sampling Based Methods implementation:

RRT and its Variants:

![RRTs](https://user-images.githubusercontent.com/79450753/172021332-8275d81d-7d4e-4e96-a733-7378a9bd791f.png)

Probabilistic Roadmap using different sampling methods:

![Sampling](https://user-images.githubusercontent.com/79450753/172021347-261ea77d-e35a-4bda-8bd7-9dd89aeff7bc.png)

Sampling based methods for polygon with holes:

![Sampling_PWH](https://user-images.githubusercontent.com/79450753/172021360-bf91856d-b36b-4995-af62-a8b4f1c48b44.png)
