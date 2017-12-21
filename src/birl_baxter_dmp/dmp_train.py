import pydmps.dmp_discrete
import ipdb
import pandas as pd
import numpy as np
import sys
# please install pydmp first 
# https://github.com/studywolf/pydmps
# input
# @train_set  list 
# @n_dmps     Integer   depends on the traj demonsion
# @n_bfs      Integer   how many basis functions you wanna set
# output
# w_avarage   list       aveage the weights
# type_of_basefunc  string      the type of basis fuction
def train(train_set, n_bfs=100): 
    n_dmps = train_set.shape[1]
    dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=n_dmps, n_bfs=n_bfs)
    dmp_w = []
    for trials in train_set: 
        dmp.imitate_path(y_des=trials) #train 7 demonsion    
        dmp_w.append(dmp.w)
    print dmp_w
    t = []
    for i in dmp_w:
        t = t+i
    t= t/len(dmp_w)
    type_of_basefunc = "Gaussian" 
    return dmp_w, type_of_basefunc     


if __name__ == '__main__':
     sys.exit(train())
        
