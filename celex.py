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

user_celex_path = "/Users/km/Documents/celex2/"
#user_celex_path = "/Users/isa/Desktop/PhD/3. Projets/10. Etude du Lexique/celex_raw/" 

"""produces file with header: "lexicon,homophones,mps,neighbors,avg_lev,num_words\n"

file name is: lemma, language, model, mono, homocel, minlength, maxlength, n, homophones, iterations
to do non-English, mono has to be and it's untested

can either use argument --corpus to pass a list of words from a txt file
or can specify parameters for celex to use

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

""" --------------word cleaning functions-------------- """
vowels = {}
for v in "IE{VQU@i#$u312456789cq0~iI1!eE2@aAoO3#4$6^uU7&5+8*9(0)<>[]{}":
    vowels[v] = 0

def clean_word(word):
    """Remove stress and syllable boundaries."""
    word = re.sub("'", "", word)
    word = re.sub('"', "", word)
    if args.syll != 1 and args.pcfg!=1: word = re.sub("-", "", word)
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
""" --------------Celex reading functions-------------- """

def get_cv(word):
    cv = ""
    for letter in word:
        if letter in vowels: 
            cv += "V"
        else: cv += "C"
    if args.cv == 1: return cv
    return len(word)

def read_in_celex_lines(path):
    """ Return lines in given celex file. """
    return [line.strip().split("\\") for line in open(path, "r").readlines()]


def get_celex_monos(path, language):
    """ Return list of celex ids for monomorphemes. """
    a = read_in_celex_lines(user_celex_path + language + "/{lang}ml/{lang}ml.cd".format(lang=language[0]))
    return [i[0] for i in a if i[3] == "M"]

def get_celex_freq(path, language):
    """ Return tuples of celex ids and freq per million word. """
    a = read_in_celex_lines(user_celex_path + language + "/{lang}fl/{lang}fl.cd".format(lang=language[0]))
    if language == "english":
        return dict((i[0], i[6]) for i in a)
    else:
        return dict((i[0], i[4]) for i in a)


def get_celex_path(path, lemma, language):
    """ Return celex path, given root, lemma, language. """
    return path + language + "/{lang}p{lem}/{lang}p{lem}.cd".format(lang=language[0], lem=lemma[0])


def celex_pron_loc(language, lemma):
    """ Return location of pronunciation in celex, given language. """
    pron = 5
    if language == "german" or language== "dutch": pron = pron -2 #german one less
    if lemma == "wordform": pron += 1
    return pron

def extract_celex_info(line, freqs, language="english", lemma="lemma", model="ortho"):
    """ Return celex word (ortho or phonemic) and its freq from celex line. """
    if line[1].isalpha() and ((line[1].islower()) | (language == 'german')) and "-" not in line[1] and "." not in line[1] and "'" not in line[1] and " " not in line[1]:#we dont take proper names but careful this will not work well for German
        return line[celex_pron_loc(language, lemma)], float(freqs[line[0]]) #pron, frequency
    return


def build_celex_corpus(path, language, lemma, model, mono):
    """ Return corpus from celex, given path and parameters. """
    lines = read_in_celex_lines(path); corpus = []; monos = []
    if mono == 1: monos = get_celex_monos(path, language)
    freqs = get_celex_freq(path, language)
    corpus = [extract_celex_info(line, freqs, language, lemma, model) for line in lines if (mono == 0 or line[0] in monos)]
    return [i for i in corpus if i != None]


def build_real_lex(path, lemma, language, mono, homo, minlength, maxlength, freq, celex_list):
    celex_path = get_celex_path(path, lemma, language)
    print celex_path
    corpus = build_celex_corpus(celex_path, language, lemma, model, mono)
    corpus = [c for c in corpus if float(c[1]) > 0]
    corpus = [(clean_word(c[0]), c[1]) for c in corpus] #reduce celex to just pronunciation
    corpus =  [(celex_diphthong_sub(c[0]), c[1]) for c in corpus if "c" not in c[0] and "q" not in c[0] and "0" not in c[0] and "~" not in c[0]]
    corpus = [c for c in corpus if (len(re.sub("-", "", c[0])) >= minlength and len(re.sub("-", "", c[0])) <= maxlength)]
    dict_corpus = nltk.defaultdict(int)
    for c in corpus:
        if not c[0] in dict_corpus:
            dict_corpus[c[0]] = float(c[1])
        else:
            dict_corpus[c[0]] += float(c[1])
    if homo == 0: corpus = [(x, y) for x, y in dict_corpus.iteritems()]
    print ">>>TOTAL NB OF WORDS", len(corpus)    
    f = open("celexes/" + "_".join([str(i) for i in celex_list]) + ".txt", "w")
    if freq == 0:
        corpus = [c[0] for c in corpus]
        if args.pcfg == 0:
            for line in corpus: f.write(line + "\n")
        else:
            for line in corpus: 
                l = list(line)
                for k in l:
                    f.write(k + " ")
                f.write("\n")
    else:
        f.write('\n'.join('%s\t%s' % c for c in corpus))
    f.close()
    return corpus


#build_real_lex(user_celex_path, "lemma", "english", "nphone", 0, 1, 3, 9
parser = argparse.ArgumentParser()
#parser.add_argument('--n', metavar='--n', type=int, nargs='?',
#                    help='n for ngram', default=3)
#parser.add_argument('--homo', metavar='h', type=int, nargs='?',
#                    help='0 to exclude homophones being generated, 1 for homophones allowed', default=0)
parser.add_argument('--lemma', metavar='--lem', type=str, nargs='?',
                    help='lemma or wordform in celex', default="lemma")
parser.add_argument('--language', metavar='--lang', type=str, nargs='?',
                    help='', default="english")
#parser.add_argument('--model', metavar='--m', type=str, nargs='?',
#                    help='should be nphone for ngram model', default="nphone")
parser.add_argument('--mono', metavar='--mono', type=int, nargs='?',
                    help='1 for mono only, 0 ow', default=1)
parser.add_argument('--homocel', metavar='--homocel', type=int, nargs='?',
                    help='1 for allow homo in celex, 0 ow', default=0)
parser.add_argument('--minlength', metavar='--minl', type=int, nargs='?',
                    help='minimum length of word allowed from celex', default=4)
parser.add_argument('--maxlength', metavar='--maxl', type=int, nargs='?',
                    help='maximum length of word allowed from celex', default=8)
#parser.add_argument('--iter', metavar='--i', type=int, nargs='?',
#                   help='number of lexicons to generate', default=2)
parser.add_argument('--freq', metavar='--f', type=int, nargs='?',
                     help='add frequency to the output', default=0)
#parser.add_argument('--corpus', metavar='--c', type=str, nargs='?', help='put corpus file (list of words, one on each lien) to override celex', default='celex')
parser.add_argument('--syll', metavar='--syll', type=int, nargs='?', help='include syll in celex', default=0)
parser.add_argument('--pcfg', metavar='--pcfg', type=int, nargs='?', help='format for pcfg', default=0)
parser.add_argument('--inputsim', metavar='--inputsim', type=str, nargs='?', help='use this if you want to input a file that contains simulated lexicons instead of ngrams. the file should be a csv in format simnum,word', default="none")
parser.add_argument('--cv', metavar='--cv', type=int, nargs='?', help='put 1 here to match for CV pattern', default=0)


args = parser.parse_args()

celex_list = [args.lemma, args.language, args.mono, args.homocel, args.minlength, args.maxlength]

if args.syll == 1: celex_list = ['syll_'] + celex_list
if args.freq == 1: celex_list = ['freq_'] + celex_list
if args.pcfg == 1: celex_list = ['pcfg_'] + celex_list

#if args.corpus == 'celex': 
a = build_real_lex(user_celex_path, args.lemma, args.language, args.mono, args.homocel, args.minlength, args.maxlength, args.freq, celex_list)
argslist = "_".join([str(j) for j in celex_list] + [str(args.homocel), str(args.cv)])
