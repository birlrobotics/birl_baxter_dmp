#!/usr/bin/python
import pandas as pd
import numpy as np
from birl_baxter_dmp.dmp_train import train
from birl_baxter_dmp.dmp_generalize import dmp_imitate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pydmps
import pydmps.dmp_discrete

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
y_des = np.array([[Colum0_Traj,Colum1_Traj,Colum2_Traj]]) # 
'''
If you wanna put in a set data, do it like this  y_des = np.array([[Colum0_Traj,Colum1_Traj,Colum2_Traj]])
If you wanna put in many sets data, do it like this y_des = np.array([[Colum0_Traj,Colum1_Traj,Colum2_Traj],[Colum0_Traj,Colum1_Traj,Colum2_Traj]])
'''
######
#dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=3, n_bfs=500, ay=np.ones(3)*10.0)
#dmp.imitate_path(y_des=y_des, plot=True)
#y_track, dy_track, ddy_track = dmp.rollout()
######


train_set = y_des 


param, base_function = train(train_set)


start_point = traj[0]
ending_point = traj[-1]

y_track = dmp_imitate(starting_pose=start_point, ending_pose=ending_point, weight_mat=param )

#creat fig
fig=plt.figure()
ax = Axes3D(fig)    
plt.xlabel('X')
plt.ylabel('Y')

#plot traj fig 
ax.plot(Colum0_Traj,Colum1_Traj,Colum2_Traj,linewidth=4,alpha=0.3)       
#Plot plan fig    
ax.plot(y_track[:,0],y_track[:,1],y_track[:,2],"--")
#Plot plan fig    
#show the plot
plt.draw()
plt.show()
