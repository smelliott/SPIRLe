import time
#import pin setting library

HIGH = 1
LOW = 0

# Precise hang for pin handling
def hangSeconds(s):
	t1 = time.clock()
	while(time.clock() < t1 + s) : continue

def hangMillisecs(ms):
	hangSeconds(ms / 1000)

def hangMicroseconds(us):
	hangSeconds(us / 1000000)

# Takes pin and value to monitor. Currently has no timeout
# Returns pulse time in microseconds.
def pulseIn(pinId, value, address):
#	while(lib.get_GPIO_Pin(pinId, value, address) != value) : continue
	t1 = time.clock()
#	while(lib.get_GPIO_Pin(pinId, value, address) == value) : continue
	t2 = time.clock()
	return (t2 - t1) * 1000000
