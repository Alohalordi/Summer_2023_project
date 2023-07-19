import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy import interpolate
from scipy.interpolate import interp1d

df=pd.read_csv('Data/TAO_solution.csv')
dataframe=df.to_numpy()

XC=dataframe[:,0]
YC=dataframe[:,1]
theta=dataframe[:,2]
idx=dataframe[:,3]
thres_rho=dataframe[:,4]
u=np.cos(-theta)
v=np.sin(-theta)
unew=np.cos(-theta).reshape([20,30])
vnew=np.sin(-theta).reshape([20,30])
indexnew=0
indexlst=[500]


xsize=30
ysize=20


bandwidth = 1
XC-=min(XC)
print(XC)
YC-=min(YC)

"""========== Functions =========="""
def circumcenter(ax,ay,bx,by,cx,cy):
    t=ax**2+ay**2-bx**2-by**2
    u=ax**2+ay**2-cx**2-cy**2
    J=(ax-bx)*(ay-cy)-(ax-cx)*(ay-by)

    x=(-1*(ay-by)*u+(ay-cy)*t)/(2*J)
    y=((ax-bx)*u-(ax-cx)*t)/(2*J)
    return [x, y]


"""========== Streamlines =========="""
# regularly spaced grid spanning the domain of x and y
yi = np.linspace(YC.min(), YC.max(), ysize)
xi = np.linspace(XC.min(), XC.max(), xsize)
X,Y=np.meshgrid(xi,yi)

U = interpolate.griddata((XC, YC), u, (X, Y), method='cubic')
V = interpolate.griddata((XC, YC), v, (X, Y), method='cubic')

print(U-unew)
#new frame
le= min(XC)-bandwidth
re= max(XC)+bandwidth
te= max(YC)+bandwidth
be= min(YC)-bandwidth

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

"""========== Generate lines from seed =========="""
lines = []


trimdist = bandwidth/2
previousR=[]


plt.figure(figsize=(9,11))

l=0
while Rlst[index] >= trimdist:

    previousR.append(Rlst[index])
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
        cs=interp1d(flow_line[:,0],flow_line[:,1],kind='linear')
        xnew=np.arange(np.min(flow_line[:,0]),np.max(flow_line[:,0]),0.4)
        ynew=cs(xnew)
        flow_line=[]
        for i in range(len(xnew)):
            flow_line.append([xnew[i],ynew[i]])
        flow_line=np.array(flow_line)
        flowline2=flow_line[:,0]
        flowline3=flow_line

        if len(lines)>0:
            indexofseedpoint=np.argwhere(np.abs(flowline2-Clst[index][0])<0.7)
            print(indexofseedpoint)
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
        index=np.argmax(Rlst)
        iterator=1
    else:
        index=np.argsort(Rlst)[-2]

    if Clst[index][0] > 31 or Clst[index][0] < -1 or Clst[index][1] > 21 or Clst[index][1] < -1:
        plt.triplot(Delaunaypoints[:, 0], Delaunaypoints[:, 1], tri.simplices)
        plt.scatter(Clst[index][0], Clst[index][1], color='red')
        plt.show()
        print(tri.simplices)
        break

    # while Clst[index][0] > 31 or Clst[index][0] < -1 or Clst[index][1] > 21 or Clst[index][1] < -1:



    print(Rlst[index],l)
    # yes=False
plt.show()

print(len(lines))
# print(lines)
plt.figure(figsize=(12,9))
for i in range(len(lines)):
    plt.plot(lines[i][:,0],lines[i][:,1],'b')
plt.show()

