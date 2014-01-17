from math import log,exp,sqrt
from operator import itemgetter, mul

def freqOfFreq(freq):
  ''' given a dictionary of ngrams, re-index the ngrams by their frequency.'''
  fof = {}
  for p,s in freq.iteritems():
    for w,f in s.iteritems():
      if f not in fof:
        fof[f] = []
      fof[f].append((p,w))
  return sorted(fof.items(), key=itemgetter(0), reverse=True)
  
  
def lin_reg(list_of_tuples, fn=lambda x: x):
  ''' Given a list of tuples of floats, and a function
  return the slope and intercept of the regression line 
  of the data with the function applied to each element.
   '''
  N, x, y, x_2, x_y = 0.0, 0.0, 0.0, 0.0, 0.0
  for (f,fof) in list_of_tuples:
    N += fof
    fn_f = fn(f)
    fn_fof = fn(fof)
    x += fn_f
    y += fn_fof
    x_2 += fn_f*fn_f
    x_y += fn_f*fn_fof
  slope = (N*x_y - x*y)/(N*x_2 - x*x)
  intercept = (y - slope*x)/N
  return (slope,intercept)
  
def smoothed_counts(freq, (slope, intercept)):
  ''' for each ngram in freq, determine r* = (r+1)*n_r_+_1/n_r 
  as the smoothed count of each ngram in the model
  '''
  freq_rewrite = {}
  N = 0.0
  for p,s in freq.iteritems():
    if p not in freq_rewrite:
      freq_rewrite[p] = {}
    for w,r in s.iteritems():
      N_r = exp(intercept+slope*log(r))
      N_r1 = exp(intercept+slope*log(r+1))
      r_star = (r+1)*N_r1/N_r
      freq_rewrite[p][w] = (r_star, N_r, N_r1, r)
      N += N_r * r_star
  return (freq_rewrite, N)
  

def smoothed_probs(freq_new):
  ''' Given frequency from smoothed count, return model probability.'''
  freqs, N = freq_new
  probs = {}
  single_count_prob = 1.0
  for p,s in freqs.iteritems():
    if p not in probs:
      probs[p] = {}
    for w,c in s.iteritems():
      r_star, nr, nr1, r = c
      probs[p][w] = r/N
      if probs[p][w] < single_count_prob:
        single_count_prob = probs[p][w]
  return (probs, single_count_prob)


