'''
Created on Mar 4, 2015

@author: munichong
'''
import csv

with open("../data/c-level.csv", 'r') as clevel:
    clevel_reader = csv.reader( clevel )
    line_set = set()
    for line in clevel_reader:
        line_set.add( tuple(line) )
    
    clevel_writer = csv.writer( open( "../data/c-level_unique.csv", 'w' ) )
    for line in line_set:
        clevel_writer.writerow(line)