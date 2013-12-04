from nltk import *
import random, sys, re
import nltk
import argparse
import itertools
import Levenshtein
import time, datetime
import pickle
t = time.time()
import random, sys, re
from math import log, sqrt, exp 
import collections

try:
    os.mkdir('Lexicons')
except OSError:
    pass


vowels = {}
for v in "IE{VQU@i#$u312456789cq0~iI1!eE2@aAoO3#4$6^uU7&5+8*9(0)<>[]{}":
    vowels[v] = 0

def get_cv(word):
    cv = ""
    for letter in word:
        if letter in vowels: 
            cv += "V"
        else: cv += "C"
    if args.cv == 1: return cv
    return len(re.sub("-","",word))


""" --------------ngram model------------"""

def multichooser(context,fd):
    """ Return random choice from multinomial cfd. """
    context = "".join(context)
    cumprob = 0
    rand = random.random()
    possibles = fd[context].samples()
    possibles.sort()
    for possible in possibles:
        cumprob += fd[context].freq(possible)
        if cumprob > rand: return possible
    return



class NgramModel():
    def __init__(self, n, corpus, ngen, homo):
        self.__dict__.update(locals())
        self.cfd = ConditionalFreqDist()
        self.update_cfd(self.n, self.corpus)
        self.cpd_unsmooth = ConditionalProbDist(self.cfd, nltk.MLEProbDist)
#        self.cpd_smooth = ConditionalProbDist(self.cfd, nltk.LaplaceProbDist, len(self.cfd))#issue with SimpleGoodTuringProbDist but also with other smoothing functions, does not work as is for n = 1


    def update_cfd(self, n, corpus):
        """Update cfd using ngrams"""
        for item in corpus:
             item_ngrams = nltk.ngrams(["<S>"]*(n-1) + [i for i in item] + ["<E>"], n)
             for ng in item_ngrams:
                 self.cfd["".join(ng[:-1])].inc(ng[-1])
        return

    def generate_one(self, n, corpus):
        """Generate one word from ngram model."""
        word = ["<S>"]*(self.n - 1)
        while True:
            context = "".join(word[(len(word) - (self.n -1)):len(word)])
            word = word + [multichooser(context, self.cfd)]
            if word[-1] == "<E>":
                break
        return "".join(word[(self.n - 1):-1])

    def generate(self):
        """Generate as many words as specified by ngen"""
        words = [self.generate_one(self.n, self.corpus) for xx in range(self.ngen)]
        return words
    
    def evaluate(self, word):
        """ get the log probability of generating a given word under the language model """
        word = [i for i in word] + ["<E>"]
        fifo = ["<S>"]*(self.n -1)
        p_gram=0
        for ch in word:
            context = "".join(fifo[(len(fifo) - (self.n - 1)):len(fifo)])
            try:
                p_gram += log(self.cpd_unsmooth[context].prob(ch))#smooth or unsmooth TODO: make it as a param (evaluate vs. generate) 
            except ValueError:
                return 0.0
            fifo.append(ch)
        return p_gram 
                                                            
                                                         
    def pword_avg(self, corpus):
        """Calculate the estimated entropy of the n-gram model for a given lexicon"""
        p = 0.0
        for i in corpus:
            p += -self.evaluate(i)
        return p / float(len(corpus))




class NsyllModel():
    def __init__(self, n, corpus, ngen, homo):
        self.__dict__.update(locals())
        self.cfd = ConditionalFreqDist()
        self.update_cfd_syll(self.n, self.corpus)
        self.cpd_unsmooth = ConditionalProbDist(self.cfd, nltk.MLEProbDist)
#        self.cpd_smooth = ConditionalProbDist(self.cfd, nltk.LaplaceProbDist, len(self.cfd))#issue with SimpleGoodTuringProbDist but also with other smoothing functions, does not work as is for n = 1


    def update_cfd_syll(self, n, corpus):
        """Update cfd using ngrams for syllables"""
        for item in corpus:
             item_ngrams = nltk.ngrams(["<S>"]*(n-1) + [i for i in item.split("-")] + ["<E>"], n)
             for i,ng in enumerate(item_ngrams):
                 self.cfd["".join(ng[:-1])].inc(ng[-1])
        return

    def generate_one(self, n, corpus):
        """Generate one word from ngram model."""
        word = ["<S>"]*(self.n - 1)
        while True:
            context = "".join(word[(len(word) - (self.n -1)):len(word)])
            word = word + ["-"] + [multichooser(context, self.cfd)]
            if word[-1] == "<E>":
                break
        return "".join(word[(self.n):-2])

    def generate(self):
        """Generate as many words as specified by ngen"""
        words = [self.generate_one(self.n, self.corpus) for xx in range(self.ngen)]
        return words
    
    def evaluate(self, word):
        """ get the log probability of generating a given word under the language model """
        word = word.split("-") + ["<E>"]
        fifo = ["<S>"]*(self.n -1)
        p_gram=0
        for i, syll in enumerate(word):
            context = "".join(fifo[(len(fifo) - (self.n - 1)):len(fifo)])
            try:
                p_gram += log(self.cpd_unsmooth[context].prob(syll))#smooth or unsmooth TODO: make it as a param (evaluate vs. generate) 
            except ValueError:
                return 0.0
            fifo.append(syll)
        return p_gram 
                                                            
                                                         
    def pword_avg(self, corpus):
        """Calculate the average probability of a word under the model"""
        p = 0.0
        for i in corpus:
            p += -self.evaluate(i)
        return p / float(len(corpus))





""" --------------pcfg model------------"""

def format_grammar(f):
 	print ">>> Loading cfg counts ..."
 	f_out = open("grammars/grammar_formated.txt", 'w')
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
            return i, float(weights[i][1])


            
class PCFG(object):
    def __init__(self, ngen, ngram = None):
    	self.__dict__.update(locals())
        self.prod = collections.defaultdict(list)
        self.reject = 0
        self.p_word=collections.defaultdict(float)

    def add_prod(self, lhs, rhs):
        """ Add production to the grammar. 'rhs' can
            be several productions separated by '|'.
            Each production is a sequence of symbols
            separated by whitespace.

            Usage:
                grammar.add_prod('S', 'NP VP')
                grammar.add_prod('Num', '1|2|3|4')
        """
        prods = rhs.split('|')
        for prod in prods:
        	self.prod[lhs].append(tuple(prod.strip().split(':')))
        	
    def generate(self):
        """Generate as many words as specified by ngen"""
        words = [self.filter_word() for xx in range(self.ngen)]
        return words
        
    def generate_one(self, symbol='Word'):
        """ Generate a random word from the
            grammar, starting with the given
            symbol.
        """
        word = ''
        tot_p = 0
        if '+' in symbol:
        	s = symbol.split('+')
        else:
            rand_prod, p = weighted_choice(self.prod[symbol])
            tot_p += log(p)
            s =  [x for x in self.prod[symbol][rand_prod][0].strip().split(",")]
        for sym in s:
            if sym in self.prod or '+' in sym:# for non-terminals, recurse
                w, p = self.generate_one(sym)
                word += w
                tot_p += p
            else:
                word += sym 
        return word, tot_p

    def filter_word(self):
        word, p = self.generate_one(symbol='Word')
        if self.ngram != None:
            while self.ngram.evaluate(word)==0:
                word, p = self.generate_one(symbol='Word')
                self.reject +=1
        self.p_word[word] = p
        return word
        
	
    def pword_avg(self, corpus): 
        p = 0.0
        for item in corpus:
#            print self.p_word[item], self.ngram.evaluate(item)
            p += -self.p_word[item]
        return p /float(len(corpus))




""" --------------generate------------"""
             
def generate_correct_number(n, corpus, homo, x):
    """Generate number of words to match length, handle homophones being generated"""
    #x = NgramModel(n, corpus, 10, homo) #generate 10 at at a time
    lengths_needed = nltk.defaultdict(int)
    for item in corpus:
        lengths_needed[get_cv(item)] += 1
    newwords = []
    exist =0
    while True:
        words = x.generate()
        for w in words:
            if lengths_needed[get_cv(w)] > 0:
                if homo == 1 or w not in newwords:
                    lengths_needed[get_cv(w)] += -1
#                    if sum([lengths_needed[j] for j in lengths_needed.keys()]) %1000 == 0:
#                        print sum([lengths_needed[j] for j in lengths_needed.keys()])
                    newwords += [w]
                    if w in corpus:
                        exist +=1
            elif sum([lengths_needed[j] for j in lengths_needed.keys()]) == 0: 
                print "nb of real words", exist
                return newwords



def write_lex_file(corpus, cv, iter, model, n, homo):
    corpus = [i.strip() for i in open(args.corpus, "r").readlines()]
    outfile  = open("Lexicons/lex_" + args.corpus.split("/")[-1][:-4] + "_cv" +  str(args.cv) + "_iter" + str(args.iter) + "_m" + args.model + ".txt", "w")
    print model, len(corpus)
    if model == "nphone":#TO COMPLETE once other models will been defined
        lm = NgramModel(n, corpus, 1, homo)
    elif model == "nsyll":
        lm = NsyllModel(n, corpus, 1, homo)
    elif model == "pcfg":
    	g = open(args.grammar, 'r')
        format_grammar(g)
        g.close()
        lm =PCFG(1, NgramModel(n, corpus, 1, homo))
        g = open("grammars/grammar_formated.txt", 'r')
        for line in g:
            line.rstrip('\n')
            A, B = line.split("\t")
            lm.add_prod(A, B)
	    	
    for r in corpus:
        outfile.write("-1," + re.sub("-","",r) + "\n")
    print "lexicon: ", lm.pword_avg(corpus) # /!\ need an entropy function in the class model of the lm
    for i in range(args.iter):
        gen_lex= generate_correct_number(args.n, corpus, args.homo, lm)
        for w in enumerate(gen_lex):
            outfile.write(str(i) + "," +  re.sub("-","",w[1]) + "\n")
        print "generated lexicon: ", str(i), lm.pword_avg(gen_lex)# /!\ need an entropy function in the class model of the lm
    outfile.close()
    return



""" --------------evaluate------------"""

def evaluate_model(corpus, iter, model, n, homo, train_frac):#TO DO: create a file for output
    """Evaluate corpus with a training set and a test set using a given model """
    corpus = [i.strip() for i in open(args.corpus, "r").readlines()]
    for i in xrange(iter):
        train_corpus = random.sample(corpus, int(train_frac*len(corpus)))
        test_corpus = random.sample(corpus, int((1-train_frac)*len(corpus)))
        if model == "nphone":#TO COMPLETE once other models will been defined
            lm = NgramModel(n, train_corpus, 1, homo)
	    print iter, str(model) + " evaluation based on " + str(train_frac) + " of corpus:", lm.entropy_avg(test_corpus), lm.perplexity(test_corpus)


""" --------------main------------"""

#build_real_lex(user_celex_path, "lemma", "english", "nphone", 0, 1, 3, 9
parser = argparse.ArgumentParser()
parser.add_argument('--n', metavar='--n', type=int, nargs='?',
                    help='n for ngram', default=3)
parser.add_argument('--homo', metavar='h', type=int, nargs='?',
                    help='0 to exclude homophones being generated, 1 for homophones allowed', default=0)
#parser.add_argument('--lemma', metavar='--lem', type=str, nargs='?',
#                    help='lemma or wordform in celex', default="lemma")
#parser.add_argument('--language', metavar='--lang', type=str, nargs='?',
#                    help='', default="english")
parser.add_argument('--model', metavar='--m', type=str, nargs='?',
                    help='should be nphone for ngram model', default="nphone")
#parser.add_argument('--minlength', metavar='--minl', type=int, nargs='?',
#                   help='minimum length of word allowed from celex', default=4)
#parser.add_argument('--maxlength', metavar='--maxl', type=int, nargs='?',
#                    help='maximum length of word allowed from celex', default=8)
parser.add_argument('--iter', metavar='--i', type=int, nargs='?',
                    help='number of lexicons to generate', default=2)
parser.add_argument('--corpus', metavar='--c', type=str, nargs='?', 
                    help='put corpus file (list of words, one on each lien) to override celex')
parser.add_argument('--syll', metavar='--syll', type=int, nargs='?', 
                    help='include syll in celex', default=0)
parser.add_argument('--cv', metavar='--cv', type=int, nargs='?',
                    help='put 1 here to match for CV pattern', default=0)
parser.add_argument('--grammar', metavar='--g', type=str, nargs='?',
	                    help='grammar file for pcfg', default="grammars/grammar_mono.wlt")
parser.add_argument('--fnc', metavar='--f', type=str, nargs='?',
                     help='evaluate/generate corpus', default="generate")
parser.add_argument('--train', metavar='--t', type=float, nargs='?',
                      help='fraction of corpus use for training', default=0.75)

args = parser.parse_args()

if args.fnc == "generate":
    write_lex_file(args.corpus, args.cv, args.iter, args.model, args.n, args.homo)
else: #evaluate /!\ works only with ngrams as now
    evaluate_model(args.corpus, args.iter, args.model, args.n, args.homo, args.train)
#python ngram.py --inputsim=permuted_syllssyll__lemma_english_nphone_1_0_4_8.txt --corpus=notcelex
