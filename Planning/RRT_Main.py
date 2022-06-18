# Main and helper function

from re import A
from PIL import Image
import numpy as np
from RRT import RRT
import time

import matplotlib.pyplot as plt

def load_map(file_path, resolution_scale):
    ''' Load map from an image and return a 2D binary numpy array
        where 0 represents obstacles and 1 represents free space
    '''
    # Load the image with grayscale
    img = Image.open(file_path).convert('L')
    # Rescale the image
    size_x, size_y = img.size
    new_x, new_y  = int(size_x*resolution_scale), int(size_y*resolution_scale)
    img = img.resize((new_x, new_y), Image.ANTIALIAS)

    map_array = np.asarray(img, dtype='uint8')

    # Get bianry image
    threshold = 127
    map_array = 1 * (map_array > threshold)

    # Result 2D numpy array
    return map_array

if __name__ == "__main__":

    '''
    #Example one
    start = (70,275)
    goal = (300,445)
    map_array = load_map("D:\Educational\A WPI Assignments and Materials\Motion Planning\Project\Robot-Motion-Planning-for-an-optimal-Watchman-Route\Colored Polygons\GS10.jpeg",1.5)
    '''
    '''
    start = (50,100)
    goal = (150,430)
    map_array = load_map("D:\Educational\A WPI Assignments and Materials\Motion Planning\Project\Robot-Motion-Planning-for-an-optimal-Watchman-Route\Colored Polygons\GS5.jpeg",1)
    # [(12.004002564611195, 2.6748405823643653), (1.8319882514537322, 8.381256634659618), (4.475299130777356, 8.0519414026726), (3.447646309306825, 6.967555834038162)]

    points = [(120.04002564611195, 26.748405823643653), (1.8319882514537322, 8.381256634659618), (4.475299130777356, 8.0519414026726), (3.447646309306825, 6.967555834038162)]
    points = [(88,134),(133,173),(99,191),(261,377),(88,134)]  # 4 guards polygon - zigzag
    points = [(105,58),(180,476)] # mega one
    points = [(63,159),(121,220),(273,324),(63,159)]
    print(points)
    points = [(70,275),(300,445),(70,275)]'''

    points = [(147,130),(228,90),(265,322),(125,265),(147,130)] # Polygon with holes
    map_array = load_map("D:\Educational\A WPI Assignments and Materials\Motion Planning\Project\Results\Colored Polygons\PH_BW1.png",1)
    points = [(150,100),(300,400)]
    map_array = load_map("D:\Educational\A WPI Assignments and Materials\Motion Planning\Project\Results\Colored Polygons\GS10.jpeg",1)
    for i in range(len(points)-1):
        start = points[i]
        goal = points[i+1]
        RRT_planner = RRT(map_array, start, goal)
        # RRT_planner.RRT(n_pts=4000)
        RRT_planner.RRT_star(n_pts=4000)
        # RRT_planner.informed_RRT_star(n_pts=5000)
    
    plt.show()
    
