#!/usr/bin/env python
# -*- coding: utf-8 -*-
import multiprocessing
import baxter_interface
import time
import dmp_gen as dmp_traj_gen
import rospy

class TarjGen(multiprocessing.Process):
    def __init__(
        self,
        com_queue
    ):
        multiprocessing.Process.__init__(self)
        self.com_queue = com_queue

    def run(self):
        rospy.init_node("TarjGen")
        rospy.loginfo("TarjGen run")
        limb = 'right'
        limb_interface = baxter_interface.limb.Limb(limb)
        limb_interface.move_to_neutral()
        rospy.loginfo("move to neutral")
        joint_cmd_names = [
            'right_s0',
            'right_s1',
            'right_e0',
            'right_e1',
            'right_w0',
            'right_w1',
            'right_w2',
        ]
        """
        Move to starting position
        """
        move_to_start_position=[0.00841376457006,-0.550830582514,-0.00341249959604,0.757110843807,-0.00145716173142,1.25659545195,-0.00507347181644]
        limb_interface.move_to_joint_positions(dict(zip(joint_cmd_names, move_to_start_position)))
        rospy.loginfo("move to starting position")

        # x_0
        starting_angles_temp = [limb_interface.joint_angle(joint) for joint in limb_interface.joint_names()]
        while True:
            starting_angles = starting_angles_temp
            """
            为了不等待计算时间，我们不能把当前机器人的关节角度作为X0，而是要把DMP生成的那个点作为起始点，这样子就可以不要等待计算时间了。
            关键就在于机器人走到i点时一定要知道i+1这个点的位置！！！！！
            """
            
            # goal
            ending_angles = [0.608990372791,-0.668432128321,-0.0732475826215,1.07493703711,-0.00997087512126,1.17081083635,-0.399985490441]
            # get current time
            traj_start_time = time.time()
            # get DMP traj
            traj_to_ret = dmp_traj_gen.main( starting_angles,
                              ending_angles)
            rospy.loginfo("traj service done at %s"%(time.time()-traj_start_time,))
    
            # add traj_start_time to every timestamp in latest generated traj
            # b.c. timestamps in traj start from 0
            for idx in range(len(traj_to_ret)):
                traj_to_ret[idx][0] += traj_start_time
            self.com_queue.put(traj_to_ret)  #  写入队列
            rospy.loginfo("traj gen done at %s"%(time.time()-traj_start_time,))
            starting_angles_temp = dict(zip(joint_cmd_names, traj_to_ret))
                
            while True:
                target_changed = False
                if target_changed:
                    # get latest starting_angles
                    # get latest ending_angles
                    traj_start_time = time.now()
                    dmp_traj_gen.main( starting_angles,  ending_angles)
                    # add traj_start_time to every timestamp in latest generated traj
                    # b.c. timestamps in traj start from 0
    
                    # self.com_queue.put(latest_traj)
                else:
                    pass
                time.sleep(1)
