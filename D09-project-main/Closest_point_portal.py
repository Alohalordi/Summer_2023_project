import random
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
import time
import math
import pandas as pd

start = time.time()

lines_5 = np.load("lines5.npy", allow_pickle=True)
# print("this is lines_5")
# print(lines_5)
length=0
for i in range(len(lines_5)):
    if length < len(lines_5[i]):
        length = len(lines_5[i])
print(length)

# lines_1 = np.empty([len(lines), 2*length])
lines_1 = [[0]*(2*length) for i in range(len(lines_5))]
#print(lines_1.shape())
for i in range(len(lines_1)):
    for j in range(len(lines_5[i])):
        if len(lines_5[i])!= 1:
            lines_1[i][2*j] = lines_5[i][j][0]
            lines_1[i][2*j+1] = lines_5[i][j][1]



print("this is lines_1")
print(lines_1)
pd.DataFrame(lines_1).to_csv("MoM")

#print("this is the streamline array")
dt = pd.read_csv('MoM')
df = pd.DataFrame(data=dt)
data = df.to_numpy()
data = np.delete(data, 0, axis= 1)
data = data[~np.all(data==0, axis=1)]
print("this is data")
print(data)
# np.delete(lines_1, delete_lines, axis= 0)
#print(data)
Streamline_array = np.empty((len(data), 2, 2))
# print(len(Streamline_array))
Locations = np.empty((2*len(data), 2))
delete_lines = []
for i in range(len(lines_5)):
    if len(lines_5[i]) < 2:
        delete_lines.append(i)
print(delete_lines)
lines_5 = np.delete(lines_5, delete_lines, axis = 0)

for i in range(len(data)):
    Streamline_array[i][0][0] = lines_5[i][0][0]
    Streamline_array[i][0][1] = lines_5[i][0][1]

    print(Streamline_array[i][0])
    #Streamline_array[i][1] =
    Streamline_array[i][1][0] = lines_5[i][-1][0]
    Streamline_array[i][1][1] = lines_5[i][-1][1]

    Locations[2*i] = [lines_5[i][0][0], lines_5[i][0][1]]
    Locations[2*i+1]= [lines_5[i][-1][0], lines_5[i][-1][1]]
Streamlines=Streamline_array

print(Streamlines)
#print(Streamlines[0,1])
#print(Locations)

#make a square grid
# Square_size = 6

# Array_length = Square_size**2
# Locations = np.empty((Array_length,2), dtype=int, order='c')
# k=0
# for i in range(Square_size):
#     for j in range(Square_size):
#         Locations[k][:] = [i,j]
#         k = k+1

#have random elements fall out, such that the grid is no longer rectangular
# random.seed()
# Number_of_drops = 10
# for i in range(Number_of_drops):
#     j = random.randrange(len(Locations))
#     Locations = np.delete(Locations,j,0)

combined_x_y_arrays = np.dstack([Locations[:,0].ravel(),Locations[:,1].ravel()])[0]
# print(len(combined_x_y_arrays))
# print("It's running")


Array_length = len(Locations)
print(Array_length)
# print(Locations[204])
# print(Locations[205])




def Distance_to_edge(Locations):

    Y_top = np.max(Locations[:,1])
    X_top = np.max(Locations[:,0])
    # max = np.maximum(X_top,Y_top)
    # Y_top = max
    # X_top = max
    Y_bot = np.min(Locations[:, 1])
    X_bot= np.min(Locations[:,0])
    # min = np.minimum(X_bot,Y_bot)
    # X_bot = min
    # Y_bot = min

    distances = []
    for i in range(len(Locations)):
        dist_x = np.minimum(Locations[i, 0]-X_bot, X_top - Locations[i, 0])
        dist_y = np.minimum(Locations[i, 1]-Y_bot, Y_top - Locations[i, 1])
        dist = np.sqrt((dist_y)**2+(dist_x)**2)
        # dist = Locations[i,0]*Locations[i,1]*Y_top-Locations[i,1]*X_top-Locations[i,0]
        # dist = np.minimum(dist_y, dist_x)
        # dist = math.log(dist_y+1,2)+math.log(dist_x+1,2)

        distances.append(dist)
    return distances
distances=Distance_to_edge(Locations)
#print(distances)


def Find_Counterpart(Streamlines,combined_x_y_arrays_temp, copyindex):
    #print(combined_x_y_arrays_temp[copyindex])
    #print((Streamlines))
    for i in range(len(Streamlines)):
        streamline=[]
        streamline.append(Streamlines[i][0])
        streamline.append(Streamlines[i][1])
        if((streamline[0][0]==combined_x_y_arrays_temp[copyindex, 0])&(streamline[0][1]==combined_x_y_arrays_temp[copyindex, 1]) or (streamline[1][0]==combined_x_y_arrays_temp[copyindex, 0])&(streamline[1][1]==combined_x_y_arrays_temp[copyindex, 1])):
            Streamline_index = i
            if((streamline[0][0]==combined_x_y_arrays_temp[copyindex, 0])&(streamline[0][1]==combined_x_y_arrays_temp[copyindex, 1])):
                column_index=0
            else:
                column_index=1
    indexes=[]
    indexes.append(Streamline_index)
    indexes.append((column_index+1)%2)
    #counterindex=(column_index+1)%2
    #print("look here")
    #print(Streamlines[Streamline_index][counterindex])
    #print(combined_x_y_arrays_temp[:])
    #Counterpart = np.where((combined_x_y_arrays_temp[:,0] == Streamlines[Streamline_index][counterindex][0]) & (combined_x_y_arrays_temp[:,1] == Streamlines[Streamline_index][counterindex][1]))
    #print("below is counterpart")
    #print(Counterpart[0])
    #print(indexes)
    return indexes
        #Streamline_index = np.where((Sl.Create_Array(Locations)[:][0][0] == combined_x_y_arrays_temp[copyindex, 0]) & (Sl.Create_Array(Locations)[:][0][1] == combined_x_y_arrays_temp[copyindex, 1])) or np.where((Sl.Create_Array(Locations)[:][1][0] == combined_x_y_arrays_temp[copyindex, 0]) & (Sl.Create_Array(Locations)[:][1][1] == combined_x_y_arrays_temp[copyindex, 1]))
        #print(Streamline_index[0])
        #return Streamline_index

    #print(Locations_Temp)


def Closest_streamline(combined_x_y_arrays,Locations,weight):
    Closest_point_list = [0]
    combined_x_y_arrays_temp = combined_x_y_arrays
    copyindex=0
    choice = np.empty([4, 1])
    #print(Streamlines)


    while (len(Locations) > 4):

        #combined_x_y_arrays_temp = np.delete(combined_x_y_arrays_temp, copyindex, 0)
        #print(combined_x_y_arrays(copyindex))
        counterindex=Find_Counterpart(Streamlines,combined_x_y_arrays_temp,copyindex)
        #("it s running you moron")
        combined_x_y_arrays_temp = np.delete(combined_x_y_arrays_temp, copyindex, 0)
        Locations = np.delete(Locations, copyindex, 0)
        counterpart = np.where((combined_x_y_arrays_temp[:,0] == Streamlines[counterindex[0]][counterindex[1]][0]) & (combined_x_y_arrays_temp[:,1] == Streamlines[counterindex[0]][counterindex[1]][1]))
        Counterpart_proper = np.where((combined_x_y_arrays[:, 0] == combined_x_y_arrays_temp[counterpart[0], 0]) & (combined_x_y_arrays[:, 1] == combined_x_y_arrays_temp[counterpart[0], 1]))
        Closest_point_list.append(Counterpart_proper[0][0])
        combined_x_y_arrays_temp = np.delete(combined_x_y_arrays_temp, counterpart, 0)
        copyindex = counterpart

        mytree = sc.spatial.KDTree(combined_x_y_arrays_temp)
        dist, index = mytree.query(Locations[copyindex], k=4)
        index = index[0]
        # print("this is index")
        # print(index)
        #print(index)
        choice_1 = np.where((combined_x_y_arrays[:, 0] == combined_x_y_arrays_temp[index[0], 0]) & (combined_x_y_arrays[:, 1] == combined_x_y_arrays_temp[index[0], 1]))
        #print(combined_x_y_arrays_temp[index[0][1]])
        choice_2 = np.where((combined_x_y_arrays[:, 0] == combined_x_y_arrays_temp[index[1], 0]) & (combined_x_y_arrays[:, 1] == combined_x_y_arrays_temp[index[1], 1]))
        choice_3 = np.where((combined_x_y_arrays[:, 0] == combined_x_y_arrays_temp[index[2], 0]) & (combined_x_y_arrays[:, 1] == combined_x_y_arrays_temp[index[2], 1]))
        choice_4 = np.where((combined_x_y_arrays[:, 0] == combined_x_y_arrays_temp[index[3], 0]) & (combined_x_y_arrays[:, 1] == combined_x_y_arrays_temp[index[3], 1]))
        if (len(choice_1[0])>1):
            choice[0]=choice_1[0][0]
        else:
            choice[0]=choice_1[0]
        if (len(choice_2[0])>1):
            choice[1]=choice_2[0][0]
        else:
            choice[1] = choice_2[0]
        if (len(choice_3[0]) > 1):
            choice[2] = choice_3[0][0]
        else:
            choice[2] = choice_3[0]
        if (len(choice_4[0]) > 1):
            choice[3] = choice_4[0][0]
        else:
            choice[3] = choice_4[0]
        # print(len(Locations))
        # print(len(combined_x_y_arrays))
        # print("these are choices 4 and 3")
        # print(combined_x_y_arrays[204])
        # print(Locations[205])
        # print(choice_2[0])
        # print(choice_4[0])
        # print(choice_3[0])
        Better_distance_1 = np.minimum(
            distances[int(choice[0])]*weight+math.sqrt(((combined_x_y_arrays_temp[index[0], 0]-Locations[copyindex,0])**2)+((combined_x_y_arrays_temp[index[0], 1]-Locations[copyindex,1])**2)),
            distances[int(choice[1])]*weight+math.sqrt(((combined_x_y_arrays_temp[index[1], 0]-Locations[copyindex,0])**2)+((combined_x_y_arrays_temp[index[1], 1]-Locations[copyindex,1])**2)))
        Better_distance_2 = np.minimum(distances[int(choice[2])]*weight+math.sqrt(((combined_x_y_arrays_temp[index[2], 0]-Locations[copyindex,0])**2)+((combined_x_y_arrays_temp[index[2], 1]-Locations[copyindex,1])**2)),
                                       distances[int(choice[3])]*weight+math.sqrt((combined_x_y_arrays_temp[index[3], 0]-Locations[copyindex,0])**2+((combined_x_y_arrays_temp[index[3], 1]-Locations[copyindex,1])**2)))
        Better_distance = np.minimum(Better_distance_2,Better_distance_1)
        copyindex1=copyindex

        if Better_distance == distances[int(choice[0])]*weight+math.sqrt(((combined_x_y_arrays_temp[index[0], 0]-Locations[copyindex,0])**2)+((combined_x_y_arrays_temp[index[0], 1]-Locations[copyindex,1])**2)):
            Better_choice = int(choice[0])
            copyindex = index[0]
        elif Better_distance == distances[int(choice[1])]*weight+math.sqrt(((combined_x_y_arrays_temp[index[1], 0]-Locations[copyindex,0])**2)+((combined_x_y_arrays_temp[index[1], 1]-Locations[copyindex,1])**2)):
            Better_choice = int(choice[1])
            copyindex = index[1]
        elif Better_distance == distances[int(choice[2])]*weight+math.sqrt(((combined_x_y_arrays_temp[index[2], 0]-Locations[copyindex,0])**2)+((combined_x_y_arrays_temp[index[2], 1]-Locations[copyindex,1])**2)):
            Better_choice = int(choice[2])
            copyindex = index[2]
        else:
            Better_choice = int(choice[3])
            copyindex = index[3]

        Locations = np.delete(Locations, copyindex1, 0)
        # print("this is locations")
        # print(Locations)
        Closest_point_list.append(Better_choice)




    while (len(Locations) > 2):

        #combined_x_y_arrays_temp = np.delete(combined_x_y_arrays_temp, copyindex, 0)
        counterindex=Find_Counterpart(Streamlines,combined_x_y_arrays_temp,copyindex)
        #("it s running you moron")
        combined_x_y_arrays_temp = np.delete(combined_x_y_arrays_temp, copyindex, 0)
        Locations = np.delete(Locations, copyindex, 0)
        counterpart = np.where((combined_x_y_arrays_temp[:,0] == Streamlines[counterindex[0]][counterindex[1]][0]) & (combined_x_y_arrays_temp[:,1] == Streamlines[counterindex[0]][counterindex[1]][1]))
        Counterpart_proper = np.where((combined_x_y_arrays[:, 0] == combined_x_y_arrays_temp[counterpart[0], 0]) & (
                    combined_x_y_arrays[:, 1] == combined_x_y_arrays_temp[counterpart[0], 1]))
        Closest_point_list.append(Counterpart_proper[0][0])

        combined_x_y_arrays_temp = np.delete(combined_x_y_arrays_temp, counterpart, 0)
        copyindex = counterpart

        mytree = sc.spatial.KDTree(combined_x_y_arrays_temp)
        dist, index = mytree.query(Locations[copyindex], k=2)
        index = index[0]

        choice_1 = np.where((combined_x_y_arrays[:, 0] == combined_x_y_arrays_temp[index[0], 0]) & (combined_x_y_arrays[:, 1] == combined_x_y_arrays_temp[index[0], 1]))
        choice_2 = np.where((combined_x_y_arrays[:, 0] == combined_x_y_arrays_temp[index[1], 0]) & (combined_x_y_arrays[:, 1] == combined_x_y_arrays_temp[index[1], 1]))
        if (len(choice_1[0])>1):
            choice[0]=choice_1[0][0]
        else:
            choice[0]=choice_1[0]
        if (len(choice_2[0])>1):
            choice[1]=choice_2[0][0]
        else:
            choice[1] = choice_2[0]
        Better_distance = np.minimum(distances[int(choice[0])]*weight+math.sqrt(((combined_x_y_arrays_temp[index[0], 0]-Locations[copyindex,0])**2)+((combined_x_y_arrays_temp[index[0], 1]-Locations[copyindex,1])**2)),
                                     distances[int(choice[1])]*weight+math.sqrt(((combined_x_y_arrays_temp[index[1], 0]-Locations[copyindex,0])**2)+((combined_x_y_arrays_temp[index[1], 1]-Locations[copyindex,1])**2)))
        copyindex1 = copyindex

        if Better_distance == distances[int(choice[0])]*weight+math.sqrt(((combined_x_y_arrays_temp[index[0], 0]-Locations[copyindex,0])**2)+((combined_x_y_arrays_temp[index[0], 1]-Locations[copyindex,1])**2)):
            Better_choice = int(choice[0])
            copyindex = index[0]
        else:
            Better_choice = int(choice[1])
            copyindex = index[1]

        Closest_point_list.append(Better_choice)
        Locations = np.delete(Locations, copyindex1, 0)

    last_choice=np.where((combined_x_y_arrays[:,0]==combined_x_y_arrays_temp[(copyindex+1)%2,0]) & (combined_x_y_arrays[:,1] == combined_x_y_arrays_temp[(copyindex+1)%2, 1]))
    if (len(last_choice[0]) > 1):
        Closest_point_list.append(int(last_choice[0][0]))
    else:
        Closest_point_list.append(int(last_choice[0]))

    #print("these are all the points in order")
    #print(Closest_point_list)
    #print(combined_x_y_arrays[Closest_point_list])
    return Closest_point_list

def pathlength(Point_order):
    path=0
    for i in range(int((len(Point_order)-1)/2)):
        distance = math.sqrt((Point_order[2*i+2,0]-Point_order[2*i+1,0])**2+(Point_order[2*i+2,1]-Point_order[2*i+1,1])**2)
        path += distance
    return path
path_array=[]

def optimize_weight(combined_x_y_arrays, Locations):

    for i in range(1001):
        weight = (i-500)/100
        results = Closest_streamline(combined_x_y_arrays, Locations, weight)
        Point_order = np.empty((len(results), 2), dtype=float, order='c')
        k = 0
        for i in range(len(results)):
            Point_order[k][:] = combined_x_y_arrays[results[i], 0], combined_x_y_arrays[results[i], 1]
            k = k + 1
        path_array.append(pathlength(Point_order))
    min_path=min(path_array)
    index=path_array.index(min_path)
    bestweight = (index-500)/100
    return bestweight, min_path


start = time.time()
bestweight, path_length=optimize_weight(combined_x_y_arrays,Locations)
#print(bestweight)
#rint(path_length)
results1=Closest_streamline(combined_x_y_arrays, Locations, 0)
print("No bias")
Point_order = np.empty((len(results1), 2), dtype=float, order='c')
k = 0
for i in range(len(results1)):
    Point_order[k][:] = combined_x_y_arrays[results1[i], 0], combined_x_y_arrays[results1[i], 1]
    k = k + 1

# print(Point_order)
pathlength_unbiased = pathlength(Point_order)
print(pathlength_unbiased)
results = Closest_streamline(combined_x_y_arrays, Locations, bestweight)
print("Bias= " + str(bestweight))
print(path_length)
end = time.time()
Execution_time = end - start

print(Execution_time)



#todo: plot is broken
#print(A)

dt = pd.read_csv('MoM')
df = pd.DataFrame(data=dt)
data = df.to_numpy()
data = np.delete(data,0,1)
# print(data)
def plot():
    plt.plot(Locations[:, 0], Locations[:, 1], 'o')
    for i in range(len(data)):

        for j in range(int((len(data[i])/2-1))):
            stream_x = []
            stream_y = []
            x_i_0 = data[i][2*j]
            stream_x.append(x_i_0)
            y_i_0 = data[i][2*j + 1]
            stream_y.append(y_i_0)
            if data[i][2*j + 2] != 0:
                x_i_1 = data[i][2*j + 2]
                stream_x.append(x_i_1)
                y_i_1 = data[i][2*j + 3]
                stream_y.append(y_i_1)
                plt.plot(stream_x, stream_y, 'g')
            else:
                break

Unbiased_case = plt.figure()
plot()
for i in range(2*(len(Streamlines))):
    x_values=[]
    if i>0:
        x_values.append(combined_x_y_arrays[results1[i-1],0])
        x_values.append(combined_x_y_arrays[results1[i],0])
        y_values=[]
        y_values.append(combined_x_y_arrays[results1[i-1],1])
        y_values.append(combined_x_y_arrays[results1[i],1])
    else:
        x_values.append(combined_x_y_arrays[0, 0])
        x_values.append(combined_x_y_arrays[results1[i], 0])
        y_values = []
        y_values.append(combined_x_y_arrays[0, 1])
        y_values.append(combined_x_y_arrays[results1[i],1])
    if i%2==0:
        plt.plot(x_values,y_values,'c')
#     else:
#         plt.plot(x_values,y_values,'r')
plt.savefig('Unbiased path')
# plt.clf()

#plot for biased path
Biased_case = plt.figure()
plot()
for i in range(2*(len(Streamlines))):
    x_values=[]
    if i>0:
        x_values.append(combined_x_y_arrays[results[i-1],0])
        x_values.append(combined_x_y_arrays[results[i],0])
        y_values=[]
        y_values.append(combined_x_y_arrays[results[i-1],1])
        y_values.append(combined_x_y_arrays[results[i],1])
    else:
        x_values.append(combined_x_y_arrays[0, 0])
        x_values.append(combined_x_y_arrays[results[i], 0])
        y_values = []
        y_values.append(combined_x_y_arrays[0, 1])
        y_values.append(combined_x_y_arrays[results[i],1])
    if i%2==0:
        plt.plot(x_values,y_values,'c')
    # else:
    #     plt.plot(x_values,y_values,'r')

plt.savefig('Biased path')
# plt.clf()

Pathlength_vs_weight = plt.figure()
plt.plot(np.linspace(-5,5,1001),path_array, 'o')
plt.savefig('Pathlength_vs_weight')
# plt.clf()

Percent_change = plt.figure()
path_percent = np.empty([len(path_array),1])
for i in range(len(path_percent)):
    path_percent[i] = 100*(path_array[i]-pathlength_unbiased)/(pathlength_unbiased)
percent_decrease_opt = np.min(path_percent)
print(percent_decrease_opt)
plt.plot(np.linspace(-5,5,1001),path_percent, 'o')
plt.savefig('Relative_change_pathlength')

plt.show()



