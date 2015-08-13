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

MSG=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
i=0
settings = termios.tcgetattr(sys.stdin) # for getKey()
X_points=np.multiply(68.58/2,np.mat('-1 -1 1 1;1 -1 -1 1;0 0 0 0'))
a=np.mat(np.ones((1,4)))
X_points=np.bmat('X_points; a')
Kc=np.mat('  1058.3            0       436.85;0      -1091.6       117.55; 0            0            1')


def publish_pointestimates(servoang):
	global X_points,Kc,MSG
	#MSG[9]=726
        #servoang=0
        t=np.mat('-1.6991; 51.3061; -83.5694')
	t[2,:]=t[2,:]+MSG[9]
	#print t
	R = euler_matrix(0.0022,0.003+((servoang)/180.0*pi),-0.2652, 'rzyx')
 	R= R[0:3,0:3].T
	#print R
	#print t        
	t=R*t
	#print t
        T=np.bmat('R t')
	x=Kc*T*X_points
	x[0,:]=x[0,:]/x[2,:]
	x[1,:]=x[1,:]/x[2,:]
	x[2,:]=x[2,:]/x[2,:]
	#print x
	return x
	


def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

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

def callback8(msg):
    global MSG
    MSG[12]= round(msg.range,5)

def callback9(msg):
    global MSG
    MSG[13]= round(msg.range,5)

def callback10(msg):
    global MSG
    MSG[14]= round(msg.range,5)

def callback11(msg):
    global MSG
    MSG[15]= round(msg.range,5)

    
    

 
def listener():
    rospy.init_node('Relocdataprocessing', anonymous=True)
    rate = rospy.Rate(10.0)

    #IR data - from relocnode1/
    # TODO change the published topic to /relocNode1/relocIRx - marker massege
    rospy.Subscriber('/IRdebug/point1', Point, callback1,queue_size=1)
    rospy.Subscriber('/IRdebug/point2', Point, callback2,queue_size=1)
    rospy.Subscriber('/IRdebug/point3', Point, callback3,queue_size=1)
    rospy.Subscriber('/IRdebug/point4', Point, callback4,queue_size=1)
       

    #laser data for validation -pioneer 1
    rospy.Subscriber('/pioneer1/scan', LaserScan, callback6,queue_size=1)
    rospy.Subscriber('/pioneer1/odom', Odometry, callback7,queue_size=1)

    #USdata - from relocnode2/
    rospy.Subscriber('/relocNode2/relocUS1', Range, callback8,queue_size=1)
    rospy.Subscriber('/relocNode2/relocUS2', Range, callback9,queue_size=1)
    rospy.Subscriber('/relocNode2/relocUS3', Range, callback10,queue_size=1)
    rospy.Subscriber('/relocNode2/relocUS4', Range, callback11,queue_size=1)

    
    pubIRest1=rospy.Publisher('/IRdebug/pointest1', Point)
    pubIRest2=rospy.Publisher('/IRdebug/pointest2', Point)
    pubIRest3=rospy.Publisher('/IRdebug/pointest3', Point)
    pubIRest4=rospy.Publisher('/IRdebug/pointest4', Point)

    tf_listener = tf.TransformListener()
    pub = rospy.Publisher('rangeviztest', Marker)
    global MSG
    while not rospy.is_shutdown():
	
	#USE this to find the transformation info for caliberation
        #try:
        #    (trans,rot) = tf_listener.lookupTransform('/pioneer1/base_link', '/pioneer2/base_link', rospy.Time(0))
        #except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        #    continue
        #range_act=round(sqrt(pow(trans[0],2)+pow(trans[1],2)+pow(trans[2],2))*1000,1)
	#try:
	#	(trans,rot) = tf_listener.lookupTransform('/pioneer1/base_reloc_IRcam1', '/pioneer1/base_calib', rospy.Time(0))
        #except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
	#	continue
	#print trans[0],trans[2]
	servoang=0
	#print tf_listener.frameExists("/pioneer1/IRcam")
 	#print tf_listener.frameExists("/pioneer1/base_reloc1")
	try:
		now = rospy.Time.now()
        	#tf_listener.waitForTransform("/pioneer1/IRcam", "/pioneer1/base_reloc1", rospy.Time(0), rospy.Duration(1.0))
        	(trans,rot) = tf_listener.lookupTransform("/pioneer1/base_reloc1", "/pioneer1/IRcam", rospy.Time(0))
		(roll,pitch,yaw) = euler_from_quaternion(rot)
		servoang= yaw*180.0/pi
		#print servoang
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
		print "tf error"
        	#continue

        
	#in mm
        range_meas=round(MSG[8]*1000.0,0)
	range_laser=round(MSG[9],0)
        
	#publish caliberated versions for debuging
	az_meas=atan2(MSG[0]-512.0,1380.0)*180.0/pi;
	el_meas=atan2(-MSG[1]+384.0,sqrt(pow(1380.0,2.0)+pow(MSG[0]-512.0,2.0)))*180.0/pi;
	el_laser=atan2(130,range_laser-125)*180.0/pi;
        IRdebugest = Point()
 	#IRdebugest.x = 512
	#IRdebugest.y = 384-tan(el_laser/180*pi)*1380.0
        
	#print range_laser
	#try:
	#	IRdebugest.y = 384-(88.0/range_laser*1340.0)
	#	IRdebugest.x = 512+(34.0/range_laser*1340.0)
	#except:
	#	print "laser error"
        #IRdebugest.y=384;
        #IRdebugest.x=512-1320.0*tan(servoang/180.0*pi)
	#pubIRest1.publish(IRdebugest)
	x=publish_pointestimates(servoang)
	#print "ok"
   	IRdebugest.x=x[0,0]
        IRdebugest.y=x[1,0]
	pubIRest1.publish(IRdebugest)
	IRdebugest.x=x[0,1]
        IRdebugest.y=x[1,1]
	pubIRest2.publish(IRdebugest)
	IRdebugest.x=x[0,2]
        IRdebugest.y=x[1,2]
	pubIRest3.publish(IRdebugest)
	IRdebugest.x=x[0,3]
        IRdebugest.y=x[1,3]
	pubIRest4.publish(IRdebugest)
  

	




	#f.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15}\n'.format(range_laser,MSG[10],MSG[11],MSG[0],MSG[1],MSG[2],MSG[3],MSG[4],MSG[5],MSG[6],MSG[7],MSG[12],MSG[13],MSG[14],MSG[15],servoang))
	#print MSG[0],MSG[1],MSG[2],MSG[3],MSG[4],MSG[5],MSG[6],MSG[7],MSG[9]
	
	
        #print MSG[0],MSG[1],MSG[2],MSG[3],MSG[4],MSG[5],MSG[6],MSG[7],MSG[9]
        #print range_laser,range_meas,fabs(range_laser-range_meas),moving
	#print el_meas,range_laser,el_laser,IRdebugest.y
	#f.write('{0},{1},{2}\n'.format(range_laser,range_meas,moving))
        #print rot
	#if (MSG[0]-512.0)==0:
	#	print range_laser
	
	rate.sleep()
    

if __name__ == '__main__':  
	#matplotlib.interactive(True)
        #f = open('RelocCalib_25072013_3', 'a')
        #f.write('Range_laser,robv,robw,IRx1,IRy1,IRx2,IRy2,IRx3,IRy3,IRx4,IRy4,US1,US2,US3,US4,Ang1\n')
	listener()
	
