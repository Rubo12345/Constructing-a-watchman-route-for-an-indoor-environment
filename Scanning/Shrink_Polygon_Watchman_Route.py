from typing import Final
import numpy as np
import matplotlib.pyplot as plt
import Shrink_Polygon_AGP

''' Please make sure that the polygon used here is the same as assigned to P in Shrink_Polygon_AGP.py, or else this code may give error
    The function shrink returns scan locations (guards) and P, which is used in the search.py'''
    
def shrink():

     SP = Shrink_Polygon_AGP

     P = [(66, -22), (52, 4), (65, 4), (66,-1), (78, -4), (81,3), (78, 17), (89,15), (101, 20), (101, 31), (87, 35),
         (87,45), (63,44), (75,36), (68,25), (58,45), (49,36), (54, 29), (44,29), (44,22), (60, 22),
         (60,15), (36,15), (36, -8)]
   
     P = [(97, 80), (54, 80), (54, 40), (38, 40), (38 ,51), (10, 51), (10, 30), (25, 30), (26, 12), (2, 17), (2, 0),
        (19, -3), (34, -3), (29, -14), (54, -14), (54, -2), (76, -2), (76, -14), (110, -14), (110, -3), (88, 10),
        (88, 22), (119, 22), (119, 45), (86, 45), (86, 67), (116, 67), (116, 87), (97, 89)]

     P.reverse()   #already clockwise
     P.append(P[0])
     points = SP.shrink(P)
     points.append(points[0])
     Pb = SP.create_point_pair(P)
     Yx = SP.non_intersecting_diag(points,P,Pb)
     Yn = SP.mini_chk_pts(Pb,points,P,Yx)
     Final_Diagonals = SP.clean_up_final(Yn)
     Guards = SP.Guards(Final_Diagonals)
     return Guards, P

print(shrink())
