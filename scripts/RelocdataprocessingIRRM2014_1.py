#!/usr/bin/env python
import os, sys
import roslib; roslib.load_manifest('RelocSensorDriver')
import rospy
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
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

#global array having all the values
MSG=[range(0,26+181,1),range(0,26+181,1),range(0,26+181,1)] 

#global variables for each robot
MSGR1=np.zeros([4001,len(MSG[0][:])],np.float64) #pioneer 1
MSGR2=np.zeros([4001,len(MSG[0][:])],np.float64) #pioneer 2
MSGR3=np.zeros([4001,len(MSG[0][:])],np.float64) #drone 1

#global iterator
i=0
tf_listener = tf.TransformListener()

#standardization-the DAQ file structure
#[0-1]	 TIME		:secs,nsecs,
#[2-7]   GROUNDTRUTH	:xw,yx,zw,rollw,pitchw,yaww 
#[8-19]	 ODOM		:x,y,z,roll,pitch,yaw,vx,vy,vz,omegax,omegay,omegaz,
#[20-26] IRRM1 (US)	:rangeCorr,r,usaoa, RAW:, US1,US2,US3,US4
#[27-37] IRRM2 (IR)	:bearCorr,alpha,beta, RAW:, IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4 
#CUSTOM RAW DATA
#[38-52]	  SENSORS2 (navdata)
#[53-62]	  SENSORS3 (imu)
#[63-243] SENSORS1 (laser)  :laser
#CUSTOM PROC DATA
#AHRS1
#TARGETS1
#TARGETS2
 

#callback for scan topics	
def callback1(scan,rob): #181 data points [63-243]
    global MSG,i
    MSG[rob][63:63+len(scan.ranges)-1] = scan.ranges[0:len(scan.ranges)-1]

#callback for odometer topic
def callback2(odom,rob): #12 data points [8-19]
    global MSG
     
    MSG[rob][8]=odom.pose.pose.position.x
    MSG[rob][9]=odom.pose.pose.position.y
    MSG[rob][10]=odom.pose.pose.position.z
    rot = np.empty((4, ), dtype=np.float64)
    rot[0]=odom.pose.pose.orientation.x
    rot[1]=odom.pose.pose.orientation.y
    rot[2]=odom.pose.pose.orientation.z
    rot[3]=odom.pose.pose.orientation.w
    (roll,pitch,yaw) = euler_from_quaternion(rot)
    MSG[rob][11]= round(roll,5)
    MSG[rob][12]= round(pitch,5)
    MSG[rob][13]= round(yaw,5)
    MSG[rob][14]= odom.twist.twist.linear.x
    MSG[rob][15]= odom.twist.twist.linear.y
    MSG[rob][16]= odom.twist.twist.linear.z
    MSG[rob][17]= round(odom.twist.twist.angular.x,4)
    MSG[rob][18]= round(odom.twist.twist.angular.y,4)
    MSG[rob][19]= round(odom.twist.twist.angular.z,4)
    
    # add global localization information
    #if rob==0 : 
    #	tf_prefix="/pioneer1"
    #if rob==1 : 
    #	tf_prefix="/pioneer2"
    #if rob==2 : 
    #	tf_prefix="/drone1"
    #try:
    #	now = rospy.Time.now()
    #   	(trans,rot) = tf_listener.lookupTransform( "/map",tf_prefix+"/base_reloc2", rospy.Time(0))
    #	(roll,pitch,yaw) = euler_from_quaternion(rot)
    #    MSG[rob][8]= trans[0]
    # 	MSG[rob][9]= trans[1]
    # 	MSG[rob][10]= trans[2]
    #	MSG[rob][11]= yaw
    #	if tf_prefix=="/drone1":
    #		print trans
    #except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
    #	print "tf error"
    

#callback for range data
def callback3(msg,rob): #2 data points (correspondance , data) [20 21]
    global MSG
    MSG[rob][20] = msg.ns
    #print msg.ns
    MSG[rob][21] = msg.scale.x/2.0
    
#callback for IR bearing
def callback4(msg,rob): #3 data points (correspondance , datax2) [27-37]
    global MSG
    MSG[rob][27] = msg.ns
    if sum([msg.points[0].x,msg.points[0].y,msg.points[0].z])!=0:
    	MSG[rob][28] = atan2(msg.points[0].y,msg.points[0].x)
    	MSG[rob][29] = atan2(msg.points[0].z,sqrt(pow(msg.points[0].y,2)+pow(msg.points[0].x,2)))
        #print msg.points[1]
    else :
	MSG[rob][28] = atan2(msg.points[1].y,msg.points[1].x)
    	MSG[rob][29] = atan2(msg.points[1].z,sqrt(pow(msg.points[1].y,2)+pow(msg.points[1].x,2)))
        #print msg.points[0]

#callback for US AOA
def callback5(msg,rob): #1 data (data dirn only) [22]
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
 	MSG[rob][22]= yaw
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
	print "tf error"
    #print MSG[rob][13]    


def callback6(msg,rob):#[30 37]
    global MSG
    MSG[rob[0]][30+2*(rob[1]-1)] = msg.x
    MSG[rob[0]][30+2*(rob[1]-1)+1] = msg.y

#navdata call back
def callback7(msg,rob): #[38-52]
    global MSG
   
    MSG[rob][38] = msg.magX
    MSG[rob][39] = msg.magY
    MSG[rob][40] = msg.magZ
    MSG[rob][41] = msg.rotX   #rotation in euler
    MSG[rob][42] = msg.rotY
    MSG[rob][43] = msg.rotZ
    MSG[rob][44] = msg.pressure
    MSG[rob][45] = msg.altd
    MSG[rob][46] = msg.vx
    MSG[rob][47] = msg.vy
    MSG[rob][48] = msg.vz
    MSG[rob][49] = msg.motor1
    MSG[rob][50] = msg.motor2
    MSG[rob][51] = msg.motor3
    MSG[rob][52] = msg.motor4

#imu call back
def callback8(msg,rob):#[53-62]
    global MSG
    MSG[rob][53] = msg.linear_acceleration.x
    MSG[rob][54] = msg.linear_acceleration.y
    MSG[rob][55] = msg.linear_acceleration.z
    MSG[rob][56] = msg.angular_velocity.x
    MSG[rob][57] = msg.angular_velocity.y
    MSG[rob][58] = msg.angular_velocity.z
    MSG[rob][59] = msg.orientation.x  #rotation in quaternion
    MSG[rob][60] = msg.orientation.y
    MSG[rob][61] = msg.orientation.z
    MSG[rob][62] = msg.orientation.w

def callback9(msg,rob): #[23-26]
    global MSG
    MSG[rob][23] = msg.x
    MSG[rob][24] = msg.y
    MSG[rob][25] = msg.z
    MSG[rob][26] = msg.w
    
    

def listener():
    
    #IR data - from relocnode1/
    # TODO change the published topic to /relocNode1/relocIRx - marker massege
    #rospy.Subscriber('/pioneer1/scan', LaserScan, callback1,0,queue_size=1)
    #rospy.Subscriber('/pioneer1/odom', Odometry, callback2,0,queue_size=1)
    rospy.Subscriber('/pioneer1/relocNode/relocVizDataRange', Marker, callback3,0,queue_size=1)
    rospy.Subscriber('/pioneer1/relocNode/relocVizDataBear2', Marker, callback4,0,queue_size=1)
    rospy.Subscriber('/pioneer1/relocNode/relocUsAoa', Range, callback5,0,queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point1', Point, callback6,[0,1],queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point2', Point, callback6,[0,2],queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point3', Point, callback6,[0,3],queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point4', Point, callback6,[0,4],queue_size=1)
    rospy.Subscriber('/pioneer1/USdebug', Quaternion, callback9,0,queue_size=1)
                             

    
    #rospy.Subscriber('/drone1/odom', Odometry, callback2,2,queue_size=1)
    #rospy.Subscriber('/drone1/relocNode/relocVizDataRange', Marker, callback3,2,queue_size=1)
    #rospy.Subscriber('/drone1/relocNode/relocVizDataBear2', Marker, callback4,2,queue_size=1)
    #rospy.Subscriber('/drone1/relocNode/relocUsAoa', Range, callback5,2,queue_size=1)
    #rospy.Subscriber('/drone1/IRdebug/point1', Point, callback6,[2,1],queue_size=1)
    #rospy.Subscriber('/drone1/IRdebug/point2', Point, callback6,[2,2],queue_size=1)
    #rospy.Subscriber('/drone1/IRdebug/point3', Point, callback6,[2,3],queue_size=1)
    #rospy.Subscriber('/drone1/IRdebug/point4', Point, callback6,[2,4],queue_size=1)
    #rospy.Subscriber('/ardrone/navdata', Navdata, callback7,2,queue_size=1)
    #rospy.Subscriber('/ardrone/imu', Imu, callback8,2,queue_size=1)
       
    
    #pub = rospy.Publisher('rangeviztest', Marker)
    	
    while not rospy.is_shutdown():
	global MSG,i
	

	# GROUND TRUTH DAQ
	for rob in [0, 2]:
		if rob==0 : 
			tf_prefix="/pioneer1/Tag1"
	    	if rob==1 : 
			tf_prefix="/pioneer2/Tag2"
    		if rob==2 : 
			tf_prefix="/drone2/Tag3"
        	try:
			now = rospy.Time.now()
       			(trans,rot) = tf_listener.lookupTransform("/MyWebCam/MyWebCam",tf_prefix, rospy.Time(0))
			(roll,pitch,yaw) = euler_from_quaternion(rot)
			MSG[rob][0]= now.secs
			MSG[rob][1]= now.nsecs
        		MSG[rob][2]= trans[0]
    			MSG[rob][3]= trans[1]
    			MSG[rob][4]= trans[2]
    			MSG[rob][5]= roll
			MSG[rob][6]= pitch
			MSG[rob][7]= yaw
			print now.secs
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			print "tf error"
	#Fill robot data arrays	
	
        i=i+1
	print i
        #print MSG[0][:]

	MSGR1[i][:]=np.array(MSG[0][:],np.float64)
        MSGR2[i][:]=np.array(MSG[1][:],np.float64)
        MSGR3[i][:]=np.array(MSG[2][:],np.float64)

	# DATA FILE RECORDING
	if i==4000:
		obj_arr = np.zeros((6,), dtype=np.object)
        	obj_arr[0] = 'pioneer1     [0-1]	 TIME		:secs,nsecs, [2-7]   GROUNDTRUTH	:xw,yx,zw,rollw,pitchw,yaw, [8-19]	 ODOM		:x,y,z,roll,pitch,yaw,vx,vy,vz,omegax,omegay,omegaz, [20-26] IRRM1 (US)	:rangeCorr,r,usaoa, RAW:, US1,US2,US3,US4 [27-37] IRRM2 (IR)	:bearCorr,alpha,beta, RAW:, IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4, CUSTOM RAW DATA [38-52]	  SENSORS2 (navdata),[53-62]	  SENSORS3 (imu), [63-243] SENSORS1 (laser)  :laser'
		#print MSGR1
		obj_arr[1] = MSGR1
		obj_arr[2] = 'pioneer2     [0-1]	 TIME		:secs,nsecs, [2-7]   GROUNDTRUTH	:xw,yx,zw,rollw,pitchw,yaw, [8-19]	 ODOM		:x,y,z,roll,pitch,yaw,vx,vy,vz,omegax,omegay,omegaz, [20-26] IRRM1 (US)	:rangeCorr,r,usaoa, RAW:, US1,US2,US3,US4 [27-37] IRRM2 (IR)	:bearCorr,alpha,beta, RAW:, IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4, CUSTOM RAW DATA [38-52]	  SENSORS2 (navdata),[53-62]	  SENSORS3 (imu), [63-243] SENSORS1 (laser)  :laser'
		obj_arr[3] = MSGR2
		obj_arr[4] = 'drone1     [0-1]	 TIME		:secs,nsecs, [2-7]   GROUNDTRUTH	:xw,yx,zw,rollw,pitchw,yaw, [8-19]	 ODOM		:x,y,z,roll,pitch,yaw,vx,vy,vz,omegax,omegay,omegaz, [20-26] IRRM1 (US)	:rangeCorr,r,usaoa, RAW:, US1,US2,US3,US4 [27-37] IRRM2 (IR)	:bearCorr,alpha,beta, RAW:, IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4, CUSTOM RAW DATA [38-52]	  SENSORS2 (navdata),[53-62]	  SENSORS3 (imu), [63-243] SENSORS1 (laser)  :laser'
		obj_arr[5] = MSGR3
        	scipy.io.savemat('flighttest101.mat', {'obj_arr':obj_arr})
		sys.exit()
	rate.sleep()
    

if __name__ == '__main__':  
        rospy.init_node('Relocdataprocessing', anonymous=True)
        rate = rospy.Rate(20.0)
	listener()
	
