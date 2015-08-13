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



def talker():

    #XBee config
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    ser.write('\n')
    ser.write('b\n')
    ser.close()
    ser = serial.Serial("/dev/ttyUSB0", 115200)
    sourceaddrlist = {}  		# node set dictionary
    pubMarker = {} 			# publisher dictionary
    pubText = {}			# publisher dictionary	
    xbradio1 = xbee.ZigBee(ser)		# the DAQ radio
    rospy.init_node('RelocNode')
    pubIRdata1=rospy.Publisher('/IRdebug/point1', Point)
    pubIRdata2=rospy.Publisher('/IRdebug/point2', Point)
    pubIRdata3=rospy.Publisher('/IRdebug/point3', Point)
    pubIRdata4=rospy.Publisher('/IRdebug/point4', Point)
    pubUSdata=rospy.Publisher('/USdebug', Quaternion)
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
	
    
    while not rospy.is_shutdown():
        response = xbradio1.wait_read_frame() #response is a python dictionary
        
    #sorce address
        name=binascii.hexlify(response['source_addr_long'])
        sourceaddr=name.decode("utf-8")
	
    # check if its a new source address and initialize publishers
	nodeseen = 0   
       	for j in range(len(sourceaddrlist)):
		if sourceaddrlist[j+1]==sourceaddr:
			nodeseen = 1
			Rfdata=response['rf_data'].decode("utf-8")
 			str2=Rfdata.split(',')

		#packet data extraction
			range_flag =0
			bearing_flag =0
			packetValid=0
			try:
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
						IRang=int(str2[i+1][0:len(str2[i+1])-2])-90
						#print IRang/180.0*math.pi
						br.sendTransform((0, 0, 0.3),tf.transformations.quaternion_from_euler(0, 0, -IRang/180.0*math.pi),rospy.Time.now(),"/pioneer1/IRcam","/pioneer1/base_link")
					if str2[i] == "US":
						US1=float(str2[i+1])
						US2=float(str2[i+2])
						US3=float(str2[i+3])
						US4=float(str2[i+4])
						range_flag =1
				packetValid=1
			except:
				#print "Bad Packet\n"
				packetValid=0
				
		
		#Measurement processing
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
				#print USmin
				#print IRx1
				if IRx1==1023:
					robx=0
					roby=0
					robz=0
				else:
					rpx=math.sqrt(pow(IRx,2)+pow(IRy,2)+pow(fc,2))
					robx=fc/rpx*USmin
					roby=IRx/rpx*USmin
					robz=IRy/rpx*USmin
				if USmin==0 or USmin>9:
					USmin=0.1
				

		#Data publish
				text_marker = Marker()
				text_marker.header.frame_id="/pioneer1/base_link"
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
				
				if slog == "Range only":
					arrow_marker = Marker()
					arrow_marker.header.frame_id="/pioneer1/base_link"
	    				arrow_marker.type = Marker.CYLINDER
					arrow_marker.scale.x = (USmin+0.05)*2
	    				arrow_marker.scale.y = (USmin+0.05)*2
	    				arrow_marker.scale.z = 0.1
	    				arrow_marker.color.r = 0.0
	    				arrow_marker.color.g = 0.5
	    				arrow_marker.color.b = 0.5
	    				arrow_marker.color.a = 0.5

				else :
					arrow_marker = Marker()
					arrow_marker.header.frame_id="/pioneer1/base_link"
	    				arrow_marker.type = Marker.ARROW
					arrow_marker.points = {Point(0,0,0),Point(robx,roby,robz)}
					arrow_marker.scale.x = 0.1
	    				arrow_marker.scale.y = 0.1
	    				arrow_marker.scale.z = 0.2
	    				arrow_marker.color.r = 1.0
	    				arrow_marker.color.g = 0.5
	    				arrow_marker.color.b = 0.5
	    				arrow_marker.color.a = 0.5

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

				USdebug = Quaternion()
				USdebug.x = US1
				USdebug.y = US2
				USdebug.z = US3
				USdebug.w = US4

				pubIRdata1.publish(IRdebug1)
				pubIRdata2.publish(IRdebug2)
				pubIRdata3.publish(IRdebug3)
				pubIRdata4.publish(IRdebug4)
				pubUSdata.publish(USdebug)

				pubText[j+1].publish(text_marker)
				pubMarker[j+1].publish(arrow_marker)

			if str2[0][0:5] == "RL002":
				print str2
			#print str2
			
			
	if nodeseen == 0:  # New nodes handling
		sourceaddrlist[len(sourceaddrlist)+1]=sourceaddr
		pubText[len(pubText)+1]=rospy.Publisher('/relocNode'+str(len(pubText)+1)+'/relocVizDataText', Marker)
		pubMarker[len(pubMarker)+1]=rospy.Publisher('/relocNode'+str(len(pubMarker)+1)+'/relocVizData', Marker)
		print "New node registered:"+ sourceaddr
		#publish data of new node
		Rfdata=response['rf_data'].decode("utf-8")
			
		
                
        #print(sourceaddr+' :'+Rfdata)
	
	#Publish all topics
	
	
        rospy.sleep(0.01)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
