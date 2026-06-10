#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

pub = None
state = 'forward'

def scan_callback(msg):
    global state
    ranges = msg.ranges
    n = len(ranges)
    front = min(min(ranges[0:10]), min(ranges[-10:]))
    back = min(ranges[n//2-10:n//2+10])

    cmd = Twist()

    if state == 'forward':
        if front < 0.5:
            state = 'backward'
        else:
            cmd.linear.x = 0.2
    elif state == 'backward':
        if back < 0.5:
            state = 'forward'
        else:
            cmd.linear.x = -0.2

    pub.publish(cmd)

def main():
    global pub
    rospy.init_node('move_between_objects')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/scan', LaserScan, scan_callback)
    rospy.loginfo("Move between objects started")
    rospy.spin()

if __name__ == '__main__':
    main()
