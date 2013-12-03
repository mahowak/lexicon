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
    return len(word)


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
        
    
                
def generate_correct_number(n, corpus, homo):
    """Generate number of words to match length, handle homophones being generated"""
    x = NgramModel(n, corpus, 10, homo) #generate 10 at at a time
    lengths_needed = nltk.defaultdict(int)
    for item in corpus:
        lengths_needed[get_cv(item)] += 1
    newwords = []
    while True:
        words = x.generate()
        for w in words:
            if lengths_needed[get_cv(w)] > 0:
                if homo == 1 or w not in newwords:
                    lengths_needed[get_cv(w)] += -1
                    newwords += [w]
            elif sum([lengths_needed[j] for j in lengths_needed.keys()]) == 0: 
                return newwords


    
#build_real_lex(user_celex_path, "lemma", "english", "nphone", 0, 1, 3, 9
parser = argparse.ArgumentParser()
parser.add_argument('--n', metavar='--n', type=int, nargs='?',
                    help='n for ngram', default=3)
parser.add_argument('--homo', metavar='h', type=int, nargs='?',
                    help='0 to exclude homophones being generated, 1 for homophones allowed', default=0)
parser.add_argument('--lemma', metavar='--lem', type=str, nargs='?',
                    help='lemma or wordform in celex', default="lemma")
parser.add_argument('--language', metavar='--lang', type=str, nargs='?',
                    help='', default="english")
parser.add_argument('--model', metavar='--m', type=str, nargs='?',
                    help='should be nphone for ngram model', default="nphone")
parser.add_argument('--minlength', metavar='--minl', type=int, nargs='?',
                    help='minimum length of word allowed from celex', default=4)
parser.add_argument('--maxlength', metavar='--maxl', type=int, nargs='?',
                    help='maximum length of word allowed from celex', default=8)
parser.add_argument('--iter', metavar='--i', type=int, nargs='?',
                    help='number of lexicons to generate', default=2)
parser.add_argument('--corpus', metavar='--c', type=str, nargs='?', help='put corpus file (list of words, one on each lien) to override celex')
parser.add_argument('--syll', metavar='--syll', type=int, nargs='?', help='include syll in celex', default=0)
parser.add_argument('--cv', metavar='--cv', type=int, nargs='?', help='put 1 here to match for CV pattern', default=0)


args = parser.parse_args()

def write_lex_file(corpus, cv, iter, model, n, homo):
    corpus = [i.strip() for i in open(args.corpus, "r").readlines()]
    outfile  = open("Lexicons/lex_" + args.corpus.split("/")[-1][:-4] + "_cv" +  str(args.cv) + "_iter" + str(args.iter) + "_m" + args.model + ".txt", "w")
    for r in corpus:
        outfile.write("-1," + r + "\n")
    for i in range(args.iter):
        for w in enumerate(generate_correct_number(args.n, corpus, args.homo)):
            outfile.write(str(i) + "," +  w[1] + "\n")
        print "generated lexicon: ", str(i)
    outfile.close()
    return

write_lex_file(args.corpus, args.cv, args.iter, args.model, args.n, args.homo)

#python ngram.py --inputsim=permuted_syllssyll__lemma_english_nphone_1_0_4_8.txt --corpus=notcelex
