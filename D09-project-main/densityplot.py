import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import interpolate

df=pd.read_csv('Data/outputinterpolatedata.csv')
dataframe=df.to_numpy()

X=dataframe[1:,0]
Y=dataframe[1:,1]
Z=dataframe[1:,2]
u=dataframe[1:,3]
v=dataframe[1:,4]
w=dataframe[1:,5]
X,Y,Z,u,v,w=X.astype(float),Y.astype(float),Z.astype(float),u.astype(float),v.astype(float),w.astype(float)
ind=np.argsort(Z)
X,Y,Z,u,v,w=X[ind],Y[ind],Z[ind],u[ind],v[ind],w[ind]


first=np.argwhere(Z==8)
second=np.argwhere(Z==9)



plt.figure(figsize=(15,9))
plt.quiver(X[np.min(first):np.min(second)],Y[np.min(first):np.min(second)],u[np.min(first):np.min(second)],v[np.min(first):np.min(second)])
plt.show()

xi = np.linspace(np.min(X),np.max(X),len(X[np.min(first):np.min(second)])+1)
print(xi)
yi = np.linspace(np.min(Y),np.max(Y),len(Y[np.min(first):np.min(second)-1]))
x,y=np.meshgrid(xi,yi)

U = interpolate.griddata((X[min(first):min(second)], Y[min(first):min(second)]), u[min(first):min(second)], (x, y), method='cubic')
V = interpolate.griddata((X[min(first):min(second)], Y[min(first):min(second)]), v[min(first):min(second)], (x, y), method='cubic')
plt.figure()
plt.streamplot(x,y,U,V)
plt.show()