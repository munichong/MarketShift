'''
Created on Feb 4, 2015

@author: munichong
'''
import nltk, string

support_threshold = [ 0.002, 0.001, 0.001, 0.001 ]
min_conf_threshold = [ -1, 0.3, 0.2, 0.3 ]
rel_conf_threshold = [ -1, 0.3, 0.2, 0.3 ]
post_conf_threshold = [ -1, 0.3, 0.2, 0.3 ]
pre_conf_threshold = [ -1, 0.3, 0.2, 0.3 ]
dominance_thres = [ -1, 1.3, 1.3, 1.3 ]

class KGram:
    def __init__(self, kgram, freq):
        """ e.g. kgram = ['a', 'b'] """
        self.kgram_tuple = kgram 
        self.k = len( kgram )
        self.freq = freq
        self.prefix = kgram[ : len( kgram ) - 1 ]
        self.suffix = kgram[ 1 : ]
    
    def set_subconcept_freqs(self, prefix_freq, suffix_freq):
        self.prefix_freq = prefix_freq
        self.pre_conf = self.freq / float( prefix_freq )
        self.suffix_freq = suffix_freq
        self.post_conf = self.freq / float( suffix_freq )
        self.min_conf = self.pre_conf if self.pre_conf < self.post_conf else self.post_conf
        self.max_conf = self.pre_conf if self.pre_conf > self.post_conf else self.post_conf
        
    def set_relConf(self, max_conf_pre, max_conf_post  ):   
        denominator = max_conf_pre if max_conf_pre > max_conf_post else max_conf_post
        self.rel_conf = self.min_conf / denominator

def concept_extraction( kgrams_dict, n ):
    candidate_concepts = []
    for k in range( 1, n + 1 ):
        print( "\n****** iteration " + str(k) )
        discard_concepts = []
        for kgram in kgrams_dict.values():
            # if the length is not current focus
            if kgram.k != k:
                continue
            
            if kgram.kgram_tuple == ('film', 'sensors'):
                pass
            
            is_candidate = candidateConceptCheck( kgram, candidate_concepts, discard_concepts )
            
            if is_candidate:
                print( kgram.kgram_tuple )
                candidate_concepts.append( kgram )
        
        for cc in candidate_concepts[:]:
            if cc.kgram_tuple in discard_concepts:
                candidate_concepts.remove( cc )
#         print candidate_concepts
    
    print( "\n****** Final concepts:" )    
    confirmed_concepts = []
    for kgram in candidate_concepts:
        if not containsStopWords( kgram ):
            print( kgram.kgram_tuple )
            confirmed_concepts.append( kgram )
            
    return confirmed_concepts
    
def candidateConceptCheck( kgram, candidate_concepts, discard_concepts ):
    para_index = kgram.k - 1
#     print( str(kgram.freq) )
    if kgram.freq > support_threshold[ para_index ]:
        # if this kgram is a 1-word itemset.
        if kgram.k == 1:
            return True
        
        if ( kgram.min_conf > min_conf_threshold[ para_index ] and 
             kgram.rel_conf > rel_conf_threshold[ para_index ] ):
            if kgram.k > 2:
                discard_concepts.append( kgram.prefix )
                discard_concepts.append( kgram.suffix )
            return True
        
        if ( kgram.prefix in candidate_concepts and
            kgram.post_conf > dominance_thres[ para_index ] * kgram.pre_conf and
            kgram.post_conf > post_conf_threshold[ para_index ] ):
            discard_concepts.append( kgram.suffix )
            return True
        
        if ( kgram.suffix in candidate_concepts and
            kgram.pre_conf > dominance_thres[ para_index ] * kgram.post_conf and
            kgram.pre_conf > pre_conf_threshold[ para_index ] ):
            discard_concepts.append( kgram.suffix )
            return True
    return False

def containsStopWords( kgram ):
    conjunctions = ['after', 'although', 'and', 'as', 'if', 'because', 'before', 'both', 'but',
                   'either', 'even', 'though', 'for', 'by', 'of', 'how', 'however', 'only', 'in',
                   'neither', 'nor', 'now', 'once', 'or', 'provided', 'rather', 'than', 'then', 
                   'since', 'that', 'till', 'unless', 'until', 'when', 'whenever', 'where', 'whereas',
                   'wherever', 'whether', 'while', 'yet' ]
    articles = ['a', 'one', 'an', 'the']
    pronouns = ['all', 'another', 'any', 'anybody', 'anyone', 'anything', 'both', 'each', 'other', 
                'either', 'everybody', 'everyone', 'everthing', 'few', 'he', 'her', 'hers', 'herself',
                'him', 'himself', 'his', 'i', 'it', 'its', 'itself', 'many', 'me', 'mine', 'more',
                'most', 'much', 'myself', 'neither', 'no', 'nobody', 'yes', 'none', 'nothing', 'another',
                'other', 'others', 'ours', 'ourselves', 'several', 'she', 'some', 'somebody', 'someone',
                'something', 'theirs', 'their', 'them', 'themselves', 'there', 'they', 'this', 'those',
                'us', 'we', 'what', 'whatever', 'which', 'whichever', 'who', 'whoever', 'whom', 'whomever',
                'whose', 'you', 'your', 'yours', 'yourself', 'yourselves' ]
    stopwords = nltk.corpus.stopwords.words('english')
    punctuations = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
    
    for word in kgram.kgram_tuple:
        if ( word in conjunctions or word in articles or 
             word in pronouns or word in stopwords or 
             word in punctuations or word.isdigit() or 
             word in string.printable ):
            return True
    
    return False