'''
Created on Jan 31, 2015

@author: munichong
'''
import pandas
from pymongo import MongoClient

# pandas.set_option('display.max_columns', None)

client = MongoClient()
client = MongoClient('localhost', 27017)
collection = client['MarketShift']['CompanyTable']

company_name = raw_input( 'Please enter company name: ' )
duns = raw_input( 'Please enter company DUNS number: ' )
city = raw_input( 'Please enter the city: ' )

employee_2013 = raw_input( 'Please enter the range of the number of employees in 2013: ' )
employee_2014 = raw_input( 'Please enter the range of the number of employees in 2014: ' )
fedcontract_2013 = raw_input( 'Please enter the range of the federal contracting in 2013: ' )
fedcontract_2014 = raw_input( 'Please enter the range of the federal contracting in 2014: ' )
revenue_2013 = raw_input( 'Please enter the range of the revenue in 2013: ' )
revenue_2014 = raw_input( 'Please enter the range of the revenue in 2014: ' )

query = {}
if company_name.upper() != 'ANY':
    query['vendorname'] = company_name
if duns.upper() != 'ANY':
    query['dunsnumber'] = duns
if city.upper() != 'ANY':
    query['city'] = city.upper()
if employee_2013.upper() != 'ANY':
    minVal = float( employee_2013.split('~')[0] )
    maxVal = float( employee_2013.split('~')[1] )
    query['employee_count_2013'] = {"$gt": minVal, "$lt": maxVal}
if employee_2014.upper() != 'ANY':
    minVal = float( employee_2014.split('~')[0] )
    maxVal = float( employee_2014.split('~')[1] )
    query['employee_count_2014'] = {"$gt": minVal, "$lt": maxVal}    
if fedcontract_2013.upper() != 'ANY':
    minVal = float( fedcontract_2013.split('~')[0] )
    maxVal = float( fedcontract_2013.split('~')[1] )
    query['fed_contracting_2013'] = {"$gt": minVal, "$lt": maxVal}    
if fedcontract_2014.upper() != 'ANY':
    minVal = float( fedcontract_2014.split('~')[0] )
    maxVal = float( fedcontract_2014.split('~')[1] )
    query['fed_contracting_2014'] = {"$gt": minVal, "$lt": maxVal}      
if revenue_2013.upper() != 'ANY':
    minVal = float( revenue_2013.split('~')[0] )
    maxVal = float( revenue_2013.split('~')[1] )
    query['total_revenue_2013'] = {"$gt": minVal, "$lt": maxVal}   
if revenue_2014.upper() != 'ANY':
    minVal = float( revenue_2014.split('~')[0] )
    maxVal = float( revenue_2014.split('~')[1] )
    query['total_revenue_2014'] = {"$gt": minVal, "$lt": maxVal}      

print '\nSearch Result:'
result = collection.find( query ).sort('company_id')
table_head = [ 'vendorname' ] 
[ table_head.append( colname ) for colname in query.keys() if colname not in table_head and colname != 'company_id' ]

output_df = pandas.DataFrame( columns = table_head )
for row in result:
    output_row = []
    for colname in table_head:
        output_row.append( row[colname] )

    output_df.loc[ output_df.shape[0] ] = output_row

print output_df