#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from lab4.msg import RobotStatus
current_cmd_vel = Twist()
current_scan = None
def cmd_vel_callback(msg):
    global current_cmd_vel
    current_cmd_vel = msg
def scan_callback(msg):
    global current_scan
    current_scan = msg
def main():
    rospy.init_node('status_publisher')
    pub = rospy.Publisher('/robot_status', RobotStatus, queue_size=10)
    rospy.Subscriber('/cmd_vel', Twist, cmd_vel_callback)
    rospy.Subscriber('/scan', LaserScan, scan_callback)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if current_scan:
            msg = RobotStatus()
            msg.cmd_vel = current_cmd_vel
            ranges = current_scan.ranges
            n = len(ranges)
            msg.front_distance = min(ranges[0], ranges[-1])
            msg.left_distance = min(ranges[n//4-10:n//4+10])
            msg.right_distance = min(ranges[3*n//4-10:3*n//4+10])
            pub.publish(msg)
        rate.sleep()
if __name__ == '__main__':
    main()
