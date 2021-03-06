import serial


class SerialComm:
	"""Serial communications class"""
	def __init__(self):
		self.s = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
		return

	def conf(self, serial_port, baud_rate, tmo):
		#self.s = serial.Serial(serial_port, baud_rate, timeout=tmo)
		return

	def read(self, bytes):
	    out = self.s.read(bytes)
	    return out

	def write(self, msg):
	    self.s.write(msg)
	    return
