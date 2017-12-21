# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 22:07:50 2017

@author: tony
"""

import sys
sys.path.append("../")
import pydmps
import pydmps.dmp_discrete

import pandas as pd
import numpy as np
import sys
import ipdb
#input
# @ starting_pose  list  depend on the dimension
# @ ending_pose    list 
# @ weight_mat     list
# @ tau            time scaling
# output
# @ y_track        list     generalized traj


def dmp_imitate(starting_pose, ending_pose, weight_mat, tau=1, n_bfs=100, base_fuc="Gaussian"):
    n_dmps = len(weight_mat)
    dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=n_dmps, n_bfs=n_bfs, w=weight_mat)

    for i in range(n_dmps):
        dmp.y0[i] = starting_pose[i]  #set the initial state
        dmp.goal[i] = ending_pose[i] # set the ending goal
    y_track, dy_track, ddy_track = dmp.rollout(tau=tau)
    
    return y_track


if __name__ == '__main__':
     sys.exit(dmp_imitate())
