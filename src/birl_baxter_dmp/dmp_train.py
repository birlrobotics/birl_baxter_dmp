import pydmps.dmp_discrete
import ipdb
import pandas as pd
import numpy as np
import sys
# please install pydmp first 
# https://github.com/studywolf/pydmps
# input
# @list_of_traj_mats  list 
# @n_dmps     Integer   depends on the traj demonsion
# @n_bfs      Integer   how many basis functions you wanna set
# output
# w_avarage   list       aveage the weights
# type_of_basefunc  string      the type of basis fuction
def train(list_of_traj_mats, n_bfs=100): 

    trial_amount = len(list_of_traj_mats)
    n_dmps = list_of_traj_mats[0].shape[1]

    dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=n_dmps, n_bfs=n_bfs)

    w_list = []
    for trial in list_of_traj_mats: 
        dmp.imitate_path(y_des=trial.T) #train 7 demonsion    
        w_list.append(dmp.w)
    print w_list[0][0][0]
    w_sum = np.array(w_list)
    sum_j = 0  #iniliazition
    for j in w_sum:
        sum_j += j
    w_avarage = sum_j/len(w_list) 
    #ipdb.set_trace()
    print w_avarage[0,0] 
    if  w_list[0][0][0]==w_avarage[0,0] :
        print "right, the avrage is right"
    else:
        print "wrong, the avrage is wrong"
    type_of_basefunc = "Gaussian" 
    return w_avarage, type_of_basefunc     


if __name__ == '__main__':
     sys.exit(train())
        
