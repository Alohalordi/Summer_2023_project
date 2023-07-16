#worked on by Gabo and Alvaro and thijmen v2
#this is the current file for generating slices for rocco and mika

import numpy as np
import pyvista as pv
from matplotlib import pyplot as plt
import os
import pandas as pd
# from Official_Interpolation import getmeshgrid

# SETTING UP AND LOADING DATA ---------------------------------------------------------------------------------------------
#Setting up paths
data_dir = os.path.dirname(__file__)
path_to_data = data_dir.replace("\Interpolation_and_slicing", "") + '/Data/'

# Load the OBJ file
mesh = pv.read(path_to_data + '/DesignIsoSmooth.obj')

# Load Vector_field_to_edit_stuff.csv 
df = pd.read_csv(path_to_data + "/FinalOutputinterpolatedata.csv")      #before we used /Vector_field_to_edit_stuff.csv
vector_df = df.to_numpy()



# OBJECT HANDLING ---------------------------------------------------------------------------------------------
#Get vertices
vertices = mesh.points
vertices_np = np.array(vertices.copy())

#Getting 1D arrays each containing the x, y, z coordinates of points and identify boundaries
vertices_x, vertices_y, vertices_z = vertices_np[:,0], vertices_np[:,1], vertices_np[:,2]
Ob_xMax = max(vertices_x)
Ob_yMax = max(vertices_y)
Ob_zMax = max(vertices_z)
Ob_xMin = min(vertices_x)
Ob_yMin = min(vertices_y)
Ob_zMin = min(vertices_z)

# Lengths of object
Ob_X_len = Ob_xMax - Ob_xMin  #172.84087
Ob_Y_len = Ob_yMax - Ob_yMin  #103.78857
Ob_Z_len = Ob_zMax - Ob_zMin  #60.3064

#Scale and translate the mesh
mesh = mesh.translate([-Ob_xMin,-Ob_yMin,-Ob_zMin], inplace=True)
vertices_t = mesh.points
vertices_t_np = np.array(vertices_t.copy())

#Getting 1D arrays each containing the x_t, y_t, z_t coordinates of translated points and identify boundaries
vertices_x_t, vertices_y_t, vertices_z_t  = vertices_t_np[:,0], vertices_t_np[:,1], vertices_t_np[:,2]
Ob_xMax_t = max(vertices_x_t)
Ob_yMax_t = max(vertices_y_t)
Ob_zMax_t = max(vertices_z_t)
Ob_xMin_t = min(vertices_x_t)
Ob_yMin_t = min(vertices_y_t)
Ob_zMin_t = min(vertices_z_t)

#Slicing of the mesh                this was cool but not needed in the end
slice = mesh.slice(origin=[0, 0, 25], normal=[0, 0, 1])
n_slices_z = 40  #change to a higher number for more slices
slices = mesh.slice_along_axis(n=n_slices_z, axis="z")
# # mesh.intersect_with_plane(origin, normal)
# trialslice = slices[0]




#Random  points to check if it works 
# amount_of_points = 50000
# my_array = np.zeros((amount_of_points, 3))
# my_array[:, 0] = np.random.uniform(0, 170, size=(amount_of_points,))
# my_array[:, 1] = np.random.uniform(0, 110, size=(amount_of_points,))
# my_array[:, 2] = np.random.uniform(0, 60, size=(amount_of_points,))

# #Intersection
# points = [[0, 0, 0], [120, 35, 20]]
# points_poly = pv.PolyData(my_array)
# select = points_poly.select_enclosed_points(mesh)
# inside = select.threshold(0.5)
# outside = select.threshold(0.5, invert=True)
# print(select)


# Plot and visualize the mesh
p = pv.Plotter()
p.set_background(color = "w")
p.add_mesh(mesh)

# p.add_mesh(slice, color="k")
# p.add_mesh(trialslice, color="k")
p.show_bounds(color="k")
# p.save_graphic(".png", title='Slice of GEbraket')

p.add_mesh(slices[22], color = "k")
p.show()


# VECTOR FIELD HANDLING ------------------------------------------------------------------------------------------------
vector_xc = vector_df[:,0]
vector_yc = vector_df[:,1]
vector_zc = vector_df[:,2]
vector_ud = vector_df[:,3]
vector_vd = vector_df[:,4]
vector_wd = vector_df[:,5]

#Max values
maxvector_xc = np.max(vector_xc)
maxvector_yc = np.max(vector_yc)
maxvector_zc = np.max(vector_zc)

#Relevant ratios for scaling 
ratioX = Ob_X_len / maxvector_xc
ratioY = Ob_Y_len / maxvector_yc
ratioZ = Ob_Z_len / maxvector_zc

#Scale the vector field coordinates to match the object
vector_df[:,0] *= ratioX
vector_df[:,1] *= ratioY
vector_df[:,2] *= ratioZ

#Recollect all values of vectorfield
XC = vector_df[:,0]
YC = vector_df[:,1]
ZC = vector_df[:,2]
ud = vector_df[:,3]
vd = vector_df[:,4]
wd = vector_df[:,5]


#Plot array
# X, Y, Z, U, V, W, xi, yi, zi = getmeshgrid(XC, YC, ZC, ud, vd, wd)


# Intersection
x_coordinate = XC.reshape(-1,1)
y_coordinate = YC.reshape(-1,1)
z_coordinate = ZC.reshape(-1,1)

coordinate_array = np.hstack((x_coordinate,y_coordinate,z_coordinate))

print("coordinate array shape", coordinate_array.shape)

points_poly = pv.PolyData(coordinate_array)
select = points_poly.select_enclosed_points(mesh)
inside = select.threshold(0.5)
outside = select.threshold(0.5, invert=True)
# print(select)
print("type inside", type(inside))

inside_points = inside.GetPoints().GetData()
inside_points_np = np.array(inside_points)

print("inside_points shape", inside_points_np.shape)

# Plot and visualize the mesh
p = pv.Plotter()
p.set_background(color = "w")
# p.add_mesh(mesh)

# p.add_mesh(slice, color="k")
# p.add_mesh(trialslice, color="k")
p.show_bounds(color="k")
# p.save_graphic(".png", title='Slice of GEbraket')

p.add_mesh(inside)
p.show()

# MASK APPROACH
# mask = np.isin(coordinate_array, inside_points_np)
# # unified_mask = mask[:,0]*mask[:,1]*mask[:,2]          this results in boolean results
# unified_mask = np.prod(mask, axis=1)                   #this results in 0s and 1s
# print(mask.shape, unified_mask.shape)
# print(unified_mask)
# print(np.count_nonzero(unified_mask.T))

# print(mask[:,0])
# # intersect = coordinate_array[mask]
# # print(coordinate_array.shape, intersect.shape)
# # print("siuuu")
# # print(False in mask)  #the answer was true

# print(np.count_nonzero(mask))



# thijmen approach
# mask = np.zeros((coordinate_array.shape[0],1), dtype=int)
# indices = np.where(np.all(coordinate_array == inside_points_np[:, np.newaxis], axis=2))
# mask[indices, 0] = 1
# new_array = np.concatenate((coordinate_array, mask), axis=1)
# print(new_array.shape)



#new approach using strings

# coordinate array
# coordinate_array_string = str(coordinate_array[:,0]) + str(coordinate_array[:,1]) + str(coordinate_array[:,2]) this doesn't work 
coordinate_array_string = [",".join(item) for item in coordinate_array.astype(str)]
inside_points_lst = [",".join(item) for item in inside_points_np.astype(str)]

print("len coordinate_array_string", len(coordinate_array_string))
print("len inside_points", len(inside_points_lst))

coordinate_array_string = np.array(coordinate_array_string)
inside_points_lst = np.array(inside_points_lst)

mask = np.isin(coordinate_array_string, inside_points_lst)

#Changes boolean results to ones and zeros
mask = mask*1

print("mask ", mask)
print("mask shape", mask.shape)
print("number of trues in mask", np.count_nonzero(mask))   #FUCK YEAHHHHJHHHH



