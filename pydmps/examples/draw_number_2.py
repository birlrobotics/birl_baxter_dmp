'''
Copyright (C) 2016 Travis DeWolf

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import sys
sys.path.append("../")
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pydmps
import pydmps.dmp_discrete

y_des = np.load('2.npz')['arr_0'].T
y_des -= y_des[:, 0][:, None]

# test normal run
dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=2, n_bfs=500, ay=np.ones(2)*10.0)
y_track = []
dy_track = []
ddy_track = []

dmp.imitate_path(y_des=y_des)
plt.figure(1)
plt.subplot(311)
psi_track = dmp.gen_psi(dmp.cs.rollout())
plt.plot(psi_track)
plt.title('basis functions')

# plot the desired forcing function vs approx
plt.subplot(312)
plt.plot(np.sum(psi_track * dmp.w[0], axis=1) * dmp.dt)
plt.legend(['w*psi'])
plt.title('DMP forcing function')
plt.tight_layout()

y_track, dy_track, ddy_track = dmp.rollout()


plt.subplot(313)
plt.plot(y_track[:,0], y_track[:, 1], 'b', lw=2)
plt.title('DMP system - draw number 2')

plt.axis('equal')
plt.xlim([-2, 2])
plt.ylim([-2, 2])
plt.show()
