# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 22:07:50 2017

@author: tony
"""

import sys
sys.path.append("../")
import pydmps
import pydmps.dmp_discrete
from sensor_msgs.msg import JointState
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import rospy
import baxter_interface
from baxter_interface import CHECK_VERSION


goal = []



def make_command(line):
    """
    Cleans a single line of recorded joint positions

    @param line: the line described in a list to process
    @param names: joint name keys
    """
    
    joint_cmd_names = [
            'right_s0',
            'right_s1',
            'right_e0',
            'right_e1',
            'right_w0',
            'right_w1',
            'right_w2',
        ]
    data_line =[line[0][0],line[0][1],line[0][2],line[0][3],line[0][4],line[0][5],line[0][6]]
    command = dict(zip(joint_cmd_names, data_line))
    return command


def callback(data):
    print "get data"
    global goal
    goal = [data.joints.position[0],data.joints.position[1],data.joints.position[2],data.joints.position[3],
    data.joints.position[4], data.joints.position[5], data.joints.position[6]]
    


def main():
    print("Initializing node... ")
    rospy.init_node("pydmp_node")
    print("Getting robot state... ")    
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled
    print("Enabling robot... ")
    rs.enable()

    rospy.Subscriber("cat_to_joint", JointState, callback)

    right = baxter_interface.Limb('right')
    record_trajectory_path = "data_sets/test.txt"
    train_set = pd.read_csv(record_trajectory_path)  #using pandas read data
    train_len = len(train_set)  # the lengh of data
    resample_t = np.linspace(0, train_set.values[-1, 0], train_len) # resampling the time
    joint0_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 9])
    joint1_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 10])
    joint2_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 11])
    joint3_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 12])
    joint4_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 13])
    joint5_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 14])
    joint6_data = np.interp(resample_t, train_set.values[:, 0], train_set.values[:, 15])

    # you can manully set the number of basis functions depanding on how mant points do you have
  
    path1 = np.array(joint0_data)
    path2 = np.array(joint1_data)
    path3 = np.array(joint2_data)
    path4 = np.array(joint3_data)
    path5 = np.array(joint4_data)
    path6 = np.array(joint5_data)
    path7 = np.array(joint6_data)
    

    dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=7, n_bfs=100)        
    dmp.imitate_path(y_des=np.array([path1, path2, path3, path4, path5, path6, path7]))
    
    plt.figure(1, figsize=(6,6))
    y_track, dy_track, ddy_track = dmp.rollout()
    plt.plot(y_track[:,0], y_track[:, 1], 'b--', lw=2, alpha=.5)
    
    time_dmp = np.linspace(0.2,6,100)
    
    dmp.reset_state()
    print("moving to start position")
    rcmd_start = make_command(y_track)
    right.move_to_joint_positions(rcmd_start)
    print("sucessful")
    y_track = []
    start_time = rospy.get_time()
    for t in range(dmp.timesteps):
        y, _, _ = dmp.step()
        y_track.append(np.copy(y))
        rcmd = make_command(y_track)  
        while (rospy.get_time() - start_time) < time_dmp[t]:
            right.set_joint_positions(rcmd)
        y_track = []
        global goal
        dmp.goal = goal

    
    


if __name__ == '__main__':
     sys.exit(main())
