#!/usr/bin/env python
import os, sys
import roslib; roslib.load_manifest('RelocSensorDriver')
import rospy
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Range
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from ardrone_autonomy.msg import Navdata
import numpy as np
import matplotlib.pyplot as plt
import matplotlib, time
import threading
from math import atan2,sqrt,pow,fabs,pi,tan
from matplotlib.pyplot import figure, show, rc, draw
import tf
import sys, select, termios, tty
from tf.transformations import euler_from_quaternion, euler_matrix
import scipy
from scipy import io
import time

MSG=[range(0,26+181,1),range(0,26+181,1),range(0,26+181,1)] 
MSGR1=np.zeros([2000,len(MSG[0][:])],np.float64 )
MSGR2=np.zeros([2000,len(MSG[0][:])],np.float64)
MSGR3=np.zeros([2000,len(MSG[0][:])],np.float64)
i=0
tf_listener = tf.TransformListener()
	
def callback1(scan,rob): #181 data points
    global MSG,i
    MSG[rob][26:26+len(scan.ranges)-1] = scan.ranges[0:len(scan.ranges)-1]

def callback2(odom,rob): #8 data points
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
    #print yaw
    MSG[rob][4]= odom.twist.twist.linear.x
    MSG[rob][5]= round(odom.twist.twist.angular.z,4)
    MSG[rob][6]= odom.header.stamp.secs
    MSG[rob][7]= odom.header.stamp.nsecs
    # add global localization information
    if rob==0 : 
	tf_prefix="/pioneer1"
    if rob==1 : 
	tf_prefix="/pioneer2"
    if rob==2 : 
	tf_prefix="/drone1"
    try:
	now = rospy.Time.now()
       	(trans,rot) = tf_listener.lookupTransform( "/map",tf_prefix+"/base_reloc2", rospy.Time(0))
	(roll,pitch,yaw) = euler_from_quaternion(rot)
        MSG[rob][8]= trans[0]
    	MSG[rob][9]= trans[1]
    	MSG[rob][10]= trans[2]
    	MSG[rob][11]= yaw
	if tf_prefix=="/drone1":
		print trans
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
	print "tf error"
    


def callback3(msg,rob): #2 data points (correspondance , data)
    global MSG
    MSG[rob][12] = msg.ns
    #print msg.ns
    MSG[rob][13] = msg.scale.x/2.0
    

def callback4(msg,rob): #3 data points (correspondance , datax2)
    global MSG
    MSG[rob][14] = msg.ns
    if sum([msg.points[0].x,msg.points[0].y,msg.points[0].z])!=0:
    	MSG[rob][15] = atan2(msg.points[0].y,msg.points[0].x)
    	MSG[rob][16] = atan2(msg.points[0].z,sqrt(pow(msg.points[0].y,2)+pow(msg.points[0].x,2)))
        #print msg.points[1]
    else :
	MSG[rob][15] = atan2(msg.points[1].y,msg.points[1].x)
    	MSG[rob][16] = atan2(msg.points[1].z,sqrt(pow(msg.points[1].y,2)+pow(msg.points[1].x,2)))
        #print msg.points[0]


def callback5(msg,rob): #1 data (data dirn only)
    global MSG
    if rob==0 : 
	tf_prefix="/pioneer1"
    if rob==1 : 
	tf_prefix="/pioneer2"
    if rob==2 : 
	tf_prefix="/drone1"
    try:
	now = rospy.Time.now()
        (trans,rot) = tf_listener.lookupTransform( tf_prefix+"/base_reloc2",tf_prefix+"/base_reloc2/USAoa", rospy.Time(0))
	(roll,pitch,yaw) = euler_from_quaternion(rot)
 	MSG[rob][25]= yaw
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
	print "tf error"
    #print MSG[rob][13]    


def callback6(msg,rob):
    global MSG
    MSG[rob[0]][17+2*(rob[1]-1)] = msg.x
    MSG[rob[0]][17+2*(rob[1]-1)+1] = msg.y

def callback7(msg,rob):
    global MSG
    MSG[rob][6]= msg.header.stamp.secs
    MSG[rob][7]= msg.header.stamp.nsecs
    MSG[rob][26] = msg.magX
    MSG[rob][27] = msg.magY
    MSG[rob][28] = msg.magZ
    #print MSG[rob][28]
    #handled in imu callback
    #MSG[rob][29] = msg.ax
    #MSG[rob][30] = msg.ay
    #MSG[rob][31] = msg.az
    #MSG[rob][32] = msg.wx
    #MSG[rob][33] = msg.wy
    #MSG[rob][34] = msg.wz
    #MSG[rob][35] = msg.rotqx  #rotation in quaternion
    #MSG[rob][36] = msg.rotqy
    #MSG[rob][37] = msg.rotqz
    #MSG[rob][38] = msg.rotqw
    

    MSG[rob][39] = msg.rotX   #rotation in euler
    MSG[rob][40] = msg.rotY
    MSG[rob][41] = msg.rotZ
    MSG[rob][42] = msg.pressure
    MSG[rob][43] = msg.altd
    MSG[rob][44] = msg.vx
    MSG[rob][45] = msg.vy
    MSG[rob][46] = msg.vz
    MSG[rob][47] = msg.motor1
    MSG[rob][48] = msg.motor2
    MSG[rob][49] = msg.motor3
    MSG[rob][50] = msg.motor4

def callback8(msg,rob):
    global MSG
    #handled in imu callback
    MSG[rob][29] = msg.linear_acceleration.x
    MSG[rob][30] = msg.linear_acceleration.y
    MSG[rob][31] = msg.linear_acceleration.z
    MSG[rob][32] = msg.angular_velocity.x
    MSG[rob][33] = msg.angular_velocity.y
    MSG[rob][34] = msg.angular_velocity.z
    MSG[rob][35] = msg.orientation.x  #rotation in quaternion
    MSG[rob][36] = msg.orientation.y
    MSG[rob][37] = msg.orientation.z
    MSG[rob][38] = msg.orientation.w
    
    

def listener():
    
    #IR data - from relocnode1/
    # TODO change the published topic to /relocNode1/relocIRx - marker massege
    rospy.Subscriber('/pioneer1/scan', LaserScan, callback1,0,queue_size=1)
    rospy.Subscriber('/pioneer1/odom', Odometry, callback2,0,queue_size=1)
    rospy.Subscriber('/pioneer1/relocNode/relocVizDataRange', Marker, callback3,0,queue_size=1)
    rospy.Subscriber('/pioneer1/relocNode/relocVizDataBear2', Marker, callback4,0,queue_size=1)
    rospy.Subscriber('/pioneer1/relocNode/relocUsAoa', Range, callback5,0,queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point1', Point, callback6,[0,1],queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point2', Point, callback6,[0,2],queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point3', Point, callback6,[0,3],queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point4', Point, callback6,[0,4],queue_size=1)

    rospy.Subscriber('/pioneer2/scan', LaserScan, callback1,1,queue_size=1)
    rospy.Subscriber('/pioneer2/odom', Odometry, callback2,1,queue_size=1)
    rospy.Subscriber('/pioneer2/relocNode/relocVizDataRange', Marker, callback3,1,queue_size=1)
    rospy.Subscriber('/pioneer2/relocNode/relocVizDataBear2', Marker, callback4,1,queue_size=1)
    rospy.Subscriber('/pioneer2/relocNode/relocUsAoa', Range, callback5,1,queue_size=1)
    rospy.Subscriber('/pioneer2/IRdebug/point1', Point, callback6,[1,1],queue_size=1)
    rospy.Subscriber('/pioneer2/IRdebug/point2', Point, callback6,[1,2],queue_size=1)
    rospy.Subscriber('/pioneer2/IRdebug/point3', Point, callback6,[1,3],queue_size=1)
    rospy.Subscriber('/pioneer2/IRdebug/point4', Point, callback6,[1,4],queue_size=1)

    rospy.Subscriber('/drone1/odom', Odometry, callback2,2,queue_size=1)
    rospy.Subscriber('/drone1/relocNode/relocVizDataRange', Marker, callback3,2,queue_size=1)
    rospy.Subscriber('/drone1/relocNode/relocVizDataBear2', Marker, callback4,2,queue_size=1)
    rospy.Subscriber('/drone1/relocNode/relocUsAoa', Range, callback5,2,queue_size=1)
    rospy.Subscriber('/drone1/IRdebug/point1', Point, callback6,[2,1],queue_size=1)
    rospy.Subscriber('/drone1/IRdebug/point2', Point, callback6,[2,2],queue_size=1)
    rospy.Subscriber('/drone1/IRdebug/point3', Point, callback6,[2,3],queue_size=1)
    rospy.Subscriber('/drone1/IRdebug/point4', Point, callback6,[2,4],queue_size=1)
    rospy.Subscriber('/ardrone/navdata', Navdata, callback7,2,queue_size=1)
    rospy.Subscriber('/ardrone/imu', Imu, callback8,2,queue_size=1)
       
    
    #pub = rospy.Publisher('rangeviztest', Marker)
    while not rospy.is_shutdown():
	global MSG,i
        tf_prefix="/drone1"
 	rob = 2;
   	try:
		now = rospy.Time.now()
       		(trans,rot) = tf_listener.lookupTransform( "/map",tf_prefix+"/base_reloc2", rospy.Time(0))
		(roll,pitch,yaw) = euler_from_quaternion(rot)
        	MSG[rob][8]= trans[0]
    		MSG[rob][9]= trans[1]
    		MSG[rob][10]= trans[2]
    		MSG[rob][11]= yaw
		#if tf_prefix=="/drone1":
			#print trans
    	except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print "tf error"
	MSGR1[i][:]=np.array(MSG[0][:],np.float64)
	MSGR2[i][:]=np.array(MSG[1][:],np.float64)
	MSGR3[i][:]=np.array(MSG[2][:],np.float64)
	#print MSGR1[i][8], MSG[0][8]
	i=i+1
	print i
	if i==2000:
		obj_arr = np.zeros((6,), dtype=np.object)
        	obj_arr[0] = 'pioneer 1 Header-x,y,z,theta,vx,omega,sn Python, the gecs,nsecs,xw,yx,zw,thw,rangeCorr,r,bearCorr,alpha,beta,IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4,usaoa,laser'
		#print MSGR1
		obj_arr[1] = MSGR1
		obj_arr[2] = 'pioneer 2 Header-x,y,z,theta,vx,omega,secs,nsecs,xw,yx,zw,thw,rangeCorr,r,bearCorr,alpha,beta,IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4,usaoa,laser'
		obj_arr[3] = MSGR2
		obj_arr[4] = 'drone 1 Header-x,y,z,theta,vx,omega,secs,nsecs,xw,yx,zw,thw,rangeCorr,r,bearCorr,alpha,beta,IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4,usaoa,NavData,MSG[rob][26] = msg.magX, MSG[rob][27] = msg.magY,    MSG[rob][28] = msg.magZ,    MSG[rob][29] = msg.ax,    MSG[rob][30] = msg.ay,    MSG[rob][31] = msg.az,    MSG[rob][32] = msg.wx,    MSG[rob][33] = msg.wy,    MSG[rob][34] = msg.wz,    MSG[rob][35] = msg.rotqx ,    MSG[rob][36] = msg.rotqy,    MSG[rob][37] = msg.rotqz,    MSG[rob][38] = msg.rotqw,  MSG[rob][39] = msg.rotX  ,    MSG[rob][40] = msg.rotY,    MSG[rob][41] = msg.rotZ,    MSG[rob][42] = msg.pressure,    MSG[rob][43] = msg.altd,    MSG[rob][44] = msg.vx,    MSG[rob][45] = msg.vy,    MSG[rob][46] = msg.vz,    MSG[rob][47] = msg.motor1,    MSG[rob][48] = msg.motor2,    MSG[rob][49] = msg.motor3,    MSG[rob][50] = msg.motor4'
		obj_arr[5] = MSGR3
        	scipy.io.savemat('Calibset1.mat', {'obj_arr':obj_arr})
		sys.exit()
	rate.sleep()
    

if __name__ == '__main__':  
        rospy.init_node('Relocdataprocessing', anonymous=True)
        rate = rospy.Rate(20.0)
	listener()
	
