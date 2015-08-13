#!/usr/bin/env python
import os, sys
import roslib; roslib.load_manifest('RelocSensorDriver')
import rospy
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range
from nav_msgs.msg import Odometry
import numpy as np
import matplotlib.pyplot as plt
import matplotlib, time
import threading
from math import atan2,sqrt,pow,fabs,pi,tan
from matplotlib.pyplot import figure, show, rc, draw
import sys, select, termios, tty
from transformations import euler_from_quaternion, euler_matrix
import scipy
from scipy import io
import time

MSG=[range(0,8+181,1),range(0,8+181,1)] 
#MSGR1=np.array
#MSGR2=np.array
MSGR1=np.zeros([7000,len(MSG[0][:])])
MSGR2=np.zeros([7000,len(MSG[0][:])])
i=0
	
def callback1(scan,rob):
    #not used for now
    global MSG,i
    MSG[rob][8:8+len(scan.ranges)-1] = scan.ranges[0:len(scan.ranges)-1]
    

def callback2(odom,rob):
    global MSG
    #MSG[rob][:]=numpy.zeros(18)
    MSG[rob][0]=odom.pose.pose.position.x
    MSG[rob][1]=odom.pose.pose.position.y
    MSG[rob][2]=odom.pose.pose.position.z
    rot = np.empty((4, ), dtype=np.float64)
    rot[0]=odom.pose.pose.orientation.x
    rot[1]=odom.pose.pose.orientation.y
    rot[2]=odom.pose.pose.orientation.z
    rot[3]=odom.pose.pose.orientation.w
    (roll,pitch,yaw) = euler_from_quaternion(rot)
    MSG[rob][3]= round(yaw,5)
    MSG[rob][4]= odom.twist.twist.linear.x
    MSG[rob][5]= round(odom.twist.twist.angular.z,4)
    MSG[rob][6]= odom.header.stamp.secs
    MSG[rob][7]= odom.header.stamp.nsecs

def listener():
    
           
    
    tf_listener = tf.TransformListener()
    global MSG, MSGR1, MSGR2, i
    while not rospy.is_shutdown():
	try:
		now = rospy.Time.now()
        	(trans,rot) = tf_listener.lookupTransform("/pioneer1/odom", "/map", rospy.Time(0))
		(roll,pitch,yaw) = euler_from_quaternion(rot)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print "tf error"
	try:
		now = rospy.Time.now()
        	(trans,rot) = tf_listener.lookupTransform("/pioneer2/odom", "/map", rospy.Time(0))
		(roll,pitch,yaw) = euler_from_quaternion(rot)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print "tf error"
        
	#MSGR1=np.resize(MSGR1,[i+1,len(MSG[0][:])])
        MSGR1[i][:]=np.array(MSG[0][:])
	#MSGR2=np.resize(MSGR2,[i+1,len(MSG[1][:])])
	print i
        MSGR2[i][:]=np.array(MSG[1][:])
	#obj_arr = np.zeros((4,), dtype=np.object)
        #obj_arr[0] = 'Rob 1 Header-x,y,z,theta,vx,omega,secs,nsecs,laser'
	#obj_arr[1] = MSGR1
	#obj_arr[2] = 'Rob 2 Header-x,y,z,theta,vx,omega,secs,nsecs,laser'
	#obj_arr[3] = MSGR2
        #scipy.io.savemat('np_cells.mat', {'obj_arr':obj_arr})

	#f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}'.format(MSG[rob][0],MSG[rob][1],MSG[rob][2],MSG[rob][3],MSG[rob][4],MSG[rob][5],MSG[rob][6],MSG[rob][7],MSG[rob][8],MSG[rob][9],MSG[rob][10],MSG[rob][11],MSG[rob][12],MSG[rob][13],MSG[rob][14],MSG[rob][15],MSG[rob][16],MSG[rob][17],servoang1))
	#rob=1	
	#f.write(',{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}'.format(MSG[rob][0],MSG[rob][1],MSG[rob][2],MSG[rob][3],MSG[rob][4],MSG[rob][5],MSG[rob][6],MSG[rob][7],MSG[rob][8],MSG[rob][9],MSG[rob][10],MSG[rob][11],MSG[rob][12],MSG[rob][13],MSG[rob][14],MSG[rob][15],MSG[rob][16],MSG[rob][17],servoang2))
	#f.write('\n')
	#MSG[0][:]=np.zeros(18)
	#MSG[1][:]=np.zeros(18)
        i=i+1
	if i==6000:
		obj_arr = np.zeros((4,), dtype=np.object)
        	obj_arr[0] = 'Rob 1 Header-x,y,z,theta,vx,omega,secs,nsecs,laser'
		#print MSGR1
		obj_arr[1] = MSGR1
		obj_arr[2] = 'Rob 2 Header-x,y,z,theta,vx,omega,secs,nsecs,laser'
		obj_arr[3] = MSGR2
        	scipy.io.savemat('np_cells.mat', {'obj_arr':obj_arr})
		 
	rate.sleep()
    

if __name__ == '__main__':  
	#f = open('RelocTrajCirc_20130907', 'a')
        #f.write('P1x,y,z,Th,V,Omega,IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4,US1,US2,US3,US4,Servo,P2x,y,z,Th,V,Omega,IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4,US1,US2,US3,US4,Servo\n')
	rospy.init_node('Relocdataprocessing', anonymous=True)
    	rate = rospy.Rate(100.0)

    	#IR data - from relocnode1/
    	# TODO change the published topic to /relocNode1/relocIRx - marker massege
    	rospy.Subscriber('/pioneer1/scan', LaserScan, callback1,0,queue_size=1)
    	rospy.Subscriber('/pioneer1/odom', Odometry, callback2,0,queue_size=1)
    
    	rospy.Subscriber('/pioneer2/scan', LaserScan, callback1,1,queue_size=1)
    	rospy.Subscriber('/pioneer2/odom', Odometry, callback2,1,queue_size=1)	
        time.sleep(1)
	listener()
	
