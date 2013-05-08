#include <Boards.h>
#include <SoftwareSerial.h>
#include "Arduino.h"
#include "string.h"
#include <cstring>
#include <ctime>

#define ms() (clock() / CLOCKS_PER_SEC) * 1000

namespace SPIRLe {

	class SoftwareSerialCommProvider : public ICommProvider {
		int baud;
		int rx;
		int tx;
		SoftwareSerial s;

	public:
		SoftwareSerialCommProvider(int baud_rate, int rx_pin, int tx_pin) : baud(baud_rate), rx(rx_pin), tx(tx_pin), s(rx, tx) {
		}

		~SoftwareSerialCommProvider() {
			close();
		}

		inline bool open() {
			s.begin(baud);
			s.listen();
			return true;
		}

		inline bool close() {
			return true;
		}

		inline int available() {
			return s.available();
		}

		bool write(const string& s) {
			const char* str = s.c_str();
			size_t str_size = std::strlen(str);
			int ret = s.write(str, str_size);
			if(ret < str_size) {
				string again = s.substr(ret);
				return write(again);
			}
			return true;
		}

		bool write(const char* s) {
			string str(s);
			return write(str);
		}

		string read(int len = 0) {
			int av = available();
			if(av == 0) {
				return "";
			}
			if(len == 0) {
				len = av;
			}
			string ret = "";
			for(int i = 0; i < len; ++i) {
				ret += s.read();
			}
			return ret;
		}

		bool poll_read(int timeout = 0) {
			//have to implement own timeout on arduino
			clock_t end = ms() + timeout;
			while(ms() < end) {
				if(available() > 0) {
					return true;
				}
			}
			return false;
		}

		bool poll_write(int timeout = 0) {
			//can't poll serial writes on arduino
			return true;
		}
	};
}