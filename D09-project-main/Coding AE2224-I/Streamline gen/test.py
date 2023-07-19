import numpy as np
import matplotlib.pyplot as plt
from nonrecgrid import edgepoints

lines=np.load('linesnonrecrmax2.npy', allow_pickle=True)
time=np.load('timenonrecrmax2.npy',allow_pickle=True)
ticks=np.arange(0,len(time))
plot=False
if plot==True:
    plt.figure(figsize=(12,9))
    for i in range(len(lines)-1):
        plt.plot(lines[i][:,0],lines[i][:,1],'r')
    plt.plot(lines[-1][:,0],lines[-1][:,1],'r',label='Streamline')
    plt.scatter(edgepoints[:,0],edgepoints[:,1],label='Edge of object')
    plt.legend()
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.savefig('Figures/linesnonrecgrid2')
    plt.show()


    plt.figure()
    plt.xlabel('Iteration [-]')
    plt.ylabel('Time elapsed [s]')
    plt.plot(ticks,time)
    plt.savefig('Figures/timenonrecgrid2')
    plt.show()
print('t',len(ticks))
print(max(time))
