#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


base_path ="/home/tony/codes/dmp_group/dmpbbo_changed"  # change to your own path to the package
inputs = np.loadtxt(base_path+'/src/dmp/demos/trajectory.txt') # import the data from txt file

#demonstration
t= inputs[:,0]  # time
y_1 = inputs[:,1] # position
y_2 = inputs[:,2]
y_1_v = inputs[:,3] # velocity
y_2_v = inputs[:,4]
y_1_v_dot = inputs[:,5] # accelaration
y_2_v_dot = inputs[:,6]

# reproduced traj 
inputs_reproduce = np.loadtxt(base_path+'/data_sets/demobaxter_trajectory/reproduced_traj.txt') 
t_reproduce= inputs_reproduce[:,0]
y_1_reproduce = inputs_reproduce[:,1]
y_2_reproduce = inputs_reproduce[:,2]
y_1_v_reproduce = inputs_reproduce[:,3]
y_2_v_reproduce = inputs_reproduce[:,4]
y_1_v_dot_reproduce = inputs_reproduce[:,5]
y_2_v_dot_reproduce = inputs_reproduce[:,6]

# reproduced forcing term
reproduced_forcing_terms = np.loadtxt(base_path+'/data_sets/demobaxter_trajectory/reproduced_forcing_terms.txt') 
f_1 = reproduced_forcing_terms[:,0]
f_2 = reproduced_forcing_terms[:,1]

# reproduced fa_output term
reproduced_fa_output = np.loadtxt(base_path+'/data_sets/demobaxter_trajectory/reproduced_fa_output.txt') 
fa_output_1 = reproduced_forcing_terms[:,0]
fa_output_2 = reproduced_forcing_terms[:,1]

########## plot ##########
fig_1=plt.figure(1)
ax_1 = Axes3D(fig_1)    
plt.xlabel('X')
plt.ylabel('Y')
ax_1.set_title('position demonstration')
#plot traj fig 
ax_1.plot(y_1,y_2,linewidth=2,alpha=0.3)  
ax_1.plot(y_1_reproduce,y_2_reproduce,'--',linewidth=2,alpha=0.3 )     

fig_2=plt.figure(2)
ax_2 = Axes3D(fig_2)    
plt.xlabel('X')
plt.ylabel('Y')
ax_2.set_title('velocity demonstration')
#plot traj fig 
ax_2.plot(y_1_v,y_2_v,linewidth=2,alpha=0.3)  
ax_2.plot(y_1_v_reproduce,y_2_v_reproduce,'--',linewidth=2,alpha=0.3)

fig_3=plt.figure(3)
ax_3 = Axes3D(fig_3)    
plt.xlabel('X')
plt.ylabel('Y')
ax_3.set_title('acceleration demonstration')
ax_3.plot(y_1_v_dot,y_2_v_dot,linewidth=2,alpha=0.3)  
ax_3.plot(y_1_v_dot_reproduce,y_2_v_dot_reproduce,'--',linewidth=2,alpha=0.3)


plt.show()