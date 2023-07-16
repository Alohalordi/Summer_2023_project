# File containing all the functions needed do load, scale, intersect, and slice the GE bracket and Vector field. 
# This is the only file that should be run, it imports functions defined in otherdirectionsOfficial_Interpolation_2, and 
# Official_Slicing_Intersection_2

# The input for this part of the code is a csv file containing the vector field, and a object file containing the GE bracket model. (these can be found in Data_2 folder)
# The output for this part of the code is a csv file containing the interpolated vector field, appended with an extra colum which 
# specifies a density (either 0 or 1) to each point if they are outside or inside of the object. (these can be found in Data_2/Entire_layers_2 folder)

#import packages
import pyvista as pv
import numpy as np
import os

#import other python files
from otherdirectionsOfficial_Interpolation_2 import inTerPolation
from Official_Slicing_Intersection_2 import sCale, inTersection, geTOneslice, eXportcsv, eXportcsv_allslices
import pandas as pd


#Setting up paths for reading data
data_dir = os.path.dirname(__file__)
path_to_data = data_dir.replace("\Interpolation_Intersection_Slicing", "") + "\Data_2"
path_to_Entire_layers_folder = path_to_data + '\Entire_layers_2/'


#Load the vectorfield data
df = pd.read_csv(path_to_data + "\CSV_Final_Field_Vectors.csv")
dataframe = df.to_numpy()


print(data_dir)
print(path_to_data)
print(path_to_Entire_layers_folder)


#Load the OBJ file
mesh = pv.read(path_to_data + '\DesignIsoSmooth.obj')


#Data handling
#frame the vector field data
XC = dataframe[:,0]
YC = dataframe[:,1]
ZC = dataframe[:,2]
ud = dataframe[:,3]
vd = dataframe[:,4]
wd = dataframe[:,5]

#Get vertices from object
vertices = mesh.points
vertices_np = np.array(vertices.copy())







#INPUT FROM THE USER:
#==============================================================================================================================
#==============================================================================================================================
#What new resolution for the vectorfield do you want? (multiplication of the original resolution for the three axes) (must be integer)
x_mult = 1
y_mult = 1
z_mult = 2


#Slice to obtain
num_slice = 39   #has to be in the range of the resolution in z direction


#Saving 
proceed = True
# csvfilename='For_our_6final_trickoutputCSV.csv'
header= ("X, Y, u, v, rho       # Resolution augmented x5 in de x and y directions")

#==============================================================================================================================
#==============================================================================================================================






#Definition of the resolution
x_res = 95 * x_mult
y_res = 59 * y_mult
z_res = 36 * z_mult

new_resolution = (x_res, y_res, z_res)
#Call interpolating function

Interpolated_Field = inTerPolation(XC, YC, ZC, ud, vd, wd, new_resolution)
print("Interpolation Finished!")
X_intp, Y_intp, Z_intp, U_intp, V_intp, W_intp = Interpolated_Field

print("amount of points in cube", X_intp.shape, Y_intp.shape, Z_intp.shape)


X_sc, Y_sc, Z_sc, mesh_t = sCale(mesh, vertices_np, X_intp, Y_intp, Z_intp)
print("sCaled successfully!")

density = inTersection(X_sc, Y_sc, Z_sc,mesh_t)
print("inTersected successfully!")


X_sc_slc, Y_sc_slc, U_intp_slc, V_intp_slc, density_slc = geTOneslice(num_slice, X_sc, Y_sc, U_intp, V_intp, density, z_def=new_resolution[2])
print("getOneslice successful")

print("amount of points in one slice", X_sc_slc.shape, Y_sc_slc.shape)

# eXportcsv(X_sc_slc, Y_sc_slc, U_intp_slc, V_intp_slc, density_slc, proceed, csvfilename, header)
# print("eXporting csv successful")

z_def=new_resolution[2]
eXportcsv_allslices(X_sc, Y_sc, U_intp, V_intp, density, z_def, path_to_Entire_layers_folder, proceed=True)
