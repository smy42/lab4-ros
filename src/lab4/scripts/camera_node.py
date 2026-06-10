#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

bridge = CvBridge()

def image_callback(msg):
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    cv2.imshow("Camera - Edges", edges)
    cv2.waitKey(1)

def main():
    rospy.init_node('camera_node')
    rospy.Subscriber('/camera/rgb/image_raw', Image, image_callback)
    rospy.loginfo("Camera node started")
    rospy.spin()

if __name__ == '__main__':
    main()
