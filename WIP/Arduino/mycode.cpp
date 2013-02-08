#include "string.h"
#include "hardserial.h"
#include "pin.h"
#include "Arduino.h"
#include <stdlib.h>

#define SERIAL

using namespace SPIRLe;

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

void read_and_put(ICommProvider& p, string& out) {
	char* ret = p.read();
	out += ret;
	free(ret);
}

void try_parse(string& inst) {
	const string::size_type inst_size = inst.size();
	//minimum of 6 bytes to form valid message
	if(inst_size < 6) {
		return;
	}

	unsigned char inst_index = inst[0];
	char str[4];
	str[0] = inst[1];
	str[1] = inst[2];
	str[2] = inst[3];
	str[3] = inst[4];
	uint32_t addr = atoi(str);

	if(addr != 0  /* && addr != my_addr */) {
		return;
	}

	switch(inst_index) {
		case GPIO_GET:
			if(inst_size >= 6) {
				int ret = DigitalPin.get(inst[5]);
				char out[5];
				out = (char*)ret;
				out[4] = 0;
				p.write(out);
				inst.erase(0, 6);
			}
			break;

		case GPIO_SET:
			if(inst_size >= 7) {
				DigitalPin.set(inst[5], inst[6]);
				char out[2];
				out[0] = 1;
				out[1] = 0;
				p.write(out);
				inst.erase(0, 7);
			}
			break;

		case PWM_GET:
			if(inst_size >= 6) {
				int ret = PwmPin.get(inst[5]);
				char out[5];
				out = (char*)ret;
				out[4] = 0;
				p.write(out);
				inst.erase(0, 6);
			}
			break;

		case PWM_SET:
			if(inst_size >= 7) {
				PwmPin.set(inst[5], inst[6]);
				char out[2];
				out[0] = 1;
				out[1] = 0;
				p.write(out);
				inst.erase(0, 7);
			}
			break;

		case ANALOG_GET:
			if(inst_size >= 6) {
				int ret = AnalogPin.get(inst[5]);
				char out[5];
				out = (char*)ret;
				out[4] = 0;
				p.write(out);
				inst.erase(0, 6);
			}
			break;

		case ANALOG_SET:
			if(inst_size >= 7) {
				AnalogPin.set(inst[5], inst[6]);
				char out[2];
				out[0] = 1;
				out[1] = 0;
				p.write(out);
				inst.erase(0, 7);
			}
			break;

		case SPI_GET:
			//UNIMPLEMENTED ATM
			break;

		case SPI_SET:
			//UNIMPLEMENTED ATM
			break;

		case I2C_GET:
			//UNIMPLEMENTED ATM
			break;

		case I2C_SET:
			//UNIMPLEMENTED ATM
			break;

		case UART_GET:
			//UNIMPLEMENTED ATM
			break;

		case UART_SET:
			//UNIMPLEMENTED ATM
			break;

		default:
			//weird error
			break;
	}
}

int main() {
	init();

#if defined(USBCON)
	USB.attach();
#endif

#ifdef SERIAL
	HardwareSerialCommProvider p(9600);
#endif
#ifdef SOCKET
	EthernetSocketCommProvider p(9999);
#endif

	p.open();
	string inst = "";
	while(true) {
		read_and_put(p, inst);
		try_parse(inst);
	}
	p.close();

	return 0;
}