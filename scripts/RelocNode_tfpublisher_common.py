#!/usr/bin/env python
import roslib; roslib.load_manifest('RelocSensorDriver')
import tf
import rospy
import math
import time
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import euler_from_quaternion

pioneer1=[-0.433, -0.224, -0.000,-0.257]
pioneer2=[2.367, -1.658, -0.000, 0.835]
#drone1=[4.73816204071,-0.1,0.0,-0.992151563931,0.125041090001]
drone1=[0.0,0.0,0.0,0.0,1.0]

#todo launch this along wih odometers and update odom frame to map

def talker():

    rospy.init_node('RelocNode')
    br = tf.TransformBroadcaster()
    rospy.Subscriber('/pioneer1/initialpose', PoseWithCovarianceStamped, callback1,queue_size=1)
    rospy.Subscriber('/pioneer2/initialpose', PoseWithCovarianceStamped, callback2,queue_size=1)
    rospy.Subscriber('/drone1/initialpose', PoseWithCovarianceStamped, callback3,queue_size=1)
    while not rospy.is_shutdown():
	    #br.sendTransform((pioneer1[0], pioneer1[1], pioneer1[2]),tf.transformations.quaternion_from_euler(0, 0, pioneer1[3]),rospy.Time.now(),"/pioneer1/base_reloc2","/map")
	    #br.sendTransform((pioneer1[0], pioneer1[1], pioneer1[2]),tf.transformations.quaternion_from_euler(0, 0, pioneer1[3]),rospy.Time.now(),"/pioneer1/odom","/map")
	    #br.sendTransform((pioneer2[0], pioneer2[1], pioneer2[2]),tf.transformations.quaternion_from_euler(0, 0, pioneer2[3]),rospy.Time.now(),"/pioneer2/odom","/map")
	    #br.sendTransform((drone1[0], drone1[1], drone1[2]),(0.0, 0.0, drone1[3], drone1[4] ),rospy.Time.now(),"/pioneer1/base_reloc2","/map")
	    br.sendTransform((drone1[0], drone1[1], drone1[2]),(0.0, 0.0, drone1[3], drone1[4] ),rospy.Time.now(),"/drone1/base_reloc2","/pioneer2/base_reloc2")
	    rospy.sleep(0.01)

def callback1(msg):
    pioneer1[0]=msg.pose.pose.position.x
    pioneer1[1]=msg.pose.pose.position.y
    pioneer1[2]=msg.pose.pose.position.z
    odom_quat=[0,0,0,0]
    odom_quat[0]=msg.pose.pose.orientation.x
    odom_quat[1]=msg.pose.pose.orientation.y
    odom_quat[2]=msg.pose.pose.orientation.z
    odom_quat[3]=msg.pose.pose.orientation.w
    odom_euler= euler_from_quaternion(odom_quat)
    pioneer1[3]=odom_euler[2]

def callback2(msg):
    pioneer2[0]=msg.pose.pose.position.x
    pioneer2[1]=msg.pose.pose.position.y
    pioneer2[2]=msg.pose.pose.position.z
    odom_quat=[0,0,0,0]
    odom_quat[0]=msg.pose.pose.orientation.x
    odom_quat[1]=msg.pose.pose.orientation.y
    odom_quat[2]=msg.pose.pose.orientation.z
    odom_quat[3]=msg.pose.pose.orientation.w
    odom_euler= euler_from_quaternion(odom_quat)
    pioneer2[3]=odom_euler[2]

def callback3(msg):
    drone1[0]=msg.pose.pose.position.x
    drone1[1]=msg.pose.pose.position.y
    drone1[2]=msg.pose.pose.position.z
    odom_quat=[0,0,0,0]
    odom_quat[0]=msg.pose.pose.orientation.x
    odom_quat[1]=msg.pose.pose.orientation.y
    odom_quat[2]=msg.pose.pose.orientation.z
    odom_quat[3]=msg.pose.pose.orientation.w
    odom_euler= euler_from_quaternion(odom_quat)
    drone1[3]=odom_euler[2]
   

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
