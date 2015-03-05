'''
Created on Jan 23, 2015

@author: munichong
'''
import pandas, csv

df = pandas.read_csv( "../data/Companies_Table/companies (1).csv" )
writer = csv.writer( open('../company_averages.csv', 'w') )
for index, row in df.iterrows():
    print( index )
    company_dunsnum = row['dunsnumber']
    newrow = [ company_dunsnum ]
    
    n_e = 0
    n_f = 0
    n_t = 0
    avg_employee_count = 0
    avg_fed_contract = 0
    avg_total_revenue = 0
    for year in ['2009', '2010', '2011', '2012', '2013', '2014']:
        avg_employee_count += float( row[ 'employee_count_' + year ] )
        if float( row[ 'employee_count_' + year ] ) != 0:
            n_e += 1
            
        avg_fed_contract += float( row[ 'fed_contracting_' + year ] )
        if float( row[ 'fed_contracting_' + year ] ) != 0:
            n_f += 1
        
        avg_total_revenue += float( row[ 'total_revenue_' + year ] )
        if float( row[ 'total_revenue_' + year ] ) != 0:
            n_t += 1
    
    # summarize
    if n_e == 0:
        newrow.append('NA')
    else:
        newrow.append( avg_employee_count / n_e )
        
    if n_f == 0:
        newrow.append('NA')
    else:
        newrow.append( avg_fed_contract / n_f )
    

    if n_t == 0:
        newrow.append('NA')
    else:
        newrow.append( avg_total_revenue / n_t )
    
    writer.writerow( newrow )
       