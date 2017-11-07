# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 16:48:02 2017

@author: tony
"""
import dmp_discrete
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.mplot3d import Axes3D


def main():
    data = "data_sets/3D_demo_data.txt"
    PointCount = len(open(data,'rU').readlines())
    Colum0_Traj=[0.0]*PointCount
    Colum1_Traj=[0.0]*PointCount
    Colum2_Traj=[0.0]*PointCount
    Colum0_Traj=[float(l.split()[0]) for l in open(data)]
    Colum1_Traj=[float(l.split()[1]) for l in open(data)]
    Colum2_Traj=[float(l.split()[2]) for l in open(data)]
    
    path1 = np.array(Colum0_Traj)
    path2 = np.array(Colum1_Traj)
    path3 = np.array(Colum2_Traj)
    
    num_bfs = [100] # you can manully set the number of basis functions depanding on how mant points do you have

    for ii, bfs in enumerate(num_bfs):
        dmp = dmp_discrete.DMPs_discrete(dmps=3, bfs=bfs)

        dmp.imitate_path(y_des=np.array([path1, path2, path3])) #train 3 demonsion
        
        # set the goal
        dmp.goal[0] = Colum0_Traj[-1]
        dmp.goal[1] = Colum1_Traj[-1]
        dmp.goal[2] = Colum2_Traj[-1]
        
        #set the initial state
        dmp.y0[0] = Colum0_Traj[0]
        dmp.y0[1] = Colum1_Traj[0]
        dmp.y0[2] = Colum2_Traj[0]
    
        
        #sampling rate, y_track is joint state,dy_track is velocity information, ddy_track is accelaration
        y_track, dy_track, ddy_track = dmp.rollout() 
        
        fig=plt.figure()
        ax = Axes3D(fig)    
        plt.xlabel('X')
        plt.ylabel('Y')
        
        #plot traj fig 
        ax.plot(Colum0_Traj,Colum1_Traj,Colum2_Traj,linewidth=1,alpha=0.3)       
        #Plot plan fig    
        ax.plot(y_track[:, 0],y_track[:, 1],y_track[:, 2],"--")

    
        #show the plot
        plt.draw()
        plt.show()
if __name__ == '__main__':
    
    sys.exit(main())
