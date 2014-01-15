from math import sqrt, log, exp, sqrt
import sys
import collections
import random
import time
#from numpy import c_, exp, log, inf, NaN, sqrt
import argparse
import itertools
import Levenshtein
import itertools 
import re
import os
import nltk
from sets import Set

############################################################################################## FROM STEVE's CODE
dir_celex = "/Users/isa/Desktop/PhD/3. Projets/10. Etude du Lexique/celex_raw/"

"""
will produce folders celexes and rfiles
"""

try: 
    os.mkdir('rfiles')
except OSError: 
    pass

try:
    os.mkdir('celexes')
except OSError:
    pass
    
    
#######################################CELEX 
def clean_word(word):
    """Remove stress."""
    word = re.sub("'", "", word)
    word = re.sub('"', "", word)
    #word = re.sub("-", "", word)
    return word
    
def clean_syll(word):
    """syllable boundaries."""
    word = re.sub("-", "", word)
    return word

def celex_diphthong_sub(word):
    """ Do celex dipthong subs. """
    word = re.sub("2", "#I", word)
    word = re.sub("4", "QI", word)
    word = re.sub("6", "#U", word)
    word = re.sub("7", "I@", word)
    word = re.sub("8", "E@", word)
    word = re.sub("9", "U@", word)
    return word
    
def read_in_celex_lines(path):
    """ Return lines in given celex file. """
    return [line.strip().split("\\") for line in open(path, "r").readlines()]


def get_celex_monos(path, language):
    """ Return list of celex ids for monomorphemes. """
    a = read_in_celex_lines(dir_celex + "%s/dml/dml.cd" %language)
    return [i[0] for i in a if i[3] == "M"]

def get_celex_path(path, lemma, language):
    """ Return celex path, given root, lemma, language. """
    return path + language + "/{lang}p{lem}/{lang}p{lem}.cd".format(lang=language[0], lem=lemma[0])


def celex_pron_loc(language, lemma):
    """ Return location of pronunciation in celex, given language. """
    pron = 5
    if language == "german" or language== "dutch": pron = pron -2 #german one less
    if lemma == "wordform": pron += 1
    return pron

def extract_celex_info(line, language="english", lemma="lemma"):
    """ Return celex word (ortho or phonemic) and its freq from celex line. """
    if line[1].isalpha() and line[1].islower() and "-" not in line[1] and "." not in line[1] and "'" not in line[1] and " " not in line[1]:
        return line[celex_pron_loc(language, lemma)], line[2], line[1] #pron, frequency
    return


def build_celex_corpus(path, language, lemma, mono):
    """ Return corpus from celex, given path and parameters. """
    lines = read_in_celex_lines(path); corpus = []; monos = []
    if mono == 1: monos = get_celex_monos(path, language)
    corpus = [extract_celex_info(line, language, lemma) for line in lines if (mono == 0 or line[0] in monos)]
    return [i for i in corpus if i != None]


def extract_real_lex(path, lemma, language, mono, hom,minlength, maxlength, minsyll, maxsyll, match, celex_list):
    celex_path = get_celex_path(path, lemma, language)
    lengths = nltk.defaultdict(int)
    print celex_path
    corpus = build_celex_corpus(celex_path, language, lemma, mono)
    #corpus = [c for c in corpus if c[1] > 0] #freq greater than 0
    corpus = [clean_word(c[0]) for c in corpus] #reduce celex to just pronunciation
    corpus =  [celex_diphthong_sub(c) for c in corpus if "c" not in c and "q" not in c and "0" not in c and "~" not in c]
    corpus = [i for i in corpus if (len(i.split("-")) > minsyll and len(i.split("-")) < maxsyll)]
    corpus = [i for i in corpus if (len(re.sub("-", "", i)) > minlength and len(re.sub("-", "", i)) < maxlength)]
    if match == "length":
        corpus = [clean_syll(c) for c in corpus] #reduce celex to just pronunciation
    if hom == 0: corpus = list(set(corpus))
    print ">>>TOTAL NB OF WORDS", len(corpus)
    f = open("celexes/" + "_".join([str(i) for i in celex_list]) + ".txt", "w")
    for line in corpus: 
    	lengths[len(re.sub("-", "", line))] +=1
    	f.write(line + "\n")
    f.close()
    print ">>> Word-Length frequencies of lexicon to match"
    for k in lengths.keys():
		print k, lengths[k]
    return corpus


############################################################################################## END STEVE's CODE

##FOR NGRAMS

def count_ngrams(f, N):
	""" count ngrams frequencies (characters) from a file where there is one word per line """
	#print ">>> Computing n-gram frequency counts ..."
	#freqs[n] contains n-gram frequencies, freqs[n-1] contains (n-1)-gram frequencies, etc.
	freqs = collections.defaultdict(lambda: collections.defaultdict(int))
	tot =0
	for line in f:
		tot +=1
		w = line
		fifo = [':'] * N  # initialise n-gram storage with ":" as stop characters
		for i in range(N-1):
			w += ':'
		for c in w: 
			fifo.pop(0)
			fifo.append(c)
			for idx in range(N):	
				n = idx + 1
				ngram = ''.join(fifo[:n]) # n-gram = first n characters in fifo
				freqs[n][ngram] += 1
	return freqs
	        

def MLE(ngram, freqs):
	""" maximum likelihood estimate (unsmoothed) for ngrams """
	n = len(ngram)
	if ngram in freqs[n]:
		numerator = freqs[n][ngram]
	else:
		return 0.0
	if n == 1:
		denominator = sum(freqs[1].values()) # unigram probability (unconditional): f(x) / corpus_size
	else:
		history = ngram[0:n-1] # conditional ngram probability: f(x_1 .. x_n) / f(x_1 .. x_{n-1})
		if history in freqs[n-1]:
			denominator = freqs[n-1][history]
		else:
			return 0.0
	return float(numerator)/denominator



def pgram(w, freqs, N):
	""" return ngram proba for a given word w """
        mle = 0
        fifo = [':'] * N  
        for i in range(N-1):
        	w += ':'
        for c in w:
                fifo.pop(0)
                fifo.append(c)
                n = N
                ngram = ''.join(fifo[:n])   
                p = log(MLE(ngram, freqs))
                mle += p
        return mle


## FOR PERMUTATION

def count_syll(f):
	""" return syllabic count for a given length (in syllables) and a given position  """
	sylls = collections.defaultdict(lambda: collections.defaultdict(list))
	s_count = collections.defaultdict(int)
	for line in f:
		w_syll = line.rstrip().split('-')
		nb_syll = len(w_syll)
		word = re.sub("-", "", line).rstrip()
		for pos, syll in enumerate(w_syll):
			sylls[nb_syll][pos].append(syll)
	return sylls

def slice_start(source, string, L):
	""" return all the values of a dict starting with a given sequence of length L """
	newdict = []
	for val in source:
		if val.startswith(string) and len(val) == L:
			newdict.append(val)
	return newdict
    
def slice_end(source, string, L):
	""" return all the values of a dict ending with a given sequence of length L """
	newdict = []
	for val in source:
		if val.endswith(string) and len(val) == L:
			newdict.append(val)
	return newdict
    
    
    
####FOR GENERATION

def generate_correct_number_permut(n, corpus_name, homo, match):
	lengths_needed = nltk.defaultdict(int)
	lkl=[]
	hom=0
	sum_lkl=0
	c = open(corpus_name, "r").readlines()
	corpus = [i.strip() for i in c]
	corpus_w = [clean_syll(c) for c in corpus]
	freqs = count_ngrams(corpus_w, n)
	for total, item in enumerate(corpus):
		lengths_needed[len(re.sub("-", "", item))] += 1
		temp=0
		sum_lkl += pgram(re.sub("-", "", item), freqs, n)
		for i, s in enumerate(item.split("-")[:-1]):
			ph1= s[-1]
			ph2= item.split("-")[i+1][0]
			temp+= freqs[n][ph1+ph2]
		total +=1
		lkl += [temp]
	corpus_tup = zip(corpus, lkl)
	corpus_tup = sorted(corpus_tup, key=lambda tup: tup[1],reverse=True) #sorting corpus to make words having less frequent bigrams first (whichis dumb for more than 2 syllabic words: TODO)
	avg = sum_lkl/total
	print ">>> AVG NGRAM PROB REAL LEX", avg
	lengths_new = nltk.defaultdict(int)
	while sum(lengths_new.values()) != sum(lengths_needed.values()): #loop til we converge
		lengths_new = nltk.defaultdict(int)
		sylls = count_syll(corpus)
		newwords = []
		sum_lkl=0
		exist = 0
		hom=0
		timeout = time.time() + 60*0.3 #when it converges it doesnt take time, so a silly stoping criteria: a time limit
		for j, (w, l) in enumerate(corpus_tup):
			w = w.split("-")
			n_syll = len(w)
			while True:
				nonword = random.choice(slice_end(sylls[n_syll][0], w[0][-1], len(w[0])))
				for i, s in enumerate(w[1:]):
					ph1= nonword[-1]
					ph2= s[0]
					bigram = ph1+ph2
					set = slice_start(sylls[n_syll][i+1], ph2, len(s))
					nonword += "-"+random.choice(slice_end(set, s[-1], len(s)))
				if nonword not in newwords or homo == 1:
					for i, k in enumerate(nonword.split("-")):
						sylls[n_syll][i].remove(k)
					newwords += [nonword]
					nonword = re.sub("-", "", nonword)
					if nonword in corpus_w:
						exist+=1
					sum_lkl += pgram(nonword, freqs, n)
					lengths_new[len(nonword)] +=1
					break
				else:
					hom+=1
				if time.time() > timeout:
					break
		avg = sum_lkl/total
	print ">>> AVG NGRAM PROB RAND LEX", avg
	print "real words:", exist
	print "hom rejected:", hom
	print "non hom?", len(Set(newwords))
	print "total nb:", sum(lengths_new.values())
	return newwords
		
    
class PCFG(object):
    def __init__(self):
        self.prod = collections.defaultdict(list)

    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('NT', 'VP PP')
                grammar.add_prod('Digit', '1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
        	self.prod[lhs].append(tuple(prod.strip().split(':')))

    def gen_random(self, symbol):
        """ Generate a random word from the
            grammar, starting with the given
            symbol.
        """
        word = ''
        # select one production of this symbol randomly
        #rand_prod = random.choice(self.prod[symbol])
        #print self.prod[symbol]
        #print "node",symbol
        if '+' in symbol:
        	s = symbol.split('+')
        	#sentence += self.gen_random(symbol1)
        	#sentence += self.gen_random(symbol2)
        else:
        	rand_prod = weighted_choice(self.prod[symbol])
        	#print self.prod[symbol], rand_prod, self.prod[symbol][rand_prod][0]
        	s =  [x for x in self.prod[symbol][rand_prod][0].strip().split(",")]
        for sym in s:
        	if sym in self.prod or '+' in sym:# for non-terminals, recurse
        		word += self.gen_random(sym)
        	else:
        		word += sym 

        return word
        
        

def weighted_choice(weights):
    totals = []
    running_total = 0
    for w, p in weights:
        running_total += float(p)
        totals.append(running_total)

    rnd = random.random() * running_total
    #print rnd
    for i, total in enumerate(totals):
        if rnd < total:
            return i
            
 
def format_grammar(f):
 	print ">>> Loading cfg counts ..."
 	f_out = open("grammar_formated.txt", 'w')
	gram = collections.defaultdict(lambda: collections.defaultdict(int))
	tot = collections.defaultdict(int)
	for line in f:
		freq, rule = line.split("\t")
		A, B = rule.split(" --> ")
		B = B.rstrip('\n')
		#print A, B, len(B), freq
		if " " in B:
			B1, B2 = B.split()
			gram[A][B1+"+"+B2] = int(freq)
			tot[A] += int(freq)
		else:
			gram[A][B] = int(freq)
			tot[A] += int(freq)
	
	for i in gram.keys():
		f_out.write(i+"\t")
		for j in sorted(gram[i].keys()):
			if j == sorted(gram[i].keys())[-1]:
				f_out.write(j+":"+str(float(gram[i][j])/tot[i]))
			else:
				f_out.write(j+":"+str(float(gram[i][j])/tot[i])+" | ")
		f_out.write("\n")
	
	print ">>> Done and wrote in file"


	
			
						
			
			
def write_lex_stats(b, num, syll = None):
    """Use Levenshtein package to calcualte lev and count up mps, neighbors, etc"""
    total = 0.
    mps = 0
    neighbors = 0
    homophones = 0
    lev_total = 0
    for item in itertools.combinations(b, 2):
    	if syll != None:
	    	#if len(item[0].split("-"))==syll or len(item[1].split("-"))==syll:
		    lev = Levenshtein.distance(re.sub("-", "", item[0]), re.sub("-", "", item[1]))
		    if lev == 0: homophones += 1
		    elif lev == 1: 
		        neighbors += 1
		        if len(re.sub("-", "", item[0])) == len(re.sub("-", "", item[1])): mps += 1
		    total += 1
		    lev_total += lev
        else:
	   		lev = Levenshtein.distance(re.sub("-", "", item[0]), re.sub("-", "", item[1]))
	   		if lev == 0: homophones += 1
	   		elif lev == 1: 
	   			neighbors += 1
	   			if len(re.sub("-", "", item[0])) == len(re.sub("-", "", item[1])): mps += 1
   			total += 1
   			lev_total += lev
    print str(num)
    f.write(",".join([str(x) for x in [num, homophones, mps, neighbors, lev_total/total, len(b)] ]) + "\n")
    return
    
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--n', metavar='--n', type=int, nargs='?',
	                    help='n for ngram', default=3)
	parser.add_argument('--homophones', metavar='--h', type=int, nargs='?',
	                    help='0 exclude homophones, 1 include homophones', default=0)
	parser.add_argument('--lemma', metavar='--lem', type=str, nargs='?',
	                    help='lemma or wordform in celex', default="lemma")
	parser.add_argument('--language', metavar='--lang', type=str, nargs='?',
	                    help='', default="english")
	parser.add_argument('--mono', metavar='--mono', type=int, nargs='?',
	                    help='1 mono only, 0 all', default=1)
	parser.add_argument('--homophones_celex', metavar='--h_celex', type=int, nargs='?',
	                    help='0 exclude homophones in celex, 1 include homophones', default=0)
	parser.add_argument('--iter', metavar='--i', type=int, nargs='?',
	                    help='number of sampling', default=10)
	parser.add_argument('--match', metavar='--m', type=str, nargs='?',
	                    help='length or syll matched', default="length")
	parser.add_argument('--minl', metavar='--minl', type=int, nargs='?',
                   		 help='minimum length of word allowed from celex', default=3)
	parser.add_argument('--maxl', metavar='--maxl', type=int, nargs='?',
                    	help='maximum length of word allowed from celex', default=9)
	parser.add_argument('--minSyll', metavar='--mins', type=int, nargs='?',
						help='min number of syllables', default=1)
	parser.add_argument('--maxSyll', metavar='--maxs', type=int, nargs='?',
						help='max number of syllables', default=10)
	parser.add_argument('--levsyll', metavar='--levs', type=int, nargs='?',
						help='max number of syllables', default=None)
	parser.add_argument('--corpus', metavar='--c', type=str, nargs='?', 
                    help='put corpus file (list of words, one on each lien) to override celex')


	args = parser.parse_args()
	#celex_list = [args.lemma, args.language, args.mono, args.n, args.homophones_celex, args.match, args.levsyll]

	#real_lex = extract_real_lex(dir_celex, args.lemma, args.language,args.mono, args.homophones_celex, args.minl, args.maxl, args.minSyll, args.maxSyll, args.match, celex_list)

	#argslist = "_".join([str(j) for j in celex_list] + [str(args.n), str(args.homophones), str(args.iter)])

	f = open("rfiles/output_perm.txt", "w")
	f.write("lexicon,homophones,mps,neighbors,avg_lev,num_words\n")
	#real_lex = [clean_syll(c) for c in real_lex] #reduce celex to just pronunciation
	corpus = [i.strip() for i in open(args.corpus, "r").readlines()]
	write_lex_stats(corpus, "real")



	for it in range(args.iter):
		print "rfiles/output.txt"
		write_lex_stats(generate_correct_number_permut(args.n, args.corpus, args.homophones, args.match), it, args.levsyll)


	
