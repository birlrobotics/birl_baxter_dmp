#!/usr/bin/env python
"""
pick and place service smach server

prereqursite:

!!Please rosrun dmp dmp_joint_trajectory_action_server.py first!
"""


import baxter_interface
from dmp.srv import *
import sys
import rospy
from srv_client import *
import open_drawer_client
import smach
import smach_ros
import config
from std_msgs.msg import Empty
import os
from birl_sim_examples.srv import *

import baxter_r_arm_dmp
from baxter_interface import CHECK_VERSION

class Go_to_start_position(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['Succeed'])
      
        
    def execute(self, userdata):


        baxter_r_arm_dmp.main(
            config.recorded_go_to_start_position_path,
            config.generalized_go_to_start_position_path
            ) 
        dmp0_traj = open_drawer_client.Trajectory()
        dmp0_traj.parse_file(config.generalized_go_to_start_position_path)
        dmp0_traj.start()
        dmp0_traj.wait()        
        return 'Succeed'
        
        
class Go_to_gripper_position(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['Succeed'])
      
        
    def execute(self, userdata):
 
        
        dmp1_traj = open_drawer_client.Trajectory()
        

        baxter_r_arm_dmp.main(
            config.recorded_go_to_gripper_position_path,
            config.generalized_go_to_gripper_position_path
           ) 

        dmp1_traj.parse_file(config.generalized_go_to_gripper_position_path)
        dmp1_traj.start()
        dmp1_traj.wait()
        dmp1_traj.gripper_close()
        return 'Succeed'





class Go_back(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['Succeed'])
   
        
    def execute(self, userdata):


        baxter_r_arm_dmp.main(
            config.recorded_go_back_path,
            config.generalized_go_back_path
            ) 

        dmp2_traj = open_drawer_client.Trajectory()
        dmp2_traj.parse_file(config.generalized_go_back_path)
        dmp2_traj.start() 
        dmp2_traj.wait()
        dmp2_traj.gripper_open()
        return 'Succeed'

class Go_forward(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['Succeed'])                
    def execute(self, userdata):

        baxter_r_arm_dmp.main(
            config.recorded_go_forward_path,
            config.generalized_go_forward_path
            ) 
        dmp3_traj = open_drawer_client.Trajectory()
        dmp3_traj.parse_file(config.generalized_go_forward_path)
        dmp3_traj.start()
        dmp3_traj.wait()
        return 'Succeed'




class Go_back_to_start_position(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['Succeed'])        
        
    def execute(self, userdata):
        baxter_r_arm_dmp.main(
            config.recorded_go_back_to_start_position_path,
            config.generalized_go_back_to_start_position_path) 

        dmp4_traj = open_drawer_client.Trajectory()
        dmp4_traj.parse_file(config.generalized_go_back_to_start_position_path)
        dmp4_traj.start()
        dmp4_traj.wait()
        return 'Succeed'



        
def main():

    global limb_interface
    rospy.init_node("open_drawer_joint_trajectory")
    print("Initializing node... ")
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    print("Enabling robot... ")
    rs.enable()
    print("Running. Ctrl-c to quit")
    

    limb = 'right'
    limb_interface = baxter_interface.limb.Limb(limb)


    sm = smach.StateMachine(outcomes=['TaskSucceed'])


    with sm:

        smach.StateMachine.add(
            'Go_to_start_position', 
            Go_to_start_position(),
            transitions={
                'Succeed':'Go_to_gripper_position'
            }
        )
        
        smach.StateMachine.add(
            'Go_to_gripper_position',
            Go_to_gripper_position(),
            transitions={
                'Succeed':'Go_back'
            }
        )
                               
        
        smach.StateMachine.add(
            'Go_back',
            Go_back(),
            transitions={
                'Succeed':'TaskSucceed'
            }
        )
        
        smach.StateMachine.add(
            'Go_forward',
            Go_forward(),
            transitions={
                'Succeed':'Go_back_to_start_position'
            }
        )
        
        smach.StateMachine.add(
            'Go_back_to_start_position',
            Go_back_to_start_position(),
            transitions={
                'Succeed':'TaskSucceed'
            }
        )
        
  
    sis = smach_ros.IntrospectionServer('MY_SERVER', sm, '/SM_ROOT')

    sis.start()
    outcome = sm.execute()

    rospy.spin()


if __name__ == '__main__':
    sys.exit(main())



