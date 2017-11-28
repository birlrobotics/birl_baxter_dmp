#!/usr/bin/python
import pandas as pd
import numpy as np
from birl_baxter_dmp.dmp_train import train
from birl_baxter_dmp.dmp_generalize import dmp_imitate

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
data = os.path.join(dir_path, "3D_demo_data.txt")

PointCount = len(open(data,'rU').readlines())
Colum0_Traj=[0.0]*PointCount
Colum1_Traj=[0.0]*PointCount
Colum2_Traj=[0.0]*PointCount
Colum0_Traj=[float(l.split()[0]) for l in open(data)]
Colum1_Traj=[float(l.split()[1]) for l in open(data)]
Colum2_Traj=[float(l.split()[2]) for l in open(data)]    
traj=[[0.0, 0.0, 0.0]]*PointCount
for i in range(PointCount):
    traj[i]=[Colum0_Traj[i], Colum1_Traj[i], Colum2_Traj[i]]

train_set = np.array([traj,traj])

param, _ = train(train_set, n_dmps=3)


start_point = [1.0000000e-02 , -8.0985915e-01 , -7.9287305e-01]
ending_point = [2.0000000e+00  , 5.0469484e-01  ,-8.0178174e-02]

y = dmp_imitate(starting_pose=start_point, ending_pose=ending_point, weight_mat=param,n_dmps=3 )
print y

