#include "hardserial.h"
#include <HardwareSerial.h>
#include <stdlib.h>
#include "Arduino.h"

#define ms() (clock() / CLOCKS_PER_SEC) * 1000

//NOTE: CAN DO ASYNC PATTERNS WITH serialEvent() handler

namespace SPIRLe {

	HardwareSerialCommProvider::HardwareSerialCommProvider(int baud_rate) : baud(baud_rate) {
	}

	HardwareSerialCommProvider::~HardwareSerialCommProvider() {
		close();
	}

	bool HardwareSerialCommProvider::open() {
		Serial.begin(baud);
		return true;
	}

	bool HardwareSerialCommProvider::close() {
		Serial.flush();
		Serial.end();
		return true;
	}

	int HardwareSerialCommProvider::available() {
		return Serial.available();
	}

	bool HardwareSerialCommProvider::write(const string& s) {
		const char* str = s.c_str();
		size_t str_size = strlen(str);
		unsigned ret = Serial.write((const uint8_t*)str, str_size);
		if(ret < str_size) {
			string again = s.substr(ret, s.size());
			return write(again);
		}
		return true;
	}

	bool HardwareSerialCommProvider::write(const char* s) {
		string str(s);
		return write(str);
	}

	void HardwareSerialCommProvider::read(string& out, int len) {
		int av = available();
		if(av == 0) {
			out = "";
			return;
		}
		if(len == 0) {
			len = av;
		}
		char* cstr = (char*)malloc(len);
		Serial.readBytes(cstr, len);
		out = string(cstr);
		free(cstr);
		return;
	}

	bool HardwareSerialCommProvider::poll_read(int timeout) {
		//have to implement own timeout on arduino
		// clock_t end = ms() + timeout;
		// while(ms() < end) {
		// 	if(available() > 0) {
		// 		return true;
		// 	}
		// }
		return false;
	}

	bool HardwareSerialCommProvider::poll_write(int timeout) {
		//can't poll serial writes on arduino
		return true;
	}
}