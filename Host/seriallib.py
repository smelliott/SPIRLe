import serial


def write(msg):
    s = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
    s.write(msg)
    s.flushOutput()
    s.close()
