#!/usr/bin/env python

import baxter_interface
from dmp.srv import *
import sys
import rospy
from srv_client import *
import pick_and_place_client
import smach
import smach_ros
import config
import os
from birl_sim_examples.srv import *
from baxter_core_msgs.msg import JointCommand

import baxter_r_arm_dmp
from baxter_interface import CHECK_VERSION

class Go_to_hover_position(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['Succeed'])
      
        
    def execute(self, userdata):
        global limb_interface
        global joint_states
        current_angles = [limb_interface.joint_angle(joint) for joint in limb_interface.joint_names()]
        baxter_r_arm_dmp.main(
            config.recorded_go_to_hover_position_path ,
            config.generalized_go_to_hover_position_path,
            current_angles, 
            [joint_states[0],joint_states[1],joint_states[2],
            joint_states[3],joint_states[4],joint_states[5],
            joint_states[6]]) 
        
        dmp0_traj = pick_and_place_client.Trajectory()
        dmp0_traj.parse_file(config.generalized_go_to_hover_position_path)
        dmp0_traj.start()
        dmp0_traj.wait()        
        return 'Succeed'
        
        """
class Go_to_pick_position(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['Succeed'])
      
        
    def execute(self, userdata):
 	global limb_interface
        current_angles = [limb_interface.joint_angle(joint) for joint in limb_interface.joint_names()]
        
        dmp1_traj = pick_and_place_client.Trajectory()
        

        baxter_r_arm_dmp.main(
            config.recorded_go_to_pick_position_path,
            config.generalized_go_to_pick_position_path,
           current_angles) 

        dmp1_traj.parse_file(config.generalized_go_to_pick_position_path)
        dmp1_traj.start()
        dmp1_traj.wait()
        dmp1_traj.gripper_close()
        return 'Succeed'





class Go_to_place_position(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['Succeed'])
   
        
    def execute(self, userdata):
	global limb_interface
        current_angles = [limb_interface.joint_angle(joint) for joint in limb_interface.joint_names()]

        baxter_r_arm_dmp.main(
            config.recorded_go_to_place_position_path,
            config.generalized_go_to_place_position_path,
            current_angles) 

        dmp2_traj = pick_and_place_client.Trajectory()
        dmp2_traj.parse_file(config.generalized_go_to_place_position_path)
        dmp2_traj.start() 
        dmp2_traj.wait()
        dmp2_traj.gripper_open()
        return 'Succeed'

class Go_back_to_start_position(smach.State):
    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['Succeed'])                
    def execute(self, userdata):
	global limb_interface
        current_angles = [limb_interface.joint_angle(joint) for joint in limb_interface.joint_names()]
        baxter_r_arm_dmp.main(
            config.recorded_go_back_position_path,
            config.generalized_go_back_position_path,
            current_angles) 
        dmp3_traj = pick_and_place_client.Trajectory()
        dmp3_traj.parse_file(config.generalized_go_back_position_path)
        dmp3_traj.start()
        dmp3_traj.wait()
        return 'Succeed'
        """

def callback(data):
	#rospy.loginfo("get the version information")
	global joint_states
	joint_states = data.command
	
	
	


joint_states =[]
        
def main():

    global limb_interface
    rospy.init_node("open_drawer_joint_trajectory")
    print("Initializing node... ")
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    print("Enabling robot... ")
    rs.enable()
    print("Running. Ctrl-c to quit")
    
    global limb_interface
    limb = 'right'
    limb_interface = baxter_interface.limb.Limb(limb)
    global joint_states
    rospy.Subscriber("/robot/limb/right/Joint_Commands", JointCommand, callback)
    
    rospy.loginfo("get joint_states ")
    
    
   

    sm = smach.StateMachine(outcomes=['TaskSucceed'])


    with sm:

        smach.StateMachine.add(
            'Go_to_hover_position', 
            Go_to_hover_position(),
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



