-model.py
main file for adding and implementing different models has two functions: 
1. generating rand lexicon according to a given model (default mode)
2. evaluating the given model on a corpus (splitted between train and test set)
currently implemented:
ngrams on phones (default) 
ngrams on syllables: --model nsyll
pcfg --model pcfg
ngrams using pool of pre-generated word --model npool (match each real word with a non word of same ngram proba +/- eps)

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


Code Notes:
- the ngram syllable class is redundant with the simple ngram class, just made it as it is now to not mess up with the rest but could be merged
- the smoothing function in nltk is buggy or just did not get why the number of bins should be precised if it is precisely for unseen data... (only useful for the evaluation function) UPDATE: it seems it work ok if you give an upper bound (such as the number of possible syllables or possible phonemes) but it may actually underestimate the right proba...
- the npool model is not written as a class I just added a function generate_correct_number_pool. There is also an extra function for generating this pool of words if it does not already exist
- there are several inelegant stuff I did, feel free to modify whatever you want, I am not particularly attached to anything!!

Results Notes:
- the npool model get actually pretty close to the number of neighbors compared to the true lexicon if you make the eps quite small... compare between eps = 1e-2 and 1e-6 (it under or overshoots depending on the generated pool in fact), results are similar to the bisyllabic ngram model, about 80% of existing words generated so not surprinsingly very close to what the real lexicon is.
- Also when evaluating the proba of a word in this model, even if it is true that we matched the ngram proba, the actual proba of the word is not that (or at least in the way i did it) because we need to take into account that we take a random word from the set S of all words in the interval +/-eps around the ngram proba of the real word. So the actual proba should be Pgram * 1/card(S)
