import numpy as np
import pandas as pd
from scipy.interpolate import interp1d, RegularGridInterpolator


#read csv file
df2 = pd.read_csv('Formatted_Field_Vectors_CSV')
dataframe2 = df.to_numpy()

#frame the data
XC = dataframe2[:,0]
YC = dataframe2[:,1]
ZC = dataframe2[:,2]
ud = dataframe2[:,3]
vd = dataframe2[:,4]
wd = dataframe2[:,5]

#Interpolating function for the u, v and w components

interp_u = interp1d(ZC, u[:,:,:], kind='cubic')
interp_v = interp1d(ZC, v[:,:,:], kind='cubic')
interp_w = interp1d(ZC, w[:,:,:], kind='cubic')

#Create new points in the Z direction

N = 72 #number of points wanted in the z-direction
ZC_new = np.linspace(0, 36, N)

#Create new vectors at the new points
ud_new = interp_u(ZC_new)
vd_new = interp_v(ZC_new)
wd_new = interp_w(ZC_new)

#Create new vector field
New_Field = np.stack([ud_new, vd_new, wd_new])