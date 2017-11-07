#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:18:31 2017

@author: tony
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

record_trajectory_path = 'joint_raw_data_part2.txt'  # this traj is from recored baxter joint movement
train_set = pd.read_csv(record_trajectory_path)    
train_len = len(train_set) # the lengh of data

resample_t = np.linspace(train_set.values[0,0],train_set.values[-1,0],train_len)  # resample the time t
joint0_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,9]) # regenerate the traj relative to t
joint1_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,10])
joint2_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,11])
joint3_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,12])
joint4_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,13])
joint5_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,14])
joint6_data = np.interp(resample_t, train_set.values[:,0], train_set.values[:,15])

joint_data = [joint0_data,joint1_data,joint2_data,joint3_data,joint4_data,joint5_data,joint6_data] # for easy compute all the data 
joint_v_data = [joint0_data*0,joint1_data*0,joint2_data*0,joint3_data*0,joint4_data*0,joint5_data*0,joint6_data*0]
joint_v_dot_data = [joint0_data*0,joint1_data*0,joint2_data*0,joint3_data*0,joint4_data*0,joint5_data*0,joint6_data*0]

# compute velocity and accelaration
for k in range(0,7):             
    for i in xrange(1, train_len):    
        dx = joint_data[k][i] - joint_data[k][i-1]
        dt = resample_t[i] - resample_t[i-1]
        v = dx/dt    
        joint_v_data[k][i]=v
        v_dot = (joint_v_data[k][i] - joint_v_data[k][i-1]) / dt    
        joint_v_dot_data[k][i]=v_dot


f1, axarr1 = plt.subplots(7, sharex=True)
axarr1[0].plot(resample_t, joint0_data)
axarr1[0].set_title('right_arm_joint_space')
axarr1[1].plot(resample_t, joint1_data)
axarr1[2].plot(resample_t, joint2_data)
axarr1[3].plot(resample_t, joint3_data)
axarr1[4].plot(resample_t, joint4_data)
axarr1[5].plot(resample_t, joint5_data)
axarr1[6].plot(resample_t, joint6_data)

f2, axarr2 = plt.subplots(7, sharex=True)
axarr2[0].plot(resample_t, joint_v_data[0])
axarr2[0].set_title('right_arm_joint_velocity_space')
axarr2[1].plot(resample_t, joint_v_data[1])
axarr2[2].plot(resample_t, joint_v_data[2])
axarr2[3].plot(resample_t, joint_v_data[3])
axarr2[4].plot(resample_t, joint_v_data[4])
axarr2[5].plot(resample_t, joint_v_data[5])
axarr2[6].plot(resample_t, joint_v_data[6])

f2, axarr2 = plt.subplots(7, sharex=True)
axarr2[0].plot(resample_t, joint_v_data[0])
axarr2[0].set_title('right_arm_acceleratiom_space')
axarr2[1].plot(resample_t, joint_v_dot_data[1])
axarr2[2].plot(resample_t, joint_v_dot_data[2])
axarr2[3].plot(resample_t, joint_v_dot_data[3])
axarr2[4].plot(resample_t, joint_v_dot_data[4])
axarr2[5].plot(resample_t, joint_v_dot_data[5])
axarr2[6].plot(resample_t, joint_v_dot_data[6])


# write the data to file
WriteFileDir="test_real_robot.txt"
f = open(WriteFileDir,'w')
for i in range(train_len-1):   
   f.write(str(resample_t[i])+' '
   +str(joint0_data[i])+' '+str(joint1_data[i])+' '+str(joint2_data[i])+' '+str(joint3_data[i])+' '+str(joint4_data[i])
   +' '+str(joint5_data[i])+' '+str(joint6_data[i])+' '
   +str(joint_v_data[0][i])+' '+str(joint_v_data[1][i])+' '+str(joint_v_data[2][i])+' '+str(joint_v_data[3][i])+' '
   +str(joint_v_data[4][i])+' '+str(joint_v_data[5][i])+' '+str(joint_v_data[6][i])+' '
   + str(joint_v_dot_data[0][i])+' '+ str(joint_v_dot_data[1][i])+' '+ str(joint_v_dot_data[2][i])+' '+ str(joint_v_dot_data[3][i])+' '
   + str(joint_v_dot_data[4][i])+' '+ str(joint_v_dot_data[5][i])+' '+ str(joint_v_dot_data[6][i])+' '
   +'\n')

f.close()
    
plt.show()    
    