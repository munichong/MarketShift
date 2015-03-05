'''
Created on Jan 21, 2015

@author: munichong
'''
import os, re, htmlentitydefs
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

def unescape(text):
    """ This function converts HTML entities and character references to ordinary characters. """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def cleanhtml( raw_html ):
    cleanr = re.compile('<script[\d\D]*?/script>|<style[\d\D]*?/style>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleanr = re.compile('<[\d\D]*?>')
    cleantext = re.sub(cleanr, '', cleantext)
#     cleantext = unescape( cleantext )
#     print(cleantext)
    return cleantext

def filter_words( tokens ):
    content = [ w.lower() for w in tokens 
               if ( w.lower() not in stopwords.words('english') )
               and ( len(w) > 1 )
               and ( w[0]!='&' ) ]
    return content

def extract_freq_words( raw_page ):
    page_text = cleanhtml( raw_page )
    tokens = word_tokenize( page_text )
    tokens = filter_words( tokens )
    fdist = FreqDist( tokens )
    return fdist.items()

path = "../MarketShift_Company_Websites/"
for duns_folder in os.listdir( path ):
    for filename in os.listdir( path + duns_folder ):
        if filename == "Products":
            for pfilename in os.listdir( path + duns_folder + '/Products' ):
                with open( path + duns_folder + "/Products/" + pfilename, "r" ) as page:
                    print( "### Product Page: {0}".format( pfilename ) )
                    freq_words = extract_freq_words( page.read() )
                    print( freq_words[:10] )
        else:
            with open( path + duns_folder + "/" + filename, "r" ) as page:
                print( filename )
                freq_words = extract_freq_words( page.read() )
                print( freq_words[:10] )
                