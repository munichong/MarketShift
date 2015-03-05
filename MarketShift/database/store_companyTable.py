'''
Created on Jan 31, 2015

@author: munichong
'''
import pandas, math
from pymongo import MongoClient

company_table = pandas.read_csv( "../data/Companies_Table/companies_NA.csv" )

client = MongoClient()
client = MongoClient('localhost', 27017)
collection = client['MarketShift']['CompanyTable']

for index, row in company_table.iterrows():
    company = {}
    for col_name, val in row.iteritems():
        if not isinstance( val, float ) or not math.isnan( val ):
            company[ col_name ] = val
            print( col_name + ", " + str(val) )
    collection.insert( company )
