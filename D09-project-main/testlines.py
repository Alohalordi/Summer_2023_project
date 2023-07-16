import csv
import numpy as np
import pandas as pd


with open('newlines.csv', 'r') as csv_file:
    # Create a reader object
    csv_reader = csv.reader(csv_file)

    data_list= []
    for row in csv_reader:
        # Print each row
        data_list.append(row)



print(data_list[0][:])

# df=pd.read_csv('newlines.csv')
# dataframe=df.to_numpy()
# print(dataframe[0][0][0][:])