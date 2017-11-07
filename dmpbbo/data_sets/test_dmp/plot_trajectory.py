# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 21:32:52 2017

@author: tony
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt



inputs = np.loadtxt('/home/tony/dmpbbo/src/dmp/demos/trajectory.txt') 

t= inputs[:,0]
y_1 = inputs[:,1]
y_2 = inputs[:,2]
y_1_v = inputs[:,3]
y_2_v = inputs[:,4]
y_1_v_dot = inputs[:,5]
y_2_v_dot = inputs[:,6]

f1, axarr1 = plt.subplots(6, sharex=True)
axarr1[0].set_title('demonstration')
axarr1[0].plot(t, y_1)
axarr1[1].plot(t, y_2)
axarr1[2].plot(t, y_1_v)
axarr1[3].plot(t, y_2_v)
axarr1[4].plot(t, y_1_v_dot)
axarr1[5].plot(t, y_2_v_dot)

inputs_reproduce = np.loadtxt('/home/tony/dmpbbo/data_sets/demobaxter_trajectory/reproduced_traj.txt') 

t_reproduce= inputs_reproduce[:,0]
y_1_reproduce = inputs_reproduce[:,1]
y_2_reproduce = inputs_reproduce[:,2]
y_1_v_reproduce = inputs_reproduce[:,3]
y_2_v_reproduce = inputs_reproduce[:,4]
y_1_v_dot_reproduce = inputs_reproduce[:,5]
y_2_v_dot_reproduce = inputs_reproduce[:,6]

f2, axarr2 = plt.subplots(6, sharex=True)
axarr2[0].plot(t_reproduce, y_1_reproduce)
axarr2[0].set_title('reproduced trajectory')
axarr2[1].plot(t_reproduce, y_2_reproduce)
axarr2[2].plot(t_reproduce, y_1_v_reproduce)
axarr2[3].plot(t_reproduce, y_2_v_reproduce)
axarr2[4].plot(t_reproduce, y_1_v_dot_reproduce)
axarr2[5].plot(t_reproduce, y_2_v_dot_reproduce)

reproduced_forcing_terms = np.loadtxt('/home/tony/dmpbbo/data_sets/demobaxter_trajectory/reproduced_forcing_terms.txt') 
f_1 = reproduced_forcing_terms[:,0]
f_2 = reproduced_forcing_terms[:,1]
f3, axarr3 = plt.subplots(2, sharex=True)
axarr3[0].plot(t_reproduce, f_1)
axarr3[0].set_title('reproduced_forcing_terms')
axarr3[1].plot(t_reproduce, f_1)


reproduced_fa_output = np.loadtxt('/home/tony/dmpbbo/data_sets/demobaxter_trajectory/reproduced_fa_output.txt') 
fa_output_1 = reproduced_forcing_terms[:,0]
fa_output_2 = reproduced_forcing_terms[:,1]
f4, axarr4 = plt.subplots(2, sharex=True)
axarr4[0].plot(t_reproduce, fa_output_1)
axarr4[0].set_title('reproduced_fa_output')
axarr4[1].plot(t_reproduce, fa_output_1)


plt.show()