#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

pub = None

def scan_callback(msg):
    ranges = msg.ranges
    n = len(ranges)
    front = min(min(ranges[0:10]), min(ranges[-10:]))
    right = min(ranges[3*n//4-10:3*n//4+10])

    cmd = Twist()

    if front < 0.5:
        cmd.linear.x = 0.0
        cmd.angular.z = 0.5
    elif right > 0.4:
        cmd.linear.x = 0.15
        cmd.angular.z = -0.3
    elif right < 0.25:
        cmd.linear.x = 0.15
        cmd.angular.z = 0.3
    else:
        cmd.linear.x = 0.2
        cmd.angular.z = 0.0

    pub.publish(cmd)

def main():
    global pub
    rospy.init_node('wall_follower')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/scan', LaserScan, scan_callback)
    rospy.loginfo("Wall follower started")
    rospy.spin()

if __name__ == '__main__':
    main()
