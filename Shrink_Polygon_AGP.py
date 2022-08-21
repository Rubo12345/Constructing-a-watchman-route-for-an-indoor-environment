import matplotlib.pyplot as plt
import math
import pyclipper
from shapely.geometry import Point, Polygon  # used to chk pt in or out of poly
import time

from sympy import Max

# Start = time.time() #starting the time
# print("The start time is:",Start)
X = [];Y = [];Pi = [];PS = [];Xn = [];S = [];Yx = [];Yn = [];Yy = [];Pout = [];MP = [];Ym = [];Yp = [];Poly = [];YN = [];m = []

''' To find the scan locations on the vertices of the polygon, for any polygon Poly, please assign the list of co-ordinates of any polygon to a variable "Poly" as 
    shown in the test examples below. Make sure that the list contains vertices of the polygon in anti-clockwise direction'''

''' Following are the 4 interesting test example polygons'''
Poly = [(10, 36), (10, 31), (16, 29), (15, 22), (9, 22), (9, 13), (14, 9), (14, 13), (22, 13), (22, 4), (31, 5),
        (25, 13), (25, 17), (35, 17), (35, 12), (30, 13), (34, 4), (42, 4), (42, -2), (48, -2), (48, 3), (54, 5),
        (54, 15), (50, 15), (50, 22), (58, 22), (58, 33), (55, 33), (55, 29), (49, 37), (42, 30), (36, 30), (36, 36),
        (41, 36), (40, 43), (31, 43), (31, 37), (16, 37), (16,31)]

Poly = [(66, -22), (52, 4), (65, 4), (66, -1), (78, -4), (81, 3), (78, 17), (89, 15), (101, 20), (101, 31), (87, 35),
     (87, 45), (63, 44), (75, 36), (68, 25), (58, 45), (49, 36), (54, 29), (44, 29), (44, 22), (60, 22), (60, 15),
     (36, 15), (36, -8)]

Poly = [(72 ,-13), (90 ,-27) ,(122 ,-36),(126 ,-20),(109 ,-21),(97 ,-2),(116 ,-2),(116 ,13),(134 ,13),(128 ,-7),
        (150 ,-7),(150 ,6),(167 ,6),(167 ,20),(153 ,20),(132 ,30),(132 ,40),(153 ,40),(153 ,51),(140 ,51),(140 ,69),
        (109, 69),(99 ,55),(110 ,55),(110 ,30),(98 ,25),(98 ,36),(84 ,36),(84 ,23),(75 ,23),(75 ,6)]

Poly = [(97, 80), (54, 80), (54, 40), (38, 40), (38 ,51), (10, 51), (10, 30), (25, 30), (26, 12), (2, 17), (2, 0),
        (19, -3), (34, -3), (29, -14), (54, -14), (54, -2), (76, -2), (76, -14), (110, -14), (110, -3), (88, 10),
        (88, 22), (119, 22), (119, 45), (86, 45), (86, 67), (116, 67), (116, 87), (97, 89)]

''' Only reverse the poly if the polygon is in anti-clockwise direction'''
Poly.reverse()  
P = Poly; AP = P; P.append(P[0])

''' The function det calculates the determinant'''
def det(a, b):  
    return a[0] * b[1] - a[1] * b[0]


''' The function point_of_intersection find the point of intersection between the two given lines'''
def point_of_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])  # Typo was here
    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


''' The function shrink scales down the polygon by shrink_x and shrink_y factor'''
def shrink(Poly):
    # how much the coordinates are moved as an absolute value
    shrink_x = 0.1
    shrink_y = 0.1
    # coords must be clockwise
    lines = [[Poly[i - 1], Poly[i]] for i in range(len(Poly))]
    new_lines = []
    for i in lines:
        dx = i[1][0] - i[0][0]
        dy = i[1][1] - i[0][1]
        # this is to take into account slopes
        if (dx * dx + dy * dy) == 0:
            continue
        else:
            factor = 1 / (dx * dx + dy * dy) ** 0.5
            new_dx = dy * shrink_x * factor
            new_dy = dx * shrink_y * factor
            new_lines.append([(i[0][0] + new_dx, i[0][1] - new_dy),
                              (i[1][0] + new_dx, i[1][1] - new_dy)])
    # find position of intersection of all the lines
    new_polygon = []
    for i in range(len(new_lines)):
        new_polygon.append((point_of_intersection(new_lines[i - 1], new_lines[i])))
    return new_polygon


Pc = shrink(Poly)
Start = time.time()  # starting the time
Pc.append(Pc[0])
AAP = Pc

''' The function Sorting sorts the list'''
def Sorting(lst):
    lst2 = sorted(lst, key=len, reverse=True)
    return lst2


''' orientation function: To check the orientation on points (x1,y1),(x2,y2),(x3,y3)'''
def orientation(x1, y1, x2, y2, x3, y3):
    val = (float((y2 - y1) * (x3 - x2))) - (float((x2 - x1) * (y3 - y2)))
    if (val > 0):
        return 1  # clockwise
    elif (val < 0):
        return 2  # counterclockwise
    else:
        return 0  # collinear


''' point_in_seg_area function: To check if the point lies in segment area'''
def point_in_seg_area(x1, y1, x2, y2, x3, y3):
    if ((x2 <= max(x1, x3)) and (x2 >= min(x1, x3)) \
            and (y2 <= max(y1, y3)) and (y2 >= min(y1, y3))):
        return True
    return False


''' check_intersection function: To check if the line formed by points (x1,y1) and (x2,y2) intersects line
      formed by (x3,y3) and (x4,y4)'''
def check_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    o1 = orientation(x1, y1, x2, y2, x3, y3)
    o2 = orientation(x1, y1, x2, y2, x4, y4)
    o3 = orientation(x3, y3, x4, y4, x1, y1)
    o4 = orientation(x3, y3, x4, y4, x2, y2)
    if ((o1 == 0) and point_in_seg_area(x1, y1, x3, y3, x2,
                                        y2)):  # both are neede to tell if the point is on the segment
        return False
    if ((o2 == 0) and point_in_seg_area(x1, y1, x4, y4, x2, y2)):
        return False
    if ((o3 == 0) and point_in_seg_area(x3, y3, x1, y1, x4, y4)):
        return False
    if ((o4 == 0) and point_in_seg_area(x3, y3, x1, y1, x4, y4)):
        return False
    if ((o1 != o2) and (o3 != o4)):
        return True
    return False


'''The function create_point_pair creates edges from points'''
def create_point_pair(P):
    Pb = []
    for i in range(len(P) - 1):
        Pa = []
        Pa.append(P[i])
        Pa.append(P[i + 1])
        Pb.append(Pa)
    return Pb
Pb = create_point_pair(P)


''' The function non_intersecting_diag creates non intersecting diagonals in the polygon. 
    Non intersecting diagonals do not intersect with the exterior of the polygon'''
def non_intersecting_diag(Pc, P, Pb):
    for i in range(len(Pc) - 1):
        S = []
        for j in range(len(P) - 1):
            Pi = []
            Pi.append(Pc[i])
            Pi.append(P[j])
            S.append(Pi)
        PS.append(S)
    # print("Bhai PS:",PS)
    for n in range(len(PS)):
        for k in range(len(PS[n])):
            Xn = []
            for l in range(len(P) - 1):
                if check_intersection(PS[n][k][0][0], PS[n][k][0][1], PS[n][k][1][0] \
                        , PS[n][k][1][1], P[l][0], P[l][1], P[l + 1][0], P[l + 1][1]) == True:
                    continue
                else:
                    Xn.append(PS[n][k][0])
                    Xn.append(PS[n][k][1])
            Y = []
            if len(Xn) == 2 * (len(P) - 1):  # no intersection with any polygon side
                Y.append(Xn[0])
                Y.append(Xn[1])
            if Y == []:
                continue
            else:
                Yx.append(Y)
    for m in range(len(Yx)):
        px = float((Yx[m][0][0] + Yx[m][1][0]) / 2)
        py = float((Yx[m][0][1] + Yx[m][1][1]) / 2)
        mp = (px, py)
        if not (Point(mp).within(Polygon(AP))):  # chk point in or out
            Pout.append(Yx[m])
        MP.append(mp)
    for n in range(len(Pout)):
        if Pout[n] in Yx:
            Yx.remove(Pout[n])
    return Yx
Yx = non_intersecting_diag(Pc, P, Pb)


''' The function mini_chk_pts implements the proposed algorithm and returns the list of the scan locations' diagonals'''
def mini_chk_pts(Pb, Pc, P, Yx):
    Yn = [];M = [];Ys1 = [];Yk1 = [];Yy1 = [];Yf1 = [];Ye1 = [];R = []
    for r in range(len(Pc) - 1):  # this is important for arranging the diagonals.
        Yy1 = []
        for s in range(len(Yx)):
            if Pc[r] == Yx[s][0]:
                Yy1.append(Yx[s])
        if not Yy1 == []:
            Yy1.append(Yy1[0])
        Ys1.append(Yy1)
    Yk1 = Sorting(Ys1)  # sorting in descending order of  length of sub-list.
    # print("The list Yk1 is:",Yk1)
    for b in range(len(Yk1)):
        Yg = []
        for c in range(len(Yk1[b]) - 1):
            for a in range(len(P) - 1):
                Yf = []
                if ((P[a] == Yk1[b][c][1]) and (P[a + 1] == Yk1[b][c + 1][1])):
                    Yf.append(Yk1[b][c])
                    Yf.append(Yk1[b][c + 1])
                    Yg.append(Yf)
        if not Yg == []:
            Ye1.append(Yg)
    Yf1 = Sorting(Ye1)
    F = Pb
    Yf2 = []

    while F != []:
        Yy = [];Ys = [];M = []

        for a in range(
                len(Yf1)):  # So this loop is find the guards which guard maximum of the unguarded edges (first case is similar to yf1)
            Yy = []
            for b in range(len(Yf1[a])):
                for c in range(len(F)):
                    if (F[c][0] in Yf1[a][b][0]) and (F[c][1] in Yf1[a][b][1]) \
                            and (Yf1[a][b][0][1] in F[c]) and Yf1[a][b][1][1] in F[c]:
                        Yy.append(Yf1[a][b])
            Ys.append(Yy)
        Yf2 = Sorting(Ys)

        '''...........................................................'''
        '''This part of code compares the distances of the guards with the previous guards, in the hope of binding them closer'''

        Yf2_len = []
        for i in Yf2:
            Yf2_len.append(len(i))
        # print(Yf2_len)

        high = []
        for i in Yf2:
            if len(i) == len(Yf2[0]):
                high.append(Yf2.index(i))

        Dist = []
        for i in high:
            if Yn == []:
                continue
            else:
                a = Yn[len(Yn) - 1][0][0]  # Because the first element has no one to compare with
                b = Yf2[i][0][0][0]  # current elements list
                dist = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
                Dist.append(dist)

        '''..........................................................'''
        # if Yn == []:
        #     A2 = Yf2[0]
        # else:
        #     A2 = Yf2[Dist.index(min(Dist))]

        A2 = Yf2[0]
        for i in range(len(A2)):
            Yn.append(A2[i])
        # print(Yn)
        Yf2.remove(A2)
        for j in range(len(F)):
            for k in range(len(A2)):
                if (F[j][0] == A2[k][0][1]) and (F[j][1] == A2[k][1][1]):
                    M.append(F[j])
                else:
                    continue
        F2 = []
        for l in range(len(F)):
            if not F[l] in M:
                F2.append(F[l])
            else:
                continue
        Yf1 = Yf2
        F = F2
    return Yn
Yn = mini_chk_pts(Pb, Pc, P, Yx)


''' The function Guards given the final list of the scan locations '''
def clean_up_final(Yn):
    final = [];R = [];r = []
    for i in Yn:  # avoiding repetition
        if not i in final:
            final.append(i)
    for p in range(len(final)):  # solution for adjecent points
        for q in range(len(final)):  # this is a big change!!!!!!!!!
            for r in range(len(Pc) - 1):
                if (final[p][0][0] or final[p][1][0]) == Pc[r]:
                    if (Pc[r + 1] or Pc[r - 1]) == (final[q][0][1] or final[q][1][1]):
                        R.append(final[q])
    for r in range(len(R)):
        if R[r] in final:
            final.remove(R[r])
    Yn = final
    return Yn
Final_Diagonals = clean_up_final(Yn)
Yn = Final_Diagonals


''' The function Guards given the final list of the scan locations '''
def Guards(Final_Diagonals):
    Guards = []
    for i in range(len(Final_Diagonals)):
        if not Final_Diagonals[i][0][0] in Guards:
            Guards.append(Final_Diagonals[i][0][0])
    return Guards


''' The function plt_plot plots the polygon and scan locations with diagonals'''
def plt_plot(P, Yn):
    Px = [];Py = [];Dx = [];Dy = [];Sx = [];Sy = [];APx = [];APy = []
    for h in range(len(AAP)):
        APx.append(AAP[h][0])
        APy.append(AAP[h][1])
    for i in range(len(P)):
        Px.append(P[i][0])
        Py.append(P[i][1])
    for j in range(len(Yn)):
        Dx = [];Dy = []
        Dx.append(Yn[j][0][0][0])
        Dy.append(Yn[j][0][0][1])
        Dx.append(Yn[j][0][1][0])
        Dy.append(Yn[j][0][1][1])
        Dx.append(Yn[j][1][0][0])
        Dy.append(Yn[j][1][0][1])
        Dx.append(Yn[j][1][1][0])
        Dy.append(Yn[j][1][1][1])
        Sx.append(Yn[j][0][0][0])
        Sy.append(Yn[j][0][0][1])
        plt.plot(Dx, Dy, color='g')
    plt.plot(Px, Py, color='b')
    # plt.plot(APx, APy, color='r')
    plt.scatter(Sx, Sy, s=700, marker='.', color='k')
    End = time.time()
    return plt.show()

# print(Guards(Final_Diagonals))
# plt_plot(P, Yn)



