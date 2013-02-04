import commlib

def flashLed(ledId):
	commlib.sockwrite("flashLed\n" + ledId + "\n\n")
	commlib.serialwrite("flashLed\n" + ledId + "\n\n")

