import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import Delaunay
from scipy.interpolate import RectBivariateSpline
from scipy.spatial import distance
import time

"""===================================================="""
"""==== Import grid and vector field from csv file ===="""
"""===================================================="""
# import csv file
print('Starting initialization...')
initialtime=time.perf_counter()
df=pd.read_csv('Data/For_our_5final_trickoutputCSV.csv')
dataframe=df.to_numpy()
plot=False
c=0
m=1
distance=2

#define size of x and y axis
xi=dataframe[0:,0]
yi=dataframe[0:,1]
xipoints=[]
yipoints=[]
xipoint=1
for i in range(len(yi)):
    if yi[i]!=xipoint:
        yipoints.append(yi[i])
        xipoint=yipoints[-1]

for i in range(190):
    xipoints.append(xi[i])

xsize = len(xipoints)
ysize = len(yipoints)

X,Y=np.meshgrid(xipoints,yipoints)

resolution=5
minflowlinelength=2
#create grid with values of 0 at every point
grid = np.zeros((ysize,xsize))


#from csv file get value of density (0 or 1) at each point in the grid
rho=dataframe[:,4].reshape(ysize, xsize)

# #change the value of the density of the grid defined above


#from csv file get theta of vecotr field
u=dataframe[:,2]
v=dataframe[:,3]

U=(u.reshape(ysize,xsize))
V=(v.reshape(ysize,xsize))


"""========== Refine grid to identify edge points and create a frame around it =========="""
Rmax=100
lines=[]
h=0

#Add frame of zeros to grid and vector fields
framedgrid=np.pad(rho,pad_width=2,mode='constant', constant_values=0)
U=np.pad(U,pad_width=2,mode='constant',constant_values=0)
V=np.pad(V,pad_width=2,mode='constant',constant_values=0)

xi=np.linspace(xipoints[0],xipoints[-1],len(framedgrid[0]))
yi=np.linspace(yipoints[0],yipoints[-1],len(framedgrid))
# xinew=np.arange(0,len(framedgrid[0]),0.5)
# yinew=np.arange(0,len(framedgrid),0.5)
X,Y=np.meshgrid(xi,yi)

#Define edge by setting the "density" of edge points to 2
edgepoints=[]
edgepointsindex=[]
for i in range(len(framedgrid)):
    for j in range(len(framedgrid[i])):
        if framedgrid[i][j]==1 and (framedgrid[i+1][j]==0 or framedgrid[i-1][j]==0 or framedgrid[i][j+1]==0 or framedgrid[i][j-1]==0 or framedgrid[i+1][j+1]==0 or framedgrid[i+1][j-1]==0 or framedgrid[i-1][j+1]==0 or framedgrid[i-1][j-1]==0):
            edgepoints.append([xi[j],yi[i]])
            edgepointsindex.append([j,i])
            framedgrid[i][j] = 2
edgepoints=np.array(edgepoints)
edgepointsindex=np.array(edgepointsindex)


#Make a frame around the edge. Setting the density of the Outer frame to 3
for i in range(len(edgepoints)):
    pointx=edgepointsindex[i][0]
    pointy=edgepointsindex[i][1]
    for j in range(4):
        if framedgrid[pointy][pointx+1]==0:
            framedgrid[pointy][pointx+1]=3

        elif framedgrid[pointy][pointx-1]==0:
            framedgrid[pointy][pointx - 1] = 3

        elif framedgrid[pointy+1][pointx]==0:
            framedgrid[pointy + 1][pointx]=3

        elif framedgrid[pointy-1][pointx]==0:
            framedgrid[pointy - 1][pointx] =3

#Add all outer edge points to a list
outer_edgepoints=[]
for i in range(len(framedgrid)):
    for j in range(len(framedgrid[i])):
        if framedgrid[i][j]==3:
            outer_edgepoints.append([xi[j],yi[i]])

outer_edgepoints = np.array(outer_edgepoints)

# set the vector field at the edge, outer edge and empty points to 0
for i in range(len(framedgrid)):
    for j in range(len(framedgrid[i])):
        if framedgrid[i,j]==0 or framedgrid[i,j]==3:
            U[i,j]=0
            V[i,j]=0

#regularly spaced grid spanning the domain of x and y

# Xnew,Ynew=np.meshgrid(xinew,yinew)
#
# fu=RectBivariateSpline(yi,xi,U)
# fv=RectBivariateSpline(yi,xi,V)
# Unew=fu(yinew,xinew)
# Vnew=fv(yinew,xinew)
#Defining the function that calculates the circumcenter of a triangle

def circumcenter(ax,ay,bx,by,cx,cy):
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return [ux, uy]

Delaunaypoints=[]

#List of delauny points in the shape including outer edge
for i in range(len(framedgrid)):
    for j in range(len(framedgrid[i])):
        if framedgrid[i][j] == 2 or framedgrid[i][j] == 3:
            Delaunaypoints.append([xi[j],yi[i]])
Delaunaypoints=np.array(Delaunaypoints)
inittime=time.perf_counter()

# fig = plt.figure(figsize=(14, 9))
# ax = plt.axes(projection='3d')
#
# # Creating plot
# ax.plot_surface(X, Y, U,cmap='coolwarm')
#
# # show plot
# plt.show()
timelst=[]
print('Finished initialization in ', inittime-initialtime, ' seconds')



"""========== Loop to repeat delauny triangulation until the radius is 0.7 and generate streamlines =========="""
if __name__=="__main__":
    while Rmax>distance:
        timestamp = time.perf_counter()
        timelst.append(timestamp)
        #Delauny triangulation on object including edge frame
        tri=Delaunay(Delaunaypoints)

        #Removing triangle with edge points
        triangles=np.array(Delaunaypoints[tri.simplices])
        mask=[]
        for i in range(len(triangles)):
            for n in range(len(triangles[i])):
                for k in range(len(outer_edgepoints)):
                    if np.abs(triangles[i][n][0] - outer_edgepoints[k][0])<0.01 and np.abs(triangles[i][n][1] - outer_edgepoints[k][1])<0.01:
                        triangles[i]=0
            if (triangles[i][0] == [0, 0]).all() and (triangles[i][1] == [0, 0]).all() and (triangles[i][2] == [0, 0]).all():
                mask.append(False)
            else:
                mask.append(True)
        # plt.figure()
        # # plt.imshow(framedgrid)
        # plt.triplot(Delaunaypoints[:, 0], Delaunaypoints[:, 1], tri.simplices[mask])
        # plt.show()

        triangles=triangles[mask]
        #Calculating the largest circle
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

        index=np.argsort(Rlst)[-1-c]
        # Continue =False
        # m=1
        #
        # while Continue==False:
        #     v=1
        #     xindex=np.argsort(np.abs(xi-Clst[index][0]))[:3]
        #     yindex=np.argsort(np.abs(yi-Clst[index][1]))[:3]
        #     for i in range(len(xindex)):
        #         for j in range(len(yindex)):
        #             if U[yindex[j]][xindex[i]]==0:
        #                 v+=1
        #
        #     if v>1:
        #         index = np.argsort(Rlst)[-1 - m]
        #         m += 1
        #         print(m)
        #     else:
        #         Continue=True

        # Continue=False
        # m=1
        # while Continue ==False:
        #     if Clst[index][0]>np.max(xi) or Clst[index][0]<np.min(xi) or Clst[index][1]>np.max(yi) or Clst[index][1]<np.min(yi):
        #         index = np.argsort(Rlst)[-1 - m]
        #         m += 1
        #         print(m)
        #     else:
        #         Continue =True
        #Preventing seed point to be at the edge of the object. (Skip to next Rmax if that's the case)
        Continue = False
        if m>4:
            m -=3
        else:
            m=1
        while Continue == False:
            if Clst[index][0] < np.max(xi) and Clst[index][0] > np.min(xi) and Clst[index][1] < np.max(yi) and Clst[index][1] > np.min(yi):
                strm = np.array(plt.streamplot(X, Y, -U, -V, start_points=[[Clst[index][0], Clst[index][1]]], color='red', density=3, broken_streamlines=False).lines.get_segments())
                if len(strm)<1:
                    strm=np.array(plt.streamplot(X, Y, U, V, start_points=[[Clst[index][0], Clst[index][1]]], color='red', density=3, broken_streamlines=False).lines.get_segments())

                if len(strm) > 2 :
                    streamline = strm[:, 0]
                    flow_line2 = streamline[:, 0]
                    if len(np.argwhere(np.abs(flow_line2-Clst[index][0])<0.05))>0:
                        indexofseedpoint = int(np.average(np.argwhere(np.abs(flow_line2 - Clst[index][0]) < 0.5)[0][0]))
                        print('Seedpoint index = ', indexofseedpoint)
                        flow_linefirst = streamline[:indexofseedpoint + 1]
                        flow_linesecond = streamline[indexofseedpoint - 1:]
                        klst = []
                        slst = []
                        if len(lines) > 0:
                            for i in range(len(lines)):
                                for j in range(len(lines[i])):
                                    x = lines[i][j][0]
                                    y = lines[i][j][1]
                                    for k in range(len(flow_linefirst)):
                                        xflow = flow_linefirst[k][0]
                                        yflow = flow_linefirst[k][1]
                                        dist = np.linalg.norm(np.array((x, y)) - np.array((xflow, yflow)))
                                        if dist < distance:
                                            klst.append(k)
                                        elif dist >= distance:
                                            klst.append(0)
                                    for k in range(len(flow_linesecond)):
                                        xflow = flow_linesecond[k][0]
                                        yflow = flow_linesecond[k][1]
                                        dist = np.linalg.norm(np.array((x, y)) - np.array((xflow, yflow)))
                                        if dist < distance:
                                            slst.append(k)
                                        else:
                                            slst.append(len(flow_linesecond))
                            if len(klst) > 0:
                                flow_linefirst = flow_linefirst[max(klst) + 1:]
                            flow_linesecond = flow_linesecond[:min(slst)]
                            if len(klst) > 0 and len(slst) > 0:
                                flow_line = np.concatenate((flow_linefirst, flow_linesecond), axis=0)
                            elif len(klst) > 0 and len(slst) == 0:
                                flow_line = flow_linefirst
                            elif len(slst) > 0 and len(klst) == 0:
                                flow_line = flow_linesecond


                        else:
                            flow_line = streamline
                        if len(flow_line)>2:
                            Delaunaypoints = np.vstack((Delaunaypoints, flow_line))
                            lines.append(flow_line)
                            Continue = True
                        else:
                            index = np.argsort(Rlst)[-1 - m]
                            m += 1
                            print('m = ', m)
                    else:
                        index = np.argsort(Rlst)[-1 - m]
                        m += 1
                        print('m = ', m)
                else:
                    index = np.argsort(Rlst)[-1 - m]
                    m += 1
                    print('m = ', m)
            else:
                index = np.argsort(Rlst)[-1 - m]
                m += 1
                print('m = ', m)
        # print(Clst[index])
        # plt.figure()
        # plt.imshow(U)
        # plt.show()

        #strm = plt.streamplot(X, Y, -U, -V, start_points=[[Clst[index][0], Clst[index][1]]], color='red', density=5, broken_streamlines=False)

        print(Clst[index])
        # while Continue==False:
        #     strmlst=[]
        #     lengthslst=[]
        #     for i in range(5):
        #         index = np.argsort(Rlst)[-m - i]
        #         strmlst.append(np.array(plt.streamplot(X, Y, U,V, start_points=[[Clst[index][0], Clst[index][1]]], color='red', density=5).lines.get_segments()))
        #     strmarray=np.array(strmlst)
        #     for i in range(len(strmarray)):
        #         if(len(strmarray[i])>0):
        #             lengthslst.append(distance.euclidean(tuple(strmarray[i][0][0]),tuple(strmarray[i][-1][0])))
        #     lengths=np.array(lengthslst)
        #     print('lengths' ,lengths)
        #     if len(lengths)>=1:
        #         indexlengths=np.argmax(lengths)
        #         strm=strmarray[indexlengths]
        #         index=np.argsort(Rlst)[-m-indexlengths]
        #         Continue=True
        #     else:
        #         m+=5

        #
        #     if len(lengths)>0:
        #         Continue=True
        #     else:
        #         # index=np.argsort(Rlst)[-m-indexlengths]
        #         m+=5
        #         print(m)




        #Used to plot all the streamlines.
        # strm = plt.streamplot(X, Y, U, V, start_points=[[Clst[index][0], Clst[index][1]]], color='red', density=10)
        # print(strm)
        # streamline=strm[:,0]


        # Continue = False
        #
        # # while Continue == False:
        #     # Continue1=False
        #     # n=1
        #     # while Continue1==False:
        #     #     indexofseedpointlist=np.argwhere((np.abs(flow_line2-Clst[index][0]))<0.001)
        #     #     if len(indexofseedpointlist)>0:
        #     #         indexofseedpoint = indexofseedpointlist[0][0]
        #     #         Continue1=True
        #     #     else:
        #     #         index = np.argsort(Rlst)[-1 - m-n]
        #     #         n += 1
        #
        #
        #
        #
        #
        # if len(flow_line) > minflowlinelength:
        #     Delaunaypoints = np.vstack((Delaunaypoints, flow_line))
        #     lines.append(flow_line)
        #     c=0
        #     Continue = True
        # else:
        #     index = np.argsort(Rlst)[-1 - c]
        #     c += 1
        #     print('c = ', c)
        if Rlst[index]<0.7 and plot==True:
            plt.figure(figsize=(12, 9))
            for i in range(len(lines)):
                plt.plot(lines[i][:, 0], lines[i][:, 1], 'r')
            plt.scatter(edgepoints[:, 0], edgepoints[:, 1])
            plt.show()
            np.save('lines', np.array(lines))
            plot=False

        #Printing and plotting/visualizing data
        print('Streamline #: ', h)
        h+=1
        Rmax=Rlst[index]
        print(Rmax)
        print(Clst[index])
        # plt.figure()
        # plt.triplot(Delaunaypoints[:,0],Delaunaypoints[:,1],tri.simplices[mask])
        # plt.imshow(framedgrid)
        # plt.show()
        # plt.figure(figsize=(12, 9))
        # for i in range(len(lines)):
        #     plt.plot(lines[i][:, 0], lines[i][:, 1], 'b')
        # plt.scatter(edgepoints[:, 0], edgepoints[:, 1])
        # plt.imshow(framedgrid)
        # # plt.quiver(X,Y,U,V)
        # plt.show()

    #PLOTTING FIGURE
    plt.figure(figsize=(12,9))
    plt.imshow(framedgrid )
    for i in range(len(lines)):
        plt.plot(lines[i][:,0],lines[i][:,1],'r')
    plt.scatter(edgepoints[:,0],edgepoints[:,1])
    plt.show()




    # #print(framedgrid)
    # plt.figure()
    #
    # # plt.imshow(framedgrid)
    #
    # # plt.triplot(Delaunaypoints[:,0],Delaunaypoints[:,1],tri.simplices[mask])
    # # plt.scatter(Clst[index][0],Clst[index][1],color='r')
    # plt.show()
    # print(strm.lines.get_segments())
    # print("VECTOR V: ",V[4][15])
    # print("DENSITY: ",framedgrid[4][15])
    # print(np.array(lines))
    np.save('timenonrecrmax2',np.array(timelst))
    np.save('linesnonrecrmax2', np.array(lines,dtype=object))

