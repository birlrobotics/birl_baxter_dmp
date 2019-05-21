#!/usr/bin/python
import pandas as pd
import numpy as np
from birl_baxter_dmp.dmp_train import train
from birl_baxter_dmp.dmp_generalize import dmp_imitate
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import pydmps
import pydmps.dmp_discrete
import ipdb
import os

matplotlib.rcParams['font.family'] = "Times New Roman"
matplotlib.rcParams['legend.fontsize'] = 12
matplotlib.rcParams['font.size'] = 14

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
y_des = np.array([Colum0_Traj,Colum1_Traj,Colum2_Traj]) # 
y_des = y_des.T

train_set = [y_des] 

param, base_function = train(train_set)

#creat fig
fig=plt.figure()#figsize=(6,6)
ax = Axes3D(fig)    
ax.set_xlabel('x(m)')
ax.set_ylabel('y(m)')
ax.set_zlabel('z(m)')


start_point = traj[0]
ending_point = traj[-1]
#plot traj fig 
ax.plot(Colum0_Traj,Colum1_Traj,Colum2_Traj,linewidth=2, alpha=1.0, c ='blue' , label="Demonstration")
y_track = dmp_imitate(starting_pose=start_point, ending_pose=ending_point, weight_mat=param )
#Plot plan fig    
ax.plot(y_track[:,0],y_track[:,1],y_track[:,2],ls = "--", c = 'gray', label="Generation")

track_sample = 20
mu, sigma = 0.1, 0.1
noises = np.random.normal(mu, sigma, (track_sample, 3))

for i in range(track_sample):
    noise = noises[i, :]
    start_point = (np.array(traj[0]) + noise).tolist()
    ending_point = (np.array(traj[-1]) + noise).tolist()                       
    y_track = dmp_imitate(starting_pose=start_point, ending_pose=ending_point, weight_mat=param )
    #Plot plan fig    
    ax.plot(y_track[:,0],y_track[:,1],y_track[:,2],ls = "--", c = 'gray')


plt.legend(loc=5)
plt.draw()
fig.savefig('dmp_demo.eps', format='eps', dpi=300)
fig.savefig('dmp_demo.png', format='png', dpi=300)
plt.show()
