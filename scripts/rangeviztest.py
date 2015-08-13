#!/usr/bin/env python
import os, sys
import roslib; roslib.load_manifest('RelocSensorDriver')
import rospy
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
import numpy as np
import matplotlib.pyplot as plt
import matplotlib, time
import threading
from math import atan2
from matplotlib.pyplot import figure, show, rc, draw

MSG=[0,0,0,0,0,0,0,0,0]

def callback1(msg):
    global MSG
    MSG[0] = msg.x
    MSG[1] = msg.y
    

def callback2(msg):
    global MSG
    MSG[2] = msg.x
    MSG[3] = msg.y

def callback3(msg):
    global MSG
    MSG[4] = msg.x
    MSG[5] = msg.y

def callback4(msg):
    global MSG
    MSG[6] = msg.x
    MSG[7] = msg.y	

def callback5(msg):
    global MSG
    MSG[8]=msg.points[0].x
    if MSG[8]==0 or MSG[8]>9:
 	MSG[8]=0.1


 
def listener():
    rospy.init_node('rangeviztest', anonymous=True)
    rospy.Subscriber('/IRdebug/point1', Point, callback1,queue_size=1)
    rospy.Subscriber('/IRdebug/point2', Point, callback2,queue_size=1)
    rospy.Subscriber('/IRdebug/point3', Point, callback3,queue_size=1)
    rospy.Subscriber('/IRdebug/point4', Point, callback4,queue_size=1)
    rospy.Subscriber('/relocNode2/relocVizData', Marker, callback5,queue_size=1)
    pub = rospy.Publisher('rangeviztest', Marker)
    global MSG
    while not rospy.is_shutdown():
        cyinder_marker = Marker()
	cyinder_marker.header.frame_id="/pioneer1/base_link"
	cyinder_marker.type = Marker.CYLINDER
	cyinder_marker.scale.x = MSG[8]*2
	cyinder_marker.scale.y = MSG[8]*2
	cyinder_marker.scale.z = 0.2
	cyinder_marker.color.r = 0.0
	cyinder_marker.color.g = 0.5
	cyinder_marker.color.b = 0.5
	cyinder_marker.color.a = 0.5
    	pub.publish(cyinder_marker)	
    	rospy.sleep(0.05)
    

if __name__ == '__main__':  
	#matplotlib.interactive(True)
	listener()
	
