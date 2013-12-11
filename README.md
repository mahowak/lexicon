-model.py
main file for adding and implementing different models has two functions: 
1. generating rand lexicon according to a given model (default mode)
2. evaluating the given model on a corpus (splitted between train and test set)
currently implemented:
ngrams on phones (default) 
ngrams on syllables: --model nsyll
pcfg --model pcfg
bigmatch --model bigmatch_both
--model bigmatch_ngram
--model bigmatch_

-calc_stats.py
input lex file in format and output lexical stats in rfiles
-1,word
-1,word
0,simword
0,simword
1,simword1
1,simword1

-celex.py
input arguments, output celex file in folder celexes (one word per line)


Notes:
- the ngram syllable class is redundant with the simple ngram class, just made it as it is now to not mess up with the rest but could be merged
- the smoothing function in nltk is buggy or just did not get why the number of bins should be precised if it is precisely for unseen data... (only useful for the evaluation function)
- there are several inelegant stuff I did, feel free to modify whatever you want, I am not particularly attached to anything!!

-make_hists.R
-takes all files in rfiles (either indwords_ or global_) and makes histograms
-right now just for neighbors but easily modifiable for all
-ind_words contains length separated versions

