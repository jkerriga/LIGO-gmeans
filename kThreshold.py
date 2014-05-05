from numpy import *
from pylab import *
import matplotlib

def kThreshold(labels):
    below = 0
    for r in range(max(labels)+1):
        if len(labels[labels == r]) <= 20:
            below += 1
        else:
            continue
    return below
