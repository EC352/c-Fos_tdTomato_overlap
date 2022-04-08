"""Only stores coordinates within the required pixels of each other, this can be used for mapping afterwards"""
from collections import Counter
import os

#Determine storage, files, the required distance (and its negate)
BaseDirectory = 'C:/Users/emmac/PycharmProjects'
cfos_file = os.path.join (BaseDirectory, 'cfos_cells.csv')
tdtomato_file = os.path.join (BaseDirectory, 'tdtom_cells.csv')
required_pixels = 3.0
required_pixels_negative = 1 - required_pixels

#Generate list with a set of coordinates (x, y, z) for every list item (only for cfos)
cfos = []
with open (cfos_file) as f:
    for line in f:
        line = line.strip ('\n')
        cfos.append (line)

# Determine values for storage of x, y and z coordinates in dictionaries
x_cfos, y_cfos, z_cfos = [], [], []
cfos_dict_x = {}
cfos_dict_y = {}

# Extract x, y and z coordinates from aforementioned list and store x and y in seperate dicts
# In the dictionary the x and y coordinates are the values stored per plane (key)
for i in range (0, len(cfos)):
    x, y, z = cfos[i].split(',')
    x_cfos.append(x)
    y_cfos.append(y)
    z = round (float(z), 0)
    z_cfos.append(z)

counts = Counter (z_cfos)
i = 0
counts = dict (counts)

for plane in counts:
    plane = plane
    count = counts[plane]
    cfos_dict_x [plane] = x_cfos[i:i+count]
    cfos_dict_y [plane] = y_cfos[i:i+count]
    i += count

#Generate list with a set of coordinates (x, y, z) for every list item (only for tdtomato)
tdtomato = []
with open (tdtomato_file) as f:
    for line in f:
        line = line.strip ('\n')
        tdtomato.append (line)

# Determine values for storage of x, y and z coordinates in dictionaries
x_tdtomato, y_tdtomato, z_tdtomato = [], [], []
tdtomato_dict_x = {}
tdtomato_dict_y = {}

# Extract x, y and z coordinates from aforementioned list and store x and y in seperate dicts
# In the dictionary the x and y coordinates are the values stored per plane (key)
for i in range (0, len (tdtomato)):
    x, y, z = tdtomato[i].split(',')
    x_tdtomato.append(x)
    y_tdtomato.append(y)
    z = round(float(z), 0)
    z_tdtomato.append (z)

counts = Counter (z_tdtomato)
i = 0
counts = dict (counts)
for plane in counts:
    count = counts[plane]
    tdtomato_dict_x [plane] = x_tdtomato [i:i+count]
    tdtomato_dict_y [plane] = y_tdtomato [i:i+count]
    i += count

#Determine values needed to compare coordinates and store them in an overlap file
x_coordinates_c = []
y_coordinates_c = []
x_es = []
planes = []
y_es = []

# X-values of the tdtomato dictionary (so tdtomato x coordinates) are substracted from cfos x cooridnates
# When the difference between these x values is less than the required value (as set in the beginning), it is stored in a new list
for plane in tdtomato_dict_x.keys():
    x_coordinates_c = cfos_dict_x [plane]
    x_coordinates_t = tdtomato_dict_x [plane]
    for x_coordinate_t in x_coordinates_t:
        for x_coordinate_c in x_coordinates_c:
            x_coordinate_difference = float(x_coordinate_t) - float(x_coordinate_c)
            if x_coordinate_difference <= required_pixels and x_coordinate_difference >= required_pixels_negative:
                x_es.append(x_coordinate_t)
                planes.append(str(plane))
            else:
                x_es.append(0)
                planes.append('none')

# Y-values of the tdtomato dictionary (so tdtomato y coordinates) are substracted from cfos y cooridnates
# When the difference between these y values is less than the required value (as set in the beginning), it is stored in a new list
for plane in tdtomato_dict_y.keys():
    y_coordinates_c = cfos_dict_y [plane]
    y_coordinates_t = tdtomato_dict_y [plane]
    for y_coordinate_t in y_coordinates_t:
        for y_coordinate_c in y_coordinates_c:
            y_coordinate_difference = float(y_coordinate_t) - float(y_coordinate_c)
            if y_coordinate_difference <= required_pixels and y_coordinate_difference >= required_pixels_negative:
                y_es.append(y_coordinate_t)
            else:
                y_es.append(0)

# Write the lists obtained in the previous step to a new file
# This new file can be used for mapping coordinates to an atlas, similar to what is done to regular coordinate files
# The file is called overlapped_coordinates.csv and is stored in the determined base directory
overlap_f = os.path.join(BaseDirectory, 'overlapped_coordinates.csv')
overlap_file = open (overlap_f, 'w')
for i in range (0, len(x_es)):
    if x_es[i] != 0 and y_es[i] != 0:
        overlap_file.write (x_es[i])
        overlap_file.write (',')
        overlap_file.write(y_es[i])
        overlap_file.write(',')
        overlap_file.write(planes[i])
        overlap_file.write('\n')

overlap_file.close()