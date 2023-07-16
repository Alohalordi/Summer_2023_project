
"""===================================================="""
"""This file generates streamlines over the whole rectangular grid.
    This corresponds to the second method as described in the final paper.
    Slicing of the streamlines is performed in recgridplotresults.py"""
"""===================================================="""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import Delaunay
from scipy.interpolate import RectBivariateSpline
from scipy.spatial import distance
import time
from nonrecgrid import edgepoints

# import csv file
print('Starting initialization...')
initialtime=time.perf_counter()
df=pd.read_csv('newgrid.csv')
dataframe=df.to_numpy()
plot=False
c=0
m=1
spacing=2


xi=dataframe[0:,0]
yi=dataframe[0:,1]
xipoints=[]
yipoints=[]
xipoint=1
for i in range(len(yi)):
    if yi[i]!=xipoint:
        yipoints.append(yi[i])
        xipoint=yipoints[-1]

for i in range(34):
    xipoints.append(xi[i])
print(yipoints)
xsize = len(xipoints)
ysize = len(yipoints)

X,Y=np.meshgrid(xipoints,yipoints)

resolution=5
minflowlinelength=2
#create grid with values of 0 at every point
grid = np.zeros((ysize,xsize))


#from csv file get value of density (0 or 1) at each point in the grid
rho=dataframe[0:,4].reshape((ysize,xsize))


# #change the value of the density of the grid defined above


#from csv file get theta of vecotr field
u=dataframe[:,2]
v=dataframe[:,3]
print(u[0])

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
X,Y=np.meshgrid(xi,yi)


def circumcenter(ax,ay,bx,by,cx,cy):
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return [ux, uy]

Delaunaypoints=[]

#List of delauny points in the shape including outer edge
for columns in range(len(X[0])):
    Delaunaypoints.append([X[0][columns],Y[0][0]])
    Delaunaypoints.append([X[0][columns],Y[-1][0]])

for rows in range(len(Y)-2):
    Delaunaypoints.append([X[0][0],Y[rows+1][0]])
    Delaunaypoints.append([X[0][-1],Y[rows+1][0]])
Delaunaypoints=np.array(Delaunaypoints)
inittime=time.perf_counter()

timelst=[]
print('Finished initialization in ', inittime-initialtime, ' seconds')



"""========== Loop to repeat delauny triangulation until the radius is 0.7 and generate streamlines =========="""
if __name__=="__main__":
    initialtime=time.perf_counter()
    while Rmax>spacing:
        timestamp=time.perf_counter()
        timelst.append(float(timestamp-initialtime))
        #Delauny triangulation on object including edge frame
        tri=Delaunay(Delaunaypoints)

        #Removing triangle with edge points
        triangles=np.array(Delaunaypoints[tri.simplices])


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

        Continue = False
        if m>4:
            m -=3
        else:
            m=1
        while Continue == False:
            if Clst[index][0] < np.max(xi) and Clst[index][0] > np.min(xi) and Clst[index][1] < np.max(yi) and Clst[index][1] > np.min(yi):
                strm = np.array(plt.streamplot(X, Y, -U, -V, start_points=[[Clst[index][0], Clst[index][1]]], color='red', density=0.5, broken_streamlines=False).lines.get_segments())
                if len(strm)<1:
                    strm=np.array(plt.streamplot(X, Y, U, V, start_points=[[Clst[index][0], Clst[index][1]]], color='red', density=0.5, broken_streamlines=False).lines.get_segments())

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
                                        if dist < spacing:
                                            klst.append(k)
                                        elif dist >= spacing:
                                            klst.append(0)
                                    for k in range(len(flow_linesecond)):
                                        xflow = flow_linesecond[k][0]
                                        yflow = flow_linesecond[k][1]
                                        dist = np.linalg.norm(np.array((x, y)) - np.array((xflow, yflow)))
                                        if dist < spacing:
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
                        if len(flow_line)>0:
                            Delaunaypoints = np.vstack((Delaunaypoints, flow_line))
                            lines.append(np.array(flow_line))
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

        print(Clst[index])

        if Rlst[index]<1 and plot==True:
            plt.figure(figsize=(12, 9))
            for i in range(len(lines)):
                plt.plot(lines[i][:, 0], lines[i][:, 1], 'r')
            plt.scatter(edgepoints[:, 0], edgepoints[:, 1])
            plt.show()
            np.save('linesrec', np.array(lines))
            plot=False

        #Printing and plotting/visualizing data
        print('Streamline #: ', h)
        h+=1
        Rmax=Rlst[index]
        print(Rmax)
        print(Clst[index])


    #PLOTTING FIGURE
    plt.figure(figsize=(12,9))
    plt.imshow(framedgrid )
    for i in range(len(lines)):
        plt.plot(lines[i][:,0],lines[i][:,1],'r')
    plt.scatter(edgepoints[:,0],edgepoints[:,1])
    plt.show()



    #save final results for streamlines and computational time to numpy arrays.
    np.save('linesrec', np.array(lines,dtype=object))
    np.save('timerectangulargrid',np.array(timelst))
