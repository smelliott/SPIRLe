import socket

def read():
	return ''

def write(msg):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('localhost', 9999))
	s.send(msg)
	s.close()
