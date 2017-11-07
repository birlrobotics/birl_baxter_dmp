#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:18:31 2017

@author: tony
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from mpl_toolkits.mplot3d import Axes3D  

record_trajectory_path = 'cartesian_raw_data.txt'  # this traj is from recored baxter joint movement
train_set = pd.read_csv(record_trajectory_path)    
train_len = len(train_set) # the lengh of data

resample_t = np.linspace(train_set.values[0,0],train_set.values[-1,0],train_len)  # resample the time t
point_x_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,1]) # regenerate the traj relative to t
point_y_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,2])
point_z_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,3])
quan_x_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,4])
quan_y_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,5])
quan_z_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,6])
quan_w_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,7])

pose_data = [point_x_data,point_y_data,point_z_data,quan_x_data,quan_y_data,quan_z_data,quan_w_data] # for easy compute all the data 
pose_v_data = [point_x_data*0,point_y_data*0,point_z_data*0,quan_x_data*0,quan_y_data*0,quan_z_data*0,quan_w_data*0]
pose_v_dot_data = [point_x_data*0,point_y_data*0,point_z_data*0,quan_x_data*0,quan_y_data*0,quan_z_data*0,quan_w_data*0]

# compute velocity and accelaration
for k in range(0,7):             
    for i in xrange(1, train_len):    
        dx = pose_data[k][i] - pose_data[k][i-1]
        dt = resample_t[i] - resample_t[i-1]
        v = dx/dt    
        pose_v_data[k][i]=v
        v_dot = (pose_v_data[k][i] - pose_v_data[k][i-1]) / dt    
        pose_v_dot_data[k][i]=v_dot


#f1, axarr1 = plt.subplots(7, sharex=True)
#axarr1[0].set_title('right_arm_cartesion_space')
#axarr1[0].plot(resample_t, point_x_data )
#axarr1[1].plot(resample_t, point_y_data )
#axarr1[2].plot(resample_t, point_z_data )
#axarr1[3].plot(resample_t, quan_x_data )
#axarr1[4].plot(resample_t, quan_y_data)
#axarr1[5].plot(resample_t, quan_z_data)
#axarr1[6].plot(resample_t, quan_w_data)

ax = plt.figure().add_subplot(111, projection = '3d')  
xs = point_x_data
ys = point_y_data
zs = point_z_data
ax.scatter(xs, ys, zs, c = 'g') #点为红色三角形  
ax.set_xlabel('X Label')  
ax.set_ylabel('Y Label')  
ax.set_zlabel('Z Label')
plt.show() 


#f2, axarr2 = plt.subplots(7, sharex=True)
#axarr2[0].set_title('right_arm_cartesion_accelaration_space')
#axarr2[0].plot(resample_t, pose_v_dot_data[0])
#axarr2[1].plot(resample_t, pose_v_dot_data[1])
#axarr2[2].plot(resample_t, pose_v_dot_data[2])
#axarr2[3].plot(resample_t, pose_v_dot_data[3])
#axarr2[4].plot(resample_t, pose_v_dot_data[4])
#axarr2[5].plot(resample_t, pose_v_dot_data[5])
#axarr2[6].plot(resample_t, pose_v_dot_data[6])
#
#f3, axarr3 = plt.subplots(7, sharex=True)
#axarr3[0].set_title('right_arm_cartesion_velocity_space')
#axarr3[0].plot(resample_t, pose_v_data[0])
#axarr3[1].plot(resample_t, pose_v_data[1])
#axarr3[2].plot(resample_t, pose_v_data[2])
#axarr3[3].plot(resample_t, pose_v_data[3])
#axarr3[4].plot(resample_t, pose_v_data[4])
#axarr3[5].plot(resample_t, pose_v_data[5])
#axarr3[6].plot(resample_t, pose_v_data[6])


# write the data to file
#WriteFileDir="cartesion_baxter_data.txt"
#f = open(WriteFileDir,'w')
#for i in range(train_len-1):   
#   f.write(str(resample_t[i])+' '
#   +str(point_x_data[i])+' '+str(point_y_data[i])+' '+str(point_z_data[i])+' '+str(quan_x_data[i])+' '+str(quan_y_data[i])
#   +' '+str(quan_z_data[i])+' '+str(quan_w_data[i])+' '
#   +str(pose_v_data[0][i])+' '+str(pose_v_data[1][i])+' '+str(pose_v_data[2][i])+' '+str(pose_v_data[3][i])+' '
#   +str(pose_v_data[4][i])+' '+str(pose_v_data[5][i])+' '+str(pose_v_data[6][i])+' '
#   + str(pose_v_dot_data[0][i])+' '+ str(pose_v_dot_data[1][i])+' '+ str(pose_v_dot_data[2][i])+' '+ str(pose_v_dot_data[3][i])+' '
#   + str(pose_v_dot_data[4][i])+' '+ str(pose_v_dot_data[5][i])+' '+ str(pose_v_dot_data[6][i])+' '
#   +'\n')
#
#f.close()
#    
#plt.show()    
    
