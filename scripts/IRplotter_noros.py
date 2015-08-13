#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib, time
import serial
from pylab import *

ser = serial.Serial("/dev/ttyUSB0", 115200)
MSG=[0,0,0,0,0,0,0,0]
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
points,=ax.plot(np.random.randn(4),np.random.randn(4),'o')
plt.ylim((-1100,1100))
plt.xlim((-10,1100))
plt.draw()
packetValid=0
 
while True:
	str=ser.readline()
	print str
	str2=str.split(',')
	#print str2
	#Attempt to decode packet
	try:
		for i in range(len(str2)):
			if str2[i][0:2] == "RL":
				robID = int(str2[i][2:])
			if str2[i] == "IR":
				IRx1=int(str2[i+1])
				IRy1=int(str2[i+2])
				IRx2=int(str2[i+3])
				IRy2=int(str2[i+4])
				IRx3=int(str2[i+5])
				IRy3=int(str2[i+6])
				IRx4=int(str2[i+7])
				IRy4=int(str2[i+8])
				packetValid=1
			if str2[i] == "SIZE":
				IRs1=int(str2[i+1])
				IRs2=int(str2[i+2])
				IRs3=int(str2[i+3])
				IRs4=int(str2[i+4])
			if str2[i] == "ANG":
				IRang=int(str2[i+1][0:len(str2[i+1])-2])
			if str2[i] == "US":
				US1=float(str2[i+1])
				US2=float(str2[i+2])
				US3=float(str2[i+3])
				US4=float(str2[i+4])
	
		
	except:
		packetValid=0
		print "Bad Packet\n"
		print str2
 	if packetValid==1:
		X=[IRx1,IRx2,IRx3,IRx4]
		Y=[IRy1,IRy2,IRy3,IRy4]
		#S=[IRs1,IRs2,IRs3,IRs4]
		points.set_data(X,Y)
		#scatter(X,Y,s=S, marker='^', c='r')
		#xlim([0,1024])
		#ylim([0,1024])
		#show()
		plt.draw()
 
	
