import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, RegularGridInterpolator
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

#read csv file
df2 = pd.read_csv('D09-project/Data/CSV_Final_Field_Vectors.csv')
dataframe2 = df2.to_numpy()
 
# print(df2[:50,0])
#frame the data                 3D array of 95x59x36 & for each u,v,w vectors
XC = dataframe2[:,0]
YC = dataframe2[:,1]
ZC = dataframe2[:,2]
ud = dataframe2[:,3]
vd = dataframe2[:,4]
wd = dataframe2[:,5]

xsize = 95
ysize = 59
zsize = 36

xi = np.linspace(XC.min(), XC.max(), xsize)
yi = np.linspace(YC.min(), YC.max(), ysize)
zi = np.linspace(ZC.min(), ZC.max(), zsize)

X, Y, Z= np.meshgrid(xi, yi, zi, indexing= 'ij')

print("Starting interpolation...")
U = interpolate.griddata((XC, YC, ZC), ud, (X, Y, Z), method='nearest')  # it does work 
V = interpolate.griddata((XC, YC, ZC), vd, (X, Y, Z), method='nearest')  # it does work 
W = interpolate.griddata((XC, YC, ZC), wd, (X, Y, Z), method='nearest')  # it does work 
print("Finished")

# print("The values for the point should be (-0.46656,0.8832,0.047692), and they are", U[5,1,2], V[5,1,2], W[5,1,2])  #remember the indexing or np.array starts from 0, so take this into account
# print("shape: ",X.shape)
# print(X)
# print("first 20 of X", X[:20].shape)
# print("Y is ", Y)
# print("first 20 of y ", Y[:20][:20].shape)


#THESE ARE THE ONES THAT WORK
#dimensions to be plotted
dimx = 5
dimy = 5
dimz = 5
dimz2 = dimz*2
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X[:dimx,:dimy,:dimz], Y[:dimx,:dimy,:dimz], Z[:dimx,:dimy,:dimz], U[:dimx,:dimy,:dimz], V[:dimx,:dimy,:dimz], W[:dimx,:dimy,:dimz], length=0.3, normalize=True)
# ax.quiver(X[:20,:20,:20], Y[:20,:20,:20], Z[:20,:20,:20], U[:20,:20,:20], V[:20,:20,:20], W[:20,:20,:20], length=0.1, normalize=True)
# ax.quiver(X[:20][:20][:20], Y[:20][:20][:20], Z[:20][:20][:20], U[:20][:20][:20], V[:20][:20][:20], W[:20][:20][:20], length=0.1, normalize=True)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


current_dir = os.getcwd()
path_to_fig = current_dir + '/D09-project/Figures/'
figurename = "currentfigure.png"
plt.savefig(path_to_fig + figurename)
# plt.show()


# from chattie GPT ↓↓↓↓↓↓↓
  # the original z-coordinates     are zi
# zi_axis = np.linspace(1.0, 36.0, 72) # the new z-coordinates with double the number of points.....  np.around(np.linspace(1, 36, 72), 1)

stepsize = 0.5

zi_axis = np.arange(1.0, 36.0 + stepsize, stepsize) # the new z-coordinates with double the number of points.....  np.around(np.linspace(1, 36, 72), 1)


zi_axis = np.arange(1.0, 36.02, 0.2)    


interp_u = interpolate.interp1d(zi, U, axis=2, kind='linear', fill_value="extrapolate")
interp_v = interpolate.interp1d(zi, V, axis=2, kind='linear', fill_value="extrapolate")
interp_w = interpolate.interp1d(zi, W, axis=2, kind='linear', fill_value="extrapolate")

u_interp = interp_u(zi_axis)
v_interp = interp_v(zi_axis)
w_interp = interp_w(zi_axis)


X_new, Y_new, Z_new = np.meshgrid(xi, yi, zi_axis, indexing= 'ij')

# print("u_interp", u_interp, u_interp.shape, type(u_interp))
# print("z_new ", Z_new, Z_new.shape)

#k = 1.0
#V = V - k


fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
zindextobeplotted = 1
ax2.quiver(X[:dimx,:dimy,:dimz], Y[:dimx,:dimy,:dimz], Z[:dimx,:dimy,:dimz], U[:dimx,:dimy,:dimz], V[:dimx,:dimy,:dimz], W[:dimx,:dimy,:dimz], length=0.01, normalize=True, color='r')
#ax2.quiver(X_new[:dimx,:dimy,:dimz2], Y_new[:dimx,:dimy,:dimz2], Z_new[:dimx,:dimy,:dimz2], u_interp[:dimx,:dimy,:dimz2], v_interp[:dimx,:dimy,:dimz2], w_interp[:dimx,:dimy,:dimz2], length=0.3, normalize=True, color='g')
# ax2.quiver(X_new[:dimx,:dimy,zindextobeplotted ], Y_new[:dimx,:dimy,zindextobeplotted ], u_interp[:dimx,:dimy, zindextobeplotted ], v_interp[:dimx,:dimy, zindextobeplotted], length=0.3, normalize=True, color='b')
figurename2 = "2DInterpolatedfigure.png"
plt.savefig(path_to_fig + figurename2)
plt.show()




save = False
if save:
    x_out = X_new.flatten()
    y_out = Y_new.flatten()
    z_out = Z_new.flatten()
    u_out = u_interp.flatten()
    v_out = v_interp.flatten()
    w_out = w_interp.flatten()

    data = np.column_stack((x_out, y_out, z_out, u_out, v_out, w_out))
    header = 'X,Y,Z,u,v,w'
    np.savetxt('outputinterpolatedataV2.csv', data, delimiter=',', header=header, comments='')

# meshgrid3D_new = np.zeros((95, 59, 72, 3))
# X, Y, Z = np.meshgrid(xi, yi, z_new, indexing='ij')
# meshgrid3D_new[:, :, :] = np.stack((X, Y, Z), axis=-1)

# meshgrid3D_new[:, :, :, 0] = u_interp
# meshgrid3D_new[:, :, :, 1] = v_interp
# meshgrid3D_new[:, :, :, 2] = w_interp

# print(meshgrid3D_new.shape)
# U = np.zeros_like(X)
# V = np.zeros_like(Y)
# W = np.zeros_like(Z)

# for i in range(len(X)):
#     for j in range(len(Y)):
#         for k in range(len(Z)):
#             mask = (X[i,j,k]==xi) & (Y[i,j,k]==yi) & (Z[i,j,k]==zi)
#             if mask.any():
#                 U[i,j,k] = u[mask][0]
#                 V[i,j,k] = v[mask][0]
#                 W[i,j,k] = w[mask][0]

# print(type(U), shape(U), size(U))

# X, Y, Z = np.meshgrid(XC, YC, ZC)
# #Interpolating function for the u, v and w components

# interp_u = interp1d(ZC, ud[:,:,:], kind='cubic')
# interp_v = interp1d(ZC, vd[:,:,:], kind='cubic')
# interp_w = interp1d(ZC, wd[:,:,:], kind='cubic')

# #Create new points in the Z direction

# N = 72 #number of points wanted in the z-direction
# ZC_new = np.linspace(0, 36, N)

# #Create new vectors at the new points
# ud_new = interp_u(ZC_new)
# vd_new = interp_v(ZC_new)
# wd_new = interp_w(ZC_new)

# #Create new vector field
# New_Field = np.stack([ud_new, vd_new, wd_new])

# print(New_Field)






#links to check
# https://www.sharpsightlabs.com/blog/numpy-meshgrid/ 
# https://www.geeksforgeeks.org/numpy-meshgrid-function/ 

