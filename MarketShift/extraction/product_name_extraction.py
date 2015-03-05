'''
Created on Jan 28, 2015

@author: munichong
'''
import os, re, nltk, string, inflect
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

# def unescape(text):
#     """ This function converts HTML entities and character references to ordinary characters. """
#     def fixup(m):
#         text = m.group(0)
#         if text[:2] == "&#":
#             # character reference
#             try:
#                 if text[:3] == "&#x":
#                     return unichr(int(text[3:-1], 16))
#                 else:
#                     return unichr(int(text[2:-1]))
#             except ValueError:
#                 pass
#         else:
#             # named entity
#             try:
#                 text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
#             except KeyError:
#                 pass
#         return text # leave as is
#     return re.sub("&#?\w+;", fixup, text)

def clean_html( raw_html ):
    cleanr = re.compile('<script[\d\D]*?/script>|<style[\d\D]*?/style>')
    cleantext = re.sub(cleanr, '. ', raw_html)
    cleanr = re.compile('<[\s\S]*?>')
    cleantext = re.sub(cleanr, '. ', cleantext)
#     cleantext = unescape(cleantext)
#     print(cleantext)
    return cleantext

def filter_words( tokens ):
    content = [ w.lower() for w in tokens 
               if ( len(w) > 1 )
               and ( w[0]!='&' ) 
               and not w.isdigit() ]
    return content

def get_preNgram( word_pos, index, N ):
    preNgram = []
    p = inflect.engine()
    for m in range(N):
        # if no enough word before the word at index position
        if m > index:
            break
        # generate n-grams
        gram = []
        for start in range( index - m, index + 1 ):
            w = word_pos[start][0];
            if w in string.punctuation or w[0] == '&':
                break
            gram.append( word_pos[start][0] )
        new_ngram = ' '.join(gram)
        if len(new_ngram) > 1 and new_ngram[ len(new_ngram) - 1 ] in ".,":
            new_ngram = new_ngram[ : len(new_ngram) - 1 ]
        preNgram.append( new_ngram )
        
    
    return preNgram

def noun_phrases( word_pos ):
    nps = []
    for index, ( word, pos ) in enumerate( word_pos ):
        if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS') \
        and (word not in string.punctuation) :
            nps.extend( get_preNgram( word_pos, index, 3 ) )
    return nps

def exist_longer( word, wordList ):
    for w in wordList:
        if w[ -1*len( word ) : ] == word:
            return True
    return False 

def str2postokens(text):
    sentences = sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences
    
def get_product_names( raw_page ):
    page_text = clean_html( raw_page )
    word_pos = str2postokens( page_text )
    product_candidates = []
    for sent in word_pos:
        product_candidates.extend( noun_phrases( sent ) )
    
    product_candidates = filter_words( product_candidates )
#     print( product_candidates )
    return product_candidates

path = "../data/MarketShift_Company_Websites/"
for duns_folder in os.listdir( path ):
    print("\n*******************")
    product_candidates = []
    for filename in os.listdir( path + duns_folder ):
        if filename == "Products":
            for pfilename in os.listdir( path + duns_folder + '/Products' ):
                with open( path + duns_folder + "/Products/" + pfilename, "r" ) as page:
                    print( "### Product Page: {0}".format( pfilename ) )
                    product_names = get_product_names( page.read() )
                    product_candidates.extend( list(product_names) )
    
        else:
            with open( path + duns_folder + "/" + filename, "r" ) as page:
                print( filename )
                product_names = get_product_names( page.read() )
                product_candidates.extend( list(product_names) )
                
    fdist = FreqDist( product_candidates )
    fdist = sorted( fdist.items(), key = lambda x:x[1], reverse = True )
    # The top 2% are frequent words
    freq_threshold = fdist[int( round( len( fdist ) * 0.02 ) )][1]
    print( "The freq threshold is %d" % freq_threshold )
    
    print("\nFreq Noun ngrams:")
    for word, freq in fdist:
        if freq >= freq_threshold:
            print( "%s, %d" % (word, freq) )
    
    wordfreq_dict = {}
    for word, freq in fdist:
        if freq >= freq_threshold:
            wordfreq_dict[word] = freq
    
    # sort words from long to short
    fdist = sorted( wordfreq_dict.keys(), key = lambda x: len( word_tokenize(x) ), reverse=True )
    
    print("\n")
    for word in fdist:
        print( "%s, %d" % (word, wordfreq_dict[word]) )
    
    significant_words = []
    for word in fdist:
        word_freq = wordfreq_dict[word]
        
        if exist_longer( word, significant_words ):
            continue
        
        head = " ".join( word_tokenize(word)[1:] )
        head_freq = wordfreq_dict.get( head, 0 )
        if len(word_tokenize(word)) == 1 or word_freq / float( head_freq ) >= 0.8:
            significant_words.append( word )
    
    print("\n")
    for word in significant_words:
        print( "%s, %d" % (word, wordfreq_dict[word]) )
