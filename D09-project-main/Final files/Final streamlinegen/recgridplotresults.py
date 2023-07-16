
"""===================================================="""
"""In this file, the streamlines as produced for the whole rectangular
    grid are sliced to the shape of the object. Finally, relevant plots
    are printed."""
"""===================================================="""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from recgrid import X,Y,rho,xipoints,yipoints,edgepoints

#load results of the rectangular grid streamlines.
lines=np.load('linesrec.npy',allow_pickle=True)
time=np.load('timerectangulargrid.npy', allow_pickle=True)
ticks=np.arange(0,len(time))

#indicate if plots are wanted.
plot=False

#find indices of all points in streamlines in the grid as defined in the sliced file.
indexlst=[]

for i in range(len(lines)):
    indexlst.append([])
    for j in range(len(lines[i])):
        xindex=int(np.average(np.argwhere(np.abs(xipoints-lines[i][j,0])<1)))
        yindex=int(np.average(np.argwhere(np.abs(yipoints-lines[i][j,1])<1)))
        indexlst[i].append([xindex,yindex])


#apply a mask on the indiced, putting all points where density=0 to 0.
mask=[]

for i in range(len(indexlst)):
    mask.append([])
    for j in range(len(indexlst[i])):
        if rho[indexlst[i][j][1],indexlst[i][j][0]]==0:
            lines[i][j]=0

#append all seperate streamlines to a new list, making sure the lines get splitted and all the 0-indiced get removed.
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


#turn streamlines into numpy arrays.
finallines=[]
for i in range(len(newlines)):
    if len(newlines[i])>0:
        finallines.append(np.array(newlines[i]))


if plot==True:
    #plot final streamlines sliced to object shape.
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

    #plot computational time vs number of iterations.
    plt.figure()
    plt.xlabel('Iteration [-]')
    plt.ylabel('Time elapsed [s]')
    plt.plot(ticks,time)
    plt.savefig('Figures/timerecgrid2')
    plt.show()