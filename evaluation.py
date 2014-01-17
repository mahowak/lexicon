from math import log

def log_prob(model, w):
  return log(model.evaluate(w), 2.0)

def cross_entropy(model, words):
  W_T = 0.0
  e = 0.0
  n = 0.0
  for w in words:
    W_T += float(len(w))
    temp_n, temp_e = model.evaluate(w)
    e += temp_e
    n += temp_n
  if W_T is 0.0:
    return 0
  return -1.0/n* e
  
def perplexity(e):
	return 2**e
