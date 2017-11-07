#!/usr/bin/env python
# -*- coding: utf-8 -*-
import multiprocessing
import time
import baxter_interface
from baxter_interface import CHECK_VERSION
import rospy

class TarjExec(multiprocessing.Process):
    def __init__(
        self,
        com_queue
    ):
        multiprocessing.Process.__init__(self)
        self.com_queue = com_queue

    def run(self):
        rospy.init_node("TarjExec")
        print("Getting robot state... ")
        rs = baxter_interface.RobotEnable(CHECK_VERSION)
        init_state = rs.state().enabled
        print("Enabling robot... ")
        rs.enable()
        right = baxter_interface.Limb('right')
        joint_cmd_names = [
            'right_s0',
            'right_s1',
            'right_e0',
            'right_e1',
            'right_w0',
            'right_w1',
            'right_w2',
        ]

        traj_to_exec = self.com_queue.get()  # 获取队列中的数据
        while True:
            if not self.com_queue.empty():
                traj_to_exec = self.com_queue.get()

            if len(traj_to_exec) != 0:
                current_goal = traj_to_exec[0]
                del traj_to_exec[0]

                set_until_time = current_goal[0]

                rospy.loginfo("%s %s %s"%(time.time(),set_until_time, time.time() < set_until_time))
                while time.time() < set_until_time:
                    right.set_joint_positions(dict(zip(joint_cmd_names, current_goal[1:])))
            else:
                break