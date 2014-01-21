import sys, codecs, math, re, collections
import nltk
import time
import argparse
import random

def create_model(corpus, n):
    cfd = nltk.FreqDist()
    for item in corpus:
        if args.corpus.startswith("celexes/syll"):
            grams =nltk.ngrams(["<S>"]*(n-1) + [i for i in item.split("-")] + ["<E>"], n)
        else:
            grams =nltk.ngrams(["<S>"]*(n-1) + [i for i in item] + ["<E>"], n)
        for ng in grams:
            cfd[ng] += 1
    return cfd

class KneserNey(dict):
    def __init__(self, arg=None):
        if arg == None:
            dict.__init__(self)
        else:
            dict.__init__(self, arg)
        self.n = self.n1 = self.n2 = self.n3 = self.n4 = 1
        self.N1 = collections.defaultdict(int)
        self.N1plus = collections.defaultdict(int)
        self.N2 = collections.defaultdict(int)
        self.N3plus = collections.defaultdict(int)
    def __setitem__(self, w, v):
        dict.__setitem__(self, w, v)
        self.n += v
        k = w[:-1]
        self.N1plus[k] += 1
        if v == 1:
            self.n1 += 1
            self.N1[k] += 1
        if v == 2:
            self.n2 += 1
            self.N2[k] += 1
        if v == 3: self.n3 += 1
        if v == 4: self.n4 += 1
        if v >= 3: self.N3plus[k] += 1
    def __getitem__(self, k):
        return dict.__getitem__(self, k) if k in self else 0


def search(func, min, max):
    x1, x3 = min, max
    x2 = (x3 - x1) / (3 + math.sqrt(5)) * 2 + x1
    f1, f2, f3 = func(x1), func(x2), func(x3)
    while (x3 - x1) > 0.0001 * (max - min):
        x4 = x1 + x3 - x2
        f4 = func(x4)
        if f4 < f2:
            if x2 < x4:
                x1, x2 = x2, x4
                f1, f2 = f2, f4
            else:
                x2, x3 = x4, x2
                f2, f3 = f4, f2
        else:
            if x4 > x2:
                x3, f3 = x4, f4
            else:
                x1, f1 = x4, f4
    return x2, f2

   
def perplexity(gram, test,n, V, alpha, alphaN):
    ppl = 0.0
    N = 0
    for s in test:
        w1 = w2 = ""
        if args.corpus.startswith("celexes/syll"):
            grams =nltk.ngrams(["<S>"]*(n-1) + [i for i in s.split("-")] + ["<E>"], n)
        else:
            grams =nltk.ngrams(["<S>"]*(n-1) + [i for i in s] + ["<E>"], n)
        for w in grams:
            if n == 1:
                p = (gram[1][(w,)] + alphaN) / (gram[1].n + V * alphaN)
            elif n == 2:
                if w1 == "":
                    p = (gram[1][(w[-1],)] + alpha[1]) / (gram[1].n + V * alpha[1])
                else:
                    p = (gram[2][w] + alphaN) / (gram[1][(w1,)] + V * alphaN)
                w1 = w[-1]
            elif n == 3:
                 if w1 == "":
                    p = (gram[1][(w[-1],)] + alpha[1]) / (gram[1].n + V * alpha[1])
                 elif w2 == "":
                    p = (gram[2][w[1:]] + alpha[2]) / (gram[1][(w[-1],)] + V * alpha[2])
                 else:
                    p = (gram[3][w] + alphaN) / (gram[2][w[1:]] + V * alphaN)
                 w2, w1 = w[-2], w[-1]
            ppl -= math.log(p)
            N += 1
    return math.exp(ppl / N)    



parser = argparse.ArgumentParser()
parser.add_argument("--corpus", help="corpus list", default='?')
parser.add_argument("--n", help="", default=3)
parser.add_argument("--t", help="training fraction of corpus", default = 0.75)
args = parser.parse_args()

corpus =  [i.strip() for i in open(args.corpus, "r").readlines()]

train = random.sample(corpus, int(args.t*len(corpus)))
test = random.sample(corpus, int((1-args.t)*len(corpus))) 

gram = {}
freq = collections.defaultdict(int)
for i in range(1,int(args.n) +1):
    freq[i] = create_model(train, i)
    gram[i] = KneserNey()
    for w, c in freq[i].iteritems():
        gram[i][w] = c

voca = set(freq[1].iterkeys())
V = len(voca)

alpha = collections.defaultdict(int)

alpha[1], ppl = search(lambda a:perplexity(gram, test, 1, V, alpha, a), 0.0001, 1.0)
print "UNIGRAM perplexity=%.3f" % ppl

alpha[2], ppl = search(lambda a:perplexity(gram, test, 2, V, alpha, a), 0.0001, 1.0)
print "BIGRAM perplexity=%.3f" % ppl

alpha[3], ppl = search(lambda a:perplexity(gram, test, 3, V, alpha, a), 0.0001, 1.0)
print "TRIGRAM perplexity=%.3f" % ppl


