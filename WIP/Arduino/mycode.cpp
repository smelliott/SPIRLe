#include "string.h"
#include "hardserial.h"
#include "Arduino.h"

enum Instruction {
	GPIO_GET = 0,
	GPIO_SET = 1,
	PWM_GET = 2,
	PWM_SET = 3,
	ANALOG_GET = 4,
	ANALOG_SET = 5,
	SPI_GET = 6,
	SPI_SET = 7,
	I2C_GET = 8,
	I2C_SET = 9,
	UART_GET = 10,
	UART_SET = 11
};

int main() {
	init();

#if defined(USBCON)
	USB.attach();
#endif

	SPIRLe::HardwareSerialCommProvider p(9600);
	p.open();
	string o;
	while(true) {
		p.read(o);
		// char inst = o[0];
		// Instruction i = (Instruction)inst;
		// switch(i) {
		// 	case GPIO_GET:
		// 	DigitalPin.get();
		// }
		if(o.size() > 0) {
			p.write(o);
		}
	}
	p.close();

	return 0;
}