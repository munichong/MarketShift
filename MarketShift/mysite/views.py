from django.http import HttpResponse
from django.shortcuts import render
import pandas
from pymongo import MongoClient

def search(request):
    #return HttpResponse("Hello world")
    return render(request, 'search.html')

def do_search(request):
    
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    collection = client['MarketShift']['CompanyTable']
    #print type(collection)
    
    company_name = request.POST['company_name']
    duns = request.POST['company_duns']
    city = request.POST['city']

    employee_2013_min = request.POST['employee_2013_min']
    employee_2013_max = request.POST['employee_2013_max']
    employee_2014_min = request.POST['employee_2014_min']
    employee_2014_max = request.POST['employee_2014_max']
    fedcontract_2013_min = request.POST['fedcontract_2013_min']
    fedcontract_2013_max = request.POST['fedcontract_2013_max']
    fedcontract_2014_min = request.POST['fedcontract_2014_min']
    fedcontract_2014_max = request.POST['fedcontract_2014_max']
    revenue_2013_min = request.POST['revenue_2013_min']
    revenue_2013_max = request.POST['revenue_2013_max']
    revenue_2014_min = request.POST['revenue_2014_min']
    revenue_2014_max = request.POST['revenue_2014_max']
    
    query = {} 
    if company_name:
        query['vendorname'] = company_name
    if duns:
        query['dunsnumber'] = duns
    if city:
        query['city'] = city.upper()

    if employee_2013_min.isdigit():
        employee_2013 = query.get('employee_count_2013', {})
        employee_2013["$gt"] = float( employee_2013_min )
        query['employee_count_2013'] = employee_2013
    if employee_2013_max.isdigit():
        employee_2013 = query.get('employee_count_2013', {})
        employee_2013["$lt"] = float( employee_2013_max )
        query['employee_count_2013'] = employee_2013
    if employee_2014_min.isdigit():
        employee_2014 = query.get('employee_count_2014', {})
        employee_2014["$gt"] = float( employee_2014_min )
        query['employee_count_2014'] = employee_2014
    if employee_2014_max.isdigit():
        employee_2014 = query.get('employee_count_2014', {})
        employee_2014["$lt"] = float( employee_2014_max )
        query['employee_count_2014'] = employee_2014 

    if fedcontract_2013_min.isdigit():
        fedcontract_2013 = query.get('fed_contracting_2013', {})
        fedcontract_2013["$gt"] = float( fedcontract_2013_min )
        query['fed_contracting_2013'] = fedcontract_2013
    if fedcontract_2013_max.isdigit():
        fedcontract_2013 = query.get('fed_contracting_2013', {})
        fedcontract_2013["$lt"] = float( fedcontract_2013_max )
        query['fed_contracting_2013'] = fedcontract_2013
    if fedcontract_2014_min.isdigit():
        fedcontract_2014 = query.get('fed_contracting_2014', {})
        fedcontract_2014["$gt"] = float( fedcontract_2014_min )
        query['fed_contracting_2014'] = fedcontract_2014
    if fedcontract_2014_max.isdigit():
        fedcontract_2014 = query.get('fed_contracting_2014', {})
        fedcontract_2014["$lt"] = float( fedcontract_2014_max )
        query['fed_contracting_2014'] = fedcontract_2014 
   
    if revenue_2013_min.isdigit():
        revenue_2013 = query.get('total_revenue_2013', {})
        revenue_2013["$gt"] = float( revenue_2013_min )
        query['total_revenue_2013'] = revenue_2013
    if revenue_2013_max.isdigit():
        revenue_2013 = query.get('total_revenue_2013', {})
        revenue_2013["$lt"] = float( revenue_2013_max )
        query['total_revenue_2013'] = revenue_2013
    if revenue_2014_min.isdigit():
        revenue_2014 = query.get('total_revenue_2014', {})
        revenue_2014["$gt"] = float( revenue_2014_min )
        query['total_revenue_2014'] = revenue_2014
    if revenue_2014_max.isdigit():
        revenue_2014 = query.get('total_revenue_2014', {})
        revenue_2014["$lt"] = float( revenue_2014_max )
        query['total_revenue_2014'] = revenue_2014 
    #print query
    result = collection.find( query ).sort('company_id')
    table_head = [ 'vendorname' ] 
    [ table_head.append( colname ) for colname in query.keys() if colname not in table_head and colname != 'company_id' ]
    result_html = [ "<html>", "<table>", "<tr>" ]
    for colname in table_head:
        result_html.extend( [ "<th>", colname.upper(), "</th>" ] )
    result_html.append( "</tr>" )
    
    print result.count()
    for row in result:
        result_html.append( "<tr>" )
        for colname in table_head:
            result_html.extend( [ "<td align=\"center\">", str( row[colname] ), "</td>" ] )
        result_html.append( "</tr>" )    
    result_html.extend( ["</table>", "</html>"] )
    return HttpResponse( " ".join(result_html) )







