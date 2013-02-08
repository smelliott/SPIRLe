import serial

#TODO: create class to allow connection sharing

class serialcomm:
	def __init__(self):
		self.s = serial.Serial('/dev/ttyACM0', 9600, timeout=5)

	def read(self):
	    out = self.s.read(10)
	    return out

	def write(self, msg):
	    self.s.write(msg)
	    self.s.flushOutput()
