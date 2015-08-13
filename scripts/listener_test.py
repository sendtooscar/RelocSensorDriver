#!/usr/bin/env python  
import roslib
roslib.load_manifest('RelocSensorDriver')
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv

if __name__ == '__main__':
    rospy.init_node('listener_test')

    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/odom', '/laser', rospy.Time(0))
	    print trans
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
	    print "tf error"            
	    continue
        rate.sleep()
