# #file 

# import numpy as np
# import pyvista as pv
# from matplotlib import pyplot as plt
# import os
# from Official_Interpolation import u_interp, v_interp, w_interp, X_new, Y_new, Z_new

# current_dir = os.getcwd()
# print(current_dir)
# path_to_data = current_dir + '/D09-project/Data/DesignIsoSmooth.obj'

# # load the OBJ file
# mesh = pv.read(path_to_data)

import pyvista as pv
import numpy as np
import os
import pandas as pd
from matplotlib import pyplot as plt

data_dir = os.path.dirname(__file__)
path_to_data = data_dir.replace("\Interpolation_and_slicing", "") + '/Data/'
path_to_Entire_layers_folder = path_to_data + 'Entire_layers/'

from Global_file import X_sc, Y_sc, Z_sc, U_intp, V_intp, W_intp, density

density = density.astype(np.bool)

X_sc = X_sc[density]
Y_sc = Y_sc[density]
Z_sc = Z_sc[density]
U_intp = U_intp[density]
V_intp = V_intp[density]
W_intp = W_intp[density]



fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

ax.quiver(X_sc, Y_sc, Z_sc, U_intp, V_intp, W_intp, length=2.5, normalize=True)

plt.show()