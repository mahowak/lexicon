from lm import *
from nltk import *
from math import log, sqrt, exp 
import nltk
import random, sys, re
import time, datetime
import collections
import itertools 

""" --------------ngram model------------"""

def multichooser(context,pd,n):
    """ Return random choice from multinomial cfd. """
    context = "".join(context)
    cumprob = 0
    rand = random.random()
    possibles = pd[n][context].keys()
    possibles.sort()
    for possible in possibles:
        cumprob += pd[n][context][possible]
        if cumprob > rand: return possible
    return



class NgramModel(LM):
    def __init__(self, n, corpus, gen = 0):
        self.n = n
        self.__dict__.update(locals())
        self.cfd = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
        self.cpd  = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(int)))
        self.smoothing = 0
        self.generation = gen
        self.alpha = collections.defaultdict(lambda: collections.defaultdict(int))
        LM.__init__(self)

    def create_model(self, corpus, smoothing = 0):
        """Update cfd using ngrams"""
        unigrams = []
        for item in corpus:
            for k in range(1,self.n+1):
                item_ngrams = nltk.ngrams(["["]*(k-1)  + [i for i in item] + ["]"], k)
                for ng in item_ngrams:
                    self.cfd[k]["".join(ng[:-1])][ng[-1]] += 1
                    unigrams += [ng[-1]]
        U = len(set(unigrams))
        units = set(unigrams)
        self.smoothing = smoothing
        for k in self.cfd.keys():
            for i in self.cfd[k].keys():
                pbak = 0
                for j in self.cfd[k][i].keys():
                    self.cpd[k][i][j] = (self.cfd[k][i][j] + smoothing) / float(sum(self.cfd[k][i].values()) + smoothing*U)
                    pbak += self.cpd[k-1][i[1:]][j]
                if self.smoothing:
                    self.alpha[k][i] = (1 - sum(self.cpd[k][i].values())) / float(1 - pbak)
#        print sorted(self.cfd[1].items(), key = lambda x: x[1])
        #for generation with smoothing 
        if self.smoothing and self.generation:
            grams = [''.join(i) for i in itertools.product(units, repeat = self.n)]
            for g in grams:
                self.cpd[self.n][g[:-1]][g[-1]] = self.backoff(self.n, g[:-1], g[-1])
            for k in range(1,self.n):
                grams_border = [''.join(i) for i in itertools.product(units, repeat = k)]
                for g in grams_border:
                    s = "".join(["["]*(self.n - k) + [g])
                    self.cpd[self.n][s[:-1]][s[-1]] = self.backoff(self.n, s[:-1], s[-1])
        
        LM.create_model(self, corpus, smoothing)

    def generate(self, ngen = 1):
        """Generate as many words as specified by ngen"""
        LM.generate(self, ngen)
        words = [self.generate_one(self.n) for xx in range(ngen)]
        return words
        
        
    def generate_one(self, n):
        """Generate one word from ngram model."""
        word = ["["]*(self.n - 1)
        while True:
            context = "".join(word[(len(word) - (self.n -1)):len(word)])
            word = word + [multichooser(context, self.cpd, self.n)]
            if word[-1] == "]":
                break
            if word[-1] == "[":
                word = ["["]*(self.n - 1)
        return "".join(word[(self.n - 1):-1])


    
    def evaluate(self, word):
        """ get the log probability of generating a given word under the language model """
        LM.evaluate(self, word)
        p=0
        oov =0
        word = [i for i in word] + ["]"]
        l = len(word)
        fifo = ["["]*(self.n -1)
        for ch in word:
            context = "".join(fifo[(len(fifo) - (self.n - 1)):len(fifo)])
            pbak =  self.backoff(self.n, context, ch)
            if pbak != 0:
                p += log(pbak,10)
            else:
                oov +=1
            fifo.append(ch)
        return l,oov,p

    def backoff(self, n, h, c):
        if c in self.cpd[n][h].keys() and n > 0:#seen ngram
            return self.cpd[n][h][c]
        elif h not in self.alpha[n].keys() and n > 0:#context never been observed
            return self.backoff(n-1, h[1:], c)
        elif c not in self.cpd[n-1][h[1:]].keys() and n > 0:#unseen phone in previous n
            return self.alpha[n][h] * self.backoff(n-1, h[1:], c)
        elif n >0:
            return self.alpha[n][h] * self.cpd[n-1][h[1:]][c]
        else:
            return 0
            

