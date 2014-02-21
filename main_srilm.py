import os, sys, re, tempfile, subprocess, getopt
import argparse
from calc_stats import *
import time

NGRAM = ["/Users/isa/Desktop/srilm/bin/macosx/ngram", "/Users/km/Documents/srilm/bin/macosx/ngram"]
NGRAM_COUNT = ["/Users/isa/Desktop/srilm/bin/macosx/ngram-count", "/Users/km/Documents/srilm/bin/macosx/ngram-count"]


"""set where srilm lives"""
for n in NGRAM_COUNT:
    if os.access(n, os.X_OK): ngramcount = n
if not ngramcount:
    raise ValueError('%s is not a working binary' %ngramcountlist[0])
for n in NGRAM:
    if os.access(n, os.X_OK): ngram = n
if not ngram:
    raise ValueError('%s is not a working binary' %ngramlist[0])

def clean_up():
    """Remove tmp files"""
    os.remove('tmp.lm')
    try: 
        os.remove('train.tmp')
        os.remove('srilm.tmp')
        os.remove('test.tmp')
    except OSError: pass
    return

def turn_to_txt(f, fname):
    '''if f is a list, turn it to a temp txt file
    if it's already a txt file, check to see if it exists
    '''
    if isinstance(f, list):
        #print "converting to tmp text file"
        outfile = open(fname + '.tmp', 'w')
        for item in f:
            outfile.write(item + "\n")
        return fname + '.tmp'
    elif isinstance(f, str):
        if os.path.isfile(f): return f
    else:
        print "PROBLEM WITH FILE TYPE"
        return

vowels = {}
for v in "IE{VQU@i#$u312456789cq0~iI1!eE2@aAoO3#4$6^uU7&5+8*9(0)<>[]{}":
    vowels[v] = 0


def get_cv(word, cv = 0):
    x = ""
    for letter in word:
        if letter in vowels: 
            x += "V"
        else: x += "C"
    if cv == 1: return x
    return len(re.sub("-","",word))
 
def generate_correct_number(corpus, homo, nonwords):
    """Generate number of words to match length, handle homophones being generated"""
    lengths = nltk.defaultdict(lambda: nltk.defaultdict(int))
    lengths_needed = nltk.defaultdict(int)

    for item in corpus:
        lengths_needed[get_cv(item)] += 1
    newwords = []
    newwords2 = []
    exist = nltk.defaultdict(int)
    while True:
        for sri_w in nonwords:
            w = re.sub(" ", "",sri_w)
            if lengths_needed[get_cv(w)] > 0:
                if homo == 1 or (w not in newwords and re.sub("-","",w) not in newwords2):
                    lengths_needed[get_cv(w)] += -1
                    newwords += [w]
        #            print len(newwords)
                    newwords2 += [re.sub("-", "", w)]
                    if w in corpus:
                        exist[len(w)] +=1
            if sum([lengths_needed[j] for j in lengths_needed.keys()]) == 0: 
                print "nb of real words", sum(exist.values())
                return newwords

def write_lex_file(o, corpus, cv, iter, homo, smoothing, n):
    outfile  = open(o, "w")
    srilm = [" ".join(list(w)) for w in corpus]
    srilm_corpus = turn_to_txt(srilm, 'srilm')
    for c in corpus:
        outfile.write("-1," + re.sub("-","",c) + "\n")
    print "lexicon"
    for i in range(iter):
        nonwords = generate_srilm(srilm_corpus, smoothing, n, len(corpus))
        gen_lex= generate_correct_number(corpus, homo, nonwords)
        for w in gen_lex:
            #print re.sub(" ","", w)
            outfile.write(str(i) + "," +  re.sub("-","",w) + "\n")
        print "generated lexicon: ", str(i)
    outfile.close()
    return o


def generate_srilm(corpus, smoothing, n, length):
    a = [ngramcount, '-text', corpus, '-lm', 'tmp.lm', '-order', str(n)] 
    for o in range(1, n + 1): 
        a += ['-addsmooth' + str(o), str(smoothing), '-gt'+str(o)+'min', '0']
    rv = subprocess.call(a)
    b = [ngram, '-lm', 'tmp.lm', '-gen', str(length*5), '-order', str(n)]

    proc= subprocess.Popen(b, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    del proc
    clean_up()
    return "".join(out).split("\n")




parser = argparse.ArgumentParser()
parser.add_argument('--n', metavar='--n', type=int, nargs='?',
                    help='n for ngram', default=3)
parser.add_argument('--homo', metavar='h', type=int, nargs='?',
                    help='0 to exclude homophones being generated, 1 for homophones allowed', default=0)
parser.add_argument('--model', metavar='--m', type=str, nargs='?',
                    help='should be nphone for ngram model', default="nphone")
parser.add_argument('--minlength', metavar='--minl', type=int, nargs='?',
                   help='minimum length of word allowed from celex', default=0)
parser.add_argument('--maxlength', metavar='--maxl', type=int, nargs='?',
                    help='maximum length of word allowed from celex', default=40)
parser.add_argument('--iter', metavar='--i', type=int, nargs='?',
                    help='number of lexicons to generate', default=2)
parser.add_argument('--corpus', metavar='--c', type=str, nargs='?', 
                    help='put corpus file - list of words, one on each line')
parser.add_argument('--cv', metavar='--cv', type=int, nargs='?',
                    help='put 1 here to match for CV pattern', default=0)
parser.add_argument('--grammar', metavar='--g', type=str, nargs='?',
                        help='grammar file for pcfg', default="grammars/grammar_chom.wlt")
parser.add_argument('--fnc', metavar='--f', type=str, nargs='?',
                     help='evaluate/generate corpus', default="generate")
parser.add_argument('--train', metavar='--t', type=float, nargs='?',
                      help='fraction of corpus use for training', default=0.75)
parser.add_argument('--freq', metavar='--freq', type=int, nargs='?',
                       help='use frequency based lm', default=0)
parser.add_argument('--graph', metavar='--g', type=int, nargs='?',
                        help='output graph', default=0)
parser.add_argument('--smoothing', metavar='--s', type=float, nargs='?',
                        help='discount for add-smoothing', default=0.1)

args = parser.parse_args()
corpus = [i.strip() for i in open(args.corpus, "r").readlines()]
print args.model, len(corpus), "sample", corpus[0]

o = "Lexicons/lex_" + args.corpus.split("/")[-1][:-4] + "_cv" +  str(args.cv) + "_iter" + str(args.iter) + "_m" + args.model + "srilm" + "_n" + str(args.n) + ".txt"

lexfile = write_lex_file(o, corpus, args.cv, args.iter, args.homo, args.smoothing, args.n)
write_all(lexfile, args.minlength, args.maxlength, args.graph)
os.system('Rscript make_hists.R')
 
