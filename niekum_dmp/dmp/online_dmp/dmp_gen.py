#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import rospy
import numpy as np
import pandas as pd 
from dmp.srv import *
from dmp.msg import *
import matplotlib.pyplot as plt




class Dmp(object):


#Learn a DMP from demonstration data
    def makeLFDRequest(self,dims, traj, dt, K_gain,
                       D_gain, num_bases):
        demotraj = DMPTraj()
    
        for i in range(len(traj)):
            pt = DMPPoint();
            pt.positions = traj[i]
            demotraj.points.append(pt)
            demotraj.times.append(dt*i)
    
        k_gains = [K_gain]*dims
        d_gains = [D_gain]*dims
    
        rospy.wait_for_service('learn_dmp_from_demo')
        try:
            lfd = rospy.ServiceProxy('learn_dmp_from_demo', LearnDMPFromDemo)
            resp = lfd(demotraj, k_gains, d_gains, num_bases)
        except rospy.ServiceException, e:
            pass 

        return resp;


#Set a DMP as active for planning
    def makeSetActiveRequest(self,dmp_list):
        try:
            sad = rospy.ServiceProxy('set_active_dmp', SetActiveDMP)
            sad(dmp_list)
        except rospy.ServiceException, e:
            pass;

#Generate a plan from a DMP
    def makePlanRequest(self,x_0, x_dot_0, t_0, goal, goal_thresh,
                        seg_length, tau, dt, integrate_iter):
        rospy.wait_for_service('get_dmp_plan')
        try:
            gdp = rospy.ServiceProxy('get_dmp_plan', GetDMPPlan)
            resp = gdp(x_0, x_dot_0, t_0, goal, goal_thresh,
                       seg_length, tau, dt, integrate_iter)
        except rospy.ServiceException, e:
            pass
    
        return resp;






def main( starting_angles, ending_angles ):
    dmp = Dmp()

    import pickle
    resp = pickle.load(open("baxter_resp.pkl", "rb"))  # read data from resp.pkl
    #Set it as the active DMP

    dmp.makeSetActiveRequest(resp.dmp_list)

    #Now, generate a plan

    x_0 = starting_angles

    x_dot_0 = [0.4, 0.4, 0.4, 0.4, 0.4, 0.0, 0.4]

    t_0 = 0 # better to choose the starting time in the record file

    #goal =[ joint0_data[-1],joint1_data[-1], joint2_data[-1], joint3_data[-1],joint4_data[-1],joint5_data[-1], joint6_data[-1]         ]
    goal = ending_angles
    goal_thresh = [0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]

    seg_length = -1          #Plan until convergence to goal

    tau = 1 * resp.tau       #Desired plan should take twice as long as demo #let see change to 1
    dt = 0.01
    integrate_iter = 5       #dt is rather large, so this is > 1

    plan = dmp.makePlanRequest(x_0, x_dot_0, t_0, goal, goal_thresh,
                           seg_length, tau, dt, integrate_iter)



####################################### finish dmp #################################################################

####################################### plot the curve generated by dmp #################################################################

    Column0_plan = [0.0]*len(plan.plan.times)
    Column1_plan = [0.0]*len(plan.plan.times)
    Column2_plan = [0.0]*len(plan.plan.times)
    Column3_plan = [0.0]*len(plan.plan.times)
    Column4_plan = [0.0]*len(plan.plan.times)
    Column5_plan = [0.0]*len(plan.plan.times)
    Column6_plan = [0.0]*len(plan.plan.times)
    for i in range(len(plan.plan.times)):
        Column0_plan[i] = plan.plan.points[i].positions[0]
        Column1_plan[i] = plan.plan.points[i].positions[1]
        Column2_plan[i] = plan.plan.points[i].positions[2]
        Column3_plan[i] = plan.plan.points[i].positions[3]
        Column4_plan[i] = plan.plan.points[i].positions[4]
        Column5_plan[i] = plan.plan.points[i].positions[5]
        Column6_plan[i] = plan.plan.points[i].positions[6]

    resample_t0 = np.linspace(0.01, plan.plan.times[-1], len(plan.plan.times))

    joint0_data_plan = np.interp(resample_t0, plan.plan.times, Column0_plan)
    joint1_data_plan = np.interp(resample_t0, plan.plan.times, Column1_plan)
    joint2_data_plan = np.interp(resample_t0, plan.plan.times, Column2_plan)
    joint3_data_plan = np.interp(resample_t0, plan.plan.times, Column3_plan)
    joint4_data_plan = np.interp(resample_t0, plan.plan.times, Column4_plan)
    joint5_data_plan = np.interp(resample_t0, plan.plan.times, Column5_plan)
    joint6_data_plan = np.interp(resample_t0, plan.plan.times, Column6_plan)

    f1, axarr1 = plt.subplots(7, sharex=True)
    axarr1[0].plot(plan.plan.times, joint0_data_plan)
    axarr1[0].set_title('right_arm_joint_space1')
    axarr1[1].plot(plan.plan.times, joint1_data_plan)
    axarr1[2].plot(plan.plan.times, joint2_data_plan)
    axarr1[3].plot(plan.plan.times, joint3_data_plan)
    axarr1[4].plot(plan.plan.times, joint4_data_plan)
    axarr1[5].plot(plan.plan.times, joint5_data_plan)
    axarr1[6].plot(plan.plan.times, joint6_data_plan)
    #plt.show()
    traj_to_ret = []
    rospy.loginfo("run to traj_to_ret")
    for i in range(len(plan.plan.times)):
        traj_to_ret.append(
            [
                resample_t0[i],
                joint0_data_plan[i],
                joint1_data_plan[i],
                joint2_data_plan[i],
                joint3_data_plan[i],
                joint4_data_plan[i],
                joint5_data_plan[i],
                joint6_data_plan[i],
            ]
        )
    return traj_to_ret


if __name__ == '__main__':
     sys.exit(main())
