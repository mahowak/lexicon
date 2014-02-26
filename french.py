#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import nltk
import argparse
import re


path = "/Users/isa/Desktop/lexicon/french_lex.txt"

def read_lines(path):
    """ Return lines in given celex file. """
    return [line.rstrip().split("\t") for line in open(path, "r").readlines()]

def build_corpus(path, language, lemma, mono):
    """ Return corpus from celex, given path and parameters. """
    lines = read_lines(path); corpus = []; 
    for line in lines[1:]:
        if float(line[13]) == 1 and line[0].islower() and "-" not in line[0]  and " " not in line[0] and float(line[34]) == 1 and line[3] != "ONO" and len(line[0]) > 1:
            corpus += [(line[22], float(line[6]))]
    return [i for i in corpus if i != None]

def build_real_lex(path, lemma, language, mono, homo, minlength, maxlength,celex_list):
    corpus = build_corpus(path, language, lemma, mono)
    corpus = [c[0] for c in corpus if float(c[1]) >= 1]
    corpus = [c for c in corpus if (len(re.sub("-", "", c)) >= minlength and len(re.sub("-", "", c)) <= maxlength)]
    if args.syll != 1: corpus = [re.sub("-","",x) for x in corpus] 
    print len(corpus)
    corpus = [c for c in corpus if not re.search("^mini", c)]
    corpus = [c for c in corpus if not re.search("^ipER", c)]
    corpus = [c for c in corpus if not re.search("\(m@$", c)]
    corpus = [c for c in corpus if not re.search("im@$", c)]
    corpus = [c for c in corpus if not re.search("e5$", c)]
    corpus = [c for c in corpus if not re.search("em@$", c)]
    corpus = [c for c in corpus if not re.search("ER$", c)]
    corpus = [c for c in corpus if not re.search("sj\)$", c)]
    corpus = [c for c in corpus if not re.search("Og$", c)]
    corpus = [c for c in corpus if not re.search("2$", c)]
    corpus = [c for c in corpus if not re.search("izm$", c)]
    corpus = [c for c in corpus if not re.search("Ok$", c)]
    corpus = [c for c in corpus if not re.search("am@$", c)]
    corpus = [c for c in corpus if not re.search("jEm$", c)]
    corpus = [c for c in corpus if not re.search("sj5$", c)]
    corpus = [c for c in corpus if not re.search("t@$", c)]
    corpus = [c for c in corpus if not re.search("jal$", c)]
    corpus = [c for c in corpus if not re.search("ist", c)]

    corpus = [c for c in corpus if not re.search("^@", c) or not re.sub("^@","",c) in corpus]
    corpus = [c for c in corpus if not re.search("^a", c) or not re.sub("^a","",c) in corpus]
    corpus = [c for c in corpus if not re.search("^R\(", c) or not re.sub("^R\(","",c) in corpus]
    corpus = [c for c in corpus if not re.search("^R", c) or not re.sub("^R","",c) in corpus]
    corpus = [c for c in corpus if not re.search("^dis", c) or not re.sub("dis","",c) in corpus]
    corpus = [c for c in corpus if not re.search("^dez", c) or not re.sub("^dez","",c) in corpus]
    corpus = [c for c in corpus if not re.search("ym@$", c) or not re.sub("m@$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("^Re", c) or not re.sub("^Re","",c) in corpus]
    corpus = [c for c in corpus if not re.search("^de", c) or not re.sub("^de","",c) in corpus]
    corpus = [c for c in corpus if not re.search("^5", c) or not re.sub("^5","",c) in corpus]

    corpus = [c for c in corpus if not re.search("El$", c) or not re.sub("El$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("@$", c) or not re.sub("@$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("aR$", c) or not re.sub("aR$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("jEl$", c) or not re.sub("jEl$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("jal$", c) or not re.sub("jal$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("ik$", c) or not re.sub("k$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("je$", c) or not re.sub("je$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("ije$", c) or not re.sub("ije$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("Es$", c) or not re.sub("Es$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("\(Ri$", c) or not re.sub("\(Ri$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("abl$", c) or not re.sub("abl$","e",c) in corpus]
    corpus = [c for c in corpus if not re.search("ize$", c) or not re.sub("ize$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("te$", c) or not re.sub("te$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("ik$", c) or not re.sub("ik$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("z$", c) or not re.sub("z$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("s$", c) or not re.sub("s$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("@s$", c) or not re.sub("@s$","e",c) in corpus]
    corpus = [c for c in corpus if not re.search("i$", c) or not re.sub("i$","iR",c) in corpus]
    corpus = [c for c in corpus if not re.search("j\)$", c) or not re.sub("j\)$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("e$", c) or not re.sub("e$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("te$", c) or not re.sub("te$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("iR$", c) or not re.sub("iR$","",c) in corpus]
    corpus = [c for c in corpus if not re.search("ize$", c) or not re.sub("ize$","",c) in corpus]

    lines = read_lines(path); 
    ortho = nltk.defaultdict(str)
    for i in lines:
        ortho[i[1]] = i[0]

    if homo == 0: corpus = set(corpus)
    print ">>>TOTAL NB OF WORDS", len(corpus)
    w =[]
    for c in corpus:
        w += [c + "\t"+ ortho[c]]
    f = open("celexes/" + "_".join([str(i) for i in celex_list]) + ".txt", "w")
    f.write('\n'.join(c for c in sorted(w)))
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
                    help='', default="french")
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


