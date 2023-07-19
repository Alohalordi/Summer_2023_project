
# # load the OBJ file
# mesh = Wavefront('Data/DesignIsoSmooth.obj')
# # access the vertices
# vertices = mesh.vertices
# # access the faces
# faces = mesh.mesh_list[0].faces
# print(type(vertices), len(vertices))


# import pymesh
# from pymesh.meshio import form_mesh
# from pymesh.visualization import Viewer
# # load the OBJ file
# mesh = pymesh.load_mesh('Data/DesignIsoSmooth.obj')
# # visualize the mesh
# viewer = Viewer()
# viewer.mesh = form_mesh(mesh.vertices, mesh.faces)
# viewer.show()


#Two ways of indexing np arrays
# print(vertices_np[1,1])
# print(vertices_np[1][1])


#use these links:

# https://github.com/marcomusy/vedo/tree/master/examples/volumetric 

# https://vedo.embl.es/ 

# https://github.com/marcomusy/vedo/blob/master/examples/volumetric/mesh2volume.py
