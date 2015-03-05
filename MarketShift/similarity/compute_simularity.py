'''
Created on Jan 19, 2015

@author: munichong
'''
import csv, numpy
from scipy.spatial.distance import euclidean

# class Company:
#     def __init__(self, duns_number):
#         self.duns_number = duns_number
#         self.products = []
#     
#     def add_product(self, product_code):
#         self.products.append( product_code )


def jaccard( set1, set2 ):
    return 1 - ( len( set1.intersection(set2) ) / float(len( set1.union(set2) )) )

infile = open( "../data/Companies_Table/company_product.csv", "r" );
csvfile = csv.reader(infile, delimiter=',')
next(csvfile) # skip the headers

company_num = 0
company_vectors = {}

for row in csvfile:
    duns = row[1]
    product = row[2]
    if not company_vectors.has_key( duns ):
        company_vectors[duns] = set()
    company_vectors[duns].add( product )    
        
print( 'There are ', len(company_vectors) , " companies" )


outfile = open( "../company_product_neighbors.csv", "w" )
writer = csv.writer( outfile )
m = 0;
for company1 in company_vectors.keys():
    newrow = [ company1, len( company_vectors[company1] ) ]
    neigbors = []
    print(m)
    m+=1
    for company2 in company_vectors.keys():
        if company1 == company2:
            continue
        distance = jaccard( company_vectors[company1], company_vectors[company2]  )
        neigbors.append( (company2, distance) )
        
    neigbors = sorted( neigbors, key=lambda x :x[1] )[:5]
    #output
    for n, d in neigbors:
        newrow.append(n)
    for n, d in neigbors:
        newrow.append(len(company_vectors[n]))
    for n, d in neigbors:
        newrow.append(d)
        
    writer.writerow(newrow)
#     row.append( company.duns_number )
#     neighbor_duns = []
#     neighbor_dist = []
#     for neighbor, distance in company.top_neighbors:
#         neighbor_duns.append( neighbor.duns_number )
#         neighbor_dist.append( distance )
#     row.extend(neighbor_duns)
#     row.extend( neighbor_dist )
#     writer.writerow( row )


        
            
