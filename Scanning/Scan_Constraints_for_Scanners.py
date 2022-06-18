import matplotlib.pyplot as plt
import math
import pyclipper
from shapely.geometry import Point,Polygon #used to chk pt in or out of poly
import time
from math import sqrt
#Start = time.time() #starting the time
#print("The start time is:",Start)
X = [];Y = [];Pi = [];PS = [];Xn = []; S = [];Yx = [];Yn = []; Yy = []; Pout = []
MP = []; Ym = [];Yp = [];Poly = []; YN = [];m = []

Poly = [(24970,19250),(23600,19250),(20740,22110),(22790,24160),(19395,27554)\
    ,(17345,25504),(15560,27289),(15560,30215),(16490,30215),(16490,31500)\
    ,(20670,31500),(20670,33700),(23370,33700),(23370,31150),(25785,31150)\
    ,(25785,41415),(16740,41416),(16740,39400),(10060,39400),(10060,41415)\
    ,(4315,41415),(4315,39400),(1300,39400),(1300,31300),(3545,31300)\
    ,(3545,34300),(6245,34300),(6245,29085),(4785,29085),(4785,26570)\
    ,(2085,26570),(2085,28615),(0,28615),(0,21110),(11925,21110),(12445,21630)\
    ,(16865,17210),(14600,14946),(16407,13139),(14498,11230),(12691,13036)\
    ,(9085,9430),(11430,7085),(11430,4800),(19590,4800),(19590,9250),(26255,9250)\
    ,(26255,7085),(32000,7085),(32000,9720),(36510,9720),(36510,15050)\
    ,(34330,15050),(34330,12850),(31430,12850),(31430,19250),(34330,19250)\
    ,(34330,17050),(37480,17050),(37480,23430),(34330,23430),(34330,26060)\
    ,(28385,26060),(28385,24260),(24970,24260)]

Poly.reverse()
P = Poly
AP = P
P.append(P[0])


def det(a, b): #readymade function taken from the net
        return a[0] * b[1] - a[1] * b[0]


def point_of_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here
    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def shrink(Poly):
# how much the coordinates are moved as an absolute value
    shrink_x = 1000
    shrink_y = 1000
# coords must be clockwise
    lines = [[Poly[i-1], Poly[i]] for i in range(len(Poly))]
    new_lines = []
    for i in lines:
        dx = i[1][0] - i[0][0]
        dy = i[1][1] - i[0][1]
    # this is to take into account slopes
        if (dx*dx + dy*dy)==0:
            continue
        else:
            factor = 1 / (dx*dx + dy*dy)**0.5
            new_dx = dy*shrink_x * factor
            new_dy = dx*shrink_y * factor
            new_lines.append([(i[0][0]+ new_dx, i[0][1] - new_dy),
                            (i[1][0] + new_dx, i[1][1] - new_dy)])
# find position of intersection of all the lines
    new_polygon = []
    for i in range(len(new_lines)):
        new_polygon.append((point_of_intersection(new_lines[i-1], new_lines[i])))
    return new_polygon

Pc = shrink(Poly)
Start = time.time() #starting the time
Pc.append(Pc[0])
AAP = Pc


def find_length(A,B):
    D = sqrt(((A[0]-B[0])**2) + ((A[1]-B[1])**2))
    return D


def Sorting(lst):
    lst2 = sorted(lst, key=len, reverse = True)
    return lst2


def orientation(x1,y1,x2,y2,x3,y3):
        val = (float((y2-y1)*(x3-x2)))-(float((x2-x1)*(y3-y2)))
        if (val>0):
            return 1 #clockwise
        elif (val<0):
            return 2 #counterclockwise
        else:
            return 0 #collinear


def point_in_seg_area(x1,y1,x2,y2,x3,y3):
        if ((x2<=max(x1,x3)) and (x2>=min(x1,x3))\
                and (y2<=max(y1,y3)) and (y2>=min(y1,y3))):
            return True
        return False


def check_intersection(x1,y1,x2,y2,x3,y3,x4,y4):
        o1 = orientation(x1,y1,x2,y2,x3,y3)
        o2 = orientation(x1,y1,x2,y2,x4,y4)
        o3 = orientation(x3,y3,x4,y4,x1,y1)
        o4 = orientation(x3,y3,x4,y4,x2,y2)
        if ((o1 == 0) and point_in_seg_area(x1,y1,x3,y3,x2,y2)): #both are neede to tell if the point is on the segment
            return False
        if ((o2 == 0) and point_in_seg_area(x1,y1,x4,y4,x2,y2)):
            return False
        if ((o3 == 0) and point_in_seg_area(x3,y3,x1,y1,x4,y4)):
            return False
        if ((o4 == 0) and point_in_seg_area(x3,y3,x1,y1,x4,y4)):
            return False
        if ((o1!=o2) and (o3!=o4)):
            return True
        return  False


def create_point_pair(P):
    Pb = []
    for i in range(len(P)-1):
        Pa = []
        Pa.append(P[i])
        Pa.append(P[i+1])
        Pb.append(Pa)
    return Pb

Pb = create_point_pair(P)

Yx = []

def non_intersecting_diag(Pc,P, Pb):
    for i in range(len(Pc)-1):
        S = []
        for j in range(len(P)-1):
            Pi = []
            Pi.append(Pc[i])
            Pi.append(P[j])
            S.append(Pi)
        PS.append(S)
    for n in range(len(PS)):
        for k in range(len(PS[n])):
            Xn = []
            for l in range(len(P)-1):
                if  check_intersection(PS[n][k][0][0],PS[n][k][0][1],PS[n][k][1][0]\
                    ,PS[n][k][1][1],P[l][0],P[l][1],P[l+1][0],P[l+1][1])==True:
                      continue
                else:
                      Xn.append(PS[n][k][0])
                      Xn.append(PS[n][k][1])
            Y = []
            if len(Xn) == 2*(len(P)-1): #no intersection with any polygon side
               Y.append(Xn[0])
               Y.append(Xn[1])
            if Y == []:
                continue
            else:
                Yx.append(Y)
    for m in range(len(Yx)):
        px = float((Yx[m][0][0]+Yx[m][1][0])/2)
        py = float((Yx[m][0][1]+Yx[m][1][1])/2)
        mp = (px,py)
        if not (Point(mp).within(Polygon(AP))): #chk point in or out
               Pout.append(Yx[m])
        MP.append(mp)
    for n in range(len(Pout)):
            if Pout[n] in Yx:
                Yx.remove(Pout[n])
    return Yx

Yx = non_intersecting_diag(Pc,P,Pb)
Tx = Yx


def find_length(A,B):
    D = sqrt(((A[0]-B[0])**2) + ((A[1]-B[1])**2))
    return D

def scan_range(Tx,Yx,SR): #Do not forget to define the scan range as SR
    for i in (Tx):
        A = i[0]
        B = i[1]
        if find_length(A,B) > SR:
           Yx.remove(i)
        else:
           continue
    return Yx


Yx = scan_range(Tx,Yx,10000)

Tx = Yx

def find_angle(P1,P2,P3):
    angle = math.degrees(math.atan2(P3[1]-P2[1],P3[0]-P2[0])- \
                         math.atan2(P1[1]-P2[1],P1[0]-P2[0]))
    if angle<0:
        return angle+360
    else:
        return angle


def scan_angle(Tx,Yx,P,Pc,Pb,r):
    for i in range(len(Pb)):
        for j in Tx:
            if (j[1] == Pb[i][0]):
              Ang = find_angle(j[0],j[1],Pb[i][1])
              if ((Ang > 180 and Ang < 180+r) or Ang > 360-r): 
                     if j in Yx:
                        Yx.remove(j)
              elif (Ang < 180 and(Ang < r or Ang > 180-r)):
                     if j in Yx:
                        Yx.remove(j)
               
            elif (j[1] == Pb[i][1]):
                Ang = find_angle(j[0],j[1],Pb[i][0])
                if ((Ang > 180 and Ang < 180+r) or Ang > 360-r):
                     if j in Yx:
                        Yx.remove(j)
                elif (Ang < 180 and (Ang < r or Ang > 180-r)):
                     if j in Yx:
                        Yx.remove(j)  
    return Yx
Yx = scan_angle(Tx,Yx,P,Pc,Pb,8)


def mini_chk_pts(Yf1,F,Yn,Pb,Pc):
    Yf2 = []
    while F != []:
        Yy = []; Ys = []; M = []
        for a in range(len(Yf1)):
            Yy = []
            for b in range(len(Yf1[a])):
                for c in range(len(F)):
                    if (F[c][0] in Yf1[a][b][0]) and (F[c][1] in Yf1[a][b][1])\
                       and (Yf1[a][b][0][1] in F[c]) and Yf1[a][b][1][1] in F[c]:
                        Yy.append(Yf1[a][b])
            if not Yy == []:
                   Ys.append(Yy)
        Yf2 = Sorting(Ys)
        if not Yf2[0] == []:
               A2 = Yf2[0]
        for i in range(len(Yf2[0])):
            Yn.append(Yf2[0][i])
        Yf2.remove(Yf2[0])
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


def chk_pts(Pc,P,Yx):
    Yn=[];m=[];Ys1=[];Yk1=[];Yy1=[];Yf1 = [];Ye1 = []; R = []
    for r in range(len(Pc)-1):#this is important for arranging the diagonals.
        Yy1 = []
        for s in range(len(Yx)):
            if Pc[r] == Yx[s][0]:
               Yy1.append(Yx[s])
        if not Yy1 == []:
               Yy1.append(Yy1[0])
        Ys1.append(Yy1)
    Yk1 = Sorting(Ys1)  #sorting in descending order of  length of sub-list.
    #print("The list Yk1 is:",Yk1)
    for b in range(len(Yk1)):
            Yg = []
            for c in range(len(Yk1[b])-1):
                 for a in range(len(P)-1):
                     Yf = []
                     if ((P[a] == Yk1[b][c][1]) and (P[a+1] == Yk1[b][c+1][1])):
                         Yf.append(Yk1[b][c])
                         Yf.append(Yk1[b][c+1])
                         Yg.append(Yf)
            if not Yg == []:
                Ye1.append(Yg)
    Yf1 = Sorting(Ye1)

    A1 = Yf1[0]
    for d in range(len(Yf1[0])):
        Yn.append(Yf1[0][d])
    Yf1.remove(Yf1[0])
    
    for e in range(len(Pb)):
        for f in range(len(A1)):
            if ((Pb[e][0] == A1[f][0][1]) and (Pb[e][1] == A1[f][1][1])):
                m.append(Pb[e])
            else:
                continue
    F = []
    for g in range(len(Pb)):
         if not Pb[g] in m:
            F.append(Pb[g])

    Pfinal = mini_chk_pts(Yf1,F,Yn,Pb,Pc)
    final = []
    for i in Pfinal:
         if not i in final:
                 final.append(i)
    r = []
    for p in range(len(final)): #solution for adjecent points
        for q in range(len(final)): #this is a big change!!!!!!!!!
            for r in range(len(Pc)-1):
                if (final[p][0][0] or final[p][1][0]) == Pc[r]:
                   if (Pc[r+1] or Pc[r-1])==(final[q][0][1] or final[q][1][1]):
                          R.append(final[q])

    for r in range(len(R)):
        if R[r] in final:
            final.remove(R[r])
    return final

Yn = (chk_pts(Pc,P,Yx))
Final_Diagonals = Yn

def Guards(Final_Diagonals):
    Guards = []
    for i in range(len(Final_Diagonals)):
        if not Final_Diagonals[i][0][0] in Guards:
            Guards.append(Final_Diagonals[i][0][0])
    return Guards


def plt_plot(P,Yn):
    Px = [];Py = [];Dx = [];Dy = [];Sx = [];Sy = [];APx = [];APy = []
    for h in range(len(AAP)):
        APx.append(AAP[h][0])
        APy.append(AAP[h][1])
    for i in range(len(P)):
        Px.append(P[i][0])
        Py.append(P[i][1])
    for j in range(len(Yn)):
        Dx=[];Dy=[]
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
        plt.plot(Dx,Dy, color = 'g')
    plt.plot(Px,Py,color = 'b')
   # plt.plot(APx,APy,color = 'r')
    plt.scatter(Sx,Sy,s = 600,marker = '.',color = 'k')
    End = time.time()
    return plt.show()

print(Guards(Final_Diagonals))
plt_plot(P,Yn)
