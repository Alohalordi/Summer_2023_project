#Program to identify whether a point is inside or outside of the object

#from Slicing_Intersection import trialslice
import numpy as np
import pyvista as pv
from otherdirectionsOfficial_Interpolation import new_grid

print(new_grid)


"""
Input: series of layers which contain a contour line of object, and a grid of points.

Need to come up with an algorithm to determine wether each point of the grid is inside or outside of the contour.

import points grid as X and Y from
for i in range(len(X)):
    for j in range(len(Y)):
        if point is inside:
            rho at point = 1
        else:
            rho at point = 0




Output: the grid points with 1 if inside and 0 if outside



"""