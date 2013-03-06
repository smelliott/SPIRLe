import time, conversions
from pinhelper import *
#import pin setting library

# Takes pinId and address.
# Returns distance in cm detected by the GP2D12 infrared rangefinder.
def do(pinId, address):

	#prepare cycle information
	CYCLEPERIOD_SECONDS = 0.032
	t1 = time.clock()
	
	# read and convert
	# assume get_analog_pin handles A\D
#	result = conversions.convert_cm_GP2D12(lib.get_analog_pin(pinId, address))
	result = 0
	
	# enforce cycle period
	hangSeconds(CYCLEPERIOD_SECONDS + t1 - time.clock())
	
	return result