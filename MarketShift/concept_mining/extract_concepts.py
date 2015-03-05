'''
Created on Feb 4, 2015

@author: munichong
'''
import os, nltk, re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from concept_mining import KGram, concept_extraction
    
def get_kgram( raw_page, k ):
    page_text = clean_html( raw_page.lower() )
    sentences = sent_tokenize( page_text )
    kgram = []
    for k in range(1, k + 1 ):
        for sent in sentences:
            kgram.extend( ngrams( nltk.word_tokenize(sent), k ) )
    return kgram

def clean_html( raw_html ):
    cleanr = re.compile('<script[\d\D]*?/script>|<style[\d\D]*?/style>')
    cleantext = re.sub(cleanr, ' ', raw_html)
    cleanr = re.compile('<[\s\S]*?>')
    cleantext = re.sub(cleanr, ' ', cleantext)
    return cleantext

path = "../data/MarketShift_Company_Websites/"
n = 4
for duns_folder in os.listdir( path ):
    print("\n*******************")
    company_kgrams = []
    for filename in os.listdir( path + duns_folder ):
        page_kgram = []
        if filename == "Products":
            for pfilename in os.listdir( path + duns_folder + '/Products' ):
                with open( path + duns_folder + "/Products/" + pfilename, "r" ) as page:
                    print( "### Product Page: {0}".format( pfilename ) )
                    page_kgram = get_kgram( page.read(), n )
                    company_kgrams.extend( page_kgram )
#                     print company_kgrams
        else:
            with open( path + duns_folder + "/" + filename, "r" ) as page:
                print( filename )
                page_kgram = get_kgram( page.read(), n )
                company_kgrams.extend( page_kgram )
#                 print company_kgrams
    # summarize a company: unique kgrams and their freqs
    kgram_fd = {}
    total_freq = 0.0
    for kgram_tuple in company_kgrams:
        if not kgram_fd.has_key( kgram_tuple ):
            freq = company_kgrams.count( kgram_tuple )
            kgram_fd[ kgram_tuple ] = freq
            total_freq += freq
    kgram_dict = {}
    for kgram_tuple in kgram_fd.keys():
        kgram_class = KGram( kgram_tuple, kgram_fd[ kgram_tuple ] / total_freq )
        if kgram_class.k > 1:
            kgram_class.set_subconcept_freqs( kgram_fd[ kgram_class.prefix ] / total_freq
                                              , kgram_fd[ kgram_class.suffix ] / total_freq )
        kgram_dict[ kgram_tuple ] = kgram_class
    # compute rel_conf for each KGram
    for kgram_class in kgram_dict.values():
        if kgram_class.k > 1:
            max_conf_pre = kgram_dict[ kgram_class.prefix ].max_conf if kgram_class.k != 2 else 1 
            max_conf_post = kgram_dict[ kgram_class.suffix ].max_conf if kgram_class.k != 2 else 1 
            kgram_class.set_relConf( max_conf_pre, max_conf_post )
#     print kgram_dict[('film', 'sensors')].freq
#     print kgram_dict[('moi', 'thin','film', 'sensors')].freq
    concept_extraction( kgram_dict, n )
    