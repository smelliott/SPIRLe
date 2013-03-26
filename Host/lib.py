#from socketlib import *
from seriallib import *
from socketlib import *
import struct

class Comm:
	"""Robot communication library"""

	def __init__(self):
		self.s = None
		self.type = ""
		return

	def setup_serial(self, serial_port, baud_rate, timeout):
		self.type = "SERIAL"
		self.serial_port = serial_port
		self.baud_rate = baud_rate
		self.timeout = timeout
		return

	def setup_socket(self, addr, port, timeout):
		self.type = "SOCKET"
		self.addr = addr
		self.port = port
		self.timeout = timeout
		return

	def init(self):
		if self.s == None:
			if self.type == "":
				return False

			if self.type == "SERIAL":
				self.s = SerialComm()
				self.s.conf(self.serial_port, self.baud_rate, self.timeout)
				return True

			if self.type == "SOCKET":
				self.s = SocketComm()
				self.s.conf(self.addr, self.port, self.timeout)
				return True

			return False
		return True


	# ! in pack means network order (big endian)

	def get_GPIO_pin(self, pinId, address = 0):
		# ______ _______________________ _______
		# uchar | uint32                | uchar
		# ------ ----------------------- -------
		# inst  | address               | pin
		# ------ ----------------------- -------
		#
		out = struct.pack('!BIB', 0, address, pinId)
		self.init()
		self.s.write(out)
		#need read
		return 1

	def set_GPIO_pin(self, pinId, value, address = 0):
		# ______ _______________________ _______ _______
		# uchar | uint32                | uchar | uchar
		# ------ ----------------------- ------- -------
		# inst  | address               | pin   | value
		# ------ ----------------------- ------- -------
		#
		out = struct.pack('<BIBB', 1, address, pinId, value)
		s = serialcomm()
		s.write(out)
		x = s.read()
		#x = struct.unpack('<s', x)
		#print x
		return

	def get_analog_pin(self, pinId, address = 0):
		# ______ _______________________ _______
		# uchar | uint32                | uchar
		# ------ ----------------------- -------
		# inst  | address               | pin
		# ------ ----------------------- -------
		#
		out = struct.pack('!BIB', 2, address, pinId)
		write(out)
		#need read
		return 1

	def set_analog_pin(self, pinId, value, address = 0):
		# ______ _______________________ _______ _______
		# uchar | uint32                | uchar | uchar
		# ------ ----------------------- ------- -------
		# inst  | address               | pin   | value
		# ------ ----------------------- ------- -------
		#
		out = struct.pack('!BIBB', 3, address, pinId, value)
		write(out)
		return

	def get_PWM_pin(self, pinId, address = 0):
		# ______ _______________________ _______
		# uchar | uint32                | uchar
		# ------ ----------------------- -------
		# inst  | address               | pin
		# ------ ----------------------- -------
		#
		out = struct.pack('!BIB', 4, address, pinId)
		write(out)
		#need read
		return 1

	def set_PWM_pin(self, pinId, value, address = 0):
		# ______ _______________________ _______ _______
		# uchar | uint32                | uchar | uchar
		# ------ ----------------------- ------- -------
		# inst  | address               | pin   | value
		# ------ ----------------------- ------- -------
		#
		out = struct.pack('!BIBB', 5, address, pinId, value)
		write(out)
		return

	def write_SPI(self, hwId, data, address = 0):
		# ______ _______________________ ________________________ _______ ____________
		# uchar | uint32                | uint32                 | uchar | variable..
		# ------ ----------------------- ------------------------ ------- ------------
		# inst  | address               | hw id (SPI #)          |length | payload
		# ------ ----------------------- ------------------------ ------- ------------
		#
		out = struct.pack('!BIIBs', 6, address, hwId, len(data), data)
		write(out)
		return

	def read_SPI(self, hwId, length, address = 0):
		out = struct.pack('!BII', 7, address, hwId)
		write(out)
		return 'hello'

	def read_SPI(self, hwId, address = 0):
		#as above but reads all available from given SPI
		out = struct.pack('!BII', 7, address, hwId)
		write(out)
		return 'hi'

	def write_I2C(self, hwId, data, address = 0):
		return

	def read_I2C(self, hwId, length, address = 0):
		return 'hello'

	def read_I2C(self, hwId, address = 0):
		#as above but reads all available from given I2C
		return 'hi'

	def write_UART(self, hwId, data, address = 0):
		return

	def read_UART(self, hwId, length, address = 0):
		return 'hello'

	def read_UART(self, hwId, address = 0):
		#as above but reads all available from given UART
		return 'hi'

