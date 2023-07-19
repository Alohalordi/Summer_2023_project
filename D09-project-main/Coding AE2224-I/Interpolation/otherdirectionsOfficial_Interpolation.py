import numpy as np
import pandas as pd
import scipy.interpolate as interpolate
import os
import matplotlib.pyplot as plt


def inTerPolation(XC, YC, ZC, ud, vd, wd, new_resolution):

    #Original sizes of the vectorfield
    xsize = int(XC.max())
    ysize = int(YC.max())
    zsize = int(ZC.max())

    #All points in the original field
    xi = np.linspace(XC.min(), XC.max(), xsize)
    yi = np.linspace(YC.min(), YC.max(), ysize)
    zi = np.linspace(ZC.min(), ZC.max(), zsize)

    #original grid
    X1, Y1, Z1= np.meshgrid(xi, yi, zi, indexing = 'ij')

    #Assigning all vectorvalues to the field
    #print("Starting interpolation...")
    U = interpolate.griddata((XC, YC, ZC), ud, (X1, Y1, Z1), method='nearest')
    V = interpolate.griddata((XC, YC, ZC), vd, (X1, Y1, Z1), method='nearest')
    W = interpolate.griddata((XC, YC, ZC), wd, (X1, Y1, Z1), method='nearest')
    #print("Finished")
    #yeah
    #Some definitions for the interpolation
    orig_grid = (xi, yi, zi)
    vectors = (U, V, W)

    #The new resolution you want in the order (X, Y, Z)
    step_x = xsize / new_resolution[0] 
    step_y = ysize / new_resolution[1]  
    step_z = zsize / new_resolution[2]  



    #New grid creation
    new_X, new_Y, new_Z = np.meshgrid(np.arange(X1.min(), X1.max() + 1, step_x),     #update this later
                                        np.arange(Y1.min(), Y1.max() + 1, step_y),
                                        np.arange(Z1.min(), Z1.max() + 1, step_z))

    new_grid = (new_X, new_Y, new_Z)

    #Interpolating function
    interpolators = [interpolate.RegularGridInterpolator(orig_grid, vectors[i], method='linear', bounds_error=False, fill_value=None) for i in range(3)]

    #Creating the new vectors
    new_vectors = [interpolators[i](new_grid) for i in range(3)]

    #The new U, V and W values in the correct shape
    new_U = new_vectors[0]
    new_V = new_vectors[1]
    new_W = new_vectors[2]

    new_X = new_X.flatten()
    new_Y = new_Y.flatten()
    new_Z = new_Z.flatten()
    new_U = new_U.flatten()
    new_V = new_V.flatten()
    new_W = new_W.flatten()

    return new_X, new_Y, new_Z, new_U, new_V, new_W

if __name__ == '__main__':
    print("this file is running")
    #Read the data
    # data_dir = os.path.dirname(__file__)
    # path_to_data = data_dir.replace("\Interpolation_and_slicing", "") + '/Data/'
    # df = pd.read_csv(path_to_data + "/CSV_Final_Field_Vectors.csv")
    # dataframe = df.to_numpy()
    # new_resolution = (190, 118, 72)
    #frame the data
    # XC = dataframe[:,0]
    # YC = dataframe[:,1]
    # ZC = dataframe[:,2]
    # ud = dataframe[:,3]
    # vd = dataframe[:,4]
    # wd = dataframe[:,5]

    #print("Plotting...")
    #plotting as a check
    # dimx = 5
    # dimy = 5
    # dimz = 5
    # dimx2 = dimx*2
    # dimy2 = dimy*2
    # dimz2 = dimz*2
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # # ax.quiver(new_X[:dimx2,:dimy2,:dimz2], new_Y[:dimx2,:dimy2,:dimz2], new_Z[:dimx2,:dimy2,:dimz2], new_U[:dimx2,:dimy2,:dimz2], new_V[:dimx2,:dimy2,:dimz2], new_W[:dimx2,:dimy2,:dimz2], length=0.1, normalize=True)
    # # ax.quiver(X1[:dimx,:dimy,:dimz], Y1[:dimx,:dimy,:dimz], Z1[:dimx,:dimy,:dimz], U[:dimx,:dimy,:dimz], V[:dimx,:dimy,:dimz], W[:dimx,:dimy,:dimz], length=0.1, normalize=True, color='r')
    # ax.quiver(new_X, new_Y, new_Z, new_U, new_V, new_W, length = 0.1, normalize = True)
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    #
    # plt.show()
    # print("Plot Finished")





    # save = False
    # if save:
    #     x_out = new_X.flatten()
    #     y_out = new_Y.flatten()
    #     z_out = new_Z.flatten()
    #     u_out = new_U.flatten()
    #     v_out = new_V.flatten()
    #     w_out = new_W.flatten()
    #
    #     data = np.column_stack((x_out, y_out, z_out, u_out, v_out, w_out))
    #
    #     data_dir = os.path.dirname(__file__)
    #     path_to_data = data_dir.replace("\Interpolation_and_slicing", "") + '/Data/'
    #     csvfilename = 'Final3DInterpolatedField.csv'
    #     header = 'X,Y,Z,u,v,w   #this is the last one'
    #     np.savetxt(path_to_data + csvfilename, data, delimiter=',', header=header, comments='')''

    #First the original file goes into this one to interpolate.
    #We want a low resolution for now for low computation time. We pick 72 layers for now, s0 72 slices.
    #Then the interpolated data goes into the Slicing_intersection file, which first scales the vectorfield to the object dimensions.
    #It should scale all axes such that the edges of the object touch the edges of the vectorfield in all directions.
    #Then we slice the vector field and the object at all Z locations (in this case 0, 0.5, 1, 1.5 and so on...)
    #We put the two slices on top of each other and assign a 1 to the points inside and a O to the points outside.