#from socketlib import *
from seriallib import *
import struct


# ! in pack means network order (big endian)

def get_GPIO_pin(pinId, address = 0):
	# ______ _______________________ _______
	# uchar | uint32                | uchar
	# ------ ----------------------- -------
	# inst  | address               | pin
	# ------ ----------------------- -------
	#
	out = struct.pack('!BIB', 0, address, pinId)
	write(out)
	#need read
	return 1

def set_GPIO_pin(pinId, value, address = 0):
	# ______ _______________________ _______ _______
	# uchar | uint32                | uchar | uchar
	# ------ ----------------------- ------- -------
	# inst  | address               | pin   | value
	# ------ ----------------------- ------- -------
	#
	out = struct.pack('!BIBB', 1, address, pinId, value)
	write(out)

def get_analog_pin(pinId, address = 0):
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

def set_analog_pin(pinId, value, address = 0):
	# ______ _______________________ _______ _______
	# uchar | uint32                | uchar | uchar
	# ------ ----------------------- ------- -------
	# inst  | address               | pin   | value
	# ------ ----------------------- ------- -------
	#
	out = struct.pack('!BIBB', 3, address, pinId, value)
	write(out)

def get_PWM_pin(pinId, address = 0):
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

def set_PWM_pin(pinId, value, address = 0):
	# ______ _______________________ _______ _______
	# uchar | uint32                | uchar | uchar
	# ------ ----------------------- ------- -------
	# inst  | address               | pin   | value
	# ------ ----------------------- ------- -------
	#
	out = struct.pack('!BIBB', 5, address, pinId, value)
	write(out)

def write_SPI(hwId, data, address = 0):
	# ______ _______________________ ________________________ _______ ____________
	# uchar | uint32                | uint32                 | uchar | variable..
	# ------ ----------------------- ------------------------ ------- ------------
	# inst  | address               | hw id (SPI #)          |length | payload
	# ------ ----------------------- ------------------------ ------- ------------
	#
	out = struct.pack('!BIIBs', 6, address, hwId, len(data), data)
	write(out)

def read_SPI(hwId, length, address = 0):
	return 'hello'

def read_SPI(hwId, address = 0):
	#as above but reads all available from given SPI
	return 'hi'

def write_I2C(hwId, data, address = 0):
	return

def read_I2C(hwId, length, address = 0):
	return 'hello'

def read_I2C(hwId, address = 0):
	#as above but reads all available from given I2C
	return 'hi'

def write_UART(hwId, data, address = 0):
	return

def read_UART(hwId, length, address = 0):
	return 'hello'

def read_UART(hwId, address = 0):
	#as above but reads all available from given UART
	return 'hi'

