'''
Created on Jan 23, 2015

@author: munichong
'''
import pandas, csv, math
    
df = pandas.read_csv( '../company_averages.csv' )

writer = csv.writer( open('../total_revenue_similarity.csv', 'w') )
for index1, row1 in df.iterrows():
    print( index1 )
    duns1 = str( int( row1['company_dunsnum'] ) )
    average1 = row1['avg_total_revenue']

    if math.isnan( average1 ):
        writer.writerow( [duns1, 'NA'] )
        print('NA')
        continue
    
    result = []
    for index2, row2 in df.iterrows():
#         print( " "+str(index2) )
        if index2 == index1 or math.isnan( row2['avg_total_revenue'] ):
            continue
        duns2 = str( int( row2['company_dunsnum']) )
        average2 = row2['avg_total_revenue']
        result.append( ( duns2, average2, abs( float(average1) - float(average2) ) ) )
    result = sorted( result, key = lambda x: x[2])[:5]
    newrow = [ duns1, average1 ]
    for duns2, _, _ in result:
        newrow.append( duns2 )
    for _, average2, _ in result:
        newrow.append( average2 )
    writer.writerow( newrow )
        
    
    