import numpy as np
from matplotlib.path import Path
import numpy as np
import pyvista as pv
from matplotlib import pyplot as plt

# load the OBJ file
mesh = pv.read('Data/DesignIsoSmooth.obj')

vertices = mesh.points
#print(type(vertices[:10]))
vertices_np = np.array(vertices.copy())
#print(type(vertices_np))

# Two ways of indexing np arrays
# print(vertices_np[1,1])
# print(vertices_np[1][1])

#print(vertices_np[:10, 2])
x_vertices = vertices_np[:, 0]
y_vertices = vertices_np[:, 1]
z_vertices = vertices_np[:, 2]

#print("xMax is: ", max(x_vertices), "\nxMin is: ", min(x_vertices))
#print("yMax is: ", max(y_vertices), "\nyMin is: ", min(y_vertices))
#print("zMax is: ", max(z_vertices), "\nzMin is: ", min(z_vertices))

# Number of unique values in z_vertices
#z_unique = np.unique(z_vertices)
#len_unique = z_unique.size
#print("number of different z values", len_unique)
# print(z_unique[:20])

# plot the mesh
p = pv.Plotter()
p.add_mesh(mesh)
# p.show()

lst_of_points = []  # list of points with z = 0.66528

# Z value of slice to be plotted:
slice_z = 16.270610
for i in range(len(z_vertices)):
    if abs((vertices_np[i, 2] - slice_z)) <= 0.0001:
        # print(vertices_np[i,:])
        lst_of_points.append(vertices_np[i, :])


x_size = 95
y_size = 59
#print("length is: ", len(lst_of_points))
xi = np.linspace(x_vertices.min(), x_vertices.max(), x_size)
yi = np.linspace(y_vertices.min(), y_vertices.max(), y_size)

# define the resolution of the grid

# create the meshgrid
X, Y = np.meshgrid(xi, yi, indexing= 'ij')

# print(lst_of_points[2][0])

for i in range(len(lst_of_points)):
    x = lst_of_points[i][0]
    y = lst_of_points[i][1]
    plt.plot(x, y, marker="o", markersize=2, markerfacecolor="green")

plt.plot(X, Y, '.', markersize = 1)

plt.show()


# create the path object from the outline points
paths = [Path(lst_of_points, codes = None) for xnew, ynew]

points = np.column_stack((X.ravel(), Y.ravel()))
inside = np.zeros(len(points), dtype=bool)
for path in paths:
    inside = np.logical_or(inside, path.contains_points(points))
np.set_printoptions(threshold=np.inf)
print(inside)

# convert boolean values to 0 or 1
#result = inside.astype(int).reshape(xx.shape)
np.set_printoptions(threshold=np.inf)
#print(result)