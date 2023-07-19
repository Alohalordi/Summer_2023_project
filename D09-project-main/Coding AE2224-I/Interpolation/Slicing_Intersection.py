#worked on by Gabo and Alvaro

import numpy as np
import pyvista as pv
from matplotlib import pyplot as plt
import os
import pandas as pd
from Official_Interpolation import getmeshgrid


data_dir = os.path.dirname(__file__)
# print("datadirrr" + data_dir)
current_dir = os.getcwd()
print(current_dir)
path_to_data = data_dir.replace("\Interpolation_and_slicing", "") + '/Data/DesignIsoSmooth.obj'

# load the OBJ file
mesh = pv.read(path_to_data)

#Get vertices
vertices = mesh.points
vertices_np = np.array(vertices.copy())

#Getting 1D arrays each containing the x, y, z coordinates of all points
vertices_x = vertices_np[:,0]
vertices_y = vertices_np[:,1]
vertices_z = vertices_np[:,2]

#Identify boundaries
# print("xMax is: ", max(vertices_x), "\nxMin is: ", min(vertices_x))
# print("yMax is: ", max(vertices_y), "\nyMin is: ", min(vertices_y))
# print("zMax is: ", max(vertices_z), "\nzMin is: ", min(vertices_z))
xMax = max(vertices_x)
yMax = max(vertices_y)
zMax = max(vertices_z)
xMin = min(vertices_x)
yMin = min(vertices_y)
zMin = min(vertices_z)

#Scale and translate the mesh
mesh = mesh.translate([-xMin,-yMin,-zMin], inplace=True)
vertices_t = mesh.points
vertices_t_np = np.array(vertices_t.copy())

#Getting 1D arrays each containing the x_t, y_t, z_t coordinates of all points
vertices_x_t = vertices_t_np[:,0]
vertices_y_t = vertices_t_np[:,1]
vertices_z_t = vertices_t_np[:,2]

#Identify new bounds after translation
xMax_t = max(vertices_x_t)   #172.84087
yMax_t = max(vertices_y_t)
zMax_t = max(vertices_z_t)

xMin_t = min(vertices_x_t)
yMin_t = min(vertices_y_t)
zMin_t = min(vertices_z_t)

#Slicing of the mesh
slice = mesh.slice(normal=[0, 0, 1])
n_slices_z = 5  #change to a higher number for more slices
slices = mesh.slice_along_axis(n=n_slices_z, axis="z")
# mesh.intersect_with_plane(origin, normal)
trialslice = slices[0]

# Plot and visualize the mesh
p = pv.Plotter()
# p.add_mesh(mesh)
# p.set_background(color = "w")
p.add_mesh(trialslice, color="k")
# p.add_mesh(slices, color="k")
p.show_bounds(color="k")
# p.save_graphic(".png", title='Slice of GEbraket')
#Uncoment line below to show
#p.show()

#Important values 
Vf_x = 95
Vf_y = 59
Vf_z = 36

X_len = xMax - xMin  #172.84087
Y_len = yMax - yMin  #103.78857
Z_len = zMax - zMin  #60.3064

ratioX = X_len / Vf_x
ratioY = Y_len / Vf_y
ratioZ = Z_len / Vf_z

#Import Vector_field_to_scale.csv 
data_dir = os.path.dirname(__file__)
path_to_data = data_dir.replace("\Interpolation_and_slicing", "") + '/Data/'
df2 = pd.read_csv(path_to_data + "/Vector_field_to_edit_stuff.csv")
dataframe2 = df2.to_numpy()

#Scale the vector field to match the object
dataframe2[:,0] *= ratioX
dataframe2[:,1] *= ratioY
dataframe2[:,2] *= ratioZ

XC = dataframe2[:,0]
YC = dataframe2[:,1]
ZC = dataframe2[:,2]
ud = dataframe2[:,3]
vd = dataframe2[:,4]
wd = dataframe2[:,5]

#Plot array
X, Y, Z, U, V, W, xi, yi, zi = getmeshgrid(XC, YC, ZC, ud, vd, wd)








# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# dimx = len(X)
# dimy = len(Y)
# dimz = len(Z)
# dimz2 = dimz*2
# ax.quiver(X[:dimx,:dimy,:dimz], Y[:dimx,:dimy,:dimz], Z[:dimx,:dimy,:dimz], U[:dimx,:dimy,:dimz], V[:dimx,:dimy,:dimz], W[:dimx,:dimy,:dimz], length=0.3, normalize=True)
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()


"""
We dont use this either__

#Number of unique values in vertices_z
# z_unique = np.unique(vertices_z)
# len_unique = z_unique.size
# print("number of different z values", len_unique)
# print("zunique items are",z_unique[:40])
# print("zunique step is",z_unique[40]-z_unique[39])
# print("zunique step is",z_unique[41]-z_unique[40])
# print("zunique step is",z_unique[42]-z_unique[41])
# print("zunique step is",z_unique[43]-z_unique[42])
# print("zunique step is",z_unique[44]-z_unique[43])
#Saving the histogram of number of points per z layer, depending on amount of layers
# num_bins = 72
# plt.hist(z_unique, bins = num_bins)
# plt.title("histogram of number of points per z layer, depending on amount of layers")
# current_dir = os.getcwd()
# path_to_fig = current_dir + '/Figures/GE_bracket/'
# figurename = f"Histogrampointdensityforzlayernumofbins{num_bins}.png"
# plt.savefig(path_to_fig + figurename)
# plt.show()
"""

"""
__This we dont use anymore for now__

#list of points in the same z layer
lst_of_points = []
#Z value of slice to be plotted:
slice_z = 6.954830
#Z layer index to be plotted. (there are 58844 layers)
index_z = 0
for i in range(len(vertices_z)):
    if abs((vertices_np[i,2] - slice_z)) <= 0.0001:
        # print(vertices_np[i,:])
        lst_of_points.append(vertices_np[i,:])
# print("amount of different points for this slize_z value is: ", len(lst_of_points))
for i in range(len(lst_of_points)):
    x = lst_of_points[i][0]
    y = lst_of_points[i][1]
    plt.plot(x, y, marker="o", markersize=2, markerfacecolor="green")
# plt.show()
"""

""""
scale the vector field to match the object
horizontal slicing for the object, using pyvista. this gives the contour even when not slicing through a layer of points.
this contour layer can be used to determine whether points lie inside of it or not.
interpolate in the x and y direction so that there are enough vector fields in the x and y direction inside the coontour. 
then we use the scaled vector field, to identify which points of the 2D vector field are within the contour, and assign a 1 or a 0 for its 

links: https://github.com/marcomusy/vedo/blob/master/examples/advanced/line2mesh_tri.py

https://github.com/marcomusy/vedo/blob/master/examples/advanced/interpolate_field.py 

Notes for GG 
Object size is:
xMax is:  12.309739 
xMin is:  -160.53113
yMax is:  30.796593
yMin is:  -72.991974
zMax is:  60.972927 
zMin is:  0.666528

Vector_field_i size is:
95*59*36
"""