'''
Created on Jan 19, 2015

@author: munichong
'''
import csv

infile = open( "../company_neighbors.csv", "r" );
csvfile = csv.reader(infile, delimiter=',')
next(csvfile) # skip the headers

all_distances = {}
for row in csvfile:
    for dist in row[-5:]:
        dist = float(dist)
        if dist < 1:
            all_distances["0"] = all_distances.get("0", 0) + 1
        elif dist < 10:
            all_distances["10"] = all_distances.get("10", 0) + 1
        elif dist < 100:
            all_distances["100"] = all_distances.get("100", 0) + 1
        elif dist < 1000:
            all_distances["1000"] = all_distances.get("1000", 0) + 1
        elif dist < 10000:
            all_distances["10000"] = all_distances.get("10000", 0) + 1
        elif dist < 100000:
            all_distances["100000"] = all_distances.get("100000", 0) + 1
        elif dist < 1000000:
            all_distances["1000000"] = all_distances.get("1000000", 0) + 1
        elif dist < 10000000:
            all_distances["10000000"] = all_distances.get("10000000", 0) + 1
        elif dist < 100000000:
            all_distances["100000000"] = all_distances.get("100000000", 0) + 1
        elif dist < 1000000000:
            all_distances["100000000"] = all_distances.get("1000000000", 0) + 1    
        else:
            all_distances["more"] = all_distances.get("more", 0) + 1
            
for ad in all_distances.keys():
    print( str( ad ) + "," + str( all_distances[ad] ) )
    
