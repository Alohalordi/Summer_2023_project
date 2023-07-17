import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from recgrid import X,Y,rho,xipoints,yipoints,edgepoints

# df=pd.read_csv('Data/For_our_5final_trickoutputCSV.csv')
# dataframe=df.to_numpy()
lines=np.load('linesrec.npy',allow_pickle=True)
time=np.load('timerectangulargrid.npy', allow_pickle=True)
ticks=np.arange(0,len(time))
plot=False

# xi=dataframe[0:,0]
# yi=dataframe[0:,1]
# xipoints=[]
# yipoints=[]
# xipoint=1
# for i in range(len(yi)):
#     if yi[i]!=xipoint:
#         yipoints.append(yi[i])
#         xipoint=yipoints[-1]
#
# for i in range(190):
#     xipoints.append(xi[i])
#
# xsize = len(xipoints)
# ysize = len(yipoints)
#
# X,Y=np.meshgrid(xipoints,yipoints)


#from csv file get value of density (0 or 1) at each point in the grid
# rho=dataframe[:,4].reshape(ysize, xsize)
indexlst=[]

for i in range(len(lines)):
    indexlst.append([])
    for j in range(len(lines[i])):
        xindex=int(np.average(np.argwhere(np.abs(xipoints-lines[i][j,0])<1)))
        yindex=int(np.average(np.argwhere(np.abs(yipoints-lines[i][j,1])<1)))
        indexlst[i].append([xindex,yindex])


mask=[]

for i in range(len(indexlst)):
    mask.append([])
    for j in range(len(indexlst[i])):
        if rho[indexlst[i][j][1],indexlst[i][j][0]]==0:
            lines[i][j]=0
print(lines)
# for i in range(len(lines)):
#     for j in range(len(lines[i])):
#         if mask[i][j]==False:
#             lines[i][j]=[0]
newlines=[[]]
k=0

for i in range(len(lines)):
    for j in range(len(lines[i])):
        if np.abs(sum(lines[i][j]))>0.001:
            newlines[k].append(lines[i][j])
        else:
            k+=1
            newlines.append([])
    k += 1
    newlines.append([])
print(newlines)
finallines=[]
for i in range(len(newlines)):
    if len(newlines[i])>0:
        finallines.append(np.array(newlines[i]))

print('t', len(ticks))
print(max(time))

if plot==True:
    plt.figure(figsize=(12,9))
    for i in range(len(finallines)-1):
        plt.plot(finallines[i][:,0],finallines[i][:,1],'r')
    plt.plot(finallines[-1][:, 0], finallines[-1][:, 1], 'r',label='Streamline')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.scatter(edgepoints[:,0],edgepoints[:,1],label='Edge of object')
    plt.legend()
    plt.savefig('Figures/linesrecgrid2')
    plt.show()

    plt.figure()
    plt.xlabel('Iteration [-]')
    plt.ylabel('Time elapsed [s]')
    plt.plot(ticks,time)
    plt.savefig('Figures/timerecgrid2')
    plt.show()