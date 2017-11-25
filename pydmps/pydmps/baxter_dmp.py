# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 16:48:02 2017

@author: tony
"""
import sys
sys.path.append("../")
import pydmps.dmp_discrete as dmp_discrete
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    # this file is recoded by baxter 
    # run this command to record data "rosrun baxter_examples joint_recorder.py -f path/file_name
    record_trajectory_path = "data_sets/baxter_training_data.txt"  
    train_set = pd.read_csv(record_trajectory_path)  #using pandas read data
    train_len = len(train_set)  # the lengh of data
    resample_t = np.linspace(0, train_set.values[-1, 0], train_len) # resampling the time
    joint0_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 9])
    joint1_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 10])
    joint2_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 11])
    joint3_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 12])
    joint4_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 13])
    joint5_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 14])
    joint6_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 15])

    num_bfs = [100] # you can manully set the number of basis functions depanding on how mant points do you have
  
    path1 = np.array(joint0_data)
    path2 = np.array(joint1_data)
    path3 = np.array(joint2_data)
    path4 = np.array(joint3_data)
    path5 = np.array(joint4_data)
    path6 = np.array(joint5_data)
    path7 = np.array(joint6_data)
    

    for ii, bfs in enumerate(num_bfs):
        dmp = dmp_discrete.DMPs_discrete(n_dmps=7, n_bfs=bfs)

        dmp.imitate_path(y_des=np.array([path1, path2, path3, path4, path5, path6, path7])) #train 7 demonsion
        
        # set the goal
        dmp.goal[0] = joint0_data[-1]
        dmp.goal[1] = joint1_data[-1]
        dmp.goal[2] = joint2_data[-1]
        dmp.goal[3] = joint3_data[-1]
        dmp.goal[4] = joint4_data[-1]
        dmp.goal[5] = joint5_data[-1]
        dmp.goal[6] = joint6_data[-1]
        
        #set the initial state
        dmp.y0[0] = joint0_data[0]
        dmp.y0[1] = joint1_data[0]
        dmp.y0[2] = joint2_data[0]
        dmp.y0[3] = joint3_data[0]
        dmp.y0[4] = joint4_data[0]
        dmp.y0[5] = joint5_data[0]
        dmp.y0[6] = joint6_data[0]
        
        # set time
        time_dmp = np.linspace(0,6,500) # this time is for dmp, in here the lengh of time is 6
        
        #sampling rate, y_track is joint state,dy_track is velocity information, ddy_track is accelaration
        y_track, dy_track, ddy_track = dmp.rollout(tau=0.2) 
        
        
#######################################  For plotting      
        plt.figure(1)  
        plt.subplot(711)
        plt.plot(resample_t, joint0_data,linewidth=1, linestyle="-", label="demestration")       
        plt.plot(time_dmp, y_track[:, 0],label='DMP imitation', lw=1)
        plt.xlabel("time")
        plt.ylabel("right_s0")
        plt.grid(True)
        plt.legend(loc='upper right')
        
        plt.subplot(712)
        plt.plot(resample_t, joint1_data,linewidth=1, linestyle="-", label="demestration")       
        plt.plot(time_dmp, y_track[:, 1],label='DMP imitation', lw=1)
        plt.ylabel("right_s1")
        plt.grid(True)

        plt.subplot(713)
        plt.plot(resample_t, joint2_data,linewidth=1, linestyle="-", label="demestration")       
        plt.plot(time_dmp, y_track[:, 2],label='DMP imitation', lw=1)
        plt.ylabel("right_e0")
        plt.grid(True)
        
        plt.subplot(714)
        plt.plot(resample_t, joint3_data,linewidth=1, linestyle="-", label="demestration")       
        plt.plot(time_dmp, y_track[:, 3],label='DMP imitation', lw=1)
        plt.ylabel("right_e1")
        plt.grid(True)
        
        plt.subplot(715)
        plt.plot(resample_t, joint4_data,linewidth=1, linestyle="-", label="demestration")       
        plt.plot(time_dmp, y_track[:, 4],label='DMP imitation', lw=1)
        plt.ylabel("right_w0")
        plt.grid(True)
        
        plt.subplot(716)
        plt.plot(resample_t, joint5_data,linewidth=1, linestyle="-", label="demestration")       
        plt.plot(time_dmp, y_track[:, 5],label='DMP imitation', lw=1)
        plt.ylabel("right_w1")
        plt.grid(True)
        
        plt.subplot(717)
        plt.plot(resample_t, joint6_data,linewidth=1, linestyle="-", label="demestration")       
        plt.plot(time_dmp, y_track[:, 6],label='DMP imitation', lw=1)
        plt.ylabel("right_w2")
        plt.grid(True)   
        plt.show()

#######################################  For plotting        

#######################################  saving data to a file 
  
#        
#        WriteFileDir = "./data_sets/baxter_dmp_runing.txt"   ## the path of generated dmp traj
#        plan_len = len(y_track[:,0])
#        f = open(WriteFileDir,'w')
#        f.write('time,')
#        f.write('right_s0,')
#        f.write('right_s1,')
#        f.write('right_e0,')
#        f.write('right_e1,')
#        f.write('right_w0,')
#        f.write('right_w1,')
#        f.write('right_w2\n')
#            
#        for i in range (plan_len):
#            f.write("%f," % (time_dmp[i],))
#            f.write(str(y_track[:, 0][i])+','+str(y_track[:, 1][i])+','+str(y_track[:, 2][i])+','
#            +str(y_track[:, 3][i])+','+str(y_track[:, 4][i])+','+str(y_track[:, 5][i])+','+str(y_track[:, 6][i])
#            +'\n')        
#        f.close()
   
if __name__ == '__main__':
     sys.exit(main())
