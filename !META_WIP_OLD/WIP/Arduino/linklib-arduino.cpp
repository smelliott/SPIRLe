#include "Arduino.h"
#include "string.h"

class Spi {
public:
	static void open(const int slave_pin = -1) {
		if(slave_pin == -1) {
			SPI.begin();
		}
		else {
			SPI.begin(slave_pin);
		}
	}

	static void close(const int slave_pin = -1) {
		if(slave_pin == -1) {
			SPI.end(slave_pin);
		}
		else {
			SPI.end();
		}
	}

	static char swap(const char v) {
		return SPI.transfer(v);
	}
};


class I2c {
public:
	static void open() {
		//Wire.begin(address) -- 7 bit addr
		Wire.begin();
	}

	static void close() {
		//no close
		return;
	}

	static void write(const string& v) {
		Wire.beginTransmission(0); //requires addr
		Wire.write(v);
		Wire.endTransmission();
	}

	static int available() {
		return Wire.available();
	}

	static void read(string& out, int length = 0) {
		int av = available();
		if(length == 0) {
			length = av;
		}
		else if(av < length) {
			//requires addr (0)
			//need to check that true is sensible
			Wire.requestFrom(0, length - av, true);
		}

		out = "";
		for(int i = 0; i < length; ++i) {
			out += Wire.read();
		}
	}
};


//UART/Serial connections are basically already implemented in commlib