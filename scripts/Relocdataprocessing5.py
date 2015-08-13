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
import tf
import sys, select, termios, tty
from tf.transformations import euler_from_quaternion, euler_matrix

MSG=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]] #18
i=0
settings = termios.tcgetattr(sys.stdin) # for getKey()

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key
	
def callback1(scan,rob):
    #not used for now
    global MSG,i
    i=i+1
    midscan= [round(x*1000.0,0) for x in  scan.ranges[80:101]]
    midavg= sum(midscan)/len(midscan)
    mid = round(scan.ranges[90]*1000,0)
    #mid = scan.ranges[90]*1000
    #print midavg
    #MSG[9] = mid
    #print i,round(MSG[9]/i,0)

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
    #print yaw/pi*180.0
    MSG[rob][4]= odom.twist.twist.linear.x
    MSG[rob][5]= round(odom.twist.twist.angular.z,4)

def callback3(msg,rob):
    global MSG
    MSG[rob][6] = msg.x
    MSG[rob][7] = msg.y
    

def callback4(msg,rob):
    global MSG
    MSG[rob][8] = msg.x
    MSG[rob][9] = msg.y

def callback5(msg,rob):
    global MSG
    MSG[rob][10] = msg.x
    MSG[rob][11] = msg.y

def callback6(msg,rob):
    global MSG
    MSG[rob][12] = msg.x
    MSG[rob][13] = msg.y

def callback7(msg,rob):
    global MSG
    MSG[rob][14]= round(msg.range,5)

def callback8(msg,rob):
    global MSG
    MSG[rob][15]= round(msg.range,5)

def callback9(msg,rob):
    global MSG
    MSG[rob][16]= round(msg.range,5)

def callback10(msg,rob):
    global MSG
    MSG[rob][17]= round(msg.range,5)

    
    

 
def listener():
    rospy.init_node('Relocdataprocessing', anonymous=True)
    rate = rospy.Rate(10.0)

    #IR data - from relocnode1/
    # TODO change the published topic to /relocNode1/relocIRx - marker massege
    rospy.Subscriber('/pioneer1/scan', LaserScan, callback1,0,queue_size=1)
    rospy.Subscriber('/pioneer1/odom', Odometry, callback2,0,queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point1', Point, callback3,0,queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point2', Point, callback4,0,queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point3', Point, callback5,0,queue_size=1)
    rospy.Subscriber('/pioneer1/IRdebug/point4', Point, callback6,0,queue_size=1)
    # TODO publish IRdebug/Ang
    rospy.Subscriber('/pioneer1/relocNode/relocUS1', Range, callback7,0,queue_size=1)
    rospy.Subscriber('/pioneer1/relocNode/relocUS2', Range, callback8,0,queue_size=1)
    rospy.Subscriber('/pioneer1/relocNode/relocUS3', Range, callback9,0,queue_size=1)
    rospy.Subscriber('/pioneer1/relocNode/relocUS4', Range, callback10,0,queue_size=1)

    rospy.Subscriber('/pioneer2/scan', LaserScan, callback1,1,queue_size=1)
    rospy.Subscriber('/pioneer2/odom', Odometry, callback2,1,queue_size=1)
    rospy.Subscriber('/pioneer2/IRdebug/point1', Point, callback3,1,queue_size=1)
    rospy.Subscriber('/pioneer2/IRdebug/point2', Point, callback4,1,queue_size=1)
    rospy.Subscriber('/pioneer2/IRdebug/point3', Point, callback5,1,queue_size=1)
    rospy.Subscriber('/pioneer2/IRdebug/point4', Point, callback6,1,queue_size=1)
    rospy.Subscriber('/pioneer2/relocNode/relocUS1', Range, callback7,1,queue_size=1)
    rospy.Subscriber('/pioneer2/relocNode/relocUS2', Range, callback8,1,queue_size=1)
    rospy.Subscriber('/pioneer2/relocNode/relocUS3', Range, callback9,1,queue_size=1)
    rospy.Subscriber('/pioneer2/relocNode/relocUS4', Range, callback10,1,queue_size=1)
       
    
    tf_listener = tf.TransformListener()
    pub = rospy.Publisher('rangeviztest', Marker)
    global MSG
    while not rospy.is_shutdown():
	servoang1=0
	servoang2=0
	#print tf_listener.frameExists("/pioneer1/IRcam")
 	#print tf_listener.frameExists("/pioneer1/base_reloc1")
	try:
		now = rospy.Time.now()
        	#tf_listener.waitForTransform("/pioneer1/IRcam", "/pioneer1/base_reloc1", rospy.Time(0), rospy.Duration(1.0))
        	(trans,rot) = tf_listener.lookupTransform("/pioneer1/base_reloc1", "/pioneer1/IRcam", rospy.Time(0))
		(roll,pitch,yaw) = euler_from_quaternion(rot)
		servoang1= yaw*180.0/pi
		#print servoang
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print "tf error"
	try:
		now = rospy.Time.now()
        	#tf_listener.waitForTransform("/pioneer1/IRcam", "/pioneer1/base_reloc1", rospy.Time(0), rospy.Duration(1.0))
        	(trans,rot) = tf_listener.lookupTransform("/pioneer2/base_reloc1", "/pioneer2/IRcam", rospy.Time(0))
		(roll,pitch,yaw) = euler_from_quaternion(rot)
		servoang2= yaw*180.0/pi
		#print servoang
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print "tf error"
        	#continue
        
        rob=0
	#f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}'.format(MSG[rob][0],MSG[rob][1],MSG[rob][2],MSG[rob][3],MSG[rob][4],MSG[rob][5],MSG[rob][6],MSG[rob][7],MSG[rob][8],MSG[rob][9],MSG[rob][10],MSG[rob][11],MSG[rob][12],MSG[rob][13],MSG[rob][14],MSG[rob][15],MSG[rob][16],MSG[rob][17],servoang1))
	rob=1	
	#f.write(',{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}'.format(MSG[rob][0],MSG[rob][1],MSG[rob][2],MSG[rob][3],MSG[rob][4],MSG[rob][5],MSG[rob][6],MSG[rob][7],MSG[rob][8],MSG[rob][9],MSG[rob][10],MSG[rob][11],MSG[rob][12],MSG[rob][13],MSG[rob][14],MSG[rob][15],MSG[rob][16],MSG[rob][17],servoang2))
	#f.write('\n')
	#MSG[0][:]=np.zeros(18)
	#MSG[1][:]=np.zeros(18)
	rate.sleep()
    

if __name__ == '__main__':  
	#f = open('RelocTrajCirc_20130907', 'a')
        #f.write('P1x,y,z,Th,V,Omega,IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4,US1,US2,US3,US4,Servo,P2x,y,z,Th,V,Omega,IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4,US1,US2,US3,US4,Servo\n')
	listener()
	
