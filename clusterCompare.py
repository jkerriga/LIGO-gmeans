from numpy import *
from scipy import *
from pylab import *

def clusterCompare(obs,init_labels,found_labels):
    acc = []
    clst_track = []
    for i in arange(max(init_labels)+1):
        labels_a = obs[init_labels == i,1]
        clst_acc = []
        x = 0
        for j in arange(max(found_labels)+1):
            x = 0
            labels_b = obs[found_labels == j,1]
            for a in labels_a:
                for b in labels_b:
                    if(a == b):
                        x += 1.0
                        break
            x = x/len(labels_a)
            clst_acc.append(x)
            
            x = 0

        clst_track.append(argmax(clst_acc))
        acc.append(max(clst_acc))

    return acc,clst_track
