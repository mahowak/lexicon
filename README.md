**As of 15/01/14
As the main file (models_kyle.py) was getting messy, I took the initiative to split the file in several subfiles:
main.py (it's in the name)
A super class: lm.py (with methods create_model, generate, evaluate)
inheriting from the subclasses:
-> nphone.py
-> nsyll.py
-> bigmatch.py
-> pcfg.py
Option to chose the model should be specified in the command line:
(default nphone --n 3)
--model bigmatch_ngram
--model bigmatch_blick
--model bigmatch_both
--model pcfg
--model nsyll (only for n = 1 or n = 2)

Methods for evaluation are in evaluation.py (as now the cross entropy function is NOT returning cross-entropy but average logprob as I was checking for consistency with previous results -- I was used to the logprob -- so do not mind the crazy perplexity score)
Methods for generation are in generation.py

Now we can evaluate from nphone and nsyll by specifying:
--fnc evaluate
it smoothes the conditional probabilities with Katz's smoothing from katz.py and gt.py
As now the implementation is ugly and need to be updated, it was just to test that all is working fine.

--perplexity.py uses srilm--for any computer used, add srilm path at top of file
It accepts as input either a training list and a test list (with words already separate and spaced) or a training file and a test file with one word per line.
Currently can do either addsmooth or wbdiscount. If addsmooth, set the smoothing alpha (currently = .1)
New smoothing can be easily added by specifying it.


**OLD
-model.py main file for adding and implementing different models has two functions: 1. generating rand lexicon according to a given model (default mode) 2. evaluating the given model on a corpus (splitted between train and test set) currently implemented: ngrams on phones (default) ngrams on syllables: --model nsyll pcfg --model pcfg ngrams using pool of pre-generated word --model npool (match each real word with a non word of same ngram proba +/- eps)
--model bigmatch_ngram
--model bigmatch_blick
--model bigmatch_both

-calc_stats.py input lex file in format and output lexical stats in rfiles -1,word -1,word 0,simword 0,simword 1,simword1 1,simword1

-celex.py input arguments, output celex file in folder celexes (one word per line)

Code Notes:

the ngram syllable class is redundant with the simple ngram class, just made it as it is now to not mess up with the rest but could be merged
the smoothing function in nltk is buggy or just did not get why the number of bins should be precised if it is precisely for unseen data... (only useful for the evaluation function) UPDATE: it seems it work ok if you give an upper bound (such as the number of possible syllables or possible phonemes) but it may actually underestimate the right proba...
the npool model is not written as a class I just added a function generate_correct_number_pool. There is also an extra function for generating this pool of words if it does not already exist
there are several inelegant stuff I did, feel free to modify whatever you want, I am not particularly attached to anything!!
Results Notes:

the npool model get actually pretty close to the number of neighbors compared to the true lexicon if you make the eps quite small... compare between eps = 1e-2 and 1e-6 (it under or overshoots depending on the generated pool in fact), results are similar to the bisyllabic ngram model, about 80% of existing words generated so not surprinsingly very close to what the real lexicon is.
Also when evaluating the proba of a word in this model, even if it is true that we matched the ngram proba, the actual proba of the word is not that (or at least in the way i did it) because we need to take into account that we take a random word from the set S of all words in the interval +/-eps around the ngram proba of the real word. So the actual proba should be Pgram * 1/card(S)

-make_hists.R
-takes all files in rfiles (either indwords_ or global_) and makes histograms
-right now just for neighbors but easily modifiable for all
-ind_words contains length separated versions

