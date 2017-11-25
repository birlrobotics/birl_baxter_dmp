import sys
sys.path.append("../")
import pydmps
import pydmps.dmp_discrete
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



record_trajectory_path = "./cart.txt"
train_set = pd.read_csv(record_trajectory_path)  #using pandas read data
train_len = len(train_set)  # the lengh of data

x_data = train_set.values[:, 1]
y_data = train_set.values[:, 2]
z_data = train_set.values[:, 3]
w_x_data = train_set.values[:, 4]
w_y_data = train_set.values[:, 5]
w_z_data = train_set.values[:, 6]
w_w_data = train_set.values[:, 7]

path1 = np.array(x_data)
path2 = np.array(y_data)
path3 = np.array(z_data)
path4 = np.array(w_x_data)
path5 = np.array(w_y_data)
path6 = np.array(w_z_data)
path7 = np.array(w_w_data)

dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=7, n_bfs=200)
    
dmp.imitate_path(y_des=np.array([path1, path2, path3, path4, path5, path6, path7]))
#set the initial state
dmp.y0[0] = path1[0]
dmp.y0[1] = path2[0]
dmp.y0[2] = path3[0]
dmp.y0[3] = path4[0]
dmp.y0[4] = path5[0]
dmp.y0[5] = path6[0]
dmp.y0[6] = path7[0]

dmp.goal[0] = path1[-1]
dmp.goal[1] = path2[-1]
dmp.goal[2] = path3[-1]
dmp.goal[3] = path4[-1]
dmp.goal[4] = path5[-1]
dmp.goal[5] = path6[-1]
dmp.goal[6] = path7[-1]

y_track, dy_track, ddy_track = dmp.rollout(tau=0.2)


plt.figure(1)
plt.plot(x_data, label='x')
plt.plot(y_data,label='y')
plt.plot(z_data,label='z')
plt.plot(w_x_data,label='w_x')
plt.plot(w_y_data,label='w_y')
plt.plot(w_z_data,label='w_z')
plt.plot(w_w_data,label='w_w')
plt.legend()

plt.figure(2)
plt.plot(y_track[:,0],label='x')
plt.plot(y_track[:,1],label='y')
plt.plot(y_track[:,2],label='z')
plt.plot(y_track[:,3],label='w_x')
plt.plot(y_track[:,4],label='w_y')
plt.plot(y_track[:,5],label='w_z')
plt.plot(y_track[:,6],label='w_w')
plt.legend()
plt.show()

