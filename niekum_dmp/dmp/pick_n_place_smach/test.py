#!/usr/bin/env python
import rospy
from baxter_core_msgs.msg import JointCommand
import ipdb 
 
def callback(data):
    rospy.loginfo("get it")
    joint_states = data.command
    
    #ipdb.set_trace()
    
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/robot/limb/right/Joint_Commands", JointCommand, callback)
    global joint_states
    rospy.loginfo("get joint_states ", )
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

