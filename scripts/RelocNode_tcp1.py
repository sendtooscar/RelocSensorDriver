#!/usr/bin/env python
import roslib; roslib.load_manifest('RelocSensorDriver')
import tf
import rospy
import xbee 
import serial
import binascii 
import math
import time
from std_msgs.msg import String
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import Range
import socket
import sys


#TCP_IP = '127.0.0.1'
#TCP_PORT = 5000
#BUFFER_SIZE = 5000

#taking server parameters from the command line
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv[1])

if len(sys.argv)<3:
	print "Usage <ip> <port>"
	sys.exit(-1)

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 5000



def talker():

    #tcp config
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    pubMarker = {} 			# publisher dictionary
    pubText = {}			# publisher dictionary	
    pubUS1 = {}
    pubUS2 = {}
    pubUS3 = {}
    pubUS4 = {}
    rospy.init_node('RelocNode')

    #debug topics
    pubIRdata1=rospy.Publisher('IRdebug/point1', Point)
    pubIRdata2=rospy.Publisher('IRdebug/point2', Point)
    pubIRdata3=rospy.Publisher('IRdebug/point3', Point)
    pubIRdata4=rospy.Publisher('IRdebug/point4', Point)
    pubUSdata=rospy.Publisher('USdebug', Quaternion)

    #The published topics
    pubText=rospy.Publisher('relocNode/relocVizDataText', Marker)
    pubMarkerRange=rospy.Publisher('relocNode/relocVizDataRange', Marker)
    pubMarkerBear=rospy.Publisher('relocNode/relocVizDataBear', Marker)
    pubMarkerBear2=rospy.Publisher('relocNode/relocVizDataBear2', Marker)
    pubMarkerBear3=rospy.Publisher('relocNode/relocVizDataBear3', Marker)
    pubUSAoa = rospy.Publisher('relocNode/relocUsAoa', Range)
    pubUSAoa2 = rospy.Publisher('relocNode/relocUsAoa2', Range)
    
    #Us range sensors
    pubUS1=rospy.Publisher('relocNode/relocUS1', Range)
    pubUS2=rospy.Publisher('relocNode/relocUS2', Range)
    pubUS3=rospy.Publisher('relocNode/relocUS3', Range)
    pubUS4=rospy.Publisher('relocNode/relocUS4', Range)

    

    #parameter for tf prefix
    if rospy.has_param("~tf_prefix"):	
    	tf_prefix = rospy.get_param("~tf_prefix")
    else:
	tf_prefix= ""
    
    br = tf.TransformBroadcaster()
    robId="??"
    IRx1=0
    IRy1=0
    IRx2=0
    IRy2=0
    IRx3=0
    IRy3=0
    IRx4=0
    IRy4=0
    IRang=0
    US1=0
    US2=0
    US3=0
    US4=0
    time_pre=0

    # initialy flush the buffer
    response = s.recv(BUFFER_SIZE)
	
    
    while not rospy.is_shutdown():
        response = s.recv(BUFFER_SIZE)
        
   	
    # check if its a new source address and initialize publishers
	Rfdata=response
	#print response
 	str2=Rfdata.split(',')

	#packet data extraction
	range_flag =0
	bearing_flag =0
	packetValid =0
	new_packet =0
	robId="??"
	
	try:
		for i in range(len(str2)):
			if str2[i][0:2] == "RL" or str2[i][0:2] == "rl":
				robID = str2[i][2:]
				localID = str2[i][2]
				targetID = str2[i][4]
				#print localID,targetID
				#transmit the previous set
			if str2[i] == "IR" or str2[i] == "ir":
				IRx1=int(str2[i+1])
				IRy1=int(str2[i+2])
				IRx2=int(str2[i+3])
				IRy2=int(str2[i+4])
				IRx3=int(str2[i+5])
				IRy3=int(str2[i+6])
				IRx4=int(str2[i+7])
				IRy4=int(str2[i+8])
				bearing_flag =1
				packetValid=1
			if str2[i] == "ANG" or str2[i] == "ang":
				#print str2[i+1] 				
				IRang=int(str2[i+1])-90
				#print IRang/180.0*math.pi
				br.sendTransform((0.085, 0, -0.035),tf.transformations.quaternion_from_euler(0, 0, -IRang/180.0*math.pi),rospy.Time.now(),tf_prefix+"/IRcam",tf_prefix+"/base_reloc2")
				br.sendTransform((0.085, 0, -0.035),tf.transformations.quaternion_from_euler(0, 0, 0),rospy.Time.now(),tf_prefix+"/IRcamBase",tf_prefix+"/base_reloc2")
				#br.sendTransform((0, 0, 0.3),tf.transformations.quaternion_from_euler(0, 0, -IRang/200.0*2*math.pi),rospy.Time.now(),"/pioneer1/IRcam","/pioneer1/base_reloc1")
			if str2[i] == "US" or str2[i] == "us":
				US1=float(str2[i+1])
				US2=float(str2[i+2])
				US3=float(str2[i+3])
				US4=float(str2[i+4])
				range_flag =1
				packetValid=1
	except:
		print "Bad Packet\n"
		print str2,robID
		packetValid=0
				
		
		#Measurement processing
	if packetValid==1:
		#print targetID,US1,US2,US3,US4,IRx1,IRang
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
			IRx=IRx1-1024/2
			IRy=-IRy1+768/2
			USmin=10
			fc =1380
			slog = "Bearing only"
		if range_flag==1 and bearing_flag==1:
			IRx=IRx1-1024/2
			IRy=-IRy1+768/2
			USmin=min(US1,US2,US3,US4)/1000.0
			fc =1380
			slog = "Range Bearing"
		#print slog		
		#print USmin
		#print IRx1
		if IRx1==1023 or bearing_flag==0:
			robx=0
			roby=0
			robz=0
		else:
			rpx=math.sqrt(pow(IRx,2)+pow(IRy,2)+pow(fc,2))
			robx=fc/rpx*USmin
			roby=IRx/rpx*USmin
			robz=IRy/rpx*USmin
		if USmin==0 or USmin>9:
			USmin=0
		

		#Data publish
		text_marker = Marker()
		text_marker.header.frame_id=tf_prefix+"/base_reloc2"
		text_marker.type = Marker.TEXT_VIEW_FACING
		text_marker.text = "%s%s" % (localID,targetID)
		text_marker.pose.position.x= 0
		text_marker.pose.position.y= 0
		text_marker.pose.position.z= 0
		text_marker.scale.z = 0.1
		text_marker.color.r = 0.0
		text_marker.color.g = 0.5
		text_marker.color.b = 0.5
		text_marker.color.a = 1
		
		if slog == "Range only" or "Range Bearing":
			arrow_marker = Marker()
			arrow_marker.header.frame_id=tf_prefix+"/base_reloc2"
			arrow_marker.ns="%s%s" % (localID,targetID)
			arrow_marker.type = Marker.CYLINDER
			arrow_marker.scale.x = (USmin+0.05)*2
			arrow_marker.scale.y = (USmin+0.05)*2
			arrow_marker.scale.z = 0.1
			arrow_marker.color.r = 0.0
			arrow_marker.color.g = 0.5
			arrow_marker.color.b = 0.5
			arrow_marker.color.a = 0.5
		if slog == "Bearing only" or "Range Bearing":
			arrow_marker2 = Marker()
			#arrow_marker2.header.frame_id=tf_prefix+"/base_reloc2"
			arrow_marker2.header.frame_id=tf_prefix+"/IRcam"
			arrow_marker2.ns="%s%s" % (localID,targetID)
			arrow_marker2.type = Marker.ARROW
			arrow_marker2.points = {Point(0,0,0),Point(robx,roby,robz)}
			arrow_marker2.scale.x = 0.1
			arrow_marker2.scale.y = 0.1
			arrow_marker2.scale.z = 0.2
			arrow_marker2.color.r = 1.0
	    		arrow_marker2.color.g = 0.5
	    		arrow_marker2.color.b = 0.5
	    		arrow_marker2.color.a = 0.5
			arrow_marker3 = Marker()
			#arrow_marker2.header.frame_id=tf_prefix+"/base_reloc2"
			arrow_marker3.header.frame_id=tf_prefix+"/IRcamBase"
			arrow_marker3.ns="%s%s" % (localID,targetID)
			arrow_marker3.type = Marker.ARROW
			arrow_marker3.points = {Point(0,0,0),Point(robx,roby,robz)}
			arrow_marker3.scale.x = 0.1
			arrow_marker3.scale.y = 0.1
			arrow_marker3.scale.z = 0.2
			arrow_marker3.color.r = 1.0
	    		arrow_marker3.color.g = 0.5
	    		arrow_marker3.color.b = 0.5
	    		arrow_marker3.color.a = 0.5
			arrow_marker4 = Marker()
			arrow_marker4.header.frame_id=tf_prefix+"/IRcamBase"
			arrow_marker4.ns="%s%s" % (localID,targetID)
			arrow_marker4.type = Marker.ARROW
			arrow_marker4.points = {Point(0,0,0),Point(robx,-roby,robz)}
			arrow_marker4.scale.x = 0.1
			arrow_marker4.scale.y = 0.1
			arrow_marker4.scale.z = 0.2
			arrow_marker4.color.r = 1.0
	    		arrow_marker4.color.g = 0.5
	    		arrow_marker4.color.b = 0.5
	    		arrow_marker4.color.a = 0.5
		

		IRdebug1 = Point()
		IRdebug1.x = IRx1
		IRdebug1.y = IRy1
		IRdebug2 = Point()
		IRdebug2.x = IRx2
		IRdebug2.y = IRy2
		IRdebug3 = Point()
		IRdebug3.x = IRx3
		IRdebug3.y = IRy3
		IRdebug4 = Point()
		IRdebug4.x = IRx4
		IRdebug4.y = IRy4

		if slog == "Range only" or "Range Bearing":
			USang1=0.0
			USarr=[US1/1000.0,US2/1000.0,US3/1000.0,US4/1000.0]
			#print USarr
			USIds=[0,1,2,3]
			USmin1=min(USarr)
			USminId=USarr.index(min(USarr))
			USIds.remove(USminId)
			del USarr[USminId]
			if USminId==0: USang1=90.0
			if USminId==1: USang1=-90.0
			if USminId==2: USang1=0.0
			if USminId==3: USang1=180.0
			USminId=USarr.index(min(USarr))
			USmin2=min(USarr)
			if USminId==0: USang2=90.0
			if USminId==1: USang2=-90.0
			if USminId==2: USang2=0.0
			if USminId==3: USang2=180.0
			corr=(USmin2-USmin1)*45/0.1
			if corr>45:corr=45
			if corr<-45:corr=-45
			#print USmin2-USmin1
			USang =(USang1+USang2)/2-corr
			#print (USang1+USang2)/2-corr
			#print USang1
			#print USang2
			#print "------------"
			#angular coorection
			
			br.sendTransform((0, 0, 0),tf.transformations.quaternion_from_euler(0, 0, USang1*math.pi/180.0),rospy.Time.now(),tf_prefix+"/base_reloc2/USAoa",tf_prefix+"/base_reloc2")
			USAoa = Range()
			USAoa.header.frame_id=tf_prefix+"/base_reloc2/USAoa"
			USAoa.radiation_type=0
			USAoa.field_of_view =math.pi/4.0
			USAoa.min_range = 0.5
			USAoa.max_range = 10.0
			USAoa.range     = USmin

			br.sendTransform((0, 0, 0),tf.transformations.quaternion_from_euler(0, 0, -USang1*math.pi/180.0),rospy.Time.now(),tf_prefix+"/base_reloc2/USAoa2",tf_prefix+"/base_reloc2")
			USAoa2 = Range()
			USAoa2.header.frame_id=tf_prefix+"/base_reloc2/USAoa2"
			USAoa2.radiation_type=0
			USAoa2.field_of_view =math.pi/4.0
			USAoa2.min_range = 0.5
			USAoa2.max_range = 10.0
			USAoa2.range     = USmin

		USdebug = Quaternion()
		USdebug.x = US1
		USdebug.y = US2
		USdebug.z = US3
		USdebug.w = US4

		USrange1 = Range()
		USrange1.header.frame_id=tf_prefix+"/base_reloc2/US1"
		USrange1.radiation_type=0
		USrange1.field_of_view =math.pi/2.0
		USrange1.min_range = 0.5
		USrange1.max_range = 10.0
		USrange1.range     = US3/1000.0

		br.sendTransform((0, 0, 0),tf.transformations.quaternion_from_euler(0, 0, 0),rospy.Time.now(),tf_prefix+"/base_reloc2/US1",tf_prefix+"/base_reloc2")

		USrange2 = Range()
		USrange2.header.frame_id=tf_prefix+"/base_reloc2/US2"
		USrange2.radiation_type=0
		USrange2.field_of_view =math.pi/2.0
		USrange2.min_range = 0.5
		USrange2.max_range = 10.0
		USrange2.range     = US2/1000.0
				
		br.sendTransform((0, 0, 0),tf.transformations.quaternion_from_euler(0, 0, math.pi/2.0),rospy.Time.now(),tf_prefix+"/base_reloc2/US2",tf_prefix+"/base_reloc2/US1")

		USrange3 = Range()
		USrange3.header.frame_id=tf_prefix+"/base_reloc2/US3"
		USrange3.radiation_type=0
		USrange3.field_of_view =math.pi/2.0
		USrange3.min_range = 0.5
		USrange3.max_range = 10.0
		USrange3.range     = US4/1000.0

		br.sendTransform((0, 0, 0),tf.transformations.quaternion_from_euler(0, 0, math.pi),rospy.Time.now(),tf_prefix+"/base_reloc2/US3",tf_prefix+"/base_reloc2/US1")

		USrange4 = Range()
		USrange4.header.frame_id=tf_prefix+"/base_reloc2/US4"
		USrange4.radiation_type=0
		USrange4.field_of_view =math.pi/2.0
		USrange4.min_range = 0.5
		USrange4.max_range = 10.0
		USrange4.range     = US1/1000.0

		br.sendTransform((0, 0, 0),tf.transformations.quaternion_from_euler(0, 0, 3.0*math.pi/2.0),rospy.Time.now(),tf_prefix+"/base_reloc2/US4",tf_prefix+"/base_reloc2/US1")

		#print USdebug
		#print arrow_marker
		pubIRdata1.publish(IRdebug1)
		pubIRdata2.publish(IRdebug2)
		pubIRdata3.publish(IRdebug3)
		pubIRdata4.publish(IRdebug4)
		pubUSdata.publish(USdebug)
		pubText.publish(text_marker)
		pubMarkerRange.publish(arrow_marker)
		pubMarkerBear.publish(arrow_marker2)
		pubMarkerBear2.publish(arrow_marker3)
 		pubMarkerBear3.publish(arrow_marker4)
		pubUS1.publish(USrange1)
		pubUS2.publish(USrange2)
		pubUS3.publish(USrange3)
		pubUS4.publish(USrange4)
		pubUSAoa.publish(USAoa)
		pubUSAoa2.publish(USAoa2)
		


	#print str2
			
			
rospy.sleep(0.001)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
