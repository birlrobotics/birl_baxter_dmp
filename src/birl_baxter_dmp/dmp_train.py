


import pydmps.dmp_discrete
import ipdb
import pandas as pd
import numpy as np
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
    w_list = []
    n_dmps = train_set[0].shape[1]
    dmp = pydmps.dmp_discrete.DMPs_discrete(dmps=n_dmps, bfs=n_bfs)
    for trial in train_set:     # for every trial
        dmp.imitate_path(y_des=trial) #train 7 demonsion
        w_list.append(dmp.w)
    w_sum = np.array(w_list)
    sum_j = 0  #iniliazition
    for j in w_sum:
        sum_j += j
    w_avarage = sum_j/len(w_list)         
    type_of_basefunc = "Gaussian" 
    return w_avarage, type_of_basefunc     


if __name__ == '__main__':
     sys.exit(train())
        
