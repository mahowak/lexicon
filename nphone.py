from lm import *
from nltk import *
from math import log, sqrt, exp 
import nltk
import random, sys, re
import time, datetime
from katz import *


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



class NgramModel(LM):
    def __init__(self, n, corpus):
        self.n = n
        self.__dict__.update(locals())
        self.cfd = ConditionalFreqDist()
        self.cpd  = {}
        self.smoothing = 0
        LM.__init__(self)

       # self.cpd_smooth = ConditionalProbDist()#self.cfd, nltk.LaplaceProbDist, 35)#issue with SimpleGoodTuringProbDist but also with other smoothing functions, does not work as is for n = 1

    def create_model(self, corpus, smoothing = None):
        """Update cfd using ngrams"""
        for item in corpus:
            item_ngrams = nltk.ngrams(["<S>"]*(self.n-1) + [i for i in item] + ["<E>"], self.n)
            for ng in item_ngrams:
                self.cfd["".join(ng[:-1])].inc(ng[-1])
        if smoothing == None:
            self.cpd  = ConditionalProbDist(self.cfd, nltk.MLEProbDist)
        elif smoothing == "katz":
            self.smoothing = 1
            m  = KatzSmoothing(self.n)
            self.cpd = m.smooth_cpd(self.cfd)
        LM.create_model(self, corpus, smoothing)

    def generate(self, ngen = 1):
        """Generate as many words as specified by ngen"""
        LM.generate(self, ngen)
        words = [self.generate_one(self.n) for xx in range(ngen)]
        return words
        
        
    def generate_one(self, n):
        """Generate one word from ngram model."""
        word = ["<S>"]*(self.n - 1)
        while True:
            context = "".join(word[(len(word) - (self.n -1)):len(word)])
            word = word + [multichooser(context, self.cfd)]
            if word[-1] == "<E>":
                break
        return "".join(word[(self.n - 1):-1])


    
    def evaluate(self, word):
        """ get the log probability of generating a given word under the language model """
        LM.evaluate(self, word)
        p=0
        if self.smoothing:
            grams=nltk.ngrams(["<S>"]*(self.n-1) + [i for i in word] + ["<E>"], self.n)
            probs,unseen_prob = self.cpd
            cf =  generate_cf(ConditionalFreqDist(), grams)
            for prefix,suffix in cf.iteritems():
                if prefix not in probs:
                    p += log(unseen_prob)
                else:
                    for term,count in suffix.iteritems():
                        N = len(probs[prefix])
                        if term in probs[prefix]:
                            p += count * log(probs[prefix][term], 2)
                        else:
                            p += log(unseen_prob)
        else:
            word = [i for i in word] + ["<E>"]
            fifo = ["<S>"]*(self.n -1)
            for i, ch in enumerate(word):
                context = "".join(fifo[(len(fifo) - (self.n - 1)):len(fifo)])
                try:
                    p += log(self.cpd[context].prob(ch))#smooth or unsmooth TODO: make it as a param (evaluate vs. generate) 
                except ValueError:
                    return 0.0
                fifo.append(ch)
        return p
                                                            
                                                         
