import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
import scipy.interpolate as interpolate
from scipy.spatial import Delaunay
from scipy.interpolate import interp1d
import csv

from nonrecgrid import X,Y,rho,xipoints,yipoints,U,V

# framedgrid=np.pad(rho,pad_width=2,mode='constant', constant_values=0)
# U=np.pad(U,pad_width=2,mode='constant',constant_values=0)
# V=np.pad(V,pad_width=2,mode='constant',constant_values=0)

# xi=np.linspace(xipoints[0],xipoints[-1],len(framedgrid[0]))
# yi=np.linspace(yipoints[0],yipoints[-1],len(framedgrid))
#
# X,Y=np.meshgrid(xi,yi)

# XC=dataframe[:,0]
# YC=dataframe[:,1]
# theta=dataframe[:,2]
# idx=dataframe[:,3]
# thres_rho=dataframe[:,4]
# u=np.cos(-theta)
# v=np.sin(-theta)
# indexnew=0
# indexlst=[500]
#
# xsize=30
# ysize=20
# XC-=min(XC)
# YC-=min(YC)
"""========== Functions =========="""
def circumcenter(ax,ay,bx,by,cx,cy):
    t=ax**2+ay**2-bx**2-by**2
    u=ax**2+ay**2-cx**2-cy**2
    J=(ax-bx)*(ay-cy)-(ax-cx)*(ay-by)

    x=(-1*(ay-by)*u+(ay-cy)*t)/(2*J)
    y=((ax-bx)*u-(ax-cx)*t)/(2*J)
    return [x, y]
"""========== Quiverplot =========="""

"""========== Streamlines =========="""
# regularly spaced grid spanning the domain of x and y



#new frame


Delaunaypoints=[]
for columns in range(len(X[0])):
    Delaunaypoints.append([X[0][columns],Y[0][0]])
    Delaunaypoints.append([X[0][columns],Y[-1][0]])

for rows in range(len(Y)-2):
    Delaunaypoints.append([X[0][0],Y[rows+1][0]])
    Delaunaypoints.append([X[0][-1],Y[rows+1][0]])
Delaunaypoints=np.array(Delaunaypoints)
#print(Delaunaypoints)
tri=Delaunay(Delaunaypoints)

triangles=Delaunaypoints[tri.simplices]
# print(triangles)

Clst=[]
Rlst=[]
for i in range(len(triangles)):
    ax=triangles[i][0][0]
    ay=triangles[i][0][1]
    bx=triangles[i][1][0]
    by=triangles[i][1][1]
    cx=triangles[i][2][0]
    cy=triangles[i][2][1]
    C=circumcenter(ax,ay,bx,by,cx,cy)
    R=np.sqrt((C[0]-ax)**2+(C[1]-ay)**2)
    Clst.append(C)
    Rlst.append(R)

index=np.argmax(Rlst)

"""========== Generate lines from seed =========="""
lines = []

bandwidth = 1
trimdist = bandwidth/2



plt.figure(figsize=(9,11))
l=0
#Get streamline boundary points for triangulation

while Rlst[index] >= trimdist:
    previousR=Rlst[index]
    l+=1
    print(l)
    print(previousR)
    #forward
    flow_lineout=[]
    strm = np.array(plt.streamplot(X, Y, U, V, start_points=[[Clst[index][0], Clst[index][1]]],color='blue').lines.get_segments())
    if len(strm)>0:
        flow_line=strm[:,0]
    # num_pts = len(strm.lines.get_segments())
    # flow_line = np.full((num_pts, 2), np.nan)
    # for i in range(num_pts):
    #     flow_line[i, :] = strm.lines.get_segments()[i][0, :]
    # if len(flow_line)>0:
        klst=[]
        # cs=interp1d(flow_line[:,0],flow_line[:,1],kind='linear')
        # xnew=np.arange(np.min(flow_line[:,0]),np.max(flow_line[:,0]),0.4)
        # ynew=cs(xnew)
        # flow_line=[]
        # for i in range(len(xnew)):
        #     flow_line.append([xnew[i],ynew[i]])
        # flow_line=np.array(flow_line)
        flowline2=flow_line[:,0]
        flowline3=flow_line


        if len(lines)>0:
            indexofseedpoint=np.argwhere(np.abs(flowline2-Clst[index][0])<0.7)
            flow_linefirst=flow_line[:indexofseedpoint[0,0]+1]
            flow_linesecond=flow_line[indexofseedpoint[0,0]-1:]
            for i in range(len(lines)):
                for j in range(len(lines[i])):
                    x=lines[i][j][0]
                    y=lines[i][j][1]
                    for k in range(len(flow_linefirst)):
                        xflow=flow_linefirst[k][0]
                        yflow=flow_linefirst[k][1]
                        dist=np.sqrt((x-xflow)**2+(y-yflow)**2)
                        if dist<0.5:
                            klst.append(k)
                        elif dist>=0.5:
                            klst.append(0)
            if len(klst)>0:
                flow_linefirst=flow_linefirst[max(klst)+1:]
            slst=[]
            for i in range(len(lines)):
                for j in range(len(lines[i])):
                    x=lines[i][j][0]
                    y=lines[i][j][1]
                    for k in range(len(flow_linesecond)):
                        xflow=flow_linesecond[k][0]
                        yflow=flow_linesecond[k][1]
                        dist=np.sqrt((x-xflow)**2+(y-yflow)**2)
                        if dist<0.5:
                            slst.append(k)
                        else:
                            slst.append(len(flow_linesecond))
            flow_linesecond = flow_linesecond[:min(slst)]
            if len(klst)>0 and len(slst)>0:
                flow_line=np.concatenate((flow_linefirst,flow_linesecond),axis=0)
            elif len(klst)>0 and len(slst)==0:
                flow_line=flow_linefirst
            elif len(slst)>0 and len(klst)==0:
                flow_line=flow_linesecond





    #split flowline into two parts that are not close to previous streamlines
    if len(flow_line)>1:
        lines.append(flow_line)
        Delaunaypoints = np.append(Delaunaypoints,flow_line[:],axis = 0)
        tri=Delaunay(Delaunaypoints)

        triangles=Delaunaypoints[tri.simplices]
        Clst=[]
        Rlst=[]
        for i in range(len(triangles)):
            ax=triangles[i][0][0]
            ay=triangles[i][0][1]
            bx=triangles[i][1][0]
            by=triangles[i][1][1]
            cx=triangles[i][2][0]
            cy=triangles[i][2][1]
            C=circumcenter(ax,ay,bx,by,cx,cy)
            R=np.sqrt((C[0]-ax)**2+(C[1]-ay)**2)
            Clst.append(C)
            Rlst.append(R)

        index=np.argmax(Rlst)
        iterator=1
    else:
        index=np.argsort(Rlst)[-1]


    while previousR<Rlst[index] or Clst[index][0] > np.max(xipoints) or Clst[index][0] < np.min(xipoints) or Clst[index][1] > np.max(yipoints) or Clst[index][1] < np.min(yipoints):
        index = np.argsort(Rlst)[-iterator]
        iterator += 1

# #TRIMMING OF STREAMLINES OUTSIDE OBJECT
# newlines = []
# XC=dataframe[:,0]
# YC=dataframe[:,1]
#
# for i in range(len(lines)):
#     newpoints = []
#     for j in range(len(lines[i])):
#         minimum = 100
#         x = lines[i][j][0]
#         y = lines[i][j][1]
#         for k in range(len(XC)):
#             x_dist = XC[k]-x
#             y_dist = YC[k]-y
#             grid_dist = x_dist**2+y_dist**2
#             if grid_dist<minimum:
#                 minimum = grid_dist
#                 point_index = k
#         if thres_rho[point_index] != 0:
#             point = [x,y]
#             newpoints.append(point)
#     if len(newpoints) > 1:
#         newlines.append(newpoints)
#
#
# finalx = []
# finaly = []
# for i in range(len(newlines)):
#     x_lstnew = []
#     y_lstnew = []
#     for j in range(len(newlines[i])):
#         x_lstnew.append(newlines[i][j][0])
#         y_lstnew.append(newlines[i][j][1])
#         finalx.append(x_lstnew)
#         finaly.append(y_lstnew)
#
#
# grid = np.zeros((20, 30))
#
# rho = dataframe[:, 4].reshape(30, 20)
#
# for i in range(len(grid)):
#     for j in range(len(grid[i])):
#         if rho[j][i] == 1:
#             grid[i][j] = 1
#
#
# framedgrid = np.pad(grid, pad_width=0, mode='constant', constant_values=0)
#
#
#
#
# # regularly spaced grid spanning the domain of x and y
# xi = np.arange(0, len(framedgrid[0]))
# yi = np.arange(0, len(framedgrid))
# X, Y = np.meshgrid(xi, yi)
#
# plt.figure(figsize=(12,9))
# for i in range(len(finalx)):
#     plt.plot(finalx[i],finaly[i],'b')
# plt.imshow(framedgrid)
# plt.show()
#
#




#print(x_lstnew)
#plt.figure()
#plt.plot(finalx, finaly)
#plt.show()

#print(lines)
# print("NEWLINES", newlines)
#np.asarray(newlines)
#print(newlines[0][:,0])
#
# plt.figure(figsize=(12,9))
# for j in range(len(newlines)):
#     for i in range(len(newlines[j])):
#         plt.plot(newlines[j][i][0, :],newlines[j][i][1, :],'b')
# plt.show()



#Start and end of each streamlines
# print_streamlines = []
#
# for i in range(len(lines)):
#     start_and_end = []
#     start_and_end.append(lines[i][0])
#     start_and_end.append(lines[i][-1])
#     print_streamlines.append(start_and_end)
#
# with open('start_end_lines.csv', mode='w') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Start', 'End'])
#     for row in print_streamlines:
#         writer.writerow([str(cell) for cell in row])
#
#
#
# #Entire Streamlines
# with open('newlines.csv', mode='w') as file:
#     writer = csv.writer(file)
#     # headers = []
#     # for i in range(len(lines)):
#     #     index = 0
#     #     if len(lines[i]) > len(lines[index]):
#     #         index = i
#     # for j in range(len(lines[index])):
#     #     headers.append('Coordinate {}'.format(j + 1))
#     # writer.writerow(headers)
#
#     for k in range(len(lines)):
#         linek = []
#         for h in range(len(lines[k])):
#             linek.append(lines[k][h])
#         writer.writerow(linek)
#
# #print streamline
# with open('newlines.csv', 'r') as csv_file:
#     # Create a reader object
#     csv_reader = csv.reader(csv_file)
#
#     data_list= []
#     for row in csv_reader:
#         # Print each row
#         data_list.append(row)

#print last streamline
# print(data_list[-1][:])




# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# from scipy.spatial import Delaunay
#
# """========== Import grid and vector field from csv file =========="""
# # import csv file
# df = pd.read_csv('Data/TAO_solution.csv')
# dataframe = df.to_numpy()
#
# # define size of x and y axis
# xsize = 30
# ysize = 20
#
# # create grid with values of 0 at every point
# grid = np.zeros((20, 30))
#
# # from csv file get value of density (0 or 1) at each point in the grid
# rho = dataframe[:, 4].reshape(30, 20)
#
# # change the value of the density of the grid defined above
# for i in range(len(grid)):
#     for j in range(len(grid[i])):
#         if rho[j][i] == 1:
#             grid[i][j] = 1
#
# # from csv file get theta of vecotr field
# theta = dataframe[:, 2]
# theta = (theta.reshape(30, 20)).T
# print(theta)
#
# U = np.cos(-theta)
# V = np.sin(-theta)
# """========== Refine grid to identify edge points and create a frame around it =========="""
# Rmax = 100
# lines = []
# h = 0
#
# # Add frame of zeros to grid and vector fields
# framedgrid = np.pad(grid, pad_width=2, mode='constant', constant_values=0)
# U = np.pad(U, pad_width=2, mode='constant', constant_values=0)
# V = np.pad(V, pad_width=2, mode='constant', constant_values=0)
#
# # Define edge by setting the "density" of edge points to 2
# edgepoints = []
# for i in range(len(framedgrid)):
#     for j in range(len(framedgrid[i])):
#         if framedgrid[i][j] == 1 and (
#                 framedgrid[i + 1][j] == 0 or framedgrid[i - 1][j] == 0 or framedgrid[i][j + 1] == 0 or framedgrid[i][
#             j - 1] == 0 or framedgrid[i + 1][j + 1] == 0 or framedgrid[i + 1][j - 1] == 0 or framedgrid[i - 1][
#                     j + 1] == 0 or framedgrid[i - 1][j - 1] == 0):
#             edgepoints.append([j, i])
#             framedgrid[i][j] = 2
# edgepoints = np.array(edgepoints)
#
# # Make a frame around the edge. Setting the density of the Outer frame to 3
# for i in range(len(edgepoints)):
#     pointx = edgepoints[i][0]
#     pointy = edgepoints[i][1]
#     for j in range(4):
#         if framedgrid[pointy][pointx + 1] == 0:
#             framedgrid[pointy][pointx + 1] = 3
#
#         elif framedgrid[pointy][pointx - 1] == 0:
#             framedgrid[pointy][pointx - 1] = 3
#
#         elif framedgrid[pointy + 1][pointx] == 0:
#             framedgrid[pointy + 1][pointx] = 3
#
#         elif framedgrid[pointy - 1][pointx] == 0:
#             framedgrid[pointy - 1][pointx] = 3
#
# # Add all outer edge points to a list
# outer_edgepoints = []
# for i in range(len(framedgrid)):
#     for j in range(len(framedgrid[i])):
#         if framedgrid[i][j] == 3:
#             outer_edgepoints.append([j, i])
#
# outer_edgepoints = np.array(outer_edgepoints)
#
# # set the vector field at the edge, outer edge and empty points to 0
# for i in range(len(framedgrid)):
#     for j in range(len(framedgrid[i])):
#         if framedgrid[i, j] == 0 or framedgrid[i, j] == 3 or framedgrid[i, j] == 2:
#             U[i, j] = 0
#             V[i, j] = 0
#
# # regularly spaced grid spanning the domain of x and y
# xi = np.arange(0, len(framedgrid[0]))
# yi = np.arange(0, len(framedgrid))
# X, Y = np.meshgrid(xi, yi)
#
#
# # Defining the function that calculates the circumcenter of a triangle
# def circumcenter(ax, ay, bx, by, cx, cy):
#     t = ax ** 2 + ay ** 2 - bx ** 2 - by ** 2
#     u = ax ** 2 + ay ** 2 - cx ** 2 - cy ** 2
#     J = (ax - bx) * (ay - cy) - (ax - cx) * (ay - by)
#
#     x = (-1 * (ay - by) * u + (ay - cy) * t) / (2 * J)
#     y = ((ax - bx) * u - (ax - cx) * t) / (2 * J)
#     return [x, y]
#
#
# Delaunaypoints = []
#
# # List of delauny points in the shape including outer edge
# for i in range(len(framedgrid)):
#     for j in range(len(framedgrid[i])):
#         if framedgrid[i][j] == 2 or framedgrid[i][j] == 3:
#             Delaunaypoints.append([j, i])
# Delaunaypoints = np.array(Delaunaypoints)
#
# """========== Loop to repeat delauny triangulation until the radius is 0.7 and generate streamlines =========="""
# while Rmax > 1.2:
#     # Delauny triangulation on object including edge frame
#     tri = Delaunay(Delaunaypoints)
#
#     # Removing triangle with edge points
#     triangles = np.array(Delaunaypoints[tri.simplices])
#
#     mask = []
#
#     for i in range(len(triangles)):
#         for n in range(len(triangles[i])):
#             for k in range(len(outer_edgepoints)):
#                 if triangles[i][n][0] == outer_edgepoints[k][0] and triangles[i][n][1] == outer_edgepoints[k][1]:
#                     triangles[i] = 0
#
#     for i in range(len(triangles)):
#         if (triangles[i][0] == [0, 0]).all() and (triangles[i][1] == [0, 0]).all() and (
#                 triangles[i][2] == [0, 0]).all():
#             mask.append(False)
#         else:
#             mask.append(True)
#
#     triangles = triangles[mask]
#
#     # Calculating the largest circle
#     Clst = []
#     Rlst = []
#     for i in range(len(triangles)):
#         ax = triangles[i][0][0]
#         ay = triangles[i][0][1]
#         bx = triangles[i][1][0]
#         by = triangles[i][1][1]
#         cx = triangles[i][2][0]
#         cy = triangles[i][2][1]
#         C = circumcenter(ax, ay, bx, by, cx, cy)
#         R = np.sqrt((C[0] - ax) ** 2 + (C[1] - ay) ** 2)
#         Clst.append(C)
#         Rlst.append(R)
#
#     index = np.argmax(Rlst)
#
#     # Preventing seed point to be at the edge of the object. (Skip to next Rmax if that's the case)
#     # Continue=False
#     # while Continue==False:
#     #     yes=0
#     #     m=1
#     #     for i in range(len(edgepoints)):
#     #         x=edgepoints[i][0]
#     #         y=edgepoints[i][1]
#     #         if np.linalg.norm(np.array((x,y))-np.array((Clst[index][0],Clst[index][1])))<0.5:
#     #             yes+=1
#     #     if yes==0:
#     #         Continue=True
#     #     else:
#     #         index=np.argsort(np.max(Rlst, axis=0))[-1-m]
#     #         m+=1
#
#     # Used to plot all the streamlines.
#     strm = plt.streamplot(X, Y, U, V, start_points=[[Clst[index][0], Clst[index][1]]], color='red', density=10)
#     streamline = np.array(strm.lines.get_segments())[:, 0]
#     Delaunaypoints = np.vstack((Delaunaypoints, streamline))
#     lines.append(streamline)
#
#     # Printing and plotting/visualizing data
#     print(h)
#     h += 1
#     Rmax = Rlst[index]
#     print(Rmax)
#     print(Clst[index])
#     # plt.figure()
#     # plt.triplot(Delaunaypoints[:,0],Delaunaypoints[:,1],tri.simplices[mask])
#     # plt.imshow(framedgrid)
#     # plt.show()
#     # plt.figure(figsize=(12, 9))
#     for i in range(len(lines)):
#         plt.plot(lines[i][:, 0], lines[i][:, 1], 'b')
#     plt.scatter(edgepoints[:, 0], edgepoints[:, 1])
#     plt.imshow(framedgrid)
#     # plt.quiver(X,Y,U,V)
#     plt.show()
#
# # PLOTTING FIGURE
# plt.figure(figsize=(12, 9))
np.save('strmrec', np.array(lines))
for i in range(len(lines)):
    plt.plot(lines[i][:, 0], lines[i][:, 1], 'b')
plt.scatter(edgepoints[:, 0], edgepoints[:, 1])
plt.show()
#
# print(lines)
# # #print(framedgrid)
# # plt.figure()
# #
# # # plt.imshow(framedgrid)
# #
# # # plt.triplot(Delaunaypoints[:,0],Delaunaypoints[:,1],tri.simplices[mask])
# # plt.scatter(Clst[index][0],Clst[index][1],color='r')
# # plt.show()
# # print(strm.lines.get_segments())
# # print("VECTOR V: ",V[4][15])
# # print("DENSITY: ",framedgrid[4][15])



