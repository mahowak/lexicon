from nltk import *
import random, sys, re, os
from math import log, sqrt, exp
import math
import nltk
import argparse
import itertools
import Levenshtein
import time, datetime
import pickle
t = time.time()
import random, sys, re
from networkx import *
import networkx as nx
import matplotlib.pyplot as plt
from collections import *
import numpy as np

"""Take in simulated lexicons file with -1 for real lexicon and 0-N for simulated lexicon
and output lexical stats"""
try: 
    os.mkdir('rfiles')
except OSError: 
    pass

def find_minimal_pair_diff(word1, word2):
    """ return minimal difference, only use when you know it's an mp"""
    for i in range(len(word1)):
        if word1[i] != word2[i]: return sorted(set([word1[i], word2[i]]))

def entropy_from_dict(d):
    """Input dictionary, return the entropy."""
    prob = [float(i)/sum(d.values()) for i in d.values()]
    return sum([- p * math.log(p, 2) for p in prob ])

def num_ambiguous(d):
    """Find how many values in the dict are 1.
    A word is unique at that length if it has a 1 in its start_dict."""
    return float(sum([i for i in d.values() if i != 1]))



def write_lex_stats(b, num, f, f2, graph= False):
    """Use Levenshtein package to calcualte lev and count up mps, neighbors, etc"""
    total = 0.
    mps = 0
    neighbors = 0
    homophones = 0
    lev_total = 0
    specific_mps = defaultdict(int)
    ndict = nltk.defaultdict(int)
    mdict = nltk.defaultdict(int)
    hdict = nltk.defaultdict(int)
    uniq = nltk.defaultdict(int)
    start_dict = defaultdict(dict)
    end_dict = defaultdict(dict)
    for k in range(5):
        start_dict[k] = defaultdict(int)
        end_dict[k] = defaultdict(int)
    g = nx.Graph()
    g.l = {}
    for item in b:
        for i in range(5):
            if i < len(item):
                start_dict[i][item[:(i + 1)]] += 1
                end_dict[i][item[-(i + 1):]] += 1
    #print start_dict[3]
    for item in itertools.combinations(b, 2):
        lev = Levenshtein.distance(item[0], item[1])
        g.add_node(item[0])
        g.add_node(item[1])
        g.l[item[0]] = len(item[0])
        g.l[item[1]] = len(item[1])
        if lev == 0: 
            homophones += 1
            hdict[item[0]] += 1
        elif lev == 1:
            g.add_edge(item[0], item[1])
            neighbors += 1
            ndict[item[0]] += 1#*log(dict_b[item[1]])
            ndict[item[1]] += 1#*log(dict_b[item[0]])
            if len(item[0]) == len(item[1]): #if it's a minimal pair
                specific_mps["_".join(find_minimal_pair_diff(item[0], item[1]))] += 1                
                mps += 1
                mdict[item[0]] += 1#*log(dict_b[item[1]])
                mdict[item[1]] += 1#*log(dict_b[item[0]])
        
        uniq[item[0]] = 1
        total += 1
        lev_total += lev
    print "neighbors", neighbors
    print "average clustering", average_clustering(g)
    if graph == True:
        plt.figure(figsize=(50,50))
        pos=nx.spring_layout(g)
#    node_color=[float(g.degree(w)) for w in g]
        nx.draw_networkx(g,pos, with_labels = False,  node_size = 40, edge_color = '0.8', node_color='k')
#        nx.draw_networkx_nodes(g,pos, node_size=40)
        plt.savefig('graph/' + str(num))
    f.write(",".join([str(x) for x in [num, len(hdict), len(b) - (len(uniq) - len(hdict)) - 1 , mps, neighbors, lev_total/total, len(b), nx.average_clustering(g), nx.transitivity(g), specific_mps["b_p"], specific_mps["d_t"], specific_mps["g_k"]] + [entropy_from_dict(start_dict[i]) for i in range(5)] + [1 - num_ambiguous(start_dict[i])/len(b) for i in range(5)] + [entropy_from_dict(end_dict[i]) for i in range(5)] + [1 - num_ambiguous(end_dict[i])/len(b) for i in range(5)]]) + "\n")

    for item in b:
        f2.write(",".join([str(num), str(item), str(hdict[item]), str(mdict[item]/(hdict[item] + 1.)), str(ndict[item]/(hdict[item] + 1.)), str(len(item)), str(start_dict[0][item[:1]]), str(start_dict[1][item[:2]]), str(start_dict[2][item[:3]]), str(start_dict[3][item[:4]]), str(start_dict[4][item[:5]]) ] + [str(start_dict[i][item[:-(i+1)]]) for i in range(5)]) + "\n")
    return


def write_all(inputsim, minlength, maxlength, graph):
    ###global file
    ftowrite = inputsim.split("/")[-1][:-4]
    f = open("rfiles/" + "global_" + ftowrite + ".txt", "w")
    f.write("lexicon,homophones_type, homophones_token ,mps,neighbors,avg_lev,num_words,avg_cluster,transitivity,bppair,tdpair,kgpair,1entropy,2entropy,3entropy,4entropy,5entropy,pctunique1,pctunique2,pctunique3,pctunique4,pctunique5,1endentropy,2endentropy,3endentropy,4endentropy,5endentropy,pctendunique1,pctendunique2,pctendunique3,pctendunique4,pctendunique5\n")
    ###word-level stats
    f2 = open("rfiles/" + "indwords_" + ftowrite + ".txt", "w")
    f2.write("lexicon,word,homophones,mps,neighbors,length,numthatshareletter1,numthatshareletter2,numthatshareletter3,numthatshareletter4,numthatshareletter5,numthatshareendletter1,numthatshareendletter2,numthatshareendletter3,numthatshareendletter4,numthatshareendletter5\n")
    inputlist = nltk.defaultdict(list)
    lines = [line.strip().split(",") for line in open(inputsim).readlines()]
    lines = [line for line in lines if len(re.sub("-","",line[1])) >= minlength and len(re.sub("-","",line[1])) <= maxlength]
    for item in lines: #divide up lexicons
        inputlist[int(item[0])] += [re.sub("-","",item[1])]
    print "writing real lexicon stats", len(inputlist[-1])
    write_lex_stats(inputlist[-1], "real", f, f2)
    for i in range(0, max(inputlist.keys()) + 1):
        print "writing simulated lexicon stats: ", str(i)
        write_lex_stats(inputlist[i], i, f, f2, graph)
    f.close()
    f2.close()
    return


# parser = argparse.ArgumentParser()
# parser.add_argument('--inputsim', metavar='--inputsim', type=str, nargs='?', help='use this if you want to input a file that contains simulated lexicons instead of ngrams. the file should be a csv in format simnum,word', default="none")
# parser.add_argument('--minlength', metavar='--minl', type=int, nargs='?',
#                     help='minimum length of word allowed from celex', default=4)
# parser.add_argument('--maxlength', metavar='--maxl', type=int, nargs='?',
#                     help='maximum length of word allowed from celex', default=8)

# args = parser.parse_args()

# write_all(args.inputsim, 4, 8)
