import commlib

# def flashLed(ledId):
# 	commlib.sockwrite("flashLed\n" + ledId + "\n\n")
# 	commlib.serialwrite("flashLed\n" + ledId + "\n\n")

def setGpioPin(pinId, value):
	commlib.serialwrite("\001\000\000\000\000\013\000")
