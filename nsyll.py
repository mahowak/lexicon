from lm import *
from katz import *
from nltk import *
from math import log
import nltk
import time
import random
import collections

""" --------------nsyll model------------"""

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
    
    
    
class NsyllModel(LM):
    def __init__(self, n, corpus):
        self.__dict__.update(locals())
        self.n = n
        self.cfd = ConditionalFreqDist()
        self.cpd = collections.defaultdict(lambda: collections.defaultdict(int))
        self.smoothing = 0
        self.U = 0
        self.units =[]
        LM.__init__(self)

    def create_model(self, corpus, smoothing = 0):
        """Update cfd using ngrams for syllables"""
        unigrams = []
        for item in corpus:
             item_ngrams = nltk.ngrams(["<S>"]*(self.n-1) + [i for i in item.split("-")] + ["<E>"], self.n)
             for ng in item_ngrams:
                self.cfd["".join(ng[:-1])].inc(ng[-1])
                unigrams += [ng[-1]]
        self.U = len(set(unigrams))
        self.units = set(unigrams)
        self.smoothing = smoothing
        for i in self.cfd.keys():
            for j in self.cfd[i].keys():
            	self.cpd[i][j] = (self.cfd[i][j] + smoothing) / float(sum(self.cfd[i].values()) + smoothing*self.U)
                #print i+" "+j, log(self.cpd[i][j],10), self.cfd[i][j]
        LM.create_model(self, corpus, smoothing)

    def generate_one(self, n):
        """Generate one word from ngram model."""
        word = ["<S>"]*(self.n - 1)
        while True:
            context = "".join(word[(len(word) - (self.n -1)):len(word)])
            word = word + ["-"] + [multichooser(context, self.cfd)]
            if word[-1] == "<E>":
                break
        return "".join(word[(self.n):-2])

    def generate(self, ngen = 1):
        """Generate as many words as specified by ngen"""
        LM.generate(self, ngen)
        words = [self.generate_one(self.n) for xx in range(ngen)]
        return words
    
    def evaluate(self, word):
        """ get the log probability of generating a given word under the language model """
        LM.evaluate(self, word)
        p=0
        oov = 0
        word = word.split("-") + ["<E>"]
        n = len(word)
        fifo = ["<S>"]*(self.n -1)
        for ch in word:
            context = "".join(fifo[(len(fifo) - (self.n - 1)):len(fifo)])
            try:
                p += log(self.cpd[context][ch],10)
            except ValueError:
                if ch in self.units:
                    p += log(self.smoothing/ float(self.cfd[context][ch] + self.smoothing*self.U), 10)
                else:
                    oov +=1
            fifo.append(ch)
        if oov > 0: 
        	n =0
        	p=0
        return n, oov, p
                                                            
               
