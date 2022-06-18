# Main and helper function

from PIL import Image
import numpy as np
from RRT import RRT
from PRM import PRM
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
    # Search with PRM
    points = [(147,130),(228,90),(265,322),(125,265),(147,130)] # Polygon with holes
    points = [(150,100),(300,400)]
    print(points)
    for i in range(len(points)-1):
        start = points[i]
        goal = points[i+1]
        # map_array = load_map("D:\Educational\A WPI Assignments and Materials\Motion Planning\Project\Results\Colored Polygons\PH_BW1.png",1)
        map_array = load_map("D:\Educational\A WPI Assignments and Materials\Motion Planning\Project\Results\Colored Polygons\GS10.jpeg",1)
        PRM_planner = PRM(map_array)
        # PRM_planner.sample(n_pts=1000, sampling_method="uniform")
        # PRM_planner.search(start, goal)
        # PRM_planner.sample(n_pts=1000, sampling_method="random")
        # PRM_planner.search(start, goal)
        # PRM_planner.sample(n_pts=10000, sampling_method="gaussian")
        # PRM_planner.search(start, goal)
        # PRM_planner.sample(n_pts=20000, sampling_method="bridge")
        # PRM_planner.search(start, goal)
    plt.show()
