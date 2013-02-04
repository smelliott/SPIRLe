//basic template for native arduino C code without the IDE

#include "Arduino.h"

int main() {
	init();

#if defined(USBCON)
	USB.attach();
#endif

	for (;;) {
		//do own code
		if (serialEventRun) serialEventRun(); //needed if serialEvent() is defined as event handler
	}

	return 0;
}

