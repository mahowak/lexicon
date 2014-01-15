from gt import *


def CumFreq(acc, freqs):
    for p,s in freqs.iteritems():
        if p not in acc:
            acc[p] = {}
            for w,c in s.iteritems():
                if w not in acc[p]:
                    acc[p][w] = 0.0
                    acc[p][w] += c
    return acc

def generate_cf(cfd, grams):
    for ng in grams:
        cfd["".join(ng[:-1])].inc(ng[-1])
    return cfd




class KatzSmoothing():
  def __init__(self, n):
    self.n = n 
    self.k = 5
    self.smooth = ()

  def __d(self, r_star, r, k, n_1, n_k, n_k1):
    ''' given the gt count, actual count of ngrams, 
    limit k, and the frequency of frequency for ngrams 
    with count 1 and k+1, return the smoothing factor d 
    for ngrams with count less than k.
    '''
    factor = (k+1)*n_k1/n_1
    numerator = r_star/r - factor
    denominator = 1.0 - factor
    return numerator/denominator

  def find_n_k(self, freq_parameters):
    n1 = 0.0
    n_k = 0.0
    n_k1 = 0.0
    for p,s in freq_parameters.iteritems():
      for w,c in s.iteritems():
        r_star, nr, nr1, r = c
        if r == 1.0:
          n1 = nr
        if self.k == r:
          n_k = nr
          n_k1 = nr1
        if n1 > 0.0 and n_k > 0.0 and n_k1 > 0.0:
          #print n1, n_k, n_k1
          return n1, n_k, n_k1

  def smoothed_probs(self, freq_parameters):
    freqs, N = freq_parameters
    # get n_k, n_k1
    n1, n_k, n_k1 = self.find_n_k(freqs)
    
    probs = {}
    single_count_prob = 1.0
    for p,s in freqs.iteritems():
      if p not in probs:
        probs[p] = {}
      for w,c in s.iteritems():
        r_star, nr, nr1, r = c
        c_katz = r
        if r <= self.k:
          if r > 0.0:
            c_katz = self.__d(r_star, r, self.k, n1, n_k, n_k1)
        probs[p][w] = c_katz/N
        if probs[p][w] < single_count_prob:
          single_count_prob = probs[p][w]
    return (probs, single_count_prob)
  

  def smooth_cpd(self, cfd):
    acc = CumFreq({}, cfd)
    fof = [(i, float(len(n))) for (i,n) in freqOfFreq(acc)]
    self.smooth = smoothed_probs(smoothed_counts(acc, lin_reg(fof, log)))
    return self.smooth
 
