#!/usr/bin/env python
import roslib; roslib.load_manifest('RelocSensorDriver')
import rospy
import serial
import math
import time
from std_msgs.msg import String
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point




def talker():

    #XBee config
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    ser.write('\n')
    ser.write('b\n')
    ser.close()
    ser = serial.Serial("/dev/ttyUSB0", 115200)
    packetValid=0   

    pub = rospy.Publisher('/reloc001/relocData', String)  #this should be a custom massege for kalman filter
    pub2 = rospy.Publisher('/reloc001/relocVizData', Marker)
    pub3 = rospy.Publisher('/reloc001/relocVizDataText', Marker)
    rospy.init_node('RelocNode')
    while not rospy.is_shutdown():
         
	#Read serial port and extract massege
	str=ser.readline()
	str2=str.split(',')
	print str2
	#Attempt to decode packet
	range_flag =0
	bearing_flag =0
	try:
		if str2[0][0:2] == "RL":
			for i in range(len(str2)):
				if str2[i][0:2] == "RL":
					robID = str2[i][2:]
				if str2[i] == "IR":
					IRx1=int(str2[i+1])
					IRy1=int(str2[i+2])
					IRx2=int(str2[i+3])
					IRy2=int(str2[i+4])
					IRx3=int(str2[i+5])
					IRy3=int(str2[i+6])
					IRx4=int(str2[i+7])
					IRy4=int(str2[i+8])
					bearing_flag =1
				if str2[i] == "ANG":
					IRang=int(str2[i+1][0:len(str2[i+1])-2])
				if str2[i] == "US":
					US1=float(str2[i+1])
					US2=float(str2[i+2])
					US3=float(str2[i+3])
					US4=float(str2[i+4])
					range_flag =1
			packetValid=1
		else:
			packetValid=0
	except:
		packetValid=0
		print "Bad Packet\n"
	
	#calculations
        if packetValid==1:
		slog = "No Data"
		USmin=0
		if range_flag==1 and bearing_flag==0:
			IRx=0
			IRy=0
			USmin=min(US1,US2,US3,US4)/1000.0
			fc =1380
			slog = "Range only"
			if USmin==10725:
				slog = "No Data"
				USmin=0
		if range_flag==0 and bearing_flag==1:
			IRx=IRx1
			IRy=IRy1
			USmin=10
			fc =1380
			slog = "Bearing only"
		if range_flag==1 and bearing_flag==1:
			IRx=IRx1
			IRy=IRy1
			USmin=min(US1,US2,US3,US4)/1000.0
			fc =1380
			slog = "Range Bearing"
		print USmin
		rpx=math.sqrt(pow(IRx,2)+pow(IRy,2)+pow(fc,2))
		robx=fc/rpx*USmin
		roby=IRx/rpx*USmin
		robz=IRy/rpx*USmin

		#sphere_marker = Marker()
		#sphere_marker.header.frame_id="/odom"
	    	#sphere_marker.type = Marker.SPHERE
		#sphere_marker.scale.x = USmin*2
	    	#sphere_marker.scale.y = USmin*2
	    	#sphere_marker.scale.z = USmin*2
	    	#sphere_marker.color.r = 0.0
	    	#sphere_marker.color.g = 0.5
	    	#sphere_marker.color.b = 0.5
	    	#sphere_marker.color.a = 0.1
		#pub2.publish(sphere_marker)
		#rospy.sleep(0.1)

		
		text_marker = Marker()
		text_marker.header.frame_id="/Pioneer1/base_reloc"
	    	text_marker.type = Marker.TEXT_VIEW_FACING
		text_marker.text = "RobID : %s\nx : %f\ny : %f\nz : %f\ntheta :\n %s" % (robID,robx,roby,robz,slog)
		text_marker.pose.position.x= robx
		text_marker.pose.position.y= roby
		text_marker.pose.position.z= robz
		text_marker.scale.z = 0.1
	    	text_marker.color.r = 0.0
	    	text_marker.color.g = 0.5
	    	text_marker.color.b = 0.5
	    	text_marker.color.a = 1

		arrow_marker = Marker()
		arrow_marker.header.frame_id="/Pioneer1/base_reloc"
	    	arrow_marker.type = Marker.ARROW
		arrow_marker.points = {Point(0,0,0),Point(robx,roby,robz)}
		arrow_marker.scale.x = 0.1
	    	arrow_marker.scale.y = 0.1
	    	arrow_marker.scale.z = 0.2
	    	arrow_marker.color.r = 0.0
	    	arrow_marker.color.g = 0.5
	    	arrow_marker.color.b = 0.5
	    	arrow_marker.color.a = 0.5

		pub2.publish(arrow_marker)
	        pub3.publish(text_marker)
        rospy.sleep(0.01)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
