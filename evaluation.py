from math import log

def log_prob(model, w):
  return log(model.evaluate(w), 2.0)

def cross_entropy(model, words, n):
  W_T = 0.0
  e = 0.0
  n = 0.0
  for w in words:
    W_T += float(len(w))
    e += model.evaluate(w)
  if W_T is 0.0:
    return 0
  return e/float(len(words))#(-1.0/(W_T - n)* e
  
def perplexity(e):
	return 2**e
