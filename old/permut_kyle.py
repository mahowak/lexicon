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

############################################################################################## FROM STEVE's CODE
dir_celex = "/Users/km/Documents/celex2/"

"""
will produce folders kyle_celexes and rfiles
"""

try:
    os.mkdir('kyle_rfiles')
except OSError:
    pass

try:
    os.mkdir('kyle_celexes')
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
    a = read_in_celex_lines(dir_celex + "%s/eml/eml.cd" %language)
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
    print ">>>TOTAL NB OF WORDS", len(corpus)
    corpus = [c for c in corpus if c[1] > 0] #freq greater than 0
    corpus = [clean_word(c[0]) for c in corpus] #reduce celex to just pronunciation
    corpus =  [celex_diphthong_sub(c) for c in corpus if "c" not in c and "q" not in c and "0" not in c and "~" not in c]
    print ">>>TOTAL NB OF WORDS", len(corpus)
    corpus = [i for i in corpus if (len(i.split("-")) > minsyll and len(i.split("-")) < maxsyll)]
    print ">>>TOTAL NB OF WORDS", len(corpus)
    corpus = [i for i in corpus if (len(re.sub("-", "", i)) > minlength and len(re.sub("-", "", i)) < maxlength)]
    print ">>>TOTAL NB OF WORDS", len(corpus)
    if match == "length":
        corpus = [clean_syll(c) for c in corpus] #reduce celex to just pronunciation
    print ">>>TOTAL NB OF WORDS", len(corpus)
    if hom == 0: corpus = list(set(corpus))
    print ">>>TOTAL NB OF WORDS", len(corpus)
    f = open("kyle_celexes/" + "_".join([str(i) for i in celex_list]) + ".txt", "w")
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



def makedict(real, n):
    """Build dict to sample from"""
    m = n/2
    d = nltk.defaultdict(list)
    for word in real:
        for num, syll in enumerate(word):
            if num != 0:
                ls = str(len(syll))
                nsylls_lsylls = [str(len(word)), str(num), ls]
                d["_".join(nsylls_lsylls + [syll[:m], word[num - 1][-m:]])] += [syll]
    return(d)

def generate_correct_number_permut(n, corpus_name, hom, match):
    real = [i.strip() for i in  open(corpus_name)]
    real = [i.split("-") for i in real]
    m = n/2
    d = makedict(real, n)
    newcorpus = []
    for word in real:
        for num, syll in enumerate(word):
            ls = str(len(syll))
            if num == 0: newword = [word[0]]
            else:
                possibles = d["_".join([str(len(word)), str(num), ls, syll[:m], word[num - 1][-m:]])]
                random.shuffle(possibles)
                newword += [possibles.pop()]
                repeat = 0
                while repeat < 10: #if you get a homophone, throw it back and try again (does not guarantee no homophones)
                    if len(newword) == len(word) and newword in newcorpus and len(possibles) > 0: 
                        temp = newword[-1]
                        print newword
                        newword[-1] = possibles.pop()
                        possibles += [temp]
                        repeat += 1
                    else: 
                        break
        newcorpus += ["-".join(newword)]
    return newcorpus

    
    


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
						help='min number of syllables', default=0)
	parser.add_argument('--maxSyll', metavar='--maxs', type=int, nargs='?',
						help='max number of syllables', default=20)
	parser.add_argument('--levsyll', metavar='--levs', type=int, nargs='?',
						help='max number of syllables', default=None)
	parser.add_argument('--corpus', metavar='--c', type=str, nargs='?', 
                    help='put corpus file (list of words, one on each lien) to override celex')


	args = parser.parse_args()
	#celex_list = [args.lemma, args.language, args.mono, args.n, args.homophones_celex, args.match, args.levsyll]

	#real_lex = extract_real_lex(dir_celex, args.lemma, args.language,args.mono, args.homophones_celex, args.minl, args.maxl, args.minSyll, args.maxSyll, args.match, celex_list)

	#argslist = "_".join([str(j) for j in celex_list] + [str(args.n), str(args.homophones), str(args.iter)])

	f = open("rfiles/output_kyle_perm.txt", "w")
	f.write("lexicon,homophones,mps,neighbors,avg_lev,num_words\n")
	#real_lex = [clean_syll(c) for c in real_lex] #reduce celex to just pronunciation
	corpus = [i.strip() for i in open(args.corpus, "r").readlines()]
	write_lex_stats(corpus, "real")
    

	for it in range(args.iter):
		print "rfiles/output_kyle_permut.txt"
		write_lex_stats(generate_correct_number_permut(args.n, args.corpus, args.homophones, args.match), it, args.levsyll)
