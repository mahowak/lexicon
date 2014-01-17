from evaluation import *
import random, sys, re
import nltk

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
    
    
def generate_correct_number(corpus, homo, lm):
    """Generate number of words to match length, handle homophones being generated"""
    lengths_needed = nltk.defaultdict(int)
    for item in corpus:
        lengths_needed[get_cv(item)] += 1
    newwords = []
    newwords2 = []
    exist =0
#    hom = dict((i,corpus.count(i)) for i in corpus if corpus.count(i) > 1)
#    ratio = sum(hom.values())/float(len(hom)+1)
    while True:
        words = lm.generate()
        for w in words:
            if lengths_needed[get_cv(w)] > 0:
                if homo == 1 or (w not in newwords and re.sub("-","",w) not in newwords2):
#                    temp = newwords + [w]
#                    hom_new = Set([(i,temp.count(i)) for i in temp if temp.count(i) > 1])
#                    if len(hom_new)!= 0: 
#                        ratio_temp = sum([h[1] for h in hom_new])/float(len(hom_new))
#                    else:
#                        ratio_temp = 0
#                    if (ratio_temp <= (ratio + 0.1) and len(hom_new) <= len(hom)) or w not in newwords:
                    lengths_needed[get_cv(w)] += -1
                    if sum([lengths_needed[j] for j in lengths_needed.keys()]) %1000 == 0:
                        print sum([lengths_needed[j] for j in lengths_needed.keys()])
                    newwords += [w]
                    newwords2 += [re.sub("-", "", w)]
                    if w in corpus:
                        exist +=1
            elif sum([lengths_needed[j] for j in lengths_needed.keys()]) == 0: 
                print "nb of real words", exist
                return newwords



def write_lex_file(o, corpus, cv, iter, lm, homo):
    outfile  = open(o, "w")
    for c in corpus:
        outfile.write("-1," + re.sub("-","",c) + "\n")
    print "lexicon: ", cross_entropy(lm, corpus), perplexity(cross_entropy(lm, corpus))
    for i in range(iter):
        gen_lex= generate_correct_number(corpus, homo, lm)
        for w in gen_lex:
            outfile.write(str(i) + "," +  re.sub("-","",w) + "\n")
        print "generated lexicon: ", str(i), cross_entropy(lm, gen_lex)
    outfile.close()
    return o


