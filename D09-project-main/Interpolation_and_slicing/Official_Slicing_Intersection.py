#worked on by Gabo and Alvaro and thijmen v2

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
df = pd.read_csv(path_to_data + "/FinalOutputinterpolatedata.csv")  # then we were using "/FinalOutputinterpolatedata.csv"    # first we were using "/Vector_field_to_edit_stuff.csv")
vector_df = df.to_numpy()


def sCale(mesh, vertices_np, X_intp, Y_intp, Z_intp):

    vertices_x, vertices_y, vertices_z = vertices_np[:,0], vertices_np[:,1], vertices_np[:,2]

    Ob_xMax = max(vertices_x)
    Ob_yMax = max(vertices_y)
    Ob_zMax = max(vertices_z)
    Ob_xMin = min(vertices_x)
    Ob_yMin = min(vertices_y)
    Ob_zMin = min(vertices_z)

    Ob_X_len = Ob_xMax - Ob_xMin  
    Ob_Y_len = Ob_yMax - Ob_yMin  
    Ob_Z_len = Ob_zMax - Ob_zMin  

    mesh_t = mesh.translate([-Ob_xMin,-Ob_yMin,-Ob_zMin], inplace=True)

    maxvector_xc = np.max(X_intp)
    maxvector_yc = np.max(Y_intp)
    maxvector_zc = np.max(Z_intp)

    ratioX = Ob_X_len / maxvector_xc
    ratioY = Ob_Y_len / maxvector_yc
    ratioZ = Ob_Z_len / maxvector_zc

    X_sc = X_intp*ratioX
    Y_sc = Y_intp*ratioY
    Z_sc = Z_intp*ratioZ

    return X_sc, Y_sc, Z_sc, mesh_t

def inTersection(X_sc, Y_sc, Z_sc, mesh_t):
    x_coord = X_sc.reshape(-1,1)
    y_coord = Y_sc.reshape(-1,1)
    z_coord = Z_sc.reshape(-1,1)
    Coord_array = np.hstack((x_coord,y_coord,z_coord))

    Coord_poly = pv.PolyData(Coord_array)
    select = Coord_poly.select_enclosed_points(mesh_t)
    inside = select.threshold(0.5)

    inside_points_poly = inside.GetPoints().GetData()
    inside_points_np = np.array(inside_points_poly)

    
    Coord_array_string:np.array = np.array([",".join(item) for item in Coord_array.astype(str)])
    inside_points_array_string:np.array = np.array([",".join(item) for item in inside_points_np.astype(str)])

    #Compare the two
    density:np.array = np.isin(Coord_array_string, inside_points_array_string)*1

    return density

def geTOneslice(num_slice, X_sc, Y_sc, U_intp, V_intp, density, z_def):
    step = z_def
    X_sc_slc = X_sc[num_slice::step]
    Y_sc_slc = Y_sc[num_slice::step]
    U_intp_slc = U_intp[num_slice::step]
    V_intp_slc = V_intp[num_slice::step]
    density_slc = density[num_slice::step]

    return X_sc_slc, Y_sc_slc, U_intp_slc, V_intp_slc, density_slc

def eXportcsv(X_sc_slc, Y_sc_slc, U_intp_slc, V_intp_slc, density_slc, proceed=False, csvfilename='outputCSV.csv', header= ("X, Y, u, v, rho       #Comment")):
    test = 0
    if proceed:
        data = np.column_stack((X_sc_slc, Y_sc_slc, U_intp_slc, V_intp_slc, density_slc))
        np.savetxt(path_to_data + csvfilename, data, delimiter=',', header=header, comments='')


def eXportcsv_allslices(X_sc, Y_sc, U_intp, V_intp, density, z_def, path_to_Entire_layers_folder, proceed=False):
    num_slice = 0
    if proceed:
        for i in range(z_def-62):
            
            X_sc_slc, Y_sc_slc, U_intp_slc, V_intp_slc, density_slc = geTOneslice(num_slice, X_sc, Y_sc, U_intp, V_intp, density, z_def)
                        
            data = np.column_stack((X_sc_slc, Y_sc_slc, U_intp_slc, V_intp_slc, density_slc))
            layercsvfilename = f"Entire_layer0_5resolution{num_slice+1}.csv"
            layerheader= (f"X, Y, u, v, rho       # first attempt in obtaining all the layers. Specific layer {num_slice+1}")
            np.savetxt(path_to_Entire_layers_folder + layercsvfilename, data, delimiter=',', header=layerheader, comments='')
            print(f"slice number {num_slice+1} succesfully saved")
            num_slice += 1



if __name__ == '__main__':

    print("this file is still running")
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





    # VECTOR FIELD HANDLING ------------------------------------------------------------------------------------------------
    vector_xc = vector_df[:,0]
    vector_yc = vector_df[:,1]
    vector_zc = vector_df[:,2]
    vector_ud = vector_df[:,3]
    vector_vd = vector_df[:,4]
    vector_wd = vector_df[:,5]

    # print("Length of initial dataset")
    # print(vector_xc.shape)
    # print(vector_yc.shape)

    #Max values
    maxvector_xc = max(vector_xc)
    maxvector_yc = max(vector_yc)
    maxvector_zc = max(vector_zc)

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


    # Intersection --------------------------------------------------------------------------------------------------------------

    #Obtain numpy array of floats coordinates
    x_coord = XC.reshape(-1,1)
    y_coord = YC.reshape(-1,1)
    z_coord = ZC.reshape(-1,1)
    coordinate_array = np.hstack((x_coord,y_coord,z_coord))  #shape = (397955, 3)

    # Transform it into pv.PolyData object to check whether they are inside or outside of the GE bracket object (another pv object)
    # Hence it becomes a list of points in the domain of pv
    points_poly = pv.PolyData(coordinate_array)

    # Sort the list of points depending on whether they are inside or outside of the GE bracket object 
    select = points_poly.select_enclosed_points(mesh)
    inside = select.threshold(0.5)
    outside = select.threshold(0.5, invert=True)
    inside_points = inside.GetPoints().GetData()

    # Tranform list of points inside back to numpy
    inside_points_np = np.array(inside_points)  # shape = (23688, 3)
    # print("lululululul",inside_points_np[:200])

    # Plot and visualize the mesh
    # p = pv.Plotter()
    # p.set_background(color = "w")
    # # p.add_mesh(mesh)

    # # p.add_mesh(slice, color="k")
    # # p.add_mesh(trialslice, color="k")
    # p.show_bounds(color="k")
    # # p.save_graphic(".png", title='Slice of GEbraket')

    # p.add_mesh(inside)
    # p.show()


    # Transform both numpy arrays into a list of string arrays, where each item is a 
    coordinate_array_string:list = [",".join(item) for item in coordinate_array.astype(str)]    # length = 397955
    inside_points_lst:list = [",".join(item) for item in inside_points_np.astype(str)]          # length = 23688

    # print(len(coordinate_array_string))

    # Convert to numpy
    coordinate_array_string:np.array = np.array(coordinate_array_string)
    inside_points_lst:np.array = np.array(inside_points_lst)

    # Create the mask
    mask:np.array = np.isin(coordinate_array_string, inside_points_lst)     # shape = (397955,)   number of Trues = 23688

    #Changes boolean results to ones and zeros
    mask = mask #*1     ===================================================this was also changed for the defining, include the *1 if we want to get the 0 and 1s
    
    inside_puntitos = inside.points
    # print(inside_puntitos.shape)
    # print(inside_puntitos[:50,2])
    
    # # Plot and visualize the mesh
    # p = pv.Plotter()
    # p.set_background(color = "w")
    # # # p.add_mesh(mesh)
    # # # p.add_mesh(slice, color="k")
    # # # p.add_mesh(trialslice, color="k")
    # p.show_bounds(color="k")
    # # # p.save_graphic(".png", title='Slice of GEbraket')
    # p.add_mesh(inside)
    # p.show()

    # print("Length of middle dataset")
    # print(len(XC))
    # print(len(YC))
    print("done")

    save = False
    if save:
        step = 71
        start = 39
        XC = XC[start::step]
        YC = YC[start::step]
        ud = ud[start::step]
        vd = vd[start::step]
        mask = mask[start::step]
        
        # print("Length of final dataset")
        # print(XC.shape)
        # print(YC.shape)

        data = np.column_stack((XC, YC, ud, vd, mask,))
        csvfilename = 'slicecontaining_big_area.csv'
        header = 'X, Y, u, v, rho   #this code contains another slice of the object'
        np.savetxt(path_to_data + csvfilename, data, delimiter=',', header=header, comments='')



    start = 39
    step = 71

    XC = XC[start::step]
    YC = YC[start::step]
    mask = mask[start::step]
    print(mask[:200])
    print(XC.shape)
    z = np.ones((5605, 1))

    slicethimenwants = np.column_stack((XC[mask], YC[mask], z[mask]))

    Slicethimenwants_poly = pv.PolyData(slicethimenwants)


    # Plot and visualize the mesh
    p = pv.Plotter()
    p.set_background(color = "w")
    # # p.add_mesh(mesh)
    # # p.add_mesh(slice, color="k")
    # # p.add_mesh(trialslice, color="k")
    p.show_bounds(color="k")
    # # p.save_graphic(".png", title='Slice of GEbraket')
    p.add_mesh(Slicethimenwants_poly, color = "k")
    p.show()