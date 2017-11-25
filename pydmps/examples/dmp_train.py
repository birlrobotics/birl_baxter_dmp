import sys
sys.path.append("../")
import pydmps
import pydmps.dmp_discrete

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def train(train_set,n_dmps=7,n_bfs=100): 
    w_list = []
    dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps, n_bfs)
    for trial in train_set:     # for every trial
        dmp.imitate_path(y_des=trial) #train 7 demonsion
        w_list.append(dmp.w)
    sum_j = 0  #iniliazition
    for j in w_list:
        sum_j += j
    w_avarage = sum_j/len(w_list)         
    type_of_basefunc = "Gaussian" 
    return w_avarage, type_of_basefunc     


if __name__ == '__main__':
     sys.exit(train())
        
