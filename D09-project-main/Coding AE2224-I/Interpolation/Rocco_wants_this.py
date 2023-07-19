from Official_Slicing_Intersection import mask,XC,YC,ud,vd,path_to_data
import numpy as np
step_to_take = 143
mask = mask[::step_to_take]
XC = XC[::step_to_take]
YC = YC[::step_to_take]
ud = ud[::step_to_take]
vd = vd[::step_to_take]


sliceset = np.column_stack([XC,YC,ud,vd,mask])
print(sliceset)


data = np.column_stack((XC,YC,ud,vd,mask))

sliceset = np.column_stack([XC,YC,ud,vd,mask])
print(sliceset.shape)

csvfilename = 'slicetointegrate.csv'
header = 'X,Y,U,V,rho' #this is the last one
np.savetxt(path_to_data + csvfilename, data, delimiter=',', header=header, comments='')



print(sliceset)