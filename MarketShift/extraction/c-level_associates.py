'''
Created on Mar 3, 2015

@author: munichong
'''
import os, re, csv
from nltk import word_tokenize, ne_chunk, pos_tag

def clean_html( raw_html ):
    cleanr = re.compile('<script[\d\D]*?/script>|<style[\d\D]*?/style>')
    cleantext = re.sub(cleanr, '. ', raw_html)
    cleanr = re.compile('<[\s\S]*?>')
    cleantext = re.sub(cleanr, '. ', cleantext)
#     cleantext = unescape(cleantext)
#     print(cleantext)
    return cleantext


email_pattern = re.compile(("([a-z0-9!#$%&'*\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
def get_emails(s):
    """Returns an iterator of matched emails found in string s."""
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
    email_pos = {}
    for email in set( re.findall(email_pattern, s) ):
        if email[0].startswith('//'):
            continue
        email_pos[ email[0] ] = indexOfAll( email[0], s )
    return email_pos


phone_pattern = re.compile( r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4})''' )
def get_phones(s):
    phone_pos = {}
    for phone in set( re.findall( phone_pattern, s) ):
        phone_pos[ phone ] = indexOfAll( phone, s)
    return phone_pos


def indexOfAll(substr, fullstr):
#     print substr
    return [ m.start() for m in re.finditer( substr, fullstr ) ]


c_levels = [ ' CEO ', 'Chief executive officer', 'Chief Executive Officer', 'chief executive officer',
            ' CTO ', 'Chief technology officer', 'Chief Technology Officer', 'chief technology officer',
            ' CIO ', 'Chief information officer', 'Chief Information Officer', 'chief technology officer',
            ' COO ', 'Chief operation officer', 'Chief Operation Officer', 'chief technology officer',
            ' CFO ', 'Chief financial officer', 'Chief Financial Officer', 'chief financial officer',
            ' CMO ', 'Chief marketing officer', 'Chief Marketing Officer', 'chief marketing officer',
            'President', 'president', 
            'Vice President', 'Vice president', 'vice-president', 'vice-President', 'vice president', 'VP','V.P.'
            'Board of Director', 'board of director', 'Board of director',
            'Director', 'director', 'Manager', 'manager', 'Chairman', 'chairman',
             ]

csvfile = open('../data/c-level.csv', 'w')
csvwriter = csv.writer(csvfile)
# company_CL = {}
root = "/media/munichong/SAMSUNG/"
for mirror in [ 'mirror1', 'mirror2' ]:
    path_mirror = root + mirror
    for domain in os.listdir( path_mirror ):
        if domain[0] == '.':
            continue
        path_domain = path_mirror + "/" + domain
        
        try:
            for filename in os.listdir( path_domain ):
                path_file = path_domain + "/" + filename
                
                if os.path.isdir( path_file ):
                    continue
                
                with open( path_file, "r" ) as page:
                    page_text = clean_html( page.read() )
    #                 page_text = page.read()
    #                 print path_file
                    emails = get_emails( page_text )
                    phones = get_phones( page_text )
                    # if this page does not contain an email or phone number
                    if len( emails ) == 0 and len( phones ) == 0:
                        continue
                    
                    cl_pos = {}
                    for cl in c_levels:
                        # if this page has a c-level title
                        if cl in page_text:
                            cl_pos[cl] = indexOfAll( cl, page_text )
                            
                    if len( cl_pos ) == 0:
                        continue
                    
                    # match adjacent c-level and email and/or phone
                    for cl in cl_pos.keys():
                        for pos in cl_pos[ cl ]:
                            
                            context = page_text[ pos - 100 : pos - 100 ]
                            ne_sent = ne_chunk( pos_tag( word_tokenize( context ) ), binary=False )
                            nes = [' '.join(map(lambda x: x[0], ne.leaves())) for ne in sentt if isinstance(ne, nltk.tree.Tree)]
                            
                            email_result = ''
                            min_email_dist = 100
                            for email in emails.keys():
                                for e_pos in emails[email]:
                                    if abs( pos - e_pos ) < min_email_dist:
                                        email_result = email
                                        min_email_dist = abs( pos - e_pos )
                            
                            phone_result = ''
                            min_phone_dist = 100
                            for phone in phones.keys():
                                for p_pos in phones[phone]:
                                    if  abs( pos - p_pos ) < min_phone_dist:
                                        phone_result = phone
                                        min_phone_dist = abs( pos - p_pos )
                                        
                            if email_result == '' and phone_result == '':
                                continue
    #                         if not company_CL.has_key( path_file ):
    #                             company_CL[ path_file ] = []
    #                         company_CL[ path_file ].append( (cl, email, phone) )
                            
                            csvwriter.writerow( [ path_file, cl, email_result, phone_result ] )
                            print( path_file, cl, email_result, phone_result )
            
        except IOError:
            continue    

