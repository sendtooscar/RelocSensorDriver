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

files=[]
MSG=[0,0,0,0,0,0,0,0,0]
plt.ion()
fig = figure(figsize=(8,8))
fig.patch.set_facecolor('white')
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
bars = ax.bar(0, 10, width=0.02, bottom=0.0, alpha=0.5, fill=True)
bars2 = ax.bar(0, 9, width=np.pi*2, bottom=0.0, alpha=0.5, fill=False, lw=3)
bars3 = ax.bar(0, 10, width=np.pi*2, bottom=0.0, alpha=1, fill=False, lw=3)
plt.draw()
for bar in bars3:
    bar.set_height(11)

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
    MSG[8]=msg.points[1].x

 
def listener():
    rospy.init_node('IRplotter', anonymous=True)
    rospy.Subscriber('/IRdebug/point1', Point, callback1,queue_size=1)
    rospy.Subscriber('/IRdebug/point2', Point, callback2,queue_size=1)
    rospy.Subscriber('/IRdebug/point3', Point, callback3,queue_size=1)
    rospy.Subscriber('/IRdebug/point4', Point, callback4,queue_size=1)
    rospy.Subscriber('/relocNode1/relocVizData', Marker, callback5,queue_size=1)
    global MSG
    k=1
    while not rospy.is_shutdown():
	if MSG is not None:
 		#print atan2(MSG[0]-620,1340)
		X=[MSG[0],MSG[2],MSG[4],MSG[6]]
		Y=[MSG[1],MSG[3],MSG[5],MSG[7]]
		for bar in bars:
			bar.set_x(atan2(MSG[0]-512,1340)-np.pi/2)
			if MSG[0]==1023:
				bar.set_height(0)
			else:
				bar.set_height(10)
		for bar in bars2:
			bar.set_height(MSG[8])
		plt.draw()
		#fname = 'movie/_tmp%03d.png'%k
		k=k+1
    		fig.savefig(fname)
    		files.append(fname)
    rospy.spin()
    

if __name__ == '__main__':  
	#matplotlib.interactive(True)
	listener()
	
