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
from tf.transformations import euler_from_quaternion
import tf

MSG=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
i=0


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
    #print msg.scale.x
    MSG[8]=msg.scale.x/2.0
    if MSG[8]==0 or round(msg.scale.x,1)==0.3:
 	MSG[8]=0.100
	
def callback6(scan):
    global MSG,i
    i=i+1
    midscan= [round(x*1000.0,0) for x in  scan.ranges[80:101]]
    midavg= sum(midscan)/len(midscan)
    mid = round(scan.ranges[90]*1000,0)
    #mid = scan.ranges[90]*1000
    #print midavg
    MSG[9] = mid
    #print i,round(MSG[9]/i,0)

def callback7(odom):
    global MSG
    MSG[10]= odom.twist.twist.linear.x
    MSG[11]= odom.twist.twist.angular.z
    odom_quat=[0,0,0,0]
    odom_quat[0]=odom.pose.pose.orientation.x
    odom_quat[1]=odom.pose.pose.orientation.y
    odom_quat[2]=odom.pose.pose.orientation.z
    odom_quat[3]=odom.pose.pose.orientation.w
    odom_euler= euler_from_quaternion(odom_quat)
    MSG[11]= odom_euler[2]/pi*180.0


def callback8(range):
    global MSG
    MSG[12]= range.range

def callback9(range):
    global MSG
    MSG[13]= range.range

def callback10(range):
    global MSG
    MSG[14]= range.range

def callback11(range):
    global MSG
    MSG[15]= range.range
    

    

 
def listener():
    rospy.init_node('Relocdataprocessing', anonymous=True)
    rate = rospy.Rate(50.0)
    rospy.Subscriber('/IRdebug/point1', Point, callback1,queue_size=1)
    rospy.Subscriber('/IRdebug/point2', Point, callback2,queue_size=1)
    rospy.Subscriber('/IRdebug/point3', Point, callback3,queue_size=1)
    rospy.Subscriber('/IRdebug/point4', Point, callback4,queue_size=1)
    rospy.Subscriber('/IRdebug/point4', Point, callback4,queue_size=1)
    rospy.Subscriber('/relocNode2/relocVizData', Marker, callback5,queue_size=1)
    rospy.Subscriber('/pioneer2/scan', LaserScan, callback6,queue_size=1)
    rospy.Subscriber('/pioneer2/odom', Odometry, callback7,queue_size=1)
    rospy.Subscriber('/relocNode1/relocUS1', Range, callback8,queue_size=1)
    rospy.Subscriber('/relocNode1/relocUS2', Range, callback9,queue_size=1)
    rospy.Subscriber('/relocNode1/relocUS3', Range, callback10,queue_size=1)
    rospy.Subscriber('/relocNode1/relocUS4', Range, callback11,queue_size=1)
    pubIRest1=rospy.Publisher('/IRdebug/pointest1', Point)
    tf_listener = tf.TransformListener()
    pub = rospy.Publisher('rangeviztest', Marker)
    global MSG
    while not rospy.is_shutdown():
        #try:
        #    (trans,rot) = tf_listener.lookupTransform('/pioneer1/base_link', '/pioneer2/base_link', rospy.Time(0))
        #except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        #    continue
        #range_act=round(sqrt(pow(trans[0],2)+pow(trans[1],2)+pow(trans[2],2))*1000,1)
	#try:
	#	(trans,rot) = tf_listener.lookupTransform('/pioneer1/base_reloc_IRcam1', '/pioneer1/base_calib', rospy.Time(0))
        #except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
	#	continue
        range_meas=round(MSG[8]*1000.0,0)
	range_laser=round(MSG[9],0)
        #print trans[0],trans[2]
	az_meas=atan2(MSG[0]-512.0,1380.0)*180.0/pi;
	el_meas=atan2(-MSG[1]+384.0,sqrt(pow(1380.0,2.0)+pow(MSG[0]-512.0,2.0)))*180.0/pi;
	el_laser=atan2(130,range_laser-125)*180.0/pi;
        IRdebugest = Point()
 	#IRdebugest.x = 512
	#IRdebugest.y = 384-tan(el_laser/180*pi)*1380.0
	IRdebugest.y = 384-(150.0/4700.0*1340.0)
	IRdebugest.x = 512-(range_laser-3100.0)/4700.0*1340.0
        pubIRest1.publish(IRdebugest)
        #f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(range_laser,trans[0],MSG[0],MSG[1],MSG[2],MSG[3],MSG[4],MSG[5],MSG[6],MSG[7]))
	
	if ((MSG[10]==0)&(MSG[11]==0)):
		moving=0
	else:
		moving=1
        print MSG[11],np.argmin([MSG[12],MSG[13],MSG[14],MSG[15]])
        #print range_laser,range_meas,fabs(range_laser-range_meas),moving
	#print el_meas,range_laser,el_laser,IRdebugest.y
	f.write('{0},{1},{2},{3},{4},{5}\n'.format(MSG[11],np.argmin([MSG[12],MSG[13],MSG[14],MSG[15]]),MSG[12],MSG[13],MSG[14],MSG[15]))
        #print rot
	#if (MSG[0]-512.0)==0:
	#	print range_laser
	rate.sleep()
    

if __name__ == '__main__':  
	#matplotlib.interactive(True)
        f = open('RelocCalibrangeAoA4', 'a')
        f.write('Theta,min,US1,US2,US3,US4\n')
	listener()
	
