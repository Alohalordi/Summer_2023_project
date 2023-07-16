import numpy as np
import pandas as pd

import scipy.interpolate as interpolate
import matplotlib.pyplot as plt

import os


#read csv file
df2 = pd.read_csv('Data/CSV_Final_Field_Vectors.csv')
dataframe2 = df2.to_numpy()

#frame the data                 3D array of 95x59x36 & for each u,v,w vectors
XC = dataframe2[:,0]
YC = dataframe2[:,1]
ZC = dataframe2[:,2]
ud = dataframe2[:,3]
vd = dataframe2[:,4]
wd = dataframe2[:,5]

#Here the forming of the original 3D vector field starts
#Define the sizes of the axes
xsize = 95
ysize = 59
zsize = 36


#Create all the points on the axes to later make a 3D grid
xi = np.linspace(XC.min(), XC.max(), xsize)
yi = np.linspace(YC.min(), YC.max(), ysize)
zi = np.linspace(ZC.min(), ZC.max(), zsize)

#Create the meshgrid of all known datapoints
X, Y, Z= np.meshgrid(xi, yi, zi, indexing= 'ij')

#Assign all vectorvalues to the grid points by interpolating to the nearest point, but only on the existing data points
#Might be a better way to do this but we have not found it yet
U = interpolate.griddata((XC, YC, ZC), ud, (X, Y, Z), method='nearest')
V = interpolate.griddata((XC, YC, ZC), vd, (X, Y, Z), method='nearest')
W = interpolate.griddata((XC, YC, ZC), wd, (X, Y, Z), method='nearest')

#Here the interpolation begins, in order to add more points in the Z direction
#Create new Z axis
zi_axis = np.linspace(1, 36, 72) # The last number in this sequence is the number of points you want in the X direction (maintaining the height)

#Define the interpolation functions for the u,v and w components, only in the Z direction
interp_u = interpolate.interp1d(zi, U, axis=2, kind='linear', fill_value="extrapolate")
interp_v = interpolate.interp1d(zi, V, axis=2, kind='linear', fill_value="extrapolate")
interp_w = interpolate.interp1d(zi, W, axis=2, kind='linear', fill_value="extrapolate")

#The interpolated values of the u, v and w components of the vectors (with the new z axis)
u_interp = interp_u(zi_axis)
v_interp = interp_v(zi_axis)
w_interp = interp_w(zi_axis)

#Create the new meshgrid containing the new z axis
X_new, Y_new, Z_new = np.meshgrid(xi, yi, zi_axis, indexing= 'ij')

#The dimensions you want to see in the figure
dimx = 3
dimy = 3
dimz = 5
dimz2 = dimz*2

#Creating the figure containing both vectorfields in different colors, to check if the interpolation went well
fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')

ax2.quiver(X[:dimx,:dimy,:dimz], Y[:dimx,:dimy,:dimz], Z[:dimx,:dimy,:dimz], U[:dimx,:dimy,:dimz], V[:dimx,:dimy,:dimz], W[:dimx,:dimy,:dimz], length=0.3, normalize=True, color='r')
ax2.quiver(X_new[:dimx,:dimy,:dimz2], Y_new[:dimx,:dimy,:dimz2], Z_new[:dimx,:dimy,:dimz2], u_interp[:dimx,:dimy,:dimz2], v_interp[:dimx,:dimy,:dimz2], w_interp[:dimx,:dimy,:dimz2], length=0.3, normalize=True, color='g')
plt.show()

current_dir = os.getcwd()
path_to_fig = current_dir + '/Figures/'
figurename2 = "Interpolatedfigure.png"
plt.savefig(path_to_fig + figurename2) n