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
import collections
from calc_stats import *
import copy
from lm import *
from nphone import NgramModel
from nsyll import NsyllModel
from pcfg import PCFG
from bigmatch import BigMatch
#from kn import *
from evaluation import *
from generation import *
from perplexity import *



try:
    os.mkdir('Lexicons')
except OSError:
    pass

try:
    os.mkdir('matchedLexica')
except OSError:
    pass

try:
    os.mkdir('Graph')
except OSError:
    pass

try:
    os.mkdir('evaluation')
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
parser.add_argument('--minlength', metavar='--minl', type=int, nargs='?',
                   help='minimum length of word allowed from celex', default=3)
parser.add_argument('--maxlength', metavar='--maxl', type=int, nargs='?',
                    help='maximum length of word allowed from celex', default=8)
parser.add_argument('--iter', metavar='--i', type=int, nargs='?',
                    help='number of lexicons to generate', default=2)
parser.add_argument('--corpus', metavar='--c', type=str, nargs='?', 
                    help='put corpus file - list of words, one on each line')
parser.add_argument('--syll', metavar='--syll', type=int, nargs='?', 
                    help='include syll in celex', default=0)
parser.add_argument('--cv', metavar='--cv', type=int, nargs='?',
                    help='put 1 here to match for CV pattern', default=0)
parser.add_argument('--grammar', metavar='--g', type=str, nargs='?',
                        help='grammar file for pcfg', default="grammars/grammar_38.wlt")
parser.add_argument('--fnc', metavar='--f', type=str, nargs='?',
                     help='evaluate/generate corpus', default="generate")
parser.add_argument('--train', metavar='--t', type=float, nargs='?',
                      help='fraction of corpus use for training', default=0.75)
parser.add_argument('--freq', metavar='--freq', type=int, nargs='?',
                       help='use frequency based lm', default=0)
parser.add_argument('--graph', metavar='--g', type=int, nargs='?',
                        help='output graph', default=0)

args = parser.parse_args()
corpus = [i.strip() for i in open(args.corpus, "r").readlines()]
#train = [re.sub(" ","-",i.strip()) for i in open("train_syll.txt", "r").readlines()]
#test = [re.sub(" ","-",i.strip()) for i in open("test_syll.txt", "r").readlines()]
print args.model, len(corpus), "sample", corpus[0]

if args.model == "nphone":
    lm = NgramModel(args.n, corpus)
elif args.model == "nsyll":
    if args.corpus.startswith("celexes/syll"):
        lm = NsyllModel(args.n, corpus)
    else:
        print "Use syll__ file for this model"
        sys.exit()
elif args.model == "pcfg":
    if args.corpus.startswith("celexes/syll"):
        lm = PCFG(args.grammar, NgramModel(args.n, corpus))
    else:
        print "Use syll__ file for this model"
        sys.exit()
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
    write_all(lexfile, args.minlength, args.maxlength, args.graph)
    os.system('Rscript make_hists.R')
else: #evaluate /!\ works only with ngrams as now
    o = "evaluation/eval_" + args.corpus.split("/")[-1][:-4] + "_cv" +  str(args.cv) + "_iter" + str(args.iter) + "_m" + args.model + "_n" + str(args.n) + ".txt"
    out = open(o, 'w')
    out.write("i,smoothing,model,ppl,logprob\n")
    for i in range(args.iter):
        train = random.sample(corpus, int(args.train*len(corpus)))
        test = random.sample(corpus, int((1-args.train)*len(corpus)))
#        if args.model == "nphone":
#            lm= NgramModel(args.n, train)
#        elif args.model == "nsyll":
#            lm = NsyllModel(args.n, train)
#        elif args.model == "pcfg":
#            lm = PCFG(args.grammar, NgramModel(args.n, train))
#        else:
#            print "not yet implemented"
#            sys.exit()
#        lm.create_model(train, 0.1)
#        print i,"Laplace smoothing", logprob(lm, test), perplexity(cross_entropy(lm, test))
        if args.model == 'nphone':
            srilm_train = [" ".join(list(w)) for w in train] 
            srilm_test = [" ".join(list(w)) for w in test]
        if args.model == 'nsyll':
            srilm_train = [re.sub("-", " ", w) for w in train] 
            srilm_test = [re.sub("-", " ", w) for w in test]
        wb = compute(srilm_train, srilm_test, args.n, 'wbdiscount')
        add = compute(srilm_train, srilm_test, args.n, 'addsmooth', .1)
        out.write(str(i)+","+"srilm_wb"+","+args.model+str(args.n)+","+str(wb[0])+","+str(-wb[1])+"\n")
        out.write(str(i)+","+"srilm_add"+","+args.model+str(args.n)+","+str(add[0])+","+str(-add[1])+"\n")

        print i, "srilm_wb", args.model, args.n, wb[0], -wb[1]
        print i, "srilm_add", args.model, args.n, add[0], -add[1]

    os.system('Rscript eval.r')
    #evaluate_model(args.corpus, args.iter, args.model, args.n, args.homo, args.train, args.freq)
#python ngram.py --inputsim=permuted_syllssyll__lemma_english_nphone_1_0_4_8.txt --corpus=notcelex

