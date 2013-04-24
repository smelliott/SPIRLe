# This file is a block library for running on Mark Handley's robot simulator
# Codes taken from drive.c which I and Vaibhav wrote last year. I rewrote them to Python

import socket

def reset(socket):
	for i in range(20):
		msg = "M LR 0 0\n"
		socket.send(msg)
		socket.recv(80)
	msg = "C RME\n"
	socket.send(msg)
	socket.recv(80)

def readSensor(socket,whichSensor):
	msg = "S " + whichSensor + "\n"
	socket.send(msg)
	sensorValue = int(socket.recv(80)[3+len(whichSensor):])

	if whichSensor == "US":
		return sensorValue / 58

	if sensorValue > 5:
		sensorValue = (6787/(sensorValue-3))-4
	else:
		sensorValue = 200
	return sensorValue

def setSensor(socket,whichSensor,val):
	msg = "I " + whichSensor + " " + str(val) + "\n"
	socket.send(msg)
	socket.recv(80)
	
def moveForward(socket,speed,dist):
	if(dist<0):
		dist = -dist
	t = 0
	reset(socket)
	while(t<=dist):
		msg = "M LR " + str(speed) + " " + str(speed) + "\n"
		socket.send(msg)
		socket.recv(80)
		msg = "S MEL\n"
		socket.send(msg)
		test = socket.recv(80)
		t = abs(int(test[6:]))

def setMotor(socket,leftMotor,rightMotor):
	msg = "M LR " + str(leftMotor) + " " + str(rightMotor) + "\n"
	socket.send(msg)
	socket.recv(80)

def readMotorEncoder(socket,whichMotor):
	msg = "M " + whichMotor + "\n"
	socket.send(msg)
	val = socket.recv(80)
	ls = val.split()
	value = 0
	if whichMotor == "MELR":
		value = (int(ls[2]) + int(ls[3])) / 2
	else:
		value = int(ls[2])
	return value

def flashLED():
	#not implemented anything
	return

def turnRight(socket):
	reset(socket)
	l = 0
	while(l<120):
		msg = "M LR 48 -48\n"
		socket.send(msg)
		socket.recv(80)
		msg = "S MEL\n"
		socket.send(msg)
		temp = socket.recv(80)
		l = int(temp[6:])

def turnLeft(socket):
	reset(socket)
	r = 0
	while(r<120):
		msg = "M LR -48 48\n"
		socket.send(msg)
		socket.recv(80)
		msg = "S MER\n"
		socket.send(msg)
		temp = socket.recv(80)
		r = int(temp[6:])

if __name__ == "__main__":
	print "This file is a block library for running on Mark Handley's robot simulator"
