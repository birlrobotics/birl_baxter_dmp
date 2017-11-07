#!/usr/bin/env python
import sys
import rospy
import numpy as np
import pandas as pd
from dmp.srv import *
from dmp.msg import *
import matplotlib.pyplot as plt
import time
import baxter_interface
from baxter_interface import CHECK_VERSION
import ipdb


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


def main():
    rospy.init_node("online_dmp")
    dmp = Dmp()
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled
    print("Enabling robot... ")
    rs.enable()
    limb = "right"
    limb_interface = baxter_interface.limb.Limb(limb)
    right = baxter_interface.Limb(limb)
    joint_cmd_names = [
        'right_s0',
        'right_s1',
        'right_e0',
        'right_e1',
        'right_w0',
        'right_w1',
        'right_w2',
    ]

    import pickle
    resp = pickle.load(open("baxter_resp.pkl", "rb"))  # read data from resp.pkl
    # Set it as the active DMP

    dmp.makeSetActiveRequest(resp.dmp_list)


    x_dot_0 = [0.4, 0.4, 0.4, 0.4, 0.4, 0.0, 0.4]
    t_0 = 0  # better to choose the starting time in the record file
    goal_thresh = [0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]
    seg_length = -1  # Plan until convergence to goal
    tau = 1 * resp.tau  # Desired plan should take twice as long as demo #let see change to 1
    dt = 0.1
    integrate_iter = 2  # dt is rather large, so this is > 1


    while True:
        starting_angles = [limb_interface.joint_angle(joint) for joint in limb_interface.joint_names()]
        x_0 = starting_angles
        ending_angles = [0.144535667911,-1.01207718268,-0.2525872758,
                         0.894537748217,0.106522185666,1.28774855317,0.139064011456]
        goal = ending_angles

        plan = dmp.makePlanRequest(x_0, x_dot_0, t_0, goal, goal_thresh,
                                   seg_length, tau, dt, integrate_iter)
        #print plan



        Column0_plan = [0.0]
        Column1_plan = [0.0]
        Column2_plan = [0.0]
        Column3_plan = [0.0]
        Column4_plan = [0.0]
        Column5_plan = [0.0]
        Column6_plan = [0.0]

        Column0_plan = plan.plan.points[0].positions[0]
        Column1_plan = plan.plan.points[0].positions[1]
        Column2_plan = plan.plan.points[0].positions[2]
        Column3_plan = plan.plan.points[0].positions[3]
        Column4_plan = plan.plan.points[0].positions[4]
        Column5_plan = plan.plan.points[0].positions[5]
        Column6_plan = plan.plan.points[0].positions[6]

        joint_data = [Column0_plan,Column1_plan,Column2_plan,Column3_plan,Column4_plan,Column5_plan,Column6_plan]
        joint_cmd = dict(zip(joint_cmd_names, joint_data))

        set_until_time = plan.plan.times[0]

        start_time = time.time()
        print set_until_time 
        right.set_joint_positions(joint_cmd)
        #right.move_to_joint_positions(joint_cmd)
        while time.time()-start_time < set_until_time*0.7:
            pass

if __name__ == '__main__':
    sys.exit(main())
