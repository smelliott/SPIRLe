import serial

#TODO: create class to allow connection sharing

class SerialComm:
	"""Serial communications class"""
	def __init__(self):
		return

	def conf(self, serial_port, baud_rate, tmo):
		#self.s = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
		self.s = serial.Serial(serial_port, baud_rate, timeout=tmo)
		return

	def read(self):
	    out = self.s.read(10)
	    return out

	def write(self, msg):
	    self.s.write(msg)
	    self.s.flushOutput()
	    return
