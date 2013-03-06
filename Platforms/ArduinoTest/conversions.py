# Takes digital input from Sharp GP2D12 Laser rangefinder
# Returns distance in cm. If no obstruction detected, returns -1.
# Unreliable if sensor is close to obstruction ( < 10 cm)
def convert_cm_GP2D12(digital):
    result = (6787 / (digital - 3)) - 4
    if(result > 80):
    	return -1
    return result

# Takes input from HCSR04 Ultrasonic rangefinder in microseconds
# Returns distance in cm. If no obstruction detected, returns -1.
def convert_cm_HCSR04(uSeconds):
    if(uSeconds > 38000):
        return -1
    return uSeconds/58

# Takes input from HCSR04 Ultrasonic rangefinder in microseconds
# Returns distance in inches. If no obstruction detected, returns -1.
def convert_inches_HCSR04(uSeconds):
    if(uSeconds > 38000):
        return -1
    return uSeconds/148
