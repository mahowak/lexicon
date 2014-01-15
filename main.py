from nltk import *
import random, sys, re, os
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
#from gt import *
from calc_stats import *
#from blick import BlickLoader
import copy
#from sets import Set
from lm import *
from nphone import NgramModel
from nsyll import NsyllModel
from pcfg import PCFG
from bigmatch import BigMatch
#from kn import *
from evaluation import *
from generation import *
#from good_turing import *

#b = BlickLoader()



try:
    os.mkdir('Lexicons')
except OSError:
    pass

try:
    os.mkdir('matchedLexica')
except OSError:
    pass




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
                    help='put corpus file - list of words, one on each line')
parser.add_argument('--syll', metavar='--syll', type=int, nargs='?', 
                    help='include syll in celex', default=0)
parser.add_argument('--cv', metavar='--cv', type=int, nargs='?',
                    help='put 1 here to match for CV pattern', default=0)
parser.add_argument('--grammar', metavar='--g', type=str, nargs='?',
                        help='grammar file for pcfg', default="grammars/grammar_output_chom.wlt")
parser.add_argument('--fnc', metavar='--f', type=str, nargs='?',
                     help='evaluate/generate corpus', default="generate")
parser.add_argument('--train', metavar='--t', type=float, nargs='?',
                      help='fraction of corpus use for training', default=0.75)
parser.add_argument('--freq', metavar='--freq', type=int, nargs='?',
                       help='use frequency based lm', default=0)

args = parser.parse_args()
corpus = [i.strip() for i in open(args.corpus, "r").readlines()]
print args.model, len(corpus), "sample", corpus[0]

if args.model == "nphone":
    lm = NgramModel(args.n, corpus)
elif args.model == "nsyll":
    lm = NsyllModel(args.n, corpus)
elif args.model == "pcfg":
    lm = PCFG(args.grammar, NgramModel(args.n, corpus))
elif args.model.startswith("bigmatch"):
    lm = BigMatch(args.n, corpus, args.corpus[:-4] + "_tomatch.txt")


if args.fnc == "generate":
    lm.create_model(corpus)
    o = "Lexicons/lex_" + args.corpus.split("/")[-1][:-4] + "_cv" +  str(args.cv) + "_iter" + str(args.iter) + "_m" + args.model + ".txt"
    if args.model.startswith("bigmatch") == 0:
        lexfile = write_lex_file(o, corpus, args.cv, args.iter, lm, args.homo)
    else:
        lm.match_from_biglist(args.cv, args.iter, args.model.split("_")[-1])
        lexfile = o[:-4] + "_lex.txt"
    write_all(lexfile, 4, 8)
    os.system('Rscript make_hists.R')
else: #evaluate /!\ works only with ngrams as now
    train = random.sample(corpus, int(args.train*len(corpus)))
    test = random.sample(corpus, int((1-args.train)*len(corpus)))
    lm= NgramModel(args.n, train)
    lm.create_model(train, "katz")
    print "Katz Smoothing -----", cross_entropy(lm, test, lm.n), perplexity(cross_entropy(lm, test, lm.n))
    
    #evaluate_model(args.corpus, args.iter, args.model, args.n, args.homo, args.train, args.freq)
#python ngram.py --inputsim=permuted_syllssyll__lemma_english_nphone_1_0_4_8.txt --corpus=notcelex
