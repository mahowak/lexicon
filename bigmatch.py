import random, sys, re, os
from lm import *
from scipy.spatial import cKDTree as kd
from convert_to_disc import *
from convert_to_blick import *
from blick import BlickLoader
b = BlickLoader()
from nphone import NgramModel


vowels = {}
for v in "IE{VQU@i#$u312456789cq0~iI1!eE2@aAoO3#4$6^uU7&5+8*9(0)<>[]{}":
        vowels[v] = 0

def get_cv(word):
    x = ""
    for letter in word:
        if letter in vowels: 
            x += "V"
        else: x += "C"
        if x == 1: return x
    return len(re.sub("-","",word))

""" --------------match from big set of words------------"""

def write_row_of_bigmatch(discword, disc, outfile, x, real, T):
    if disc == 0: blickword = convert_to_blick(discword)
    if disc == 0:
        outfile.write(",".join([blickword, str(b.assessWord(blickword)), str(x.evaluate(discword)[1]), real, T, discword]) + "\n")
    else:
        outfile.write(",".join(["N", str(0), str(x.evaluate(discword)[1]), real, T, discword]) + "\n")
    return


class BigMatch(LM):
    """
    Generate 10 million words and match to real lexicon
    according to ngram, blick, or both.
    """
    
    def __init__(self, n, corpus, f):
        self.__dict__.update(locals())
        self.wordlist = {}
        self.n = n
        self.f = f
        self.disc = 0
       # self.match_from_biglist(self.bigfn, args.cv, args.iter, self.match)
        LM.__init__(self)

    def create_model(self, corpus):
        x = NgramModel(self.n, corpus)
        x.create_model(corpus)
        self.make_words(x)
        LM.create_model(self, corpus)

    def make_words(self,lm):
        """Generate 10 million words only if file does not exist already.
        Save to the corpus name with _tomatch inserted before .txt
        """
        if " " in self.corpus[0] and " " in self.corpus[1]: 
            print "assuming BLICK"
            self.corpus = [convert_to_disc(i) for i in self.corpus]
        else:
            self.disc = 1
            print "assuming Disc" 
        if not os.path.isfile(self.f):  ##check if it already exists
            print "generating 10 million words"
            outfile = open(self.f, "w")
            outfile.write("word,blick,ngram,Real,T,disc\n")
            for word in self.corpus:
                write_row_of_bigmatch(word, self.disc, outfile, lm, "Real", "1")
            while len(self.wordlist)<10000000:  
                words = lm.generate(100)
                for word in words:
                    if word not in self.wordlist and len(word) < 9: #keep only words less than len9
                        write_row_of_bigmatch(word, self.disc, outfile, lm, "Simulated", "0")
                        self.wordlist[word] = 0
        return

    def handle_blick_disc(self, word):
        if self.disc == 1: return word
        else: return convert_to_disc(word)

    def match_loop(self, outfile, outfile2, realpoints, realword, realblick, realngram, fff, cv, iter, minpoint, blick, ngram, word, tree):
        """Iterate through real lexicon points and do matching"""
        print "iteration part"
        for rpnum, rp in enumerate(realpoints): ###write real part
            outfile.write(",".join([str(-1), str(realword[rpnum]), str(realblick[rpnum]), str(realngram[rpnum])]) + "," + self.handle_blick_disc(realword[rpnum]) + "\n")
            outfile2.write(str(-1) + "," + self.handle_blick_disc(realword[rpnum]) + "\n")
        for iteration in range(iter): #write simulated lexicon
            lens = []; points = []; used = {}; space_size =0; real = 0
            for rnum, r in enumerate(realpoints):
                poss = tree.query_ball_point(r, minpoint)
                poss = [i for i in poss if word[i] not in used and get_cv(self.handle_blick_disc(word[i])) == get_cv(self.handle_blick_disc(realword[rnum]))]
                if len(poss) == 0: # use real word
                    points += [(realword[rnum], blick[rnum], ngram[rnum])]
                    lens += [0] 
                    used[realword[rnum]] = 0
                else:
                    space_size += len(poss)
                    choice = random.sample(poss, 1)[0]
                    points += [(word[choice], blick[choice], ngram[choice])]
                    lens += [len(poss)]
                    used[word[choice]] = 0
            for p in points:
                if self.handle_blick_disc(p[0]) in realword: real+=1
                outfile.write(",".join([str(iteration)] + [str(x) for x in p]) + "," + self.handle_blick_disc(p[0]) + "\n")
                outfile2.write(str(iteration) + "," + self.handle_blick_disc(p[0]) + "\n")
            print "space_size", space_size
            print "real word", real
        return

    def match_from_biglist(self, cv, iter, match):
        """Write to lexicons file 2 files: _info.txt with info and simple lex file _lex.txt"""
        a = [i.strip().split(",") for i in open(self.f).readlines()]
        word, blick, ngram, realword, realblick, realngram = [], [], [], [], [], []
        a = a[1:]
        random.shuffle(a)
        word_spot = 0
        if self.disc == 1: word_spot = -1
        for row in a[1:]:
            if row[3] != "Real":
                word += [row[word_spot]]; blick += [float(row[1])]; ngram += [float(row[2])]
            else: 
                realword += [row[word_spot]]; realblick += [float(row[1])]; realngram += [float(row[2])]
        if match == "ngram":
            p = zip(ngram); realpoints = zip(realngram); minpoint = .03
        elif match == "blick":
            p = zip(blick); realpoints = zip(realblick); minpoint = .03
        else: 
            p = zip(blick, ngram); realpoints = zip(realblick, realngram); minpoint = .03
        tree = kd(p)
        if cv == 0: minpoint = minpoint*.75
        print self.f
        outfile = open("Lexicons/lex_" + self.f.split("/")[-1][:-12] + "_cv" + str(cv) + "_iter" + str(iter) + "_mbigmatch_" + match +  "_info.txt", "w")
        outfile2 = open("Lexicons/lex_" + self.f.split("/")[-1][:-12] + "_cv" + str(cv) + "_iter" + str(iter) + "_mbigmatch_" + match + "_lex.txt", "w")
        self.match_loop(outfile, outfile2, realpoints, realword, realblick, realngram, self.f, cv, iter, minpoint, blick, ngram, word, tree)
        outfile.close()
        outfile2.close()
        return

    def evaluate(self, word):
        LM.evaluate(self, word)
        return 0.0

