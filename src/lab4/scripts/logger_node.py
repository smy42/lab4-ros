#!/usr/bin/env python3
import rospy
import json
import os
from lab4.msg import RobotStatus
from lab4.srv import SetLogging, SetLoggingResponse

logging_enabled = True

def status_callback(msg):
    global logging_enabled
    if not logging_enabled:
        return
    entry = {
        "timestamp": rospy.get_time(),
        "cmd_vel": {
            "linear_x": msg.cmd_vel.linear.x,
            "angular_z": msg.cmd_vel.angular.z
        },
        "front_distance": msg.front_distance,
        "left_distance": msg.left_distance,
        "right_distance": msg.right_distance
    }
    log_path = os.path.expanduser("~/robot_log.json")
    with open(log_path, 'a') as f:
        f.write(json.dumps(entry) + "\n")

def handle_set_logging(req):
    global logging_enabled
    logging_enabled = req.enable
    rospy.loginfo(f"Logging set to: {logging_enabled}")
    return SetLoggingResponse(True)

def main():
    rospy.init_node('logger_node')
    rospy.Subscriber('/robot_status', RobotStatus, status_callback)
    rospy.Service('/set_logging', SetLogging, handle_set_logging)
    rospy.loginfo("Logger node started")
    rospy.spin()

if __name__ == '__main__':
    main()
