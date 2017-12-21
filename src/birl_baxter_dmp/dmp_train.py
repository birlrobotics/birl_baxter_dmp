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
    n_dmps = train_set.shape[0]
    dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=n_dmps, n_bfs=n_bfs)
    dmp.imitate_path(y_des=train_set) #train 7 demonsion       
    type_of_basefunc = "Gaussian" 
    return dmp.w, type_of_basefunc     


if __name__ == '__main__':
     sys.exit(train())
        
