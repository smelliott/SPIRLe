import time, conversions
from pinhelper import * 
#import pin setting library

# Takes trigger and echo pins.
# Returns distance in cm detected by ultrasonic rangefinder.
def do(triggerPinId, answerPinId, address):

	# trigger pulse
#	lib.set_GPIO_pin(triggerPinId, HIGH, address)
	hangMicroseconds(10)
#	lib.set_GPIO_pin(triggerPinId, LOW, address)

	# prepare cycle information
	CYCLEPERIOD_SECONDS = 0.05
	t1 = time.clock()

	# answer pulse
	answer = pulseIn(answerPinId, HIGH, address)
	if(answer == -1):
		raise Error('No response from device')
	result = conversions.convert_cm_HCSR04(answer)

	# enforce cycle period
	hangSeconds(CYCLEPERIOD_SECONDS + t1 - time.clock())

	return result