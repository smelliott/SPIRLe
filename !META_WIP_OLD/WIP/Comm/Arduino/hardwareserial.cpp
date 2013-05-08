#include "hardwareserial.h"
#include <HardwareSerial.h>
#include "Arduino.h"

#define ms() (clock() / CLOCKS_PER_SEC) * 1000

//NOTE: CAN DO ASYNC PATTERNS WITH serialEvent() handler

namespace SPIRLe {

	class HardwareSerialCommProvider : public ICommProvider {
		int baud;

	public:
		HardwareSerialCommProvider(int baud_rate) : baud(baud_rate) {
		}

		~HardwareSerialCommProvider() {
			close();
		}

		inline bool open() {
			Serial.begin(baud);
			return true;
		}

		inline bool close() {
			Serial.flush();
			Serial.end();
			return true;
		}

		inline int available() {
			return Serial.available();
		}

		bool write(const std::string& s) {
			const char* str = s.c_str();
			size_t str_size = std::strlen(str);
			int ret = Serial.write(str, str_size);
			if(ret < str_size) {
				std::string again = s.substr(ret);
				return write(again);
			}
			return true;
		}

		bool write(const char* s) {
			std::string str(s);
			return write(str);
		}

		std::string read(int len) {
			int av = available();
			if(av == 0) {
				return "";
			}
			if(len == 0) {
				len = av;
			}
			return std::string(Serial.readBytes(len));
		}

		bool poll_read(int timeout) {
			//have to implement own timeout on arduino
			clock_t end = ms() + timeout;
			while(ms() < end) {
				if(available() > 0) {
					return true;
				}
			}
			return false;
		}

		bool poll_write(int timeout) {
			//can't poll serial writes on arduino
			return true;
		}
	};
}