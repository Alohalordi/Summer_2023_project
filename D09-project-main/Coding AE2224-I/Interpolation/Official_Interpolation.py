import numpy as np
import pandas as pd
import scipy.interpolate as interpolate
import os

#read csv file
current_dir = os.getcwd()
data_dir = os.path.dirname(__file__)
path_to_data = data_dir.replace("\Interpolation_and_slicing", "") + '/Data/'
print("erer" + data_dir)
# df2 = pd.read_csv(current_dir + '/D09-project/Data/CSV_Final_Field_Vectors.csv')
df2 = pd.read_csv(path_to_data + "/CSV_Final_Field_Vectors.csv")
dataframe2 = df2.to_numpy()

def getmeshgrid(XC, YC, ZC, ud, vd, wd):

    xsize = int(XC.max())
    ysize = int(YC.max())
    zsize = int(ZC.max())

    xi = np.linspace(XC.min(), XC.max(), xsize)
    yi = np.linspace(YC.min(), YC.max(), ysize)
    zi = np.linspace(ZC.min(), ZC.max(), zsize)

    X, Y, Z= np.meshgrid(xi, yi, zi, indexing= 'ij')

    print("Starting interpolation...")
    U = interpolate.griddata((XC, YC, ZC), ud, (X, Y, Z), method='nearest')
    V = interpolate.griddata((XC, YC, ZC), vd, (X, Y, Z), method='nearest')
    W = interpolate.griddata((XC, YC, ZC), wd, (X, Y, Z), method='nearest')
    print("Finished")
    return X, Y, Z, U, V, W, xi, yi, zi

#frame the data 
XC = dataframe2[:,0]
YC = dataframe2[:,1]
ZC = dataframe2[:,2]
ud = dataframe2[:,3]
vd = dataframe2[:,4]
wd = dataframe2[:,5]

X, Y, Z, U, V, W, xi, yi, zi = getmeshgrid(XC, YC, ZC, ud, vd, wd)


#Step size in between new values of interpolation
stepsize = 0.5
zi_axis = np.arange(1.0, 36.0 + stepsize, stepsize)

interp_u = interpolate.interp1d(zi, U, axis=2, kind='linear', fill_value="extrapolate")
interp_v = interpolate.interp1d(zi, V, axis=2, kind='linear', fill_value="extrapolate")
interp_w = interpolate.interp1d(zi, W, axis=2, kind='linear', fill_value="extrapolate")

u_interp = interp_u(zi_axis)
v_interp = interp_v(zi_axis)
w_interp = interp_w(zi_axis)

X_new, Y_new, Z_new = np.meshgrid(xi, yi, zi_axis, indexing= 'ij')

save = False
if save:
    x_out = X_new.flatten()
    y_out = Y_new.flatten()
    z_out = Z_new.flatten()
    u_out = u_interp.flatten()
    v_out = v_interp.flatten()
    w_out = w_interp.flatten()

    data = np.column_stack((x_out, y_out, z_out, u_out, v_out, w_out))

    # current_dir = os.getcwd()
    # data_dir = os.path.dirname(__file__)
    # path_to_Data = current_dir + '/D09-project/Data/'
    # path_to_data = data_dir.replace("\Interpolation_and_slicing", "") + '/Data/'

    data_dir = os.path.dirname(__file__)
    path_to_data = data_dir.replace("\Interpolation_and_slicing", "") + '/Data/'
    csvfilename = 'FinalOutputinterpolatedata.csv'
    header = 'X,Y,Z,u,v,w   #this is the last one'
    np.savetxt(path_to_data + csvfilename, data, delimiter=',', header=header, comments='')

print(True*True)
print(False*True)