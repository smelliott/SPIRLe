#include "string.h"
#include "hardserial.h"
#include "pin.h"
#include "Arduino.h"
#include <stdlib.h>

#define USE_SERIAL

#ifdef TESTING
#include "ArduinoUnit.h"
#include "mockcomm.h"
#endif

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

inline void read_and_put(ICommProvider& p, string& out) {
	char* ret = p.read(0);
	out += ret;
	free(ret);
}

inline void try_parse(ICommProvider& p, string& inst) {
	const string::size_type inst_size = inst.size();

	//minimum of 6 bytes to form valid message
	if(inst_size < 6) {
		return;
	}

	unsigned char inst_index = inst[0];
	char str[4];
	// IN THIS CODE WE USE DIRECT ARRAY COPIES LIKE THIS
	// UGLY BUT GUARANTEED TO BE EFFICIENT!
	str[0] = inst[1];
	str[1] = inst[2];
	str[2] = inst[3];
	str[3] = inst[4];
	const uint32_t addr = atoi(str);

	if(addr != 0  /* && addr != my_addr */) {
		return;
	}

	switch(inst_index) {
		case GPIO_GET:
			if(inst_size >= 6) {
				int ret = DigitalPin::get(inst[5]);
				char* temp = (char*)ret;
				char out[10];
				//GPIO_GET
				out[0] = 0;
				//ADDRESS
				out[1] = inst[1];
				out[2] = inst[2];
				out[3] = inst[3];
				out[4] = inst[4];
				//ERROR
				out[5] = 0;
				//RESULT
				out[6] = temp[0];
				out[7] = temp[1];
				out[8] = temp[2];
				out[9] = temp[3];
				p.write(out);
				inst.erase(0, 6);
			}
			break;

		case GPIO_SET:
			if(inst_size >= 7) {
				DigitalPin::set(inst[5], inst[6]);
				char out[6];
				//GPIO_SET
				out[0] = 1;
				//ADDRESS
				out[1] = inst[1];
				out[2] = inst[2];
				out[3] = inst[3];
				out[4] = inst[4];
				//ERROR
				out[5] = 0;
				//out[4] = (inst[6] == 1) ? 't' : 'f';
				p.write(out);
				inst.erase(0, 7);
			}
			break;

		case PWM_GET:
			if(inst_size >= 6) {
				//arduino technically doesn't actually have PWM input so this is a dummy
				int ret = PwmPin::get(inst[5]);
				char* temp = (char*)ret;
				char out[10];
				//PWM_GET
				out[0] = 2;
				//ADDRESS
				out[1] = inst[1];
				out[2] = inst[2];
				out[3] = inst[3];
				out[4] = inst[4];
				//ERROR
				out[5] = 2; // yes cos am not an instruction
				//RESULT
				out[6] = temp[0];
				out[7] = temp[1];
				out[8] = temp[2];
				out[9] = temp[3];
				p.write(out);
				inst.erase(0, 6);
			}
			break;

		case PWM_SET:
			if(inst_size >= 7) {
				PwmPin::set(inst[5], inst[6]);
				char out[6];
				//PWM_SET
				out[0] = 3;
				//ADDRESS
				out[1] = inst[1];
				out[2] = inst[2];
				out[3] = inst[3];
				out[4] = inst[4];
				//ERROR
				out[5] = 0;
				p.write(out);
				inst.erase(0, 7);
			}
			break;

		case ANALOG_GET:
			if(inst_size >= 6) {
				int ret = AnalogPin::get(inst[5]);
				char* temp = (char*)ret;
				char out[10];
				//ANALOG_GET
				out[0] = 4;
				//ADDRESS
				out[1] = inst[1];
				out[2] = inst[2];
				out[3] = inst[3];
				out[4] = inst[4];
				//ERROR
				out[5] = 0;
				//RESULT
				out[6] = temp[0];
				out[7] = temp[1];
				out[8] = temp[2];
				out[9] = temp[3];
				p.write(out);
				inst.erase(0, 6);
			}
			break;

		case ANALOG_SET:
			if(inst_size >= 7) {
				AnalogPin::set(inst[5], inst[6]);
				char out[6];
				//ANALOG_SET
				out[0] = 5;
				//ADDRESS
				out[1] = inst[1];
				out[2] = inst[2];
				out[3] = inst[3];
				out[4] = inst[4];
				//ERROR
				out[5] = 0;
				p.write(out);
				inst.erase(0, 7);
			}
			break;

		case SPI_GET:
			if(inst_size >= 10) {
				//Spi::get(inst[9]);
				//REPLY UNIMPLEMENTED
				inst.erase(0, 10);
			}
			break;

		case SPI_SET:
			if(inst_size >= 10) {
				const char expect_c = inst[9];
				const int expect = atoi(&expect_c);
				if(inst_size >= expect) {
					char out[6];
					//SPI_SET
					out[0] = 7;
					//ADDRESS
					out[1] = inst[1];
					out[2] = inst[2];
					out[3] = inst[3];
					out[4] = inst[4];
					//ERROR
					out[5] = 0;
					p.write(out);
					inst.erase(0, expect);
				}
			}
			break;

		case I2C_GET:
			if(inst_size >= 10) {
				//I2c::get(inst[9]);
				//REPLY UNIMPLEMENTED
				inst.erase(0, 10);
			}
			break;

		case I2C_SET:
			if(inst_size >= 10) {
				const char expect_c = inst[9];
				const int expect = atoi(&expect_c);
				if(inst_size >= expect) {
					char out[6];
					//I2C_SET
					out[0] = 9;
					//ADDRESS
					out[1] = inst[1];
					out[2] = inst[2];
					out[3] = inst[3];
					out[4] = inst[4];
					//ERROR
					out[5] = 0;
					p.write(out);
					inst.erase(0, expect);
				}
			}
			break;

		case UART_GET:
			if(inst_size >= 10) {
				//Uart::get(inst[9]);
				//REPLY UNIMPLEMENTED
				inst.erase(0, 10);
			}
			break;

		case UART_SET:
			if(inst_size >= 10) {
				const char expect_c = inst[9];
				const int expect = atoi(&expect_c);
				if(inst_size >= expect) {
					char out[6];
					//UART_SET
					out[0] = 11;
					//ADDRESS
					out[1] = inst[1];
					out[2] = inst[2];
					out[3] = inst[3];
					out[4] = inst[4];
					//ERROR
					out[5] = 0;
					p.write(out);
					inst.erase(0, expect);
				}
			}
			break;

		default:
			//weird error
			break;
	}
}

#ifdef TESTING
//ARDUINO UNIT TESTS
TestSuite suite;

test(t_GPIO_GET) {
	MockCommProvider p;
	char msg[] = {0,0,0,0,0,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(0, m.size());
}

test(t_GPIO_GET_a) {
	MockCommProvider p;
	char msg[] = {0,1,2,3,4,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(6, m.size());
}

test(t_GPIO_SET) {
	MockCommProvider p;
	char msg[] = {1,0,0,0,0,1,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(0, m.size());
}

test(t_GPIO_SET_a) {
	MockCommProvider p;
	char msg[] = {1,1,2,3,4,1,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(7, m.size());
}

test(t_PWM_GET) {
	MockCommProvider p;
	char msg[] = {2,0,0,0,0,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(0, m.size());
}

test(t_PWM_GET_a) {
	MockCommProvider p;
	char msg[] = {2,1,2,3,4,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(6, m.size());
}

test(t_PWM_SET) {
	MockCommProvider p;
	char msg[] = {3,0,0,0,0,1,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(0, m.size());
}

test(t_PWM_SET_a) {
	MockCommProvider p;
	char msg[] = {3,1,2,3,4,1,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(7, m.size());
}

test(t_ANALOG_GET) {
	MockCommProvider p;
	char msg[] = {4,0,0,0,0,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(0, m.size());
}

test(t_ANALOG_GET_a) {
	MockCommProvider p;
	char msg[] = {4,1,2,3,4,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(6, m.size());
}

test(t_ANALOG_SET) {
	MockCommProvider p;
	char msg[] = {5,0,0,0,0,1,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(0, m.size());
}

test(t_ANALOG_SET_a) {
	MockCommProvider p;
	char msg[] = {5,1,2,3,4,1,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(7, m.size());
}

test(t_SPI_GET) {
	MockCommProvider p;
	char msg[] = {6,0,0,0,0,0,0,0,0,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(0, m.size());
}

test(t_SPI_GET_a) {
	MockCommProvider p;
	char msg[] = {6,1,2,3,4,0,0,0,0,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(10, m.size());
}

test(t_SPI_SET) {
	MockCommProvider p;
	char msg[] = {7,1,2,3,4,0,0,0,0,4,1,1,1,1};
	string m(msg);
	try_parse(p, m);
	assertEquals(0, m.size());
}

#endif

int main() {
	init();

#if defined(USBCON)
	USB.attach();
#endif

#ifndef TESTING
#ifdef USE_SERIAL
	HardwareSerialCommProvider p(9600);
#endif
#ifdef USE_SOCKET
	EthernetSocketCommProvider p(9999);
#endif
#endif

#ifdef TESTING
	MockCommProvider p;
#endif

#ifndef TESTING
	p.open();
	string inst = "";
	while(true) {
		read_and_put(p, inst);
		try_parse(p, inst);
	}
	p.close();

	// while(true) {
	// 	DigitalPin::set(13, 0);
	// 	delay(2);
	// 	DigitalPin::set(13, 1);
	// 	delay(2);
	// }
#endif

#ifdef TESTING
	while(true) {
		suite.run();
	}
#endif

	return 0;
}

#ifdef TESTING
#endif