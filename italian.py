#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import nltk
import argparse
import re


path = "/Users/isa/Desktop/lexicon/italian_lex.txt"

def read_lines(path):
    """ Return lines in given celex file. """
    return [line.rstrip().split("\t") for line in open(path, "r").readlines()]

def build_corpus(path, language, lemma, mono):
    """ Return corpus from celex, given path and parameters. """
    lines = read_lines(path); corpus = []; 
    for line in lines[1:]:
        if line[17]== line[18] and line[18].islower() and "-" not in line[18]  and " " not in line[18] and line[16] != "I" and line[16] != "U" and line[16] != "X":
              #  print line[0]
                corpus += [(line[19], float(line[10]))]
    return [i for i in corpus if i != None]

def build_real_lex(path, lemma, language, mono, homo, minlength, maxlength,celex_list):
    corpus = build_corpus(path, language, lemma, mono)
    print len(corpus)
    corpus = [c[0] for c in corpus if float(c[1]) >= 1]
    print len(corpus)
    corpus = [c for c in corpus if (len(re.sub("-", "", c)) >= minlength and len(re.sub("-", "", c)) <= maxlength)]
    if args.syll != 1: corpus = [re.sub("-","",x) for x in corpus] 
    print len(corpus)
    corpus = [c for c in corpus if not re.search("ezza$", c)]
    corpus = [c for c in corpus if not re.search("ismo$", c)]
    corpus = [c for c in corpus if not re.search("mento$", c)]
    corpus = [c for c in corpus if not re.search("ione$", c)]
    corpus = [c for c in corpus if not re.search("ista$", c)]
    corpus = [c for c in corpus if not re.search("bile$", c)]
    corpus = [c for c in corpus if not re.search("^in", c)]
    corpus = [c for c in corpus if not re.search("^re", c) or re.sub("^re","", c) not in corpus]
    corpus = [c for c in corpus if not re.search("za$", c)]
    corpus = [c for c in corpus if not re.search("izia$", c)]
    corpus = [c for c in corpus if not re.search("evole$", c)]
    corpus = [c for c in corpus if not re.search("iere$", c)]
    corpus = [c for c in corpus if not re.search("iero$", c)]
    corpus = [c for c in corpus if not re.search("mente$", c)]
    corpus = [c for c in corpus if not re.search("acco$", c)]
    corpus = [c for c in corpus if not re.search("aLLa$", c)]
    corpus = [c for c in corpus if not re.search("ajo$", c)]
    corpus = [c for c in corpus if not re.search("^mini", c)]
    corpus = [c for c in corpus if not re.search("^micro", c)]
    corpus = [c for c in corpus if not re.search("arjo$", c)]
    corpus = [c for c in corpus if not re.search("ino$", c)]
    corpus = [c for c in corpus if not re.search("krate$", c)]
    corpus = [c for c in corpus if not re.search("krazzia$", c)]
    corpus = [c for c in corpus if not re.search("kratico$", c)]
    corpus = [c for c in corpus if not re.search("loGo$", c)]
    corpus = [c for c in corpus if not re.search("logia$", c)]
    corpus = [c for c in corpus if not re.search("^auto", c)]
    corpus = [c for c in corpus if not re.search("^de", c) or re.sub("^de","", c) not in corpus]
    corpus = [c for c in corpus if not re.search("^dis", c) or re.sub("^dis","", c) not in corpus]
    corpus = [c for c in corpus if not re.search("^s", c) or re.sub("^s","", c) not in corpus]
    corpus = [c for c in corpus if not re.search("^trans", c) or re.sub("^trans","", c) not in corpus]
    corpus = [c for c in corpus if not re.search("^tra", c) or re.sub("^tra","", c) not in corpus]
    corpus = [c for c in corpus if not re.search("^tras", c) or re.sub("^tras","", c) not in corpus]
    corpus = [c for c in corpus if not re.search("etto$", c)]
    corpus = [c for c in corpus if not re.search("etta$", c)]
    corpus = [c for c in corpus if not re.search("ino$", c)]
    corpus = [c for c in corpus if not re.search("ina$", c)]














    lines = read_lines(path); 
    ortho = nltk.defaultdict(str)
    for i in lines:
        ortho[i[19]] = i[18]

    if homo == 0: corpus = set(corpus)
    print ">>>TOTAL NB OF WORDS", len(corpus)
    w =[]
    for c in corpus:
        w += [c + "\t"+ ortho[c]]
    f = open("celexes/" + "_".join([str(i) for i in celex_list]) + ".txt", "w")
    f.write('\n'.join(c for c in sorted(corpus)))
    f.close()
    return corpus


parser = argparse.ArgumentParser()
parser.add_argument('--lemma', metavar='--lem', type=str, nargs='?',
                    help='lemma or wordform in celex', default="lemma")
parser.add_argument('--mono', metavar='--mono', type=int, nargs='?',
                    help='1 for mono only, 0 ow', default=1)
parser.add_argument('--homocel', metavar='--homocel', type=int, nargs='?',
                    help='1 for allow homo in celex, 0 ow', default=0)
parser.add_argument('--minlength', metavar='--minl', type=int, nargs='?',
                    help='minimum length of word allowed from celex', default=4)
parser.add_argument('--maxlength', metavar='--maxl', type=int, nargs='?',
                    help='maximum length of word allowed from celex', default=8)
parser.add_argument('--language', metavar='--lang', type=str, nargs='?',
                    help='', default="italian")
#
parser.add_argument('--syll', metavar='--syll', type=int, nargs='?', help='include syll in celex', default=0)
parser.add_argument('--pcfg', metavar='--pcfg', type=int, nargs='?', help='format for pcfg', default=0)
parser.add_argument('--inputsim', metavar='--inputsim', type=str, nargs='?', help='use this if you want to input a file that contains simulated lexicons instead of ngrams. the file should be a csv in format simnum,word', default="none")
parser.add_argument('--cv', metavar='--cv', type=int, nargs='?', help='put 1 here to match for CV pattern', default=0)

args = parser.parse_args()

celex_list = [args.lemma, args.language, args.mono, args.homocel, args.minlength, args.maxlength]

if args.syll == 1: celex_list = ['syll_'] + celex_list

a = build_real_lex(path, args.lemma, args.language, args.mono, args.homocel, args.minlength, args.maxlength, celex_list)
argslist = "_".join([str(j) for j in celex_list] + [str(args.homocel), str(args.cv)])


