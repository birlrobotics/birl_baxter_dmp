#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

base_path = "/home/tony/codes/dmp_group/dmpbbo_changed/data_sets/demobaxter"


inputs = np.loadtxt(base_path+'/reproduced_traj.txt') 
train_len = len(inputs)
t= inputs[:,0]
y_1 = inputs[:,1]
y_2 = inputs[:,2]
y_3 = inputs[:,3]
y_4 = inputs[:,4]
y_5 = inputs[:,5]
y_6 = inputs[:,6]
y_7 = inputs[:,7]

f1, axarr1 = plt.subplots(7, sharex=True)
axarr1[0].plot(t, y_1)
axarr1[0].set_title('reproduced trajectory')
axarr1[1].plot(t, y_2)
axarr1[2].plot(t, y_3)
axarr1[3].plot(t, y_4)
axarr1[4].plot(t, y_5)
axarr1[5].plot(t, y_6)
axarr1[6].plot(t, y_7)

y_1_v = inputs[:,8]
y_2_v = inputs[:,9]
y_3_v = inputs[:,10]
y_4_v = inputs[:,11]
y_5_v = inputs[:,12]
y_6_v = inputs[:,13]
y_7_v = inputs[:,14]

f2, axarr2 = plt.subplots(7, sharex=True)
axarr2[0].plot(t, y_1_v)
axarr2[0].set_title('reproduced velocity')
axarr2[1].plot(t, y_2_v)
axarr2[2].plot(t, y_3_v)
axarr2[3].plot(t, y_4_v)
axarr2[4].plot(t, y_5_v)
axarr2[5].plot(t, y_6_v)
axarr2[6].plot(t, y_7_v)

y_1_v_dot = inputs[:,15]
y_2_v_dot = inputs[:,16]
y_3_v_dot = inputs[:,17]
y_4_v_dot = inputs[:,18]
y_5_v_dot = inputs[:,19]
y_6_v_dot = inputs[:,20]
y_7_v_dot = inputs[:,21]

f3, axarr3 = plt.subplots(7, sharex=True)
axarr3[0].plot(t, y_1_v_dot)
axarr3[0].set_title('reproduced acceleration')
axarr3[1].plot(t, y_2_v_dot)
axarr3[2].plot(t, y_3_v_dot)
axarr3[3].plot(t, y_4_v_dot)
axarr3[4].plot(t, y_5_v_dot)
axarr3[5].plot(t, y_6_v_dot)
axarr3[6].plot(t, y_7_v_dot)

WriteFileDir="test_in_baxter.txt"
f = open(WriteFileDir,'w')
f.write('time,')
f.write('right_s0,')
f.write('right_s1,')
f.write('right_e0,')
f.write('right_e1,')
f.write('right_w0,')
f.write('right_w1,')
f.write('right_w2\n')
for i in range(train_len-1):  
    f.write(str(t[i])+','+str(y_1[i])+','+str(y_2[i])+','+str(y_3[i])+','+str(y_4[i])+','+str(y_5[i])+','+str(y_6[i])+','+str(y_7[i])
    +'\n')
f.close()
plt.show()