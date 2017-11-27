import sys
sys.path.append("../")
import pydmps
import pydmps.dmp_discrete

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

import pickle
resp = pickle.load(open("simple_dmp_list.pkl", "rb")) 
dmp_w = resp[0]
dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=7, n_bfs=100)
dmp.w = dmp_w
dmp.goal[0] = resp[2][0]
dmp.goal[1] = resp[2][1]
dmp.goal[2] = resp[2][2]
dmp.goal[3] = resp[2][3]
dmp.goal[4] = resp[2][4]
dmp.goal[5] = resp[2][5]
dmp.goal[6] = resp[2][6]

#set the initial state
dmp.y0[0] = resp[1][0]
dmp.y0[1] = resp[1][1]
dmp.y0[2] = resp[1][2]
dmp.y0[3] = resp[1][3]
dmp.y0[4] = resp[1][4]
dmp.y0[5] = resp[1][5]
dmp.y0[6] = resp[1][6]

y_track, dy_track, ddy_track = dmp.rollout(tau=0.2)
plt.figure(1)
plt.plot(y_track[:,0])
plt.plot(y_track[:,1])
plt.plot(y_track[:,2])
plt.plot(y_track[:,3])
plt.plot(y_track[:,4])
plt.plot(y_track[:,5])
plt.plot(y_track[:,6])
#plt.subplot(311)
#plt.figure(1)
#plt.subplot(311)
#psi_track = dmp.gen_psi(dmp.cs.rollout())
#plt.plot(psi_track[0])
#plt.title('basis functions')
#
## plot the desired forcing function vs approx
#plt.subplot(312)
#plt.plot(dmp.w[0])
##plt.plot(np.sum(psi_track * dmp.w[0], axis=1) * dmp.dt)
##plt.plot(np.sum(psi_track * dmp.w[1], axis=1) * dmp.dt)
##plt.plot(np.sum(psi_track * dmp.w[2], axis=1) * dmp.dt)
##plt.plot(np.sum(psi_track * dmp.w[3], axis=1) * dmp.dt)
##plt.plot(np.sum(psi_track * dmp.w[4], axis=1) * dmp.dt)
##plt.plot(np.sum(psi_track * dmp.w[5], axis=1) * dmp.dt)
##plt.plot(np.sum(psi_track * dmp.w[6], axis=1) * dmp.dt)
#plt.legend(['w*psi'])
#plt.title('DMP forcing function')
#plt.tight_layout()
#
##plt.subplot(313)
##plt.plot(y_track[:,0], y_track[:, 1], 'b', lw=2)
##plt.title('DMP system - draw number 2')
#
#plt.axis('equal')
#plt.xlim([-2, 2])
#plt.ylim([-2, 2])
plt.show()