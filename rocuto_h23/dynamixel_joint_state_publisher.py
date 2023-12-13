#!/usr/bin/env python
import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

import rospy
import yaml
from sensor_msgs.msg import JointState

# def load_config():
#     file_path = rospy.get_param("$(find dynamixel_use)/script/", 'joint_config.yaml')
#     with open(file_path, 'r') as file:
#         config = yaml.safe_load(file)
#     return config

def joint_state_publisher():
    rospy.init_node('joint_state_publisher', anonymous=True)

    # config = load_config()
    # joint_names = config.get('joint_names', [])
    # initial_positions = config.get('initial_positions', [])
    # publish_rate = config.get('publish_rate', 10) 

    joint_names = ["frame_to_link1", "link1_to_link2"]
    initial_positions = [0.0, 0.0]
    publish_rate = 10 

    num_joints = len(joint_names)
    if num_joints == 0 or num_joints != len(initial_positions):
        rospy.loggerr("Invalid joint configuration. Please check the YAML file")
        return

    pub = rospy.Publisher('/joint_states', JointState, queue_size=10)
    rate = rospy.Rate(publish_rate)

    while not rospy.is_shutdown():
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = rospy.Time.now()
        joint_state_msg.name = joint_names
        joint_state_msg.position = [0.0] * num_joints

        pub.publish(joint_state_msg)
        rate.sleep()

if __name__=='__main__':
    try:
        joint_state_publisher()
    except rospy.ROSInterruptException:
        pass
