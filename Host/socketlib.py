import socket

class SocketComm:
	"""Socket communications class"""
	def __init__(self):
		self.s = None
		return

	def __del__(self):
		if self.s != None:
			self.s.close()
		return

	def conf(self, addr, port, timeout):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((addr, port))
		return

	def read(self):
		return ''

	def write(self, msg):
		self.s.send(msg)
		return
