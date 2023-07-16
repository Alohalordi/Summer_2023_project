import pyvista as pv
import os

data_dir = os.path.dirname(__file__)

mesh = pv.read(data_dir + "/DesignIsoSmooth.obj")

n_slices_z = 60  #change to a higher number for more slices
slices = mesh.slice_along_axis(n=n_slices_z, axis="z")

p = pv.Plotter()
p.add_mesh(slices, color="k")
# p.add_axes_at_origin()
p.show_bounds(font_size= 10, show_xaxis=True, show_yaxis=True, show_zaxis=True, show_xlabels=True, show_ylabels=True, show_zlabels=True, xlabel='X Axis' , ylabel='Y Axis', zlabel='Z Axis', location='origin', color="k")

p.set_background(color = "w")
# p.add_camera_orientation_widget()


p.show()
print("done")