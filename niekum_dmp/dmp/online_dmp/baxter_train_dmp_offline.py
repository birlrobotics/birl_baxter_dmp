#!/usr/bin/env python
import roslib;
import sys
import rospy
import numpy as np
import pandas as pd
from dmp.srv import *
from dmp.msg import *
from baxter_core_msgs.msg import JointCommand
from sensor_msgs.msg import JointState


class Dmp(object):
    # Learn a DMP from demonstration data
    def makeLFDRequest(self, dims, traj, dt, K_gain,
                       D_gain, num_bases):
        demotraj = DMPTraj()

        for i in range(len(traj)):
            pt = DMPPoint();
            pt.positions = traj[i]
            demotraj.points.append(pt)
            demotraj.times.append(dt * i)

        k_gains = [K_gain] * dims
        d_gains = [D_gain] * dims

        rospy.wait_for_service('learn_dmp_from_demo')
        try:
            lfd = rospy.ServiceProxy('learn_dmp_from_demo', LearnDMPFromDemo)
            resp = lfd(demotraj, k_gains, d_gains, num_bases)
        except rospy.ServiceException, e:
            pass

        return resp;

    # Set a DMP as active for planning
    def makeSetActiveRequest(self, dmp_list):
        try:
            sad = rospy.ServiceProxy('set_active_dmp', SetActiveDMP)
            sad(dmp_list)
        except rospy.ServiceException, e:
            pass;

            # Generate a plan from a DMP

    def makePlanRequest(self, x_0, x_dot_0, t_0, goal, goal_thresh,
                        seg_length, tau, dt, integrate_iter):
        rospy.wait_for_service('get_dmp_plan')
        try:
            gdp = rospy.ServiceProxy('get_dmp_plan', GetDMPPlan)
            resp = gdp(x_0, x_dot_0, t_0, goal, goal_thresh,
                       seg_length, tau, dt, integrate_iter)
        except rospy.ServiceException, e:
            pass

        return resp;

if __name__ == '__main__':
    dmp = Dmp()

    # read file
    record_trajectory_path = "/home/tony/ros/indigo/baxter_ws/src/birl_baxter/birl_baxter_dmp/dmp/pick_place_data/go_to_hover_position.txt"
    train_set = pd.read_csv(record_trajectory_path)

    train_len = len(train_set)
    resample_t = np.linspace(train_set.values[0, 0], train_set.values[-1, 0], train_len)
    joint0_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 9])
    joint1_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 10])
    joint2_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 11])
    joint3_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 12])
    joint4_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 13])
    joint5_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 14])
    joint6_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 15])

    traj = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]] * train_len
    for i in range(train_len):
        traj[i] = [joint0_data[i], joint1_data[i], joint2_data[i], joint3_data[i], joint4_data[i], joint5_data[i],
                   joint6_data[i]]

    # Create a DMP from a 7-D trajectory
    dims = 7
    dt = 0.1
    K = 100
    D = 2.0 * np.sqrt(K)
    num_bases = 200

    resp = dmp.makeLFDRequest(dims, traj, dt, K, D, num_bases)
    import pickle
    pickle.dump(resp, open("baxter_resp.pkl", "wb"))
    print "get data"

