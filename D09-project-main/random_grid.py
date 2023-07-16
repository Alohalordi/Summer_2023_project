import numpy as np
import matplotlib.pyplot as plt

# Define the grid size and create a meshgrid
N = 20
x, y = np.meshgrid(np.arange(N), np.arange(N))

# Create a circle with a hole in the middle
r = np.sqrt((x - N/2)**2 + (y - N/2)**2)
circle = np.zeros_like(r, dtype=float)
circle[(r < 9) & (r > 6)] = 1

# Randomize the edges
edges = circle.astype(bool) & (np.random.rand(N, N) < 0)

# Create the mask by subtracting the edges from the circle
mask = circle - edges.astype(float)

# Reshape the array into a 1D array of points
points = np.vstack((x.ravel(), y.ravel(), mask.ravel())).T
points = points[points[:, 2] > 0] # Remove points inside the circle

# Plot the grid
fig, ax = plt.subplots(figsize=(6,6))
ax.scatter(points[:, 0], points[:, 1], s=50, c='b', alpha=0.5)
ax.set_xlim(-0.5, N-0.5)
ax.set_ylim(-0.5, N-0.5)
ax.set_aspect('equal')


points=points[:,:2]
points=points.tolist()
print(points)
edgepoints=[]
newedgepoints=[]

for i in range(len(points)):
    pointx=points[i][0]
    pointy=points[i][1]
    if [pointx-1,pointy] not in points or [pointx+1,pointy] not in points or [pointx,pointy-1] not in points or [pointx,pointy+1] not in points:
        edgepoints.append(points[i])
        if [pointx-1,pointy] not in points:
            newedgepoints.append([pointx-1,pointy])
        elif [pointx+1,pointy] not in points:
            newedgepoints.append([pointx + 1, pointy])
        elif [pointx,pointy-1] not in points:
            newedgepoints.append([pointx, pointy-1])
        elif [pointx,pointy+1] not in points:
            newedgepoints.append([pointx, pointy + 1])

edgepoints=np.array(edgepoints)
newedgepoints=np.array(newedgepoints)
print(edgepoints)
plt.scatter(edgepoints[:,0],edgepoints[:,1], color='red')
plt.scatter(newedgepoints[:,0],newedgepoints[:,1], color='purple')
#plt.show()
# whatever

print(newedgepoints)



