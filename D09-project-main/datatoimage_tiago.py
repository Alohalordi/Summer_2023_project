import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import patches
import scipy.interpolate as interpolate
from scipy.spatial import Delaunay
from scipy.interpolate import interp1d
import csv

df=pd.read_csv('Data/TAO_solution.csv')
dataframe=df.to_numpy()

print("kuba sucks dick")
XC=dataframe[:,0]
YC=dataframe[:,1]
theta=dataframe[:,2]
idx=dataframe[:,3]
thres_rho=dataframe[:,4]
u=np.cos(-theta)
v=np.sin(-theta)
indexnew=0
indexlst=[500]

xsize=30
ysize=20
bandwidth = 1
XC-=min(XC)
YC-=min(YC)
"""========== Functions =========="""
def circumcenter(ax,ay,bx,by,cx,cy):
    t=ax**2+ay**2-bx**2-by**2
    u=ax**2+ay**2-cx**2-cy**2
    J=(ax-bx)*(ay-cy)-(ax-cx)*(ay-by)

    x=(-1*(ay-by)*u+(ay-cy)*t)/(2*J)
    y=((ax-bx)*u-(ax-cx)*t)/(2*J)
    # d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    # ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    # uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return [x, y]
"""========== Quiverplot =========="""
# plt.figure(figsize=[15,9])
# plt.quiver(XC,YC,u,v)
# plt.show()

# def trim_streamlines(all_streamlines, current_streamline, dist):
#     streamline=[]
#     if len(all_streamlines) == 0:
#         streamline = current_streamline
#
#     for i in range(len(all_streamlines)):
#         for u in range(len(all_streamlines[i])):
#             for p in range(len(current_streamline)):
#                 distance = np.sqrt((current_streamline[p][0] - all_streamlines[i][u][0]) ** 2 + (
#                             current_streamline[p][1] - all_streamlines[i][u][1]) ** 2)
#
#                 if distance<dist:
#                     streamline = current_streamline[:p-1]
#
#     return streamline

"""========== Streamlines =========="""
# regularly spaced grid spanning the domain of x and y
yi = np.linspace(YC.min(), YC.max(), ysize)
xi = np.linspace(XC.min(), XC.max(), xsize)
X,Y=np.meshgrid(xi,yi)

U = interpolate.griddata((XC, YC), u, (X, Y), method='cubic')
V = interpolate.griddata((XC, YC), v, (X, Y), method='cubic')

# plt.figure(figsize=[15,9])
# plt.streamplot(X,Y,U,V,density=5, arrowsize=0)
# plt.show()
# startpoints=[]
# for rows in range(len(X)):
#     for columns in range(len(X[0])):
#         startpoints.append([X[rows][columns],Y[rows][columns]])
"""========== Seed points =========="""
# plt.figure(figsize=[11,9])
# start=[[1,1],[1,2]]
# plt.streamplot(X,Y,U,V, start_points=startpoints,density=5, arrowsize=0,color='blue')
# plt.streamplot(X,Y,-U,-V,start_points=startpoints,density=5, arrowsize=0, color='red')
# plt.quiver(X,Y,U,V,linewidth=0.25)
# plt.show()

#new frame
le= min(XC) - bandwidth
re= min(XC) + xsize + bandwidth
te= min(YC) + ysize + bandwidth
be= min(YC) - bandwidth

vx=np.linspace(le,re,xsize)
vy=np.linspace(be,te,ysize)
Vx,Vy=np.meshgrid(vx,vy)

Delaunaypoints=[]
for columns in range(len(Vx[0])):
    Delaunaypoints.append([Vx[0][columns],Vy[0][0]])
    Delaunaypoints.append([Vx[0][columns],Vy[-1][0]])

for rows in range(len(Vy)-2):
    Delaunaypoints.append([Vx[0][0],Vy[rows+1][0]])
    Delaunaypoints.append([Vx[0][-1],Vy[rows+1][0]])
Delaunaypoints=np.array(Delaunaypoints)
# print(Delaunaypoints)
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
#
# center=(Clst[index][0],Clst[index][1])


# plt.figure()
# plt.triplot(Delaunaypoints[:,0],Delaunaypoints[:,1],tri.simplices)
# angles = np.linspace(0 * np.pi, 2 * np.pi, 100 )
# xs = Rlst[index]*np.cos(angles)+Clst[index][0]
# ys = Rlst[index]*np.sin(angles)+Clst[index][1]
# plt.plot(Clst[index][0],Clst[index][1],'o',color='r')
# plt.plot(xs, ys, color = 'r')
# plt.Circle(center,radius=Rlst[index],fill=False,color='r')
# # plt.plot(Delaunaypoints[:,0],Delaunaypoints[:,1],'o')
# plt.show()

# center=np.array([Clst[index][0],Clst[index][1]])
"""========== Generate lines from seed =========="""
lines = []


trimdist = bandwidth/2



# idx = 1
# plt.figure()
# strm = plt.streamplot(X,Y,U,V,start_points=[[Clst[index][0],Clst[index][1]]],color='blue')
# plt.streamplot(X,Y,-U,-V,start_points=[[Clst[index][0],Clst[index][1]]],color='r')
# streamlines = []
plt.figure(figsize=(9,11))
# yes=True
l=0
#Get streamline boundary points for triangulation
# while yes ==True:
# while l<143:
while Rlst[index] >= trimdist*2:
    previousR=Rlst[index]
    l+=1
    #forward
    flow_lineout=[]
    strm = plt.streamplot(Vx, Vy, U, V, start_points=[[Clst[index][0], Clst[index][1]]], color='blue')
    num_pts = len(strm.lines.get_segments())
    flow_line = np.full((num_pts, 2), np.nan)
    for i in range(num_pts):
        flow_line[i, :] = strm.lines.get_segments()[i][0, :]
    if len(flow_line)>0:
        klst=[]
        # print(flow_line[:,1])
        cs=interp1d(flow_line[:,0],flow_line[:,1],kind='linear')
        xnew=np.arange(np.min(flow_line[:,0]),np.max(flow_line[:,0]),0.4)
        ynew=cs(xnew)
        flow_line=[]
        for i in range(len(xnew)):
            flow_line.append([xnew[i],ynew[i]])
        flow_line=np.array(flow_line)
        flowline2=flow_line[:,0]
        flowline3=flow_line
        #streamlines.append(trim_streamlines(streamlines,flow_line,bandwidth/2))
        #x=streamlines[:][:][0]
        #y=streamlines[:][:][1]
        #plt.plot(x,y,'r')

        if len(lines)>0:
<<<<<<< Updated upstream
            indexofseedpoint=np.argwhere(np.abs(flowline2-Clst[index][0])<1)
            print(indexofseedpoint)
=======
            indexofseedpoint=np.argwhere(np.abs(flowline2-Clst[index][0])<0.7)
            # print(indexofseedpoint)
>>>>>>> Stashed changes
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
        # idx = np.where(flow_line == [0,0])[0]
        # flow_lineout = np.split(flow_line[idx], np.where(np.diff(idx) != 1)[0] + 1)
        # for i in range(len(flow_lineout)):
        #     lines.append(flow_lineout[i])




    #split flowline into two parts that are not close to previous streamlines
    # and np.sqrt((flow_line[0][0] - flow_line[1][0]) ** 2 + (flow_line[0][1] - flow_line[1][1]) ** 2) > 0.3
    if len(flow_line)>1:
        lines.append(flow_line)
        Delaunaypoints = np.append(Delaunaypoints,flow_line[:],axis = 0)
    #print(Delaunaypoints)
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
        # print(Rlst)
        # print(Clst)
        # print(np.max(Rlst))
        # if Clst[index][1] < 1:
        #     break
        index=np.argmax(Rlst)
        iterator=1
    else:
        index=np.argsort(Rlst)[-1]


    # while Clst[index][0] > 31 or Clst[index][0] < -1 or Clst[index][1] > 21 or Clst[index][1] < -1:
    while previousR<Rlst[index] or Clst[index][0] > 31 or Clst[index][0] < -1 or Clst[index][1] > 21 or Clst[index][1] < -1:
        index = np.argsort(Rlst)[-iterator]
        iterator += 1



    #print(Rlst[index],l)
    # yes=False
plt.show()
print("This is the length of 'lines'" + str(len(lines)))
print("this is stupid")
# print(lines[0])
length=0
for i in range(len(lines)):
    if length < len(lines[i]):
        length = len(lines[i])
print(length)

# lines_1 = np.empty([len(lines), 2*length])
lines_1 = [[0]*(2*length) for i in range(len(lines))]
#print(lines_1.shape())
for i in range(len(lines_1)):
    for j in range(len(lines[i])):
        # if j%2 == 0:
        lines_1[i][2*j] = lines[i][j][0]
        lines_1[i][2*j+1] = lines[i][j][1]


# print(lines[1])
pd.DataFrame(lines_1).to_csv('Data/StreamlinesCoords')
# print(lines)
plt.figure(figsize=(12,9))
for i in range(len(lines)):
    plt.plot(lines[i][:,0],lines[i][:,1],'b')
plt.show()

# pd.DataFrame(lines).to_csv('Data/StreamlinesCoords')



#Start and end of each streamlines
print_streamlines = []

for i in range(len(lines)):
    start_and_end = []
    start_and_end.append(lines[i][0][0])
    start_and_end.append(lines[i][0][1])
    start_and_end.append(lines[i][-1][0])
    start_and_end.append(lines[i][-1][1])
    #start_and_end.append(lines[i][-1])
    print_streamlines.append(start_and_end)
#print("This is the streamlines")
#print(print_streamlines)
pd.DataFrame(print_streamlines).to_csv('Data/Proper_streamlines1')

with open('start_end_lines.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['Start', 'End'])
    for row in print_streamlines:
        writer.writerow([str(cell) for cell in row])



#Entire Streamlines
with open('newlines.csv', mode='w') as file:
    writer = csv.writer(file)
    # headers = []
    # for i in range(len(lines)):
    #     index = 0
    #     if len(lines[i]) > len(lines[index]):
    #         index = i
    # for j in range(len(lines[index])):
    #     headers.append('Coordinate {}'.format(j + 1))
    # writer.writerow(headers)

    for k in range(len(lines)):
        linek = []
        for h in range(len(lines[k])):
            linek.append(lines[k][h])
        writer.writerow(linek)

#print streamline
with open('newlines.csv', 'r') as csv_file:
    # Create a reader object
    csv_reader = csv.reader(csv_file)

    data_list= []
    for row in csv_reader:
        # Print each row
        data_list.append(row)

#print last streamline
# print(data_list[-1][:])
